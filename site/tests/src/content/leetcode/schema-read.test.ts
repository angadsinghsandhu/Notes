import {
  mkdir,
  mkdtemp,
  readFile,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, describe, expect, test } from 'vitest';
import {
  readCurriculum,
  validateLearningPaths,
} from '../../../../src/content/index.js';

test('loads the checked-in curriculum inventory with all 2,000 targets accounted for', async () => {
  const root = new URL('../../../../content/leetcode/', import.meta.url);
  const { version, problems, lessons, paths } = await readCurriculum(
    fileURLToPath(root),
  );
  const numbers = Array.from({ length: 2000 }, (_, index) => index + 1);
  const pilot = [
    [1, 'Two Sum', 'easy'],
    [3, 'Longest Substring Without Repeating Characters', 'medium'],
    [20, 'Valid Parentheses', 'easy'],
    [64, 'Minimum Path Sum', 'medium'],
    [98, 'Validate Binary Search Tree', 'medium'],
    [127, 'Word Ladder', 'hard'],
    [146, 'LRU Cache', 'medium'],
    [175, 'Combine Two Tables', 'easy'],
  ] as const;
  const sortedProblems = problems.toSorted((a, b) => a.number - b.number);
  const unknown = sortedProblems.filter(
    ({ evidence }) => !evidence.officialQuestion,
  );
  const byNumber = new Map(
    problems.map((problem) => [problem.number, problem]),
  );

  expect(version).toBe(1);
  expect(sortedProblems.map(({ number, id }) => [number, id])).toEqual(
    numbers.map((number) => [number, `leetcode:${number}`]),
  );
  for (const [number, title, difficulty] of pilot) {
    const slug = title.toLowerCase().replaceAll(' ', '-');
    const officialUrl = `https://leetcode.com/problems/${slug}/`;
    expect(byNumber.get(number)).toMatchObject({
      title,
      slug,
      difficulty,
      officialUrl,
      domain: number === 175 ? 'sql' : 'algorithm',
      evidence: {
        officialQuestion: {
          frontendNumber: number,
          title,
          sourceUrl: officialUrl,
        },
      },
    });
  }
  for (const problem of unknown) {
    expect(problem).toMatchObject({
      title: null,
      slug: null,
      officialUrl: null,
      domain: null,
      difficulty: null,
      topics: [],
    });
  }

  const path = validateLearningPaths(paths, problems).get('all-problems');
  expect(path).toBeDefined();
  const targets = path!.nodes.filter((node) => node.kind === 'problem');
  expect(targets.map(({ problemId }) => problemId).sort()).toEqual(
    problems.map(({ id }) => id).sort(),
  );
  const nodes = new Map(path!.nodes.map((node) => [node.id, node]));
  const pending = nodes.get('pending-classification');
  if (unknown.length > 0) {
    expect(pending).toMatchObject({
      kind: 'stage',
      title: 'Pending classification',
    });
  }
  const descendants = new Set(pending?.childIds);
  for (const id of descendants) {
    for (const child of nodes.get(id)!.childIds) descendants.add(child);
  }
  expect(
    targets
      .filter(({ id }) => descendants.has(id))
      .map(({ problemId }) => problemId)
      .sort(),
  ).toEqual(unknown.map(({ id }) => id).sort());

  const targetByProblem = new Map(
    targets.map((node) => [node.problemId, node]),
  );
  for (const id of ['leetcode:3', 'leetcode:146'] as const) {
    expect(targetByProblem.get(id)?.prerequisiteIds).toContain(
      targetByProblem.get('leetcode:1')!.id,
    );
  }

  const report: unknown = JSON.parse(
    await readFile(new URL('coverage-report.json', root), 'utf8'),
  );
  const plannedIds = sortedProblems
    .filter(({ status }) => status === 'planned')
    .map(({ number }) => number);
  const draftIds = sortedProblems
    .filter(({ status }) => status === 'draft')
    .map(({ number }) => number);
  const verified = sortedProblems.filter(({ status }) => status === 'verified');
  const reviewByProblem = new Map(
    lessons.map(({ problemId, review }) => [problemId, review]),
  );
  expect(report).toEqual({
    version: 1,
    plannedIds,
    draftIds,
    verifiedIds: verified.map(({ number }) => number),
    evidence: verified.map(({ number, id }) => ({
      id: number,
      contentSha256: reviewByProblem.get(id)!.contentSha256,
    })),
    unresolved: [
      {
        reason: 'official-metadata-pending',
        ids: unknown.map(({ number }) => number),
      },
      {
        reason: 'lesson-evidence-pending',
        ids: sortedProblems
          .filter(({ status }) => status !== 'verified')
          .map(({ number }) => number),
      },
    ].filter(({ ids }) => ids.length > 0),
  });
});

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
