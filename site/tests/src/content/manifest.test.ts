import {
  mkdtemp,
  mkdir,
  readFile,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it } from 'vitest';
import { writeManifest } from '../../../src/content/manifest.js';
import type { Manifest } from '../../../src/content/index.js';

const roots: string[] = [];
afterEach(async () => {
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
const manifest: Manifest = {
  version: 1,
  entries: [],
  assets: [],
  ledger: [
    {
      sourcePath: 'Tutorials/a.bin',
      disposition: 'unsupported',
      reason: 'Unsupported',
    },
  ],
};
it('writes deterministic internal manifest bytes in the generated snapshot only', async () => {
  const root = await mkdtemp(join(tmpdir(), 'notes-manifest-'));
  roots.push(root);
  const output = join(root, 'site/.generated/current');
  await writeManifest(manifest, output);
  const first = await readFile(join(output, 'manifest.json'), 'utf8');
  await writeManifest(manifest, output);
  expect(await readFile(join(output, 'manifest.json'), 'utf8')).toBe(first);
  expect(JSON.parse(first)).toEqual(manifest);
  await expect(
    writeManifest(manifest, join(root, 'site/dist')),
  ).rejects.toThrow(/generated/i);
});
it('refuses symlink output ancestors without replacing their contents', async () => {
  const root = await mkdtemp(join(tmpdir(), 'notes-manifest-'));
  roots.push(root);
  await mkdir(join(root, 'outside'));
  await writeFile(join(root, 'outside/keep'), 'preserve');
  await mkdir(join(root, 'site'));
  await symlink(join(root, 'outside'), join(root, 'site/.generated'));
  await expect(
    writeManifest(manifest, join(root, 'site/.generated/current')),
  ).rejects.toThrow(/symlink|symbolic/i);
  expect(await readFile(join(root, 'outside/keep'), 'utf8')).toBe('preserve');
});
