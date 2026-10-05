import { watch } from 'node:fs';
import { lstat } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  prepareContent,
  publicationExclusion,
  readPolicy,
  type Diagnostic,
  type PrepareOptions,
} from '../src/content/index.js';
import { contentOptions } from './content.js';

type WatchServices = {
  prepare?: typeof prepareContent;
  subscribe?: (
    path: string,
    recursive: boolean,
    onEvent: (filename: string | null) => void,
  ) => { close(): void };
  onDiagnostics?: (diagnostics: Diagnostic[]) => void;
};
type Server = { kill(): void; exited: Promise<void> };
type DevelopmentServices = WatchServices & { startServer?: () => Server };

/** Native events request a serialized rebuild; events during a build collapse into the next build. */
export async function startContentWatcher(
  options: PrepareOptions,
  onSuccess: () => void,
  services: WatchServices = {},
): Promise<{ close(): Promise<void> }> {
  let policy = await readPolicy(options.policyPath);
  const report =
    services.onDiagnostics ??
    ((diagnostics) => {
      for (const item of diagnostics)
        console.error(`${item.sourcePath}: ${item.message}`);
    });
  const subscribe =
    services.subscribe ??
    ((path, recursive, onEvent) => {
      const watcher = watch(path, { recursive }, (_event, filename) =>
        onEvent(filename),
      );
      watcher.on('error', (error) =>
        report([{ sourcePath: 'watcher', message: error.message }]),
      );
      return watcher;
    });
  const watchers = new Map<string, { close(): void }>();
  const prepare = services.prepare ?? prepareContent;
  let closed = false;
  let refreshing = Promise.resolve();
  let pending = false;
  let running: Promise<void> | undefined;
  function rebuild(): void {
    if (closed) return;
    pending = true;
    if (running) return;
    running = (async () => {
      while (pending && !closed) {
        pending = false;
        try {
          const result = await prepare(options);
          if (closed) break;
          if (result.diagnostics.length) report(result.diagnostics);
          else {
            policy = await readPolicy(options.policyPath);
            if (!closed) onSuccess();
          }
        } catch (error) {
          if (!closed)
            report([
              {
                sourcePath: 'watcher',
                message: error instanceof Error ? error.message : String(error),
              },
            ]);
        }
      }
    })().finally(() => {
      running = undefined;
      if (pending && !closed) rebuild();
    });
  }
  async function watchRoots(): Promise<void> {
    for (const root of policy.roots) {
      const path = join(options.rootDir, root);
      if (watchers.has(path) || closed) continue;
      try {
        const stat = await lstat(path);
        if (!stat.isDirectory() || stat.isSymbolicLink()) continue;
        if (closed) return;
        watchers.set(
          path,
          subscribe(path, true, (filename) => {
            if (
              filename &&
              publicationExclusion(
                `${root}/${filename.replaceAll('\\', '/')}`,
                policy,
              )
            )
              return;
            rebuild();
          }),
        );
      } catch (error) {
        if (!(
          error instanceof Error &&
          'code' in error &&
          error.code === 'ENOENT'
        ))
          throw error;
      }
    }
  }
  try {
    watchers.set(
      options.rootDir,
      subscribe(options.rootDir, false, (filename) => {
        if (filename && !policy.roots.includes(filename)) return;
        refreshing = refreshing
          .then(async () => {
            if (closed) return;
            for (const root of filename ? [filename] : policy.roots) {
              const path = join(options.rootDir, root);
              watchers.get(path)?.close();
              watchers.delete(path);
            }
            await watchRoots();
            rebuild();
          })
          .catch((error: unknown) =>
            report([{ sourcePath: 'watcher', message: String(error) }]),
          );
      }),
    );
    watchers.set(
      dirname(options.policyPath),
      subscribe(dirname(options.policyPath), false, (filename) => {
        if (!filename || filename === basename(options.policyPath)) rebuild();
      }),
    );
    await watchRoots();
    rebuild();
    await running;
  } catch (error) {
    for (const watcher of watchers.values()) watcher.close();
    throw error;
  }
  return {
    close: async () => {
      if (closed) return;
      closed = true;
      for (const watcher of watchers.values()) watcher.close();
      watchers.clear();
      await refreshing;
      await running;
    },
  };
}

export async function startDevelopment(
  options: PrepareOptions,
  services: DevelopmentServices = {},
): Promise<{ close(): Promise<void> }> {
  let prepared = false;
  const watcher = await startContentWatcher(
    options,
    () => {
      prepared = true;
      console.log('Content snapshot updated.');
    },
    services,
  );
  if (!prepared) {
    await watcher.close();
    throw new Error('Initial content preparation failed');
  }
  const startServer =
    services.startServer ??
    (() => {
      const child = spawn(
        process.execPath,
        [
          join(options.rootDir, 'site/node_modules/astro/bin/astro.mjs'),
          'dev',
          '--ignore-lock',
          '--host',
          '127.0.0.1',
          ...process.argv.slice(2),
        ],
        { cwd: join(options.rootDir, 'site'), stdio: 'inherit' },
      );
      const exited = new Promise<void>((resolveExit, reject) => {
        child.once('error', reject);
        child.once('exit', (code) => {
          if (code && code !== 0) process.exitCode = code;
          resolveExit();
        });
      });
      return {
        kill: () => {
          child.kill('SIGTERM');
        },
        exited,
      };
    });
  let server: Server;
  try {
    server = startServer();
  } catch (error) {
    await watcher.close();
    throw error;
  }
  let closing: Promise<void> | undefined;
  function close(): Promise<void> {
    closing ??= (async () => {
      server.kill();
      await watcher.close();
      await server.exited;
    })();
    return closing;
  }
  void server.exited.then(close, async (error: unknown) => {
    console.error(error);
    process.exitCode = 1;
    await watcher.close();
  });
  return { close };
}

if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  try {
    const development = await startDevelopment(await contentOptions());
    for (const signal of ['SIGINT', 'SIGTERM'] as const)
      process.once(signal, () => {
        void development.close().catch((error: unknown) => {
          console.error(error);
          process.exitCode = 1;
        });
      });
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
