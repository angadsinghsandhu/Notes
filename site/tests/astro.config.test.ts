import { randomUUID } from 'node:crypto';
import { EventEmitter } from 'node:events';
import type { Stats } from 'node:fs';
import { copyFile, mkdir, mkdtemp, rm, stat, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { afterEach, expect, it, vi } from 'vitest';
import { writeManifest } from '../src/content/manifest.js';
import { commitPublication } from '../src/content/publication.js';
import type { Manifest } from '../src/content/index.js';

type Listener = (current: Stats, previous: Stats) => void;
const observations = vi.hoisted(() => ({
  watches: [] as { path: string; options: object; listener: Listener }[],
  removals: [] as { path: string; listener: Listener }[],
}));
vi.mock('node:fs', async (original) => {
  const fs = await original<typeof import('node:fs')>();
  return {
    ...fs,
    watchFile(path: string, options: object, listener: Listener) {
      observations.watches.push({ path, options, listener });
      return fs.watchFile(path, options, listener);
    },
    unwatchFile(path: string, listener: Listener) {
      observations.removals.push({ path, listener });
      return fs.unwatchFile(path, listener);
    },
  };
});

const fixtures: { root: string; http: EventEmitter }[] = [];
const manifest: Manifest = { version: 1, entries: [], assets: [], ledger: [] };
async function fixture() {
  const root = await mkdtemp(join(tmpdir(), 'notes-config-'));
  const site = join(root, 'site');
  const http = new EventEmitter();
  fixtures.push({ root, http });
  await mkdir(join(site, 'node_modules'), { recursive: true });
  await symlink(
    fileURLToPath(new URL('../node_modules/astro', import.meta.url)),
    join(site, 'node_modules/astro'),
    'dir',
  );
  await copyFile(
    fileURLToPath(new URL('../astro.config.mjs', import.meta.url)),
    join(site, 'astro.config.mjs'),
  );
  const loaded: {
    default: {
      vite: {
        plugins: {
          name: string;
          configureServer: (server: object) => void;
        }[];
      };
    };
  } = await import(pathToFileURL(join(site, 'astro.config.mjs')).href);
  const watcher = Object.assign(new EventEmitter(), { add: vi.fn() });
  loaded.default.vite.plugins
    .find((plugin) => plugin.name === 'notes-prepared-snapshot')!
    .configureServer({
      watcher,
      httpServer: http,
      middlewares: { use: vi.fn() },
    });
  const generated = join(site, '.generated');
  const file = join(generated, 'current/manifest.json');
  const catalog = join(site, 'src/lib/catalog.ts');
  async function publish() {
    const stage = join(generated, `.stage-${randomUUID()}`);
    await writeManifest(manifest, stage);
    await commitPublication(
      generated,
      join(site, 'public/content-assets'),
      stage,
      manifest,
      true,
    );
  }
  return { http, watcher, site, file, catalog, publish };
}
afterEach(async () => {
  for (const { root, http } of fixtures.splice(0)) {
    http.emit('close');
    await rm(root, { recursive: true, force: true });
  }
  observations.watches.length = 0;
  observations.removals.length = 0;
});

it('forwards actual atomic manifest publications without native watcher events', async () => {
  const { watcher, file, catalog, publish } = await fixture();
  const changes: string[] = [];
  watcher.on('change', (path: string) => changes.push(path));
  await publish();
  await expect.poll(() => changes, { timeout: 3500 }).toEqual([catalog]);
  const previous = await stat(file);
  changes.length = 0;
  await publish();
  expect((await stat(file)).ino).not.toBe(previous.ino);
  await expect.poll(() => changes, { timeout: 3500 }).toEqual([catalog]);
  expect(watcher.add).not.toHaveBeenCalled();
});

it('ignores missing and non-file snapshots and unregisters its exact listener', async () => {
  const { watcher, http, file, site, catalog, publish } = await fixture();
  const subscription = observations.watches.find(
    (entry) => entry.path === file,
  );
  expect(subscription).toBeDefined();
  if (!subscription) throw new Error('Snapshot polling was not registered');
  expect(subscription.options).toEqual({ interval: 1000, persistent: false });
  const changes: string[] = [];
  watcher.on('change', (path: string) => changes.push(path));
  const directory = await stat(site);
  subscription.listener(directory, directory);
  // Node watchFile uses a zero-valued non-file Stats object for ENOENT.
  const missing = Object.create(Object.getPrototypeOf(directory)) as Stats;
  missing.mode = 0;
  subscription.listener(missing, directory);
  expect(changes).toEqual([]);
  await publish();
  const current = await stat(file);
  subscription.listener(current, directory);
  expect(changes).toEqual([catalog]);
  http.emit('close');
  expect(observations.removals).toEqual([
    { path: file, listener: subscription.listener },
  ]);
});
