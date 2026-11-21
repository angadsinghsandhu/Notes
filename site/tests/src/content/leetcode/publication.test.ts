import {
  mkdir,
  lstat,
  mkdtemp,
  readFile,
  rename,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, it } from 'vitest';
import {
  installCurriculum,
  pruneCurriculum,
  readPublishedCurriculum,
} from '../../../../src/content/leetcode/publication.js';

const roots: string[] = [];
afterEach(async () => {
  for (const root of roots.splice(0))
    await rm(root, { recursive: true, force: true });
});
const generation = 'a'.repeat(64);

async function stage() {
  const root = await mkdtemp(join(tmpdir(), 'notes-curriculum-publication-'));
  roots.push(root);
  const generated = join(root, 'site/.generated');
  const staged = join(
    generated,
    '.stage-00000000-0000-4000-8000-000000000000/curriculum',
  );
  await mkdir(staged, { recursive: true });
  const file = join(staged, 'curriculum.json');
  const snapshot = {
    version: 1,
    generation,
    problems: [],
    lessons: [],
    paths: [],
    routes: [],
    sourceVariants: [],
  };
  await writeFile(file, JSON.stringify(snapshot));
  return {
    generated,
    staged,
    file,
    snapshot,
    target: join(generated, `curriculum-${generation}`),
  };
}

it('installs an immutable generation and compares every file before reuse', async () => {
  const { generated, staged, file, snapshot, target } = await stage();
  const nested = 'worker-assets';
  await mkdir(join(staged, nested));
  await writeFile(join(staged, nested, 'asset.json'), '{}');
  await expect(readPublishedCurriculum(generated, generation)).rejects.toThrow(
    'Selected curriculum generation is missing',
  );
  await installCurriculum(generated, staged, generation);
  expect(await readPublishedCurriculum(generated, generation)).toEqual(
    snapshot,
  );
  await mkdir(staged);
  await writeFile(file, JSON.stringify(snapshot));
  await writeFile(join(staged, nested), '{}');
  await expect(
    installCurriculum(generated, staged, generation),
  ).rejects.toThrow('corrupt');
  await rm(join(staged, nested));
  await mkdir(join(staged, nested));
  await writeFile(join(staged, nested, 'asset.json'), '[]');
  await expect(
    installCurriculum(generated, staged, generation),
  ).rejects.toThrow('corrupt');
  await writeFile(join(staged, nested, 'asset.json'), '{}');
  await installCurriculum(generated, staged, generation);
  await writeFile(join(target, 'unexpected.json'), '{}');
  await expect(
    installCurriculum(generated, staged, generation),
  ).rejects.toThrow('corrupt');
  await rm(join(target, 'unexpected.json'));
  await writeFile(join(target, 'curriculum.json'), '{}');
  await expect(
    installCurriculum(generated, staged, generation),
  ).rejects.toThrow('corrupt');
  expect(await readFile(join(target, 'curriculum.json'), 'utf8')).toBe('{}');
  await expect(readPublishedCurriculum(generated, generation)).rejects.toThrow(
    'Invalid curriculum snapshot',
  );
});

it('rejects traversal and symlinks, including dangling links', async () => {
  const { generated, staged, file, target } = await stage();
  const unsafe = '../outside';
  await expect(installCurriculum(generated, staged, unsafe)).rejects.toThrow(
    'Invalid curriculum generation',
  );
  await expect(readPublishedCurriculum(generated, unsafe)).rejects.toThrow(
    'Invalid curriculum generation',
  );
  await symlink(join(generated, 'missing'), target);
  await expect(
    installCurriculum(generated, staged, generation),
  ).rejects.toThrow('Unsafe');
  await expect(readPublishedCurriculum(generated, generation)).rejects.toThrow(
    'Unsafe',
  );
  await expect(pruneCurriculum(generated)).rejects.toThrow('Unsafe');
  await rm(target);
  await rename(staged, target);
  await rm(join(target, 'curriculum.json'));
  await symlink(file, join(target, 'curriculum.json'));
  await expect(readPublishedCurriculum(generated, generation)).rejects.toThrow(
    'Unsafe',
  );
});

it('prunes only generation directories other than selected and preceding generations', async () => {
  const { generated, staged, target } = await stage();
  const prior = 'b'.repeat(64);
  const obsolete = 'c'.repeat(64);
  await rename(staged, target);
  for (const name of [prior, obsolete, 'unowned'])
    await mkdir(join(generated, `curriculum-${name}`));
  await pruneCurriculum(generated, generation, prior);
  expect(await readPublishedCurriculum(generated, generation)).toBeDefined();
  await expect(
    mkdir(join(generated, `curriculum-${prior}`)),
  ).rejects.toMatchObject({ code: 'EEXIST' });
  await expect(
    mkdir(join(generated, 'curriculum-unowned')),
  ).rejects.toMatchObject({ code: 'EEXIST' });
  await expect(
    mkdir(join(generated, `curriculum-${obsolete}`)),
  ).resolves.toBeUndefined();
});

it('preserves a dangling entry and prunes independently verified obsolete directories', async () => {
  const { generated, target } = await stage();
  await symlink(join(generated, 'missing'), target);
  const obsolete = ['b', 'c'].map((digit) =>
    join(generated, `curriculum-${digit.repeat(64)}`),
  );
  for (const directory of obsolete) await mkdir(directory);
  await expect(pruneCurriculum(generated)).rejects.toThrow('Unsafe');
  expect((await lstat(target)).isSymbolicLink()).toBe(true);
  for (const directory of obsolete)
    await expect(lstat(directory)).rejects.toMatchObject({ code: 'ENOENT' });
});
