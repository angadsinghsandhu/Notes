import { mkdir, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterEach, describe, expect, test } from 'vitest';
import { readCurriculum } from '../../../../src/content/index.js';

const draft = {
  problemId: 'leetcode:1',
  prose: null,
  examples: null,
  approaches: [],
  review: null,
};
const path = {
  id: 'all-problems',
  title: 'All problems',
  description: 'An editorial study order',
  rootIds: [],
  nodes: [],
};

function manifest() {
  return {
    version: 1,
    problems: Array.from({ length: 2000 }, (_, index) => ({
      id: `leetcode:${index + 1}`,
      number: index + 1,
      title: null,
      slug: null,
      officialUrl: null,
      domain: null,
      difficulty: null,
      topics: [],
      status: index === 0 ? 'draft' : 'planned',
      evidence: { officialQuestion: null, companies: [] },
    })),
    lessons: ['leetcode:1'],
    paths: ['all-problems'],
  };
}

let tempDir: string | undefined;

afterEach(async () => {
  if (tempDir) await rm(tempDir, { recursive: true, force: true });
  tempDir = undefined;
});

async function createTree() {
  tempDir = await mkdtemp(join(tmpdir(), 'leetcode-curriculum-'));
  const root = join(tempDir, 'leetcode');
  await mkdir(root);
  return { root, outside: tempDir };
}

async function writeJson(root: string, path: string, value: unknown) {
  const filename = join(root, path);
  await mkdir(dirname(filename), { recursive: true });
  await writeFile(filename, JSON.stringify(value));
}

describe('readCurriculum', () => {
  test('reads the versioned manifest and its listed per-problem and path metadata', async () => {
    const { root } = await createTree();
    await writeJson(root, 'manifest.json', manifest());
    await writeJson(root, 'problems/1/metadata.json', draft);
    await writeJson(root, 'paths/all-problems.json', path);
    expect(await readCurriculum(root)).toEqual({
      ...manifest(),
      lessons: [draft],
      paths: [path],
    });
  });

  test('rejects malformed or missing files with the failing file in the error', async () => {
    const { root } = await createTree();
    await expect(readCurriculum(root)).rejects.toThrow(/manifest.json/);
    await writeFile(join(root, 'manifest.json'), '{');
    await expect(readCurriculum(root)).rejects.toThrow(/manifest.json/);
    await writeJson(root, 'manifest.json', manifest());
    await expect(readCurriculum(root)).rejects.toThrow(
      /problems\/1\/metadata.json/,
    );
  });

  test('rejects invalid manifest references before reading sidecars', async () => {
    const { root } = await createTree();
    for (const changes of [
      { paths: ['../outside'] },
      { lessons: ['leetcode:01'] },
      { version: 2 },
    ]) {
      await writeJson(root, 'manifest.json', { ...manifest(), ...changes });
      await expect(readCurriculum(root)).rejects.toThrow(/manifest.json/);
    }
  });

  test('rejects symlink escapes through intermediate directories and files', async () => {
    const { root, outside } = await createTree();
    await writeJson(outside, 'other/1/metadata.json', draft);
    await writeJson(root, 'manifest.json', manifest());
    await symlink(join(outside, 'other'), join(root, 'problems'));
    await expect(readCurriculum(root)).rejects.toThrow(
      /problems\/1\/metadata.json.*outside/i,
    );

    await writeJson(outside, 'external.json', manifest());
    await rm(join(root, 'manifest.json'));
    await symlink(join(outside, 'external.json'), join(root, 'manifest.json'));
    await expect(readCurriculum(root)).rejects.toThrow(
      /manifest.json.*outside/i,
    );
  });

  test('rejects directories and cross-file identity mismatches', async () => {
    const { root } = await createTree();
    await writeJson(root, 'manifest.json', manifest());
    await mkdir(join(root, 'problems/1/metadata.json'), { recursive: true });
    await expect(readCurriculum(root)).rejects.toThrow(/metadata.json.*file/i);

    await rm(join(root, 'problems/1/metadata.json'), { recursive: true });
    await writeJson(root, 'problems/1/metadata.json', {
      ...draft,
      problemId: 'leetcode:2',
    });
    await expect(readCurriculum(root)).rejects.toThrow(
      /metadata.json.*leetcode:1/i,
    );

    await writeJson(root, 'problems/1/metadata.json', draft);
    await writeJson(root, 'paths/all-problems.json', {
      ...path,
      id: 'other-path',
    });
    await expect(readCurriculum(root)).rejects.toThrow(
      /all-problems.json.*all-problems/i,
    );
  });
});
