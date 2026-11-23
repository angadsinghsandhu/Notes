import { readFile } from 'node:fs/promises';
import { expect, it } from 'vitest';
import { portfolioSnapshotV1 } from '../../../scripts/portfolio-export/schema.js';

const fixture = await readFile(
  new URL('../../fixtures/portfolio-export/manifest.v1.json', import.meta.url),
  'utf8',
);
const snapshot = () => portfolioSnapshotV1.parse(JSON.parse(fixture));

it('reads the pinned v1 fixture without rewriting its encoded legacy alias', () => {
  expect(snapshot().entries[0]?.aliases).toEqual([
    '/notes/books/worked%20example/',
  ]);
});

it.each(['%2e', '%2E%2e', 'x%2Fy', 'x%5Cy', '%252f', '%00', '%', '%E2%9C'])(
  'rejects the unsafe or malformed encoded alias segment %s',
  (segment) => {
    const input = snapshot();
    input.entries[0]!.aliases = [`/notes/books/${segment}/`];
    expect(portfolioSnapshotV1.safeParse(input).success).toBe(false);
  },
);

const assetHash = 'b'.repeat(64);
const packageHash = 'c'.repeat(64);
const traceUrl = `/practice-traces/${packageHash}.json`;

function verifiedFixture() {
  const input = snapshot();
  const id = 'leetcode:1';
  input.verifiedCurriculumIds = [1];
  input.curriculum = {
    generation: 'a'.repeat(64),
    problems: [
      {
        id,
        number: 1,
        status: 'verified',
        title: 'Two Sum',
        slug: 'two-sum',
        officialUrl: 'https://leetcode.com/problems/two-sum/',
        domain: 'algorithm',
        difficulty: 'easy',
        topics: ['array'],
        officialQuestionObservedOn: '2026-11-23',
        companies: [],
      },
    ],
    lessons: [
      {
        problemId: id,
        route: '/practice/leetcode/1/',
        status: 'verified',
        bodyHtml: '<p>Lesson</p>',
        headings: [],
        approaches: [
          {
            id: 'example',
            title: 'Example',
            language: 'python',
            implementationSha256: 'a'.repeat(64),
            entryPoint: 'solve',
            codeHtml: '<pre>Example</pre>',
            trace: {
              url: traceUrl,
              sha256: packageHash,
              bytes: 3,
              exampleIds: ['first'],
            },
            transcripts: [
              {
                exampleId: 'first',
                steps: [
                  { stepId: 'start', codeLines: [1], explanation: 'Begin.' },
                ],
              },
            ],
          },
        ],
      },
    ],
    paths: [
      {
        id: 'basics',
        title: 'Basics',
        description: 'A practice path',
        rootIds: ['first', 'second'],
        nodes: [
          {
            kind: 'problem',
            id: 'first',
            title: 'Two Sum',
            problemId: id,
            childIds: [],
            prerequisiteIds: [],
          },
          {
            kind: 'problem',
            id: 'second',
            problemId: 'leetcode:2',
            childIds: [],
            prerequisiteIds: [],
          },
        ],
      },
    ],
    pendingPathLabels: [
      {
        pathId: 'basics',
        nodeId: 'second',
        problemId: 'leetcode:2',
        title: 'Add Two Numbers',
      },
    ],
    sourceVariants: [
      {
        sourceId: input.entries[0]!.id,
        sourceRoute: input.entries[0]!.route,
        problemId: id,
        lessonRoute: '/practice/leetcode/1/',
      },
    ],
    traceAssets: [
      {
        publicPath: traceUrl,
        exportPath: `worker-assets${traceUrl}`,
        bytes: 3,
        sha256: packageHash,
      },
    ],
  };
  return input;
}

it('requires the same frontend IDs in the verified numbers, problem records and lesson routes', () => {
  const input = verifiedFixture();
  expect(portfolioSnapshotV1.safeParse(input).success).toBe(true);
  input.verifiedCurriculumIds = [2];
  input.curriculum.lessons[0]!.route = '/practice/leetcode/2/';
  expect(portfolioSnapshotV1.safeParse(input).error?.message).toContain(
    'Verified curriculum numbers',
  );
});

it('rejects traces and source variants that are no longer owned by verified lessons', () => {
  const input = verifiedFixture();
  input.curriculum.traceAssets[0]!.exportPath = `worker-assets/practice-traces/${assetHash}.json`;
  input.curriculum.traceAssets.push({
    publicPath: `/practice-traces/${assetHash}.json`,
    exportPath: `worker-assets/practice-traces/${assetHash}.json`,
    bytes: 3,
    sha256: assetHash,
  });
  input.curriculum.sourceVariants[0]!.sourceRoute = '/notes/books/unavailable/';
  const errors = portfolioSnapshotV1.safeParse(input).error?.message;
  expect(errors).toContain('Trace reference does not match package');
  expect(errors).toContain('Unregistered Worker trace asset');
  expect(errors).toContain('Invalid curriculum source variant');
});

it('requires generation and matches every pending label to its own unverified node', () => {
  const input = verifiedFixture();
  input.curriculum.generation = null;
  input.curriculum.pendingPathLabels[0]!.nodeId = 'other';
  input.curriculum.pendingPathLabels.push({
    pathId: 'basics',
    nodeId: 'first',
    problemId: 'leetcode:1',
    title: 'Duplicate public title',
  });
  const errors = portfolioSnapshotV1.safeParse(input).error?.message;
  expect(errors).toContain('missing its verified generation');
  expect(errors).toContain('Invalid pending path node basics/second');
  expect(errors).toContain('Invalid verified path node basics/first');
  expect(errors).toContain('Unregistered pending path label');
});

it('rejects route equivalence, resources with arbitrary local paths, and unowned memberships', () => {
  const input = snapshot();
  const entry = input.entries[0]!;
  entry.aliases.push('/notes/books/worked%2Dexample/');
  entry.kind = 'pdf';
  entry.assetUrl = `/content-assets/${assetHash}.pdf`;
  input.organization.memberships[0]!.entryId = assetHash;
  input.assets = [
    {
      publicPath: `/content-assets/${packageHash}.pdf`,
      exportPath: `assets/${assetHash}.pdf`,
      bytes: 3,
      sha256: assetHash,
    },
  ];
  const errors = portfolioSnapshotV1.safeParse(input).error?.message;
  expect(errors).toContain('Duplicate public route');
  expect(errors).toContain('Pages asset export path differs');
  expect(errors).toContain('Incomplete prepared entry');
  expect(errors).toContain('Unregistered Pages asset');
  expect(errors).toContain('Organization membership IDs differ');
});

it('rejects unknown fields and credentials at the snapshot boundary', () => {
  const input = snapshot();
  const entry = input.entries[0]!;
  entry.sourceUrl = 'https://someone:secret@example.com/archive';
  Object.assign(entry, { sourcePath: 'Books/Public.md' });
  expect(portfolioSnapshotV1.safeParse(input).success).toBe(false);
  entry.sourceUrl = 'not a URL';
  expect(portfolioSnapshotV1.safeParse(input).success).toBe(false);
});
