import { createHash } from 'node:crypto';
import {
  mkdir,
  mkdtemp,
  readFile,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { expect, it } from 'vitest';
import { prepareContent } from '../../../../src/content/prepare.js';
import { readPublishedCurriculum } from '../../../../src/content/leetcode/publication.js';
import { readSourceMap } from '../../../../src/content/leetcode/source-map.js';
import { curriculum, firstProblem } from './schema-fixtures.js';

interface RecordBase {
  sourcePath: string;
  sha256: string;
  filenameNumber: number | null;
  duplicateFilenameNumber?: number;
  disposition: string;
  reason: string;
  problemId?: string;
  officialSource?: { url: string; checkedAt: string };
}

const archivePrefix = 'Interview/leetcode/Solutions/';
const root = new URL('../../../../../', import.meta.url);

function digest(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex');
}

it('preserves the frozen originals and records the approved archive provenance', async () => {
  const curriculum = new URL('site/content/leetcode/', root);
  const raw = await readFile(new URL('source-map.json', curriculum), 'utf8');
  const map = JSON.parse(raw) as {
    version: number;
    records: { shards: string[] };
  };
  expect(Object.keys(map).sort()).toEqual(['records', 'version']);
  expect(map.version).toBe(1);

  const records = (
    await Promise.all(
      map.records.shards.map(async (shard) => {
        const raw = await readFile(
          new URL(`source-map/${shard}`, curriculum),
          'utf8',
        );
        return JSON.parse(raw) as RecordBase[];
      }),
    )
  ).flat();
  const paths = records.map(({ sourcePath }) => sourcePath);
  expect(paths).toHaveLength(366);
  expect(paths).toEqual([...new Set(paths)].sort());
  expect(
    digest(
      records
        .map(({ sourcePath, sha256 }) => `${sourcePath}\0${sha256}\n`)
        .join(''),
    ),
  ).toBe('61e8e9afa3609d34de3004be4014a8e6651b63e3707b732a298303432ffdb3b5');

  // These aggregate hashes pin the frozen path/digest pairs and independent group membership.
  const duplicates = records.filter(
    (record) => record.duplicateFilenameNumber !== undefined,
  );
  expect(duplicates).toHaveLength(164);
  expect(
    new Set(duplicates.map((record) => record.duplicateFilenameNumber)).size,
  ).toBe(77);
  expect(
    digest(
      duplicates
        .map(
          ({ sourcePath, duplicateFilenameNumber }) =>
            `${sourcePath}\0${duplicateFilenameNumber}\n`,
        )
        .join(''),
    ),
  ).toBe('3a06aea4c0a063cf3fbdb31a8b03f7af36e668af5e01ad12e6de26979663685c');

  const approved = [
    [
      '18 Org/meta/LC/1 Two Sum.py',
      1,
      'solver_variant',
      'https://leetcode.com/problems/two-sum/',
    ],
    [
      '1_Two_Sum.py',
      1,
      'solver_variant',
      'https://leetcode.com/problems/two-sum/',
    ],
    [
      '3_Longest_Substring_Without_Repeating_Characters.py',
      3,
      'solver_variant',
      'https://leetcode.com/problems/longest-substring-without-repeating-characters/',
    ],
    [
      '20_Valid_Parentheses.py',
      20,
      'solver_variant',
      'https://leetcode.com/problems/valid-parentheses/',
    ],
    [
      '14 DP/64 Minimum Path Sum.py',
      64,
      'solver_variant',
      'https://leetcode.com/problems/minimum-path-sum/',
    ],
    [
      '18 Org/meta/LC/98 Validate Binary Search Tree.py',
      98,
      'solver_variant',
      'https://leetcode.com/problems/validate-binary-search-tree/',
    ],
    [
      '98_Validate_Binary_Search_Tree.py',
      98,
      'solver_variant',
      'https://leetcode.com/problems/validate-binary-search-tree/',
    ],
    [
      '127_Word_Ladder.py',
      127,
      'solver_variant',
      'https://leetcode.com/problems/word-ladder/',
    ],
    [
      '146_LRU_Cache.py',
      146,
      'solver_variant',
      'https://leetcode.com/problems/lru-cache/',
    ],
    [
      '450_Count_Good_Nodes_in_Binary_Tree.py',
      1448,
      'statement_only',
      'https://leetcode.com/problems/count-good-nodes-in-binary-tree/description/',
    ],
    [
      '11 Graph/Path Sum IV.py',
      666,
      'link_only',
      'https://leetcode.com/articles/?page=62&tag=linked-list',
    ],
    [
      '271_Encode_and_Decode_Strings.py',
      271,
      'statement_only',
      'https://leetcode.com/articles/?page=106',
    ],
    [
      '5 String/271 Encode and Decode Strings.py',
      271,
      'link_only',
      'https://leetcode.com/articles/?page=106',
    ],
  ] as const;
  const allowed = [
    'solver_variant',
    'statement_only',
    'link_only',
    'practice',
    'pending_reconciliation',
    'out_of_range',
    'archive_support',
    'empty',
  ];

  for (const record of records) {
    const {
      sourcePath,
      filenameNumber,
      reason,
      sha256,
      disposition,
      problemId,
      officialSource,
    } = record;
    expect(sourcePath.startsWith(archivePrefix)).toBe(true);
    expect(reason.trim()).not.toBe('');
    expect(allowed).toContain(disposition);
    expect(
      Object.keys(record).every((key) =>
        [
          'sourcePath',
          'sha256',
          'filenameNumber',
          'duplicateFilenameNumber',
          'disposition',
          'reason',
          'problemId',
          'officialSource',
        ].includes(key),
      ),
    ).toBe(true);
    const prefix = /^(\d+)[ _.-]/.exec(basename(sourcePath));
    expect(filenameNumber).toBe(prefix ? Number(prefix[1]) : null);
    expect(
      digest(await readFile(resolve(fileURLToPath(root), sourcePath))),
    ).toBe(sha256);
    if (record.duplicateFilenameNumber !== undefined)
      expect(record.duplicateFilenameNumber).toBe(filenameNumber);
    if (problemId === undefined) {
      expect(officialSource).toBeUndefined();
      expect(disposition).not.toBe('solver_variant');
    } else {
      expect(problemId).toMatch(/^leetcode:[1-9]\d*$/);
      expect(officialSource?.url).toMatch(
        disposition === 'solver_variant'
          ? /^https:\/\/leetcode\.com\/problems\/[a-z0-9-]+\/$/
          : /^https:\/\/leetcode\.com\/(?:problems\/[a-z0-9-]+\/(?:description\/)?|articles\/\?page=\d+(?:&tag=[a-z0-9-]+)?)$/,
      );
      expect(officialSource?.checkedAt).toMatch(
        /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/,
      );
    }
  }

  const mapped = records.filter((record) => record.problemId !== undefined);
  expect(mapped).toHaveLength(approved.length);
  for (const [relativePath, number, disposition, evidenceUrl] of approved) {
    expect(
      mapped.find(
        ({ sourcePath }) => sourcePath === archivePrefix + relativePath,
      ),
    ).toMatchObject({
      problemId: `leetcode:${number}`,
      disposition,
      officialSource: {
        url: evidenceUrl,
      },
    });
  }
  expect(mapped.some(({ problemId }) => problemId === 'leetcode:175')).toBe(
    false,
  );
  expect(raw).not.toMatch(/[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}/);
  const eligible = await readSourceMap(
    fileURLToPath(new URL('site/content/leetcode/', root)),
  );
  expect([...eligible!.keys()]).toEqual(
    mapped
      .filter(({ disposition }) => disposition === 'solver_variant')
      .map(({ sourcePath }) => sourcePath),
  );
});

const sourcePath = archivePrefix + '1_Two_Sum.py';
const sourceCode = Buffer.concat([
  Buffer.from('# Two Sum '),
  Buffer.from([0xff]),
  Buffer.from('\r\n'),
]);
const solver = {
  sourcePath,
  sha256: digest(sourceCode),
  filenameNumber: 1,
  duplicateFilenameNumber: 1,
  disposition: 'solver_variant',
  reason: 'Reviewed original',
  problemId: 'leetcode:1',
  officialSource: {
    url: firstProblem().officialUrl,
    checkedAt: '2026-11-22T11:00:00Z',
  },
};

async function sourceMapFixture(
  onCleanup: (cleanup: () => Promise<void>) => void,
) {
  const rootDir = await mkdtemp(join(tmpdir(), 'notes-curriculum-source-map-'));
  onCleanup(() => rm(rootDir, { recursive: true, force: true }));
  const outputDir = join(rootDir, 'site/.generated');
  const curriculumDir = join(rootDir, 'site/content/leetcode');
  const policyPath = join(rootDir, 'site/content/publication.json');
  async function put(path: string, data: string | Buffer) {
    await mkdir(dirname(path), { recursive: true });
    await writeFile(path, data);
  }
  async function json(path: string, data: unknown) {
    await put(path, JSON.stringify(data));
  }
  const { problems } = curriculum();
  const prose = '# Two Sum';
  await Promise.all([
    json(policyPath, {
      roots: [
        'Books',
        'Classes',
        'Courses',
        'Interview',
        'Languages',
        'Tutorials',
      ],
      exclude: ['**/hidden/**'],
      repositoryPublic: true,
      repositoryUrl: 'https://github.com/angadsinghsandhu/Notes',
      revision: 'a'.repeat(40),
    }),
    json(join(curriculumDir, 'manifest.json'), {
      version: 1,
      problems: [{ ...firstProblem(), status: 'draft' }, ...problems.slice(1)],
      lessons: ['leetcode:1'],
      paths: [],
    }),
    json(join(curriculumDir, 'problems/1/metadata.json'), {
      problemId: 'leetcode:1',
      prose: { path: 'lesson.md', sha256: digest(prose) },
      examples: null,
      approaches: [],
      review: null,
    }),
    put(join(curriculumDir, 'problems/1/lesson.md'), prose),
    put(join(rootDir, sourcePath), sourceCode),
    put(join(rootDir, archivePrefix, 'hidden/1_Draft.py'), sourceCode),
    put(join(rootDir, archivePrefix, '1_Notes.md'), 'Reader notes'),
  ]);
  const options = {
    rootDir,
    outputDir,
    curriculumDir,
    policyPath,
    hosted: false,
  };
  const mapPath = join(curriculumDir, 'source-map.json');
  return {
    options,
    mapPath,
    prepare: () => prepareContent(options),
    writeMap: (records: unknown, version = 1) =>
      json(mapPath, { version, records }),
    writeShard: (name: string, records: unknown) =>
      json(join(curriculumDir, 'source-map', name), records),
    snapshot: (generation: string) =>
      readPublishedCurriculum(outputDir, generation),
    manifest: () => readFile(join(outputDir, 'current/manifest.json')),
  };
}

it('loads each map from disk and only links published code to a matching lesson', async ({
  onTestFinished,
}) => {
  const fixture = await sourceMapFixture(onTestFinished);
  const legacy = await fixture.prepare();
  expect(legacy.diagnostics).toEqual([]);
  expect(
    (await fixture.snapshot(legacy.manifest.curriculumGeneration!))
      .sourceVariants,
  ).toEqual([]);

  const records = [
    solver,
    { ...solver, sourcePath: archivePrefix + '1_Notes.md' },
    { ...solver, sourcePath: archivePrefix + '1_Missing.py' },
    { ...solver, sourcePath: archivePrefix + 'hidden/1_Draft.py' },
    { ...solver, sourcePath: archivePrefix + '1_two_sum.py' },
    {
      ...solver,
      sourcePath: archivePrefix + '175_Reference.py',
      filenameNumber: 175,
      duplicateFilenameNumber: undefined,
      disposition: 'statement_only',
      problemId: 'leetcode:175',
      officialSource: {
        ...solver.officialSource,
        url: 'https://leetcode.com/articles/?page=106&tag=linked-list',
      },
    },
    {
      ...solver,
      sourcePath: archivePrefix + '2100_Outside.py',
      filenameNumber: 2100,
      duplicateFilenameNumber: undefined,
      disposition: 'out_of_range',
      problemId: undefined,
      officialSource: undefined,
    },
  ];
  await fixture.writeMap(records);
  const mapped = await fixture.prepare();
  expect(mapped.diagnostics).toEqual([]);
  const generation = mapped.manifest.curriculumGeneration!;
  expect(generation).not.toBe(legacy.manifest.curriculumGeneration);
  const source = mapped.manifest.entries.find(
    (entry) => entry.sourcePath === sourcePath,
  )!;
  expect(source).toEqual(
    legacy.manifest.entries.find((entry) => entry.sourcePath === sourcePath),
  );
  expect(await readFile(join(fixture.options.rootDir, sourcePath))).toEqual(
    sourceCode,
  );
  expect((await fixture.snapshot(generation)).sourceVariants).toEqual([
    {
      sourceId: source.id,
      sourceRoute: source.route,
      problemId: 'leetcode:1',
      lessonRoute: '/practice/leetcode/1/',
    },
  ]);

  await fixture.writeMap({ shards: ['first.json', 'rest.json'] });
  await fixture.writeShard('first.json', records.slice(0, 1));
  await fixture.writeShard('rest.json', records.slice(1));
  const sharded = await fixture.prepare();
  expect(sharded.diagnostics).toEqual([]);
  expect(sharded.manifest.curriculumGeneration).toBe(generation);

  await fixture.writeMap([{ ...solver, disposition: 'statement_only' }]);
  const reference = await fixture.prepare();
  expect(reference.diagnostics).toEqual([]);
  expect(reference.manifest.curriculumGeneration).toBe(
    legacy.manifest.curriculumGeneration,
  );

  await rm(fixture.mapPath);
  const removed = await fixture.prepare();
  expect(removed.diagnostics).toEqual([]);
  expect(removed.manifest.curriculumGeneration).toBe(
    legacy.manifest.curriculumGeneration,
  );
});

it('rejects wrong and repeated source map shards without changing publication', async ({
  onTestFinished,
}) => {
  const fixture = await sourceMapFixture(onTestFinished);
  const initial = await fixture.prepare();
  expect(initial.diagnostics).toEqual([]);
  const previous = await fixture.manifest();
  await fixture.writeShard('first.json', [solver]);
  await fixture.writeShard('second.json', [
    {
      ...solver,
      problemId: 'leetcode:3',
      officialSource: {
        ...solver.officialSource,
        url: 'https://leetcode.com/problems/longest-substring-without-repeating-characters/',
      },
    },
  ]);
  await fixture.writeShard('invalid.json', [{ ...solver, sha256: 'invalid' }]);
  for (const [shards, error] of [
    [['first.json', 'missing.json'], 'missing.json'],
    [['first.json', 'first.json'], 'Duplicate shard'],
    [['first.json', 'second.json'], 'Duplicate source path'],
    [['invalid.json'], 'invalid.json'],
  ] as const) {
    await fixture.writeMap({ shards });
    const invalid = await fixture.prepare();
    expect(invalid.diagnostics[0]?.message).toContain(error);
    expect(await fixture.manifest()).toEqual(previous);
  }
});

it('retains the selected generation when mapped bytes or official identity disagree', async ({
  onTestFinished,
}) => {
  const fixture = await sourceMapFixture(onTestFinished);
  await fixture.writeMap([solver]);
  const valid = await fixture.prepare();
  expect(valid.diagnostics).toEqual([]);
  const generation = valid.manifest.curriculumGeneration!;
  const previous = await fixture.manifest();
  const snapshot = await fixture.snapshot(generation);

  await writeFile(join(fixture.options.rootDir, sourcePath), '# Changed bytes');
  expect((await fixture.prepare()).diagnostics).toEqual([
    expect.objectContaining({ message: expect.stringContaining('SHA-256') }),
  ]);
  await writeFile(join(fixture.options.rootDir, sourcePath), sourceCode);

  await fixture.writeMap([
    {
      ...solver,
      officialSource: {
        ...solver.officialSource,
        url: 'https://leetcode.com/problems/valid-parentheses/',
      },
    },
  ]);
  expect((await fixture.prepare()).diagnostics).toEqual([
    expect.objectContaining({
      message: expect.stringContaining('official curriculum problem'),
    }),
  ]);
  expect(await fixture.manifest()).toEqual(previous);
  expect(await fixture.snapshot(generation)).toEqual(snapshot);
});

it('rejects malformed map data and preserves the last good publication', async ({
  onTestFinished,
}) => {
  const fixture = await sourceMapFixture(onTestFinished);
  const initial = await fixture.prepare();
  expect(initial.diagnostics).toEqual([]);
  const previous = await fixture.manifest();
  const malformed: unknown[][] = [
    [{ ...solver, sourcePath: archivePrefix + '../escaped.py' }],
    [{ ...solver, sourcePath: archivePrefix + 'Cafe\u0301.py' }],
    [{ ...solver, sourcePath: archivePrefix + 'hidden\\escaped.py' }],
    [solver, solver],
    [{ ...solver, disposition: 'solved' }],
    [{ ...solver, sourcePath: archivePrefix + 'file\u0000.py' }],
    [{ ...solver, sourcePath: archivePrefix + 'file\u007f.py' }],
    [{ ...solver, filenameNumber: 2 }],
    [{ ...solver, duplicateFilenameNumber: 2 }],
    [{ ...solver, unexpected: true }],
    [{ ...solver, sha256: 'discarded' }],
    [{ ...solver, problemId: 'leetcode:2001' }],
    [{ ...solver, officialSource: undefined }],
    [{ ...solver, disposition: 'link_only', problemId: undefined }],
    [
      {
        ...solver,
        disposition: 'link_only',
        officialSource: {
          ...solver.officialSource,
          url: 'https://leetcode.com.example/articles/?page=106',
        },
      },
    ],
    [
      {
        ...solver,
        officialSource: {
          ...solver.officialSource,
          url: 'https://leetcode.com/articles/?page=106',
        },
      },
    ],
    [
      {
        ...solver,
        officialSource: {
          ...solver.officialSource,
          checkedAt: '2026-02-30T12:00:00Z',
        },
      },
    ],
  ];
  for (const records of malformed) {
    await fixture.writeMap(records);
    expect((await fixture.prepare()).diagnostics[0]?.message).toContain(
      'source-map.json',
    );
  }
  await fixture.writeMap([solver], 2);
  expect((await fixture.prepare()).diagnostics[0]?.message).toContain(
    'source-map.json',
  );
  await writeFile(fixture.mapPath, '{');
  expect((await fixture.prepare()).diagnostics[0]?.message).toContain(
    'source-map.json',
  );
  await rm(fixture.mapPath);
  await mkdir(fixture.mapPath);
  expect((await fixture.prepare()).diagnostics[0]?.message).toContain(
    'Expected a regular file',
  );
  await rm(fixture.mapPath, { recursive: true });
  await symlink('missing.json', fixture.mapPath);
  expect((await fixture.prepare()).diagnostics[0]?.message).toContain(
    'source-map.json',
  );
  expect(await fixture.manifest()).toEqual(previous);
});

it('preserves injected variants for legacy callers and rejects conflicting sources', async ({
  onTestFinished,
}) => {
  const fixture = await sourceMapFixture(onTestFinished);
  const prepare = () =>
    prepareContent({
      ...fixture.options,
      sourceVariants: new Map([[sourcePath, 'leetcode:1']]),
    });
  const legacy = await prepare();
  expect(legacy.diagnostics).toEqual([]);
  expect(
    (await fixture.snapshot(legacy.manifest.curriculumGeneration!))
      .sourceVariants,
  ).toHaveLength(1);
  const previous = await fixture.manifest();
  await fixture.writeMap([]);
  expect((await prepare()).diagnostics[0]?.message).toContain('sourceVariants');
  expect(await fixture.manifest()).toEqual(previous);
});
