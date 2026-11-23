import { mkdir, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { expect, test } from 'vitest';
import { readCurriculum } from '../../../../src/content/index.js';

async function manifestFixture(
  problems: unknown,
  cleanup: (fn: () => Promise<void>) => void,
) {
  const outside = await mkdtemp(join(tmpdir(), 'curriculum-shards-'));
  cleanup(() => rm(outside, { recursive: true, force: true }));
  const root = join(outside, 'leetcode');
  await mkdir(join(root, 'manifest'), { recursive: true });
  await writeFile(
    join(root, 'manifest.json'),
    JSON.stringify({ version: 1, problems, lessons: [], paths: [] }),
  );
  return { root, outside };
}

test.for([
  [{ shards: ['missing.json'] }, /missing\.json/],
  [{ shards: ['part.json', 'part.json'] }, /duplicate shard/i],
  [{ shards: ['../outside.json'] }, /shard/i],
  [{ shards: ['/tmp/outside.json'] }, /shard/i],
  [{ shards: ['nested\\part.json'] }, /shard/i],
  [{ shards: ['part.json\n'] }, /shard/i],
  [{ shards: [] }, /shard/i],
  [{ shards: ['part.json'], unexpected: true }, /manifest\.json/],
  [{ shards: ['empty.json'] }, /empty\.json/],
  [{ shards: ['invalid-record.json'] }, /invalid-record\.json/],
  [{ shards: ['wrong-type.json'] }, /wrong-type\.json/],
  [{ shards: ['malformed.json'] }, /malformed\.json/],
  [{ shards: ['non-file.json'] }, /expected a regular file/i],
] as const)(
  'rejects an invalid manifest shard index or part %#',
  async ([problems, error], { onTestFinished }) => {
    const { root } = await manifestFixture(problems, onTestFinished);
    await writeFile(join(root, 'manifest/empty.json'), '[]');
    await writeFile(
      join(root, 'manifest/invalid-record.json'),
      '[{"number":1}]',
    );
    await writeFile(join(root, 'manifest/wrong-type.json'), '{}');
    await writeFile(join(root, 'manifest/malformed.json'), '[');
    await mkdir(join(root, 'manifest/non-file.json'));
    await expect(readCurriculum(root)).rejects.toThrow(error);
  },
);

test('rejects both an escaping shard and an escaping shard directory', async ({
  onTestFinished,
}) => {
  const { root, outside } = await manifestFixture(
    { shards: ['part.json'] },
    onTestFinished,
  );
  const external = join(outside, 'other');
  await mkdir(external);
  await writeFile(join(external, 'part.json'), '[1]');
  await symlink(join(external, 'part.json'), join(root, 'manifest/part.json'));
  await expect(readCurriculum(root)).rejects.toThrow(/part\.json/);
  await rm(join(root, 'manifest'), { recursive: true });
  await symlink(external, join(root, 'manifest'));
  await expect(readCurriculum(root)).rejects.toThrow(/outside/i);
});
