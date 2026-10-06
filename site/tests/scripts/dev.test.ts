import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
const faults = vi.hoisted(() => ({ cleanup: false }));
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
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
