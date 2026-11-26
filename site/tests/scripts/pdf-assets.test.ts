import {
  mkdir,
  mkdtemp,
  readFile,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it, vi } from 'vitest';
import { pdfAssets, stagePdfAssets } from '../../scripts/pdf-assets.js';
const failures = vi.hoisted(() => ({ enabled: false }));
vi.mock('node:fs/promises', async (original) => {
  const fs = await original<typeof import('node:fs/promises')>();
  return {
    ...fs,
    lstat: async (path: string) => {
      if (failures.enabled && path.endsWith('/LICENSE'))
        throw Object.assign(new Error('Denied'), { code: 'EACCES' });
      return fs.lstat(path);
    },
  };
});
const roots: string[] = [];
afterEach(async () => {
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
it('stages only exact pinned support files with licenses and no PDF scripting runtime', async () => {
  const root = await mkdtemp(join(tmpdir(), 'pdf-assets-'));
  roots.push(root);
  const assets = await pdfAssets();
  expect(assets.size).toBeGreaterThan(180);
  expect(assets.size).toBeLessThan(220);
  expect(assets.has('pdf.worker.min.mjs')).toBe(true);
  expect(assets.has('LICENSE')).toBe(true);
  expect([...assets.keys()].some((path) => path.includes('quickjs'))).toBe(
    false,
  );
  await stagePdfAssets(root);
  for (const [name, bytes] of assets)
    expect((await readFile(join(root, name))).equals(bytes)).toBe(true);
  await stagePdfAssets(root);
});
it('rejects generated symlinks instead of overwriting outside the staging tree', async () => {
  const root = await mkdtemp(join(tmpdir(), 'pdf-assets-'));
  roots.push(root);
  const other = join(root, 'other');
  await writeFile(other, 'keep');
  await symlink(other, join(root, 'LICENSE'));
  await expect(stagePdfAssets(root)).rejects.toThrow('Unsafe');
  expect(await readFile(other, 'utf8')).toBe('keep');
});

it('rejects a symlinked staging directory', async () => {
  const root = await mkdtemp(join(tmpdir(), 'pdf-assets-'));
  roots.push(root);
  const actual = join(root, 'actual');
  await mkdir(actual);
  const linked = join(root, 'linked');
  await symlink(actual, linked, 'dir');
  await expect(stagePdfAssets(linked)).rejects.toThrow(
    'Unsafe PDF asset directory',
  );
});

it('propagates filesystem errors instead of treating denied files as absent', async () => {
  const root = await mkdtemp(join(tmpdir(), 'pdf-assets-'));
  roots.push(root);
  failures.enabled = true;
  try {
    await expect(stagePdfAssets(root)).rejects.toThrow('Denied');
  } finally {
    failures.enabled = false;
  }
});
