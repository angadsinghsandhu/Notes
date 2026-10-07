import { watch } from 'chokidar';
import { lstat } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  prepareContent,
  publicationExclusion,
  readPolicy,
  type Diagnostic,
  type PrepareOptions,
} from '../src/content/index.js';
import { contentOptions } from './content.js';

type WatchHandle = { close(): void | Promise<void> };
type WatchServices = {
  prepare?: typeof prepareContent;
  subscribe?: (
    path: string,
    recursive: boolean,
    onEvent: (filename: string | null) => void,
  ) => WatchHandle | Promise<WatchHandle>;
  onDiagnostics?: (diagnostics: Diagnostic[]) => void;
};
type Server = { kill(): void; exited: Promise<void> };
type DevelopmentServices = WatchServices & { startServer?: () => Server };

/** Source events request a serialized rebuild; events during a build collapse into the next build. */
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
    (async (path, recursive, onEvent) => {
      // ponytail: 1s polling costs O(watched paths); tune only if measured load warrants it.
      const watcher = watch(path, {
        usePolling: true,
        interval: 1000,
        binaryInterval: 1000,
        ignoreInitial: true,
        followSymlinks: false,
        ...(recursive ? {} : { depth: 0 }),
        ignored: (candidate) =>
          Boolean(
            publicationExclusion(
              relative(options.rootDir, candidate).replaceAll('\\', '/'),
              { ...policy, exclude: [] },
            ),
          ),
      });
      let ready = false;
      try {
        await new Promise<void>((resolveReady, reject) => {
          watcher.once('ready', () => {
            ready = true;
            resolveReady();
          });
          watcher.on('error', (error) => {
            if (!ready) reject(error);
            else
              report([
                {
                  sourcePath: 'watcher',
                  message:
                    error instanceof Error ? error.message : String(error),
                },
              ]);
          });
          watcher.on('all', (_event, changed) =>
            onEvent(relative(path, changed).replaceAll('\\', '/')),
          );
        });
        return watcher;
      } catch (error) {
        await watcher.close();
        throw error;
      }
    });
  const watchers = new Map<string, WatchHandle>();
  const prepare = services.prepare ?? prepareContent;
  let closed = false;
  let initialized = false;
  let refreshing = Promise.resolve();
  let pending = false;
  let running: Promise<void> | undefined;
  function rebuild(): void {
    if (closed) return;
    pending = true;
    if (!initialized || running) return;
    running = (async () => {
      while (pending && !closed) {
        pending = false;
        try {
          const result = await prepare({ ...options, development: true });
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
          await subscribe(path, true, (filename) => {
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
      await subscribe(options.rootDir, false, (filename) => {
        if (filename && !policy.roots.includes(filename)) return;
        refreshing = refreshing
          .then(async () => {
            if (closed) return;
            for (const root of filename ? [filename] : policy.roots) {
              const path = join(options.rootDir, root);
              await watchers.get(path)?.close();
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
      await subscribe(dirname(options.policyPath), false, (filename) => {
        if (!filename || filename === basename(options.policyPath)) rebuild();
      }),
    );
    await watchRoots();
    initialized = true;
    rebuild();
    await running;
  } catch (error) {
    for (const watcher of watchers.values()) await watcher.close();
    throw error;
  }
  return {
    close: async () => {
      if (closed) return;
      closed = true;
      await refreshing;
      for (const watcher of watchers.values()) await watcher.close();
      watchers.clear();
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
