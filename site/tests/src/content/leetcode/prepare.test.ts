import {
  mkdir,
  mkdtemp,
  readFile,
  rename,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, beforeEach, expect, test } from 'vitest';
import { prepareCurriculum } from '../../../../src/content/leetcode/prepare.js';
import {
  digest,
  prepareFixture,
  sourceEntry,
  traceFixture,
} from './prepare-fixtures.js';

const checkComplement = {
  stepId: 'check-0',
  codeLines: [1],
  explanation: 'Look for the complement of 2.',
};

let directory: string;
beforeEach(async () => {
  directory = await mkdtemp(join(tmpdir(), 'curriculum-prepare-'));
});
afterEach(async () => {
  await rm(directory, { recursive: true, force: true });
});

test('publishes sanitized lesson, verified progress and a generation-bound trace package', async () => {
  const steps = [
    checkComplement,
    {
      stepId: 'answer',
      codeLines: [2, 1],
      explanation: 'Return the pair.',
    },
  ];
  const fixture = await prepareFixture(directory, {
    trace: (sha) =>
      '\n'.repeat(500) +
      traceFixture(sha, {
        frames: steps.map((step) => ({
          ...step,
          state: { kind: 'array', items: [2, 7] },
          highlights: [{ index: 0 }],
        })),
      }),
  });
  const snapshot = await prepareCurriculum(fixture.definition, fixture);
  expect(snapshot.generation).toMatch(/^[a-f0-9]{64}$/);
  expect(snapshot.routes.map(({ route }) => route)).toEqual([
    '/practice/leetcode/',
    '/practice/paths/',
    '/practice/leetcode/1/',
    '/practice/paths/all-problems/',
  ]);
  expect(snapshot.lessons[0]?.bodyHtml).toContain(
    'href="/practice/leetcode/1/#invariant"',
  );
  expect(snapshot.lessons[0]?.bodyHtml).toContain('id="invariant"');
  expect(snapshot.lessons[0]?.bodyHtml).not.toContain('bad()');
  expect(snapshot.lessons[0]?.approaches[0]?.codeHtml).toContain('shiki');
  expect(snapshot.lessons[0]?.approaches[0]?.transcripts).toEqual([
    { exampleId: 'pair', steps },
  ]);
  const reference = snapshot.lessons[0]!.approaches[0]!.trace!;
  const bytes = await readFile(
    join(fixture.outputDir, 'worker-assets', reference.url),
  );
  expect(reference.sha256).toBe(digest(bytes));
  expect(reference.url).toBe(`/practice-traces/${reference.sha256}.json`);
  expect(reference.bytes).toBe(bytes.length);
  expect(bytes.toString()).toBe(
    `{"version":1,"traces":[${JSON.stringify(JSON.parse(fixture.trace))}]}\n`,
  );
  const registry = await readFile(
    join(fixture.outputDir, 'progress-registry.json'),
    'utf8',
  );
  expect(JSON.parse(registry)).toEqual({
    version: 1,
    generation: snapshot.generation,
    problems: [
      {
        problemId: 'leetcode:1',
        revision: fixture.definition.lessons[0]?.review?.contentSha256,
      },
    ],
  });
  const inventory = await readFile(
    join(fixture.outputDir, 'trace-assets.json'),
    'utf8',
  );
  expect(JSON.parse(inventory)).toEqual({
    version: 1,
    generation: snapshot.generation,
    assets: [reference],
  });
  const saved = await readFile(
    join(fixture.outputDir, 'curriculum.json'),
    'utf8',
  );
  expect(JSON.parse(saved)).toEqual(snapshot);
  expect(saved).not.toMatch(
    /\/private\/source|Editorial reviewer|editorialNotes|solutions\.py|lesson\.md/,
  );
});

test('draft_body_not_reported_verified', async () => {
  const fixture = await prepareFixture(directory, { draft: true });
  const snapshot = await prepareCurriculum(fixture.definition, fixture);
  expect(snapshot.lessons[0]).toMatchObject({ status: 'draft' });
  expect(snapshot.problems.slice(0, 2).map(({ status }) => status)).toEqual([
    'draft',
    'planned',
  ]);
  const registry = await readFile(
    join(fixture.outputDir, 'progress-registry.json'),
    'utf8',
  );
  expect(JSON.parse(registry)).toMatchObject({ problems: [] });
});

test('a readable draft retains transcripts in trace evidence order', async () => {
  const fixture = await prepareFixture(directory, {
    draft: true,
    traceCount: 2,
  });
  fixture.definition.lessons[0]!.approaches[0]!.traces.reverse();
  const snapshot = await prepareCurriculum(fixture.definition, fixture);
  const approach = snapshot.lessons[0]?.approaches[0];
  expect(approach?.transcripts).toEqual(
    ['pair-1', 'pair'].map((exampleId) => ({
      exampleId,
      steps: [checkComplement],
    })),
  );
  expect(approach?.trace?.exampleIds).toEqual(['pair-1', 'pair']);
});

test('a draft without prose stays pending without publishing a route', async () => {
  const fixture = await prepareFixture(directory, { draft: true, prose: null });
  const snapshot = await prepareCurriculum(fixture.definition, fixture);
  expect(snapshot.problems[0]?.status).toBe('draft');
  expect(snapshot.lessons).toEqual([]);
  expect(snapshot.routes.map(({ route }) => route)).not.toContain(
    '/practice/leetcode/1/',
  );
});

test('claims_new_routes_against_aliases_and_source_folders', async () => {
  const fixture = await prepareFixture(directory, {
    source: sourceEntry({ aliases: ['/PRACTICE/LEETCODE/1'] }),
  });
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /Route collision/i,
  );
  const clean = await prepareFixture(directory);
  await expect(
    prepareCurriculum(clean.definition, {
      ...clean,
      additionalPages: [
        { route: '/Practice/Paths//All-Problems', owner: 'source folder' },
      ],
    }),
  ).rejects.toThrow(/Route collision.*source folder/i);
  await expect(
    prepareFixture(directory, {
      source: sourceEntry({ aliases: ['/Practice-Traces/Old.json'] }),
    }),
  ).rejects.toThrow('reserved Worker namespace /practice-traces/');
});

test('source_variants_link_without_rewriting_archive', async () => {
  const fixture = await prepareFixture(directory);
  const original = structuredClone(fixture.source);
  const snapshot = await prepareCurriculum(fixture.definition, {
    ...fixture,
    sourceVariants: new Map([[original.sourcePath, 'leetcode:1']]),
  });
  expect(snapshot.sourceVariants).toEqual([
    {
      sourceId: original.id,
      sourceRoute: original.route,
      problemId: 'leetcode:1',
      lessonRoute: '/practice/leetcode/1/',
    },
  ]);
  expect(fixture.source).toEqual(original);
  await expect(
    prepareCurriculum(fixture.definition, {
      ...fixture,
      sourceVariants: new Map([['/private/path', 'leetcode:1']]),
    }),
  ).rejects.toThrow(/source variant/i);
});

test('modified evidence fails preparation and leaves the old staging generation untouched', async () => {
  const fixture = await prepareFixture(directory);
  const before = await prepareCurriculum(fixture.definition, fixture);
  await writeFile(join(fixture.lessonDir, 'lesson.md'), 'changed');
  await expect(
    prepareCurriculum(fixture.definition, {
      ...fixture,
      outputDir: join(directory, 'next'),
    }),
  ).rejects.toThrow(/sha256/i);
  const saved = await readFile(
    join(fixture.outputDir, 'curriculum.json'),
    'utf8',
  );
  expect(JSON.parse(saved)).toEqual(before);
});

test('rejects symlinked evidence outside its lesson even with matching bytes', async () => {
  const fixture = await prepareFixture(directory);
  const outside = join(fixture.rootDir, 'elsewhere.md');
  const path = join(fixture.lessonDir, 'lesson.md');
  await writeFile(outside, await readFile(path));
  await rm(path);
  await symlink(outside, path);
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /outside.*lesson/i,
  );
});

test.each([
  {
    label: 'wrong identity',
    trace: () => '{"frames":[]}',
    reason: /identity/i,
  },
  { label: 'invalid JSON', trace: () => '{', reason: /json/i },
  {
    label: 'oversize trace',
    trace: () => ' '.repeat(1_048_577),
    reason: /1 MiB/i,
  },
  {
    label: 'too many frames',
    trace: (implementationSha256: string) =>
      traceFixture(implementationSha256, {
        frames: Array.from({ length: 2001 }, () => null),
      }),
    reason: /2000 frames/i,
  },
])('rejects $label', async ({ trace, reason }) => {
  const fixture = await prepareFixture(directory, { trace });
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    reason,
  );
});

test('a draft shows native code without publishing an empty trace package', async () => {
  const fixture = await prepareFixture(directory, {
    draft: true,
    approach: 'shell',
    traceCount: 0,
  });
  const snapshot = await prepareCurriculum(fixture.definition, {
    ...fixture,
    sourceVariants: new Map([[fixture.source.sourcePath, 'leetcode:2']]),
  });
  expect(snapshot.lessons[0]?.approaches[0]).toMatchObject({
    language: 'shell',
    entryPoint: null,
    trace: null,
    transcripts: [],
  });
  expect(snapshot.sourceVariants).toEqual([]);
});

test('publishes evidence dates and rejects credential-bearing public source links', async () => {
  const fixture = await prepareFixture(directory);
  const snapshot = await prepareCurriculum(fixture.definition, fixture);
  expect(snapshot.problems[0]).toMatchObject({
    officialQuestionObservedOn: '2026-10-24',
    companies: [
      {
        companyId: 'acme',
        observedOn: '2026-10-24',
        reportingPeriod: 'October 2026',
      },
      {
        companyId: 'public-company',
        observedOn: '2026-10-24',
        sourceUrl: 'https://example.com/report',
      },
    ],
  });
  const credentialed = await prepareFixture(directory, {
    companyUrl: 'https://notes:secret@example.com/report',
  });
  await expect(
    prepareCurriculum(credentialed.definition, credentialed),
  ).rejects.toThrow(/credentials/);
});

test('rejects an entire lesson directory symlink to another lesson', async () => {
  const fixture = await prepareFixture(directory);
  const moved = join(fixture.rootDir, 'problems/2');
  await rename(fixture.lessonDir, moved);
  await symlink(moved, fixture.lessonDir);
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /original lesson root/,
  );
});

test('requires regular evidence files', async () => {
  const fixture = await prepareFixture(directory);
  const prose = join(fixture.lessonDir, 'lesson.md');
  await rm(prose);
  await mkdir(prose);
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /regular file/,
  );
});

test('rejects oversized approach package even when its individual examples are in bounds', async () => {
  const fixture = await prepareFixture(directory, { traceCount: 25 });
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /25 MiB trace package/,
  );
});

test.each([
  { version: 2 },
  { extra: 'private' },
  { frames: false },
  { result: undefined },
])('rejects public trace structure with %j', async (changes) => {
  const fixture = await prepareFixture(directory, {
    trace: (implementationSha256) =>
      traceFixture(implementationSha256, changes),
  });
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /trace structure/,
  );
});

test('preparation ignores source formatting for package identity and binds the new review', async () => {
  const fixture = await prepareFixture(directory);
  const initial = await prepareCurriculum(fixture.definition, fixture);
  const same = await prepareCurriculum(fixture.definition, {
    ...fixture,
    outputDir: join(directory, 'same'),
  });
  expect(same.generation).toBe(initial.generation);

  const updated = await prepareFixture(directory, {
    trace: () => fixture.trace + '\n',
  });
  const next = await prepareCurriculum(updated.definition, {
    ...updated,
    outputDir: join(directory, 'next'),
  });
  const oldRef = initial.lessons[0]!.approaches[0]!.trace!;
  const newRef = next.lessons[0]!.approaches[0]!.trace!;
  expect(newRef.url).toBe(oldRef.url);
  expect(next.generation).not.toBe(initial.generation);
  for (const [outputDir, reference] of [
    [fixture.outputDir, oldRef],
    [join(directory, 'next'), newRef],
  ] as const)
    expect(
      digest(await readFile(join(outputDir, 'worker-assets', reference.url))),
    ).toBe(reference.sha256);
});

test('source variant insertion order leaves all generation files byte-identical', async () => {
  const fixture = await prepareFixture(directory);
  const second = sourceEntry({
    id: 'another-source',
    sourcePath: 'Interview/Alternate.py',
    route: '/resources/interview/alternate-py/',
  });
  fixture.sourceCatalog.sources.set(second.sourcePath, second);
  fixture.sourceCatalog.routes.set(second.route, second);
  const variants = [
    [fixture.source.sourcePath, 'leetcode:1'],
    [second.sourcePath, 'leetcode:1'],
  ] as const;
  const first = await prepareCurriculum(fixture.definition, {
    ...fixture,
    sourceVariants: new Map(variants),
  });
  const secondDir = join(directory, 'reversed');
  const reversed = await prepareCurriculum(fixture.definition, {
    ...fixture,
    outputDir: secondDir,
    sourceVariants: new Map([...variants].reverse()),
  });
  for (const filename of [
    'curriculum.json',
    'progress-registry.json',
    'trace-assets.json',
  ]) {
    const before = await readFile(join(fixture.outputDir, filename));
    const after = await readFile(join(secondDir, filename));
    expect(after.equals(before), filename).toBe(true);
  }
  expect(first.generation).toBe(reversed.generation);
});

test('lesson prose can link to known curriculum indexes and paths without changing the archive resolver', async () => {
  const fixture = await prepareFixture(directory, {
    prose:
      '[Library](/practice/leetcode/) [Path index](/practice/paths/) [Study path](/practice/paths/all-problems/)',
  });
  const archiveRoutes = [...fixture.sourceCatalog.routes];
  const snapshot = await prepareCurriculum(fixture.definition, fixture);
  for (const route of [
    '/practice/leetcode/',
    '/practice/paths/',
    '/practice/paths/all-problems/',
  ])
    expect(snapshot.lessons[0]?.bodyHtml).toContain(`href="${route}"`);
  expect([...fixture.sourceCatalog.routes]).toEqual(archiveRoutes);
});

test('lesson prose still rejects unknown curriculum paths', async () => {
  const fixture = await prepareFixture(directory, {
    prose: '[Unknown](/practice/paths/unknown/)',
  });
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /cannot resolve \/practice\/paths\/unknown\//,
  );
});

test.each([
  ['\uFEFF\r\n# heading\r\n\r\nanswer = 1\r\n', 4],
  ['\r# heading\r\ranswer = 1', 4],
  ['answer = 1\n', 1],
  ['answer = 1', 1],
  ['', 0],
] as const)(
  'binds trace code links to physical source lines in %j',
  async (code, lineCount) => {
    function linkedTrace(implementationSha256: string, line: number) {
      return traceFixture(implementationSha256, {
        frames: [
          {
            stepId: 'answer',
            codeLines: [line],
            explanation: 'Show the computed answer.',
            state: { kind: 'array', items: [1] },
            highlights: [],
          },
        ],
      });
    }
    if (lineCount > 0) {
      const accepted = await prepareFixture(directory, {
        code,
        trace: (implementationSha256) =>
          linkedTrace(implementationSha256, lineCount),
      });
      await expect(
        prepareCurriculum(accepted.definition, accepted),
      ).resolves.toBeDefined();
    }
    const rejected = await prepareFixture(directory, {
      code,
      trace: (implementationSha256) =>
        linkedTrace(implementationSha256, lineCount + 1),
    });
    await expect(
      prepareCurriculum(rejected.definition, {
        ...rejected,
        outputDir: join(directory, 'rejected'),
      }),
    ).rejects.toThrow(/source line/);
  },
);

test('rejects renderer references outside the stored frame', async () => {
  const fixture = await prepareFixture(directory, {
    trace: (implementationSha256) =>
      traceFixture(implementationSha256, {
        frames: [
          {
            stepId: 'invalid',
            codeLines: [1],
            explanation: 'Show an array cell.',
            state: { kind: 'array', items: [] },
            highlights: [{ index: 0 }],
          },
        ],
      }),
  });
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /highlight/,
  );
});

test('rejects a valid trace with a different implementation SHA despite matching file evidence', async () => {
  const fixture = await prepareFixture(directory, {
    trace: () => traceFixture('b'.repeat(64)),
  });
  await expect(prepareCurriculum(fixture.definition, fixture)).rejects.toThrow(
    /identity/,
  );
});

test('renders bare CR as a visible code line boundary', async () => {
  const fixture = await prepareFixture(directory, {
    code: '# first\r# second',
  });
  const snapshot = await prepareCurriculum(fixture.definition, fixture);
  const codeHtml = snapshot.lessons[0]?.approaches[0]?.codeHtml ?? '';
  expect(codeHtml.match(/<span class="line">/g)).toHaveLength(2);
});
