import {
  mkdtemp,
  mkdir,
  writeFile,
  readFile,
  rm,
  rename,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
const faults = vi.hoisted(() => ({
  cleanup: false,
  rootError: false,
  readyError: false,
  watchers: [] as import('chokidar').FSWatcher[],
}));
vi.mock('chokidar', async (original) => {
  const chokidar = await original<typeof import('chokidar')>();
  return {
    ...chokidar,
    watch: (...args: Parameters<typeof chokidar.watch>) => {
      const watcher = chokidar.watch(...args);
      faults.watchers.push(watcher);
      if (faults.readyError)
        queueMicrotask(() =>
          watcher.emit('error', new Error('Initial scan denied')),
        );
      return watcher;
    },
  };
});
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
    lstat: async (path: string) => {
      if (faults.rootError && path.endsWith('/Books'))
        throw Object.assign(new Error('Root access denied'), {
          code: 'EACCES',
        });
      return fs.lstat(path);
    },
    rm: async (path: string, options: Parameters<typeof fs.rm>[1]) => {
      if (faults.cleanup && path.includes('/.stage-'))
        throw new Error('injected cleanup failure');
      return fs.rm(path, options);
    },
  };
});

import { startContentWatcher, startDevelopment } from '../../scripts/dev.js';
import type {
  PreparationResult,
  PrepareOptions,
} from '../../src/content/index.js';

const roots: string[] = [];
const handles: { close(): Promise<void> }[] = [];
afterEach(async () => {
  faults.cleanup = false;
  faults.rootError = false;
  faults.readyError = false;
  faults.watchers = [];
  vi.restoreAllMocks();
  for (const handle of handles.splice(0)) await handle.close();
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
async function archive(): Promise<PrepareOptions> {
  const root = await mkdtemp(join(tmpdir(), 'notes-watcher-'));
  roots.push(root);
  await mkdir(join(root, 'Tutorials'));
  await mkdir(join(root, 'site/content'), { recursive: true });
  const policyPath = join(root, 'site/content/publication.json');
  await writeFile(
    policyPath,
    JSON.stringify({
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
      repositoryPublic: true,
      repositoryUrl: 'https://github.com/owner/repo',
      revision: 'a'.repeat(40),
    }),
  );
  return {
    rootDir: root,
    outputDir: join(root, 'site/.generated'),
    policyPath,
    hosted: false,
  };
}
function events() {
  const callbacks = new Map<string, (filename: string | null) => void>();
  const close = vi.fn();
  return {
    callbacks,
    close,
    subscribe: (
      path: string,
      _recursive: boolean,
      onEvent: (filename: string | null) => void,
    ) => {
      callbacks.set(path, onEvent);
      return { close };
    },
  };
}
const success: PreparationResult = {
  manifest: { version: 1, entries: [], assets: [], ledger: [] },
  diagnostics: [],
};
it('serializes concurrent changes and coalesces intervening events without timer sleeps', async () => {
  const options = await archive();
  const source = events();
  let release: (value: PreparationResult) => void = () => {};
  const held = new Promise<PreparationResult>((resolve) => {
    release = resolve;
  });
  let begin: () => void = () => {};
  const started = new Promise<void>((resolve) => {
    begin = resolve;
  });
  let complete: () => void = () => {};
  const completed = new Promise<void>((resolve) => {
    complete = resolve;
  });
  let active = 0;
  let maximum = 0;
  const prepare = vi.fn(async () => {
    active++;
    maximum = Math.max(maximum, active);
    if (prepare.mock.calls.length === 2) {
      begin();
      await held;
    }
    active--;
    return success;
  });
  const onSuccess = vi.fn(() => {
    if (onSuccess.mock.calls.length === 3) complete();
  });
  const watcher = await startContentWatcher(options, onSuccess, {
    subscribe: source.subscribe,
    prepare,
  });
  handles.push(watcher);
  const emit = source.callbacks.get(join(options.rootDir, 'Tutorials'))!;
  emit('first.md');
  await started;
  emit('second.md');
  emit('third.md');
  emit('fourth.md');
  release(success);
  await completed;
  expect(maximum).toBe(1);
  expect(prepare).toHaveBeenCalledTimes(3);
  await watcher.close();
  expect(source.close).toHaveBeenCalledTimes(3);
  emit('after-close.md');
  await Promise.resolve();
  expect(prepare).toHaveBeenCalledTimes(3);
});
it('a failed real rebuild keeps prior bytes and a fixed source replaces them on the latest event', async () => {
  const options = await archive();
  const source = events();
  const path = join(options.rootDir, 'Tutorials/note.md');
  await writeFile(path, '# Initial');
  let failure: () => void = () => {};
  const failed = new Promise<void>((resolve) => {
    failure = resolve;
  });
  let fix: () => void = () => {};
  const fixed = new Promise<void>((resolve) => {
    fix = resolve;
  });
  const onSuccess = vi.fn(() => {
    if (onSuccess.mock.calls.length === 2) fix();
  });
  const watcher = await startContentWatcher(options, onSuccess, {
    subscribe: source.subscribe,
    onDiagnostics: () => failure(),
  });
  handles.push(watcher);
  const before = await readFile(
    join(options.outputDir, 'current/manifest.json'),
  );
  const emit = source.callbacks.get(join(options.rootDir, 'Tutorials'))!;
  await writeFile(path, '# Broken\n[bad](absent.md)');
  emit('note.md');
  await failed;
  expect(
    await readFile(join(options.outputDir, 'current/manifest.json')),
  ).toEqual(before);
  await writeFile(path, '# Fixed');
  emit('note.md');
  await fixed;
  expect(
    await readFile(join(options.outputDir, 'current/manifest.json')),
  ).not.toEqual(before);
  expect(onSuccess).toHaveBeenCalledTimes(2);
});
it('closes the watchers and waits for its server child to terminate', async () => {
  const options = await archive();
  const source = events();
  const kill = vi.fn();
  let exit: () => void = () => {};
  const exited = new Promise<void>((resolve) => {
    exit = resolve;
  });
  const server = {
    kill: () => {
      kill();
      exit();
    },
    exited,
  };
  const development = await startDevelopment(options, {
    subscribe: source.subscribe,
    prepare: async () => success,
    startServer: () => server,
  });
  handles.push(development);
  await development.close();
  expect(kill).toHaveBeenCalledTimes(1);
  expect(source.close).toHaveBeenCalledTimes(3);
  await development.close();
  expect(kill).toHaveBeenCalledTimes(1);
});

it('refreshes publication exclusions after a successful policy edit', async () => {
  const options = await archive();
  const source = events();
  const policy = JSON.parse(
    await readFile(options.policyPath, 'utf8'),
  ) as Record<string, unknown>;
  await writeFile(
    options.policyPath,
    JSON.stringify({ ...policy, exclude: ['**/hidden/**'] }),
  );
  const prepare = vi.fn(async () => success);
  let updated: () => void = () => {};
  const update = new Promise<void>((resolve) => {
    updated = resolve;
  });
  const onSuccess = vi.fn(() => {
    if (onSuccess.mock.calls.length === 2) updated();
  });
  const watcher = await startContentWatcher(options, onSuccess, {
    subscribe: source.subscribe,
    prepare,
  });
  handles.push(watcher);
  await writeFile(
    options.policyPath,
    JSON.stringify({ ...policy, exclude: [] }),
  );
  source.callbacks.get(join(options.rootDir, 'site/content'))!(
    'publication.json',
  );
  await update;
  source.callbacks.get(join(options.rootDir, 'Tutorials'))!('hidden/note.md');
  await Promise.resolve();
  expect(prepare).toHaveBeenCalledTimes(3);
});

it('replaces a root subscription when an allowed archive folder is recreated', async () => {
  const options = await archive();
  const source = events();
  const subscribe = vi.fn(source.subscribe);
  let updated: () => void = () => {};
  const update = new Promise<void>((resolve) => {
    updated = resolve;
  });
  const onSuccess = vi.fn(() => {
    if (onSuccess.mock.calls.length === 2) updated();
  });
  const watcher = await startContentWatcher(options, onSuccess, {
    subscribe,
    prepare: async () => success,
  });
  handles.push(watcher);
  await rm(join(options.rootDir, 'Tutorials'), { recursive: true });
  await mkdir(join(options.rootDir, 'Tutorials'));
  source.callbacks.get(options.rootDir)!('Tutorials');
  await update;
  expect(
    subscribe.mock.calls.filter(
      ([path]) => path === join(options.rootDir, 'Tutorials'),
    ),
  ).toHaveLength(2);
  expect(source.close).toHaveBeenCalledTimes(1);
});

it('development watcher retains the preceding assets and reports success after committed private cleanup fails', async () => {
  const options = await archive();
  const source = events();
  await writeFile(
    join(options.rootDir, 'Tutorials/note.md'),
    '# Old\n![pixel](pixel.png)',
  );
  const image = await readFile('tests/fixtures/synthetic/task3/pixel.png');
  await writeFile(join(options.rootDir, 'Tutorials/pixel.png'), image);
  const diagnostics = vi.fn();
  const warning = vi.spyOn(console, 'warn').mockImplementation(() => {});
  let complete: () => void = () => {};
  const completed = new Promise<void>((resolve) => {
    complete = resolve;
  });
  const onSuccess = vi.fn(() => {
    if (onSuccess.mock.calls.length === 2) complete();
  });
  try {
    const watcher = await startContentWatcher(options, onSuccess, {
      subscribe: source.subscribe,
      onDiagnostics: (items) => {
        diagnostics(items);
        complete();
      },
    });
    handles.push(watcher);
    const before = JSON.parse(
      await readFile(join(options.outputDir, 'current/manifest.json'), 'utf8'),
    ) as { assets: { url: string }[] };
    faults.cleanup = true;
    await writeFile(join(options.rootDir, 'Tutorials/note.md'), '# New');
    source.callbacks.get(join(options.rootDir, 'Tutorials'))!('note.md');
    await completed;
    expect(onSuccess).toHaveBeenCalledTimes(2);
    expect(diagnostics).not.toHaveBeenCalled();
    expect(
      await readFile(
        join(options.rootDir, 'site/public', before.assets[0]!.url.slice(1)),
      ),
    ).toEqual(image);
    expect(
      JSON.parse(
        await readFile(
          join(options.outputDir, 'current/manifest.json'),
          'utf8',
        ),
      ).entries[0].title,
    ).toBe('New');
  } finally {
    warning.mockRestore();
  }
});

it('observes a single real source write and rejects initial preparation or child startup failures', async () => {
  const options = await archive();
  let updated!: () => void;
  const update = new Promise<void>((done) => {
    updated = done;
  });
  const successCallback = vi.fn(() => {
    if (successCallback.mock.calls.length === 2) updated();
  });
  const watcher = await startContentWatcher(options, successCallback, {
    prepare: async () => success,
  });
  handles.push(watcher);
  await writeFile(
    join(options.rootDir, 'Tutorials/native.md'),
    '# Single event',
  );
  await vi.waitFor(
    () => expect(successCallback.mock.calls.length).toBeGreaterThanOrEqual(2),
    { timeout: 5000 },
  );
  await update;
  await watcher.close();
  const source = events();
  await expect(
    startDevelopment(options, {
      subscribe: source.subscribe,
      prepare: async () => ({
        ...success,
        diagnostics: [
          { sourcePath: 'Tutorials/bad.md', message: 'Bad source' },
        ],
      }),
    }),
  ).rejects.toThrow('Initial content preparation failed');
  await expect(
    startDevelopment(options, {
      subscribe: source.subscribe,
      prepare: async () => success,
      startServer: () => {
        throw new Error('Child startup denied');
      },
    }),
  ).rejects.toThrow('Child startup denied');
  expect(source.close).toHaveBeenCalled();
});
it('reports thrown rebuild failures, ignores excluded/unrelated events and refreshes every root on unnamed events', async () => {
  const options = await archive();
  const source = events();
  const error = vi.spyOn(console, 'error').mockImplementation(() => {});
  const prepare = vi.fn(async (): Promise<PreparationResult> => {
    throw 'Native rebuild failure';
  });
  const onSuccess = vi.fn();
  const watcher = await startContentWatcher(options, onSuccess, {
    subscribe: source.subscribe,
    prepare,
  });
  handles.push(watcher);
  expect(error).toHaveBeenCalledWith('watcher: Native rebuild failure');
  const policy = JSON.parse(await readFile(options.policyPath, 'utf8'));
  await writeFile(
    options.policyPath,
    JSON.stringify({ ...policy, exclude: ['**/hidden/**'] }),
  );
  // Successful policy refresh must precede exclusion assertions.
  prepare.mockImplementation(async () => success);
  source.callbacks.get(join(options.rootDir, 'site/content'))!(
    'publication.json',
  );
  await vi.waitFor(() => expect(onSuccess).toHaveBeenCalledTimes(1));
  source.callbacks.get(join(options.rootDir, 'Tutorials'))!('hidden/note.md');
  source.callbacks.get(options.rootDir)!('not-allowed');
  source.callbacks.get(join(options.rootDir, 'site/content'))!(
    'unrelated.json',
  );
  expect(prepare).toHaveBeenCalledTimes(2);
  source.callbacks.get(options.rootDir)!(null);
  await vi.waitFor(() => expect(prepare).toHaveBeenCalledTimes(3));
  await watcher.close();
  source.callbacks.get(options.rootDir)!(null);
  expect(prepare).toHaveBeenCalledTimes(3);
  error.mockRestore();
});
it('does not publish a held rebuild after closing and cleans subscriptions when a later root cannot subscribe', async () => {
  const options = await archive();
  const source = events();
  let release!: (value: PreparationResult) => void;
  let started!: () => void;
  const began = new Promise<void>((done) => {
    started = done;
  });
  const held = new Promise<PreparationResult>((done) => {
    release = done;
  });
  const prepare = vi
    .fn()
    .mockResolvedValueOnce(success)
    .mockImplementation(async () => {
      started();
      return held;
    });
  const onSuccess = vi.fn();
  const watcher = await startContentWatcher(options, onSuccess, {
    subscribe: source.subscribe,
    prepare,
  });
  source.callbacks.get(join(options.rootDir, 'Tutorials'))!('held.md');
  await began;
  const closing = watcher.close();
  release(success);
  await closing;
  expect(onSuccess).toHaveBeenCalledTimes(1);
  await expect(
    startContentWatcher(options, () => {}, {
      subscribe: (path, recursive, onEvent) => {
        if (recursive) throw new Error('Subscription denied');
        return source.subscribe(path, recursive, onEvent);
      },
    }),
  ).rejects.toThrow('Subscription denied');
  expect(source.close).toHaveBeenCalled();
});
it.each([0, 2])(
  'starts and closes an actual owned Node child and retains its exit status %s',
  async (code) => {
    const options = await archive();
    const source = events();
    const childDir = join(options.rootDir, 'site/node_modules/astro/bin');
    await mkdir(childDir, { recursive: true });
    const ready = join(options.rootDir, 'child-ready');
    await writeFile(
      join(childDir, 'astro.mjs'),
      `import {writeFileSync} from 'node:fs'; writeFileSync(${JSON.stringify(ready)}, 'ready'); ${code ? `process.exit(${code});` : "process.on('SIGTERM',()=>process.exit(0)); setInterval(()=>{},1000);"}`,
    );
    const exitCode = process.exitCode;
    const development = await startDevelopment(options, {
      subscribe: source.subscribe,
      prepare: async () => success,
    });
    handles.push(development);
    try {
      await vi.waitFor(async () =>
        expect(await readFile(ready, 'utf8')).toBe('ready'),
      );
      if (code) await vi.waitFor(() => expect(process.exitCode).toBe(code));
      await development.close();
      expect(source.close).toHaveBeenCalledTimes(3);
    } finally {
      process.exitCode = exitCode;
    }
  },
);

it('reports native watcher errors and later root access failures without losing close handles', async () => {
  const options = await archive();
  const diagnostics = vi.fn();
  const watcher = await startContentWatcher(options, () => {}, {
    prepare: async () => success,
    onDiagnostics: diagnostics,
  });
  handles.push(watcher);
  faults.watchers[0]!.emit('error', new Error('Native descriptor failure'));
  expect(diagnostics).toHaveBeenCalledWith([
    { sourcePath: 'watcher', message: 'Native descriptor failure' },
  ]);
  await watcher.close();
  const source = events();
  const later = await startContentWatcher(options, () => {}, {
    subscribe: source.subscribe,
    prepare: async () => success,
    onDiagnostics: diagnostics,
  });
  handles.push(later);
  faults.rootError = true;
  source.callbacks.get(options.rootDir)!(null);
  await vi.waitFor(() =>
    expect(diagnostics).toHaveBeenCalledWith([
      { sourcePath: 'watcher', message: 'Error: Root access denied' },
    ]),
  );
  faults.rootError = false;
});
it('reports asynchronous native child startup errors and closes its owned subscriptions', async () => {
  const options = await archive();
  const source = events();
  const error = vi.spyOn(console, 'error').mockImplementation(() => {});
  const executable = process.execPath;
  const exitCode = process.exitCode;
  let development: Awaited<ReturnType<typeof startDevelopment>>;
  try {
    Object.defineProperty(process, 'execPath', {
      value: join(options.rootDir, 'missing-node'),
      configurable: true,
    });
    development = await startDevelopment(options, {
      subscribe: source.subscribe,
      prepare: async () => success,
    });
    Object.defineProperty(process, 'execPath', {
      value: executable,
      configurable: true,
    });
    await vi.waitFor(() =>
      expect(error).toHaveBeenCalledWith(
        expect.objectContaining({ code: 'ENOENT' }),
      ),
    );
    await expect(development.close()).rejects.toMatchObject({ code: 'ENOENT' });
    expect(source.close).toHaveBeenCalledTimes(3);
  } finally {
    Object.defineProperty(process, 'execPath', {
      value: executable,
      configurable: true,
    });
    process.exitCode = exitCode;
  }
});
it('executes the real CLI startup and its installed shutdown handler with an owned fixture child', async () => {
  const options = await archive();
  const site = join(options.rootDir, 'site');
  const childDir = join(site, 'node_modules/astro/bin');
  await mkdir(childDir, { recursive: true });
  const ready = join(options.rootDir, 'cli-child-ready');
  const closed = join(options.rootDir, 'cli-child-closed');
  await writeFile(
    join(childDir, 'astro.mjs'),
    `import {writeFileSync} from 'node:fs'; writeFileSync(${JSON.stringify(ready)}, 'ready'); process.on('SIGTERM',()=>{ writeFileSync(${JSON.stringify(closed)}, 'closed'); process.exit(0); }); setInterval(()=>{},1000);`,
  );
  const argv = process.argv;
  const exitCode = process.exitCode;
  const old = new Map(
    (['SIGINT', 'SIGTERM'] as const).map((signal) => [
      signal,
      new Set(process.listeners(signal)),
    ]),
  );
  vi.spyOn(process, 'cwd').mockReturnValue(site);
  process.argv = [
    process.execPath,
    new URL('../../scripts/dev.ts', import.meta.url).pathname,
  ];
  vi.resetModules();
  try {
    await import('../../scripts/dev.js');
    await vi.waitFor(async () =>
      expect(await readFile(ready, 'utf8')).toBe('ready'),
    );
    const handler = process
      .listeners('SIGTERM')
      .find((listener) => !old.get('SIGTERM')!.has(listener))!;
    expect(handler).toEqual(expect.any(Function));
    handler('SIGTERM');
    await vi.waitFor(async () =>
      expect(await readFile(closed, 'utf8')).toBe('closed'),
    );
  } finally {
    for (const signal of ['SIGINT', 'SIGTERM'] as const)
      for (const listener of process.listeners(signal))
        if (!old.get(signal)!.has(listener))
          process.removeListener(signal, listener);
    process.argv = argv;
    process.exitCode = exitCode;
  }
});

it('awaits subscription readiness before preparation and asynchronous closure on startup failure', async () => {
  const options = await archive();
  const prepare = vi.fn(async () => success);
  let ready!: () => void;
  const readiness = new Promise<void>((done) => {
    ready = done;
  });
  let closed = false;
  const close = async () => {
    await Promise.resolve();
    closed = true;
  };
  const startup = startContentWatcher(options, () => {}, {
    prepare,
    subscribe: async (_path, recursive) => {
      if (recursive) throw new Error('Later subscription denied');
      await readiness;
      return { close };
    },
  });
  await vi.waitFor(() => expect(prepare).not.toHaveBeenCalled());
  ready();
  await expect(startup).rejects.toThrow('Later subscription denied');
  expect(closed).toBe(true);
  expect(prepare).not.toHaveBeenCalled();
});
it('rejects an initial polling error after closing its allocated watcher', async () => {
  const options = await archive();
  faults.readyError = true;
  const prepare = vi.fn(async () => success);
  await expect(
    startContentWatcher(options, () => {}, { prepare }),
  ).rejects.toThrow('Initial scan denied');
  expect(prepare).not.toHaveBeenCalled();
  expect(faults.watchers).toHaveLength(1);
  expect(faults.watchers[0]!.closed).toBe(true);
});
it('awaits asynchronous close before rearming a root and before shutdown completes', async () => {
  const options = await archive();
  const source = events();
  const closed: string[] = [];
  const subscribe = vi.fn(
    async (
      path: string,
      recursive: boolean,
      callback: (filename: string | null) => void,
    ) => {
      const handle = source.subscribe(path, recursive, callback);
      return {
        close: async () => {
          await Promise.resolve();
          handle.close();
          closed.push(path);
        },
      };
    },
  );
  const prepare = vi.fn(async () => success);
  const watcher = await startContentWatcher(options, () => {}, {
    subscribe,
    prepare,
  });
  handles.push(watcher);
  source.callbacks.get(options.rootDir)!('Tutorials');
  await vi.waitFor(() => expect(prepare).toHaveBeenCalledTimes(2));
  expect(closed).toEqual([join(options.rootDir, 'Tutorials')]);
  await watcher.close();
  expect(closed).toHaveLength(4);
});
it('polls real add, modify, rename, delete, policy unexclude and root recreation without rewriting during waits', async () => {
  const options = await archive();
  const policy = JSON.parse(await readFile(options.policyPath, 'utf8'));
  await writeFile(
    options.policyPath,
    JSON.stringify({ ...policy, exclude: ['**/hidden/**'] }),
  );
  await mkdir(join(options.rootDir, 'Tutorials/hidden'));
  await mkdir(join(options.rootDir, 'Tutorials/node_modules'));
  await writeFile(
    join(options.rootDir, 'Tutorials/node_modules/ignored.md'),
    '# Internal',
  );
  const watcher = await startContentWatcher(options, () => {});
  handles.push(watcher);
  expect(
    faults.watchers.every(
      (handle) =>
        handle.options.usePolling &&
        handle.options.interval === 1000 &&
        handle.options.binaryInterval === 1000 &&
        !handle.options.followSymlinks &&
        handle.options.ignoreInitial,
    ),
  ).toBe(true);
  expect(faults.watchers[0]!.options.depth).toBe(0);
  expect(
    faults.watchers
      .flatMap((handle) => Object.keys(handle.getWatched()))
      .some((path) => path.includes('node_modules')),
  ).toBe(false);
  const manifest = async () =>
    JSON.parse(
      await readFile(join(options.outputDir, 'current/manifest.json'), 'utf8'),
    );
  const titles = async () =>
    (await manifest()).entries.map((entry: { title: string }) => entry.title);
  const path = join(options.rootDir, 'Tutorials/single.md');
  await writeFile(path, '# Added');
  await vi.waitFor(async () => expect(await titles()).toContain('Added'), {
    timeout: 6000,
  });
  await writeFile(path, '# Modified content');
  await vi.waitFor(
    async () => expect(await titles()).toContain('Modified content'),
    { timeout: 6000 },
  );
  await rename(path, join(options.rootDir, 'Tutorials/renamed.md'));
  await vi.waitFor(
    async () =>
      expect((await manifest()).entries[0].sourcePath).toBe(
        'Tutorials/renamed.md',
      ),
    { timeout: 6000 },
  );
  await rm(join(options.rootDir, 'Tutorials/renamed.md'));
  await vi.waitFor(async () => expect(await titles()).toEqual([]), {
    timeout: 6000,
  });
  await writeFile(
    join(options.rootDir, 'Tutorials/hidden/note.md'),
    '# Revealed',
  );
  await writeFile(
    options.policyPath,
    JSON.stringify({ ...policy, exclude: [] }),
  );
  await vi.waitFor(async () => expect(await titles()).toContain('Revealed'), {
    timeout: 6000,
  });
  await writeFile(
    join(options.rootDir, 'Tutorials/hidden/note.md'),
    '# Edited after unexclude',
  );
  await vi.waitFor(
    async () => expect(await titles()).toContain('Edited after unexclude'),
    { timeout: 6000 },
  );
  await rm(join(options.rootDir, 'Tutorials'), { recursive: true });
  await vi.waitFor(async () => expect(await titles()).toEqual([]), {
    timeout: 6000,
  });
  await mkdir(join(options.rootDir, 'Tutorials'));
  await writeFile(
    join(options.rootDir, 'Tutorials/recreated.md'),
    '# Recreated',
  );
  await vi.waitFor(async () => expect(await titles()).toContain('Recreated'), {
    timeout: 6000,
  });
}, 40000);

it('closes a root subscription that becomes ready while shutdown is pending', async () => {
  const options = await archive();
  const source = events();
  let release!: () => void;
  const held = new Promise<void>((done) => {
    release = done;
  });
  let started!: () => void;
  const beginning = new Promise<void>((done) => {
    started = done;
  });
  let subscriptions = 0;
  const subscribe = async (
    path: string,
    recursive: boolean,
    callback: (filename: string | null) => void,
  ) => {
    if (++subscriptions === 4) {
      started();
      await held;
    }
    return source.subscribe(path, recursive, callback);
  };
  const watcher = await startContentWatcher(options, () => {}, {
    subscribe,
    prepare: async () => success,
  });
  source.callbacks.get(options.rootDir)!('Tutorials');
  await beginning;
  const closing = watcher.close();
  release();
  await closing;
  expect(source.close).toHaveBeenCalledTimes(4);
});

it.each([false, true])(
  'serializes a real archive parent event during initial readiness and closes every allocated handle (startup failure=%s)',
  async (failure) => {
    const rootDir = resolve('..');
    const options: PrepareOptions = {
      rootDir,
      policyPath: join(rootDir, 'site/content/publication.json'),
      outputDir: join(rootDir, 'site/.generated'),
      hosted: false,
    };
    const allocated: { path: string; close: ReturnType<typeof vi.fn> }[] = [];
    let parentEvent!: (filename: string | null) => void;
    let release!: () => void;
    const held = new Promise<void>((done) => {
      release = done;
    });
    let begin!: () => void;
    const began = new Promise<void>((done) => {
      begin = done;
    });
    let books = 0;
    const prepare = vi.fn(async () => success);
    const startup = startContentWatcher(options, () => {}, {
      prepare,
      onDiagnostics: () => {},
      subscribe: async (path, recursive, callback) => {
        const handle = {
          path,
          close: vi.fn(async () => {
            await Promise.resolve();
          }),
        };
        allocated.push(handle);
        if (path === rootDir) parentEvent = callback;
        if (recursive && path === join(rootDir, 'Books') && ++books === 1) {
          begin();
          await held;
        }
        if (failure && path === join(rootDir, 'Classes')) {
          await handle.close();
          throw new Error('Initial recursive readiness failed');
        }
        return handle;
      },
    });
    const result = startup.then(
      (watcher) => ({ watcher }),
      (error: unknown) => ({ error }),
    );
    await began;
    parentEvent('Books');
    // Let the queued refresh enter its first awaits before releasing initial Books readiness.
    await Promise.resolve();
    await Promise.resolve();
    release();
    const completed = await result;
    if ('watcher' in completed) await completed.watcher.close();
    else
      expect(completed.error).toEqual(
        new Error('Initial recursive readiness failed'),
      );
    expect(allocated.length).toBeGreaterThanOrEqual(4);
    expect(
      allocated.every((handle) => handle.close.mock.calls.length === 1),
    ).toBe(true);
    if (failure) expect(prepare).not.toHaveBeenCalled();
  },
  10000,
);
