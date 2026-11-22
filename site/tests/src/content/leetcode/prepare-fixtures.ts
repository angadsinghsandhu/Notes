import { createHash } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import type { ProblemRecord } from '../../../../src/content/leetcode/types.js';
import type { ContentEntry } from '../../../../src/content/types.js';
import { createRouteCatalog } from '../../../../src/content/links.js';
import { validateCurriculum } from '../../../../src/content/leetcode/schema.js';
import { curriculum, firstProblem, signedLesson } from './schema-fixtures.js';

export function digest(bytes: string | Uint8Array) {
  return createHash('sha256').update(bytes).digest('hex');
}

export function sourceEntry(
  overrides: Partial<ContentEntry> = {},
): ContentEntry {
  return {
    title: 'Archived Two Sum',
    description: '',
    tags: [],
    draft: false,
    aliases: [],
    id: 'original-source-id',
    sourcePath: 'Interview/Two Sum.py',
    section: 'interview',
    kind: 'code',
    bytes: 1,
    groupSegments: [],
    route: '/resources/interview/two-sum-py/',
    headings: [],
    ...overrides,
  };
}

export function traceFixture(
  implementationSha256: string,
  changes: Record<string, unknown> = {},
) {
  return JSON.stringify({
    version: 1,
    problemId: 'leetcode:1',
    approachId: 'hash-map',
    exampleId: 'pair',
    implementationSha256,
    result: [0, 1],
    frames: [
      {
        stepId: 'check-0',
        codeLines: [1],
        explanation: 'Look for the complement of 2.',
        state: { kind: 'array', items: [2, 7] },
        highlights: [{ index: 0 }],
      },
    ],
    ...changes,
  });
}

export async function prepareFixture(
  directory: string,
  options: {
    prose?: string | null;
    draft?: boolean;
    trace?: (implementationSha256: string) => string;
    source?: ContentEntry;
    companyUrl?: string;
    approach?: 'shell';
    code?: string;
    traceCount?: number;
  } = {},
) {
  const rootDir = join(directory, 'curriculum');
  const outputDir = join(directory, 'output');
  const lessonDir = join(rootDir, 'problems/1');
  await mkdir(lessonDir, { recursive: true });
  async function evidence(path: string, bytes: string) {
    const filename = join(lessonDir, path);
    await mkdir(dirname(filename), { recursive: true });
    await writeFile(filename, bytes);
    return { path, sha256: digest(bytes) };
  }
  const prose =
    options.prose === null
      ? null
      : await evidence(
          'lesson.md',
          options.prose ??
            '## Invariant\n\n[Jump](#invariant)\n\n<script>bad()</script>',
        );
  const examples = await evidence(
    'examples.json',
    '{"editorialNotes":"private"}',
  );
  const implementation =
    options.approach === 'shell'
      ? {
          ...(await evidence('solution.sh', options.code ?? "printf 'safe'")),
          entryPoint: null,
        }
      : {
          ...(await evidence(
            'solutions.py',
            options.code ?? 'def two_sum():\n    return [0, 1]\n',
          )),
          entryPoint: 'two_sum',
        };
  const implementationSha256 = implementation.sha256;
  const trace =
    options.trace?.(implementationSha256) ?? traceFixture(implementationSha256);
  const problem = firstProblem();
  const record: ProblemRecord = {
    ...problem,
    status: options.draft ? 'draft' : 'verified',
    evidence: {
      ...problem.evidence,
      companies: [
        {
          companyId: 'acme',
          companyName: 'Acme',
          source: { type: 'user-supplied', reference: '/private/source' },
          observedOn: '2026-10-24',
          reportingPeriod: 'October 2026',
        },
        {
          companyId: 'public-company',
          companyName: 'Public company',
          source: {
            type: 'public',
            url: options.companyUrl ?? 'https://example.com/report',
          },
          observedOn: '2026-10-24',
        },
      ],
    },
  };
  const traces = [];
  const traceCount = options.traceCount ?? 1;
  for (let index = 0; index < traceCount; index++) {
    const exampleId = index === 0 ? 'pair' : `pair-${index}`;
    const bytes =
      traceCount === 1
        ? trace
        : traceFixture(implementationSha256, { exampleId }).padEnd(
            1_048_576,
            ' ',
          );
    traces.push({
      ...(await evidence(`traces/hash-map/${exampleId}.json`, bytes)),
      implementationSha256,
      exampleId,
    });
  }
  const lesson = signedLesson(record, {
    problemId: record.id,
    prose,
    examples,
    approaches: [
      {
        id: 'hash-map',
        title: 'Hash map',
        language: options.approach ?? 'python',
        implementation,
        traces,
        verification: options.draft
          ? null
          : {
              implementationSha256,
              examplesSha256: examples.sha256,
              entryPoint: implementation.entryPoint,
              checkedOn: '2026-10-24',
              passedExampleIds: traces.map(({ exampleId }) => exampleId),
            },
      },
    ],
  });
  const { problems, paths } = curriculum();
  const definition = validateCurriculum({
    version: 1,
    problems: [record, ...problems.slice(1)],
    lessons: [{ ...lesson, review: options.draft ? null : lesson.review }],
    paths,
  });
  const source = options.source ?? sourceEntry();
  const sourceCatalog = createRouteCatalog([source], []);
  return {
    definition,
    rootDir,
    outputDir,
    lessonDir,
    sourceCatalog,
    source,
    trace,
  };
}
