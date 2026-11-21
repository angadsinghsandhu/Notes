import { hashLessonForReview } from '../../../../src/content/index.js';
import type {
  LessonRecord,
  ProblemRecord,
} from '../../../../src/content/index.js';

const officialUrl = 'https://leetcode.com/problems/two-sum/';
export const implementationSha256 = 'a'.repeat(64);

export function verifiedContent(): Omit<LessonRecord, 'review'> {
  return {
    problemId: 'leetcode:1',
    prose: { path: 'lesson.md', sha256: 'b'.repeat(64) },
    examples: { path: 'examples.json', sha256: 'c'.repeat(64) },
    approaches: [
      {
        id: 'hash-map',
        title: 'Hash map',
        language: 'python',
        implementation: {
          path: 'solutions.py',
          sha256: implementationSha256,
          entryPoint: 'two_sum',
        },
        traces: [
          {
            exampleId: 'pair',
            path: 'traces/hash-map/pair.json',
            sha256: 'd'.repeat(64),
            implementationSha256,
          },
        ],
        verification: {
          implementationSha256,
          entryPoint: 'two_sum',
          examplesSha256: 'c'.repeat(64),
          passedExampleIds: ['pair'],
          checkedOn: '2026-10-24',
        },
      },
    ],
  } satisfies Omit<LessonRecord, 'review'>;
}

export function signedLesson(
  problem: ProblemRecord,
  content: ReturnType<typeof verifiedContent> = verifiedContent(),
) {
  const contentSha256 = hashLessonForReview(problem, content);
  return {
    ...content,
    review: {
      reviewer: 'Editorial reviewer',
      reviewedOn: '2026-10-24',
      contentSha256,
    },
  };
}

export function verifiedLesson() {
  return signedLesson(firstProblem());
}

export function pathDefinition() {
  return {
    id: 'all-problems',
    title: 'All problems',
    description: 'An editorial study order',
    rootIds: ['stage-one'],
    nodes: [
      {
        id: 'stage-one',
        kind: 'stage',
        title: 'First stage',
        childIds: ['first-problem'],
        prerequisiteIds: [],
      },
      {
        id: 'first-problem',
        kind: 'problem',
        title: 'First problem',
        problemId: 'leetcode:1',
        childIds: [],
        prerequisiteIds: [],
      },
    ],
  };
}

export function firstProblem() {
  return {
    id: 'leetcode:1',
    number: 1,
    title: 'Two Sum',
    slug: 'two-sum',
    officialUrl,
    difficulty: 'easy',
    domain: 'algorithm',
    topics: ['array', 'hash-table'],
    status: 'verified',
    evidence: {
      officialQuestion: {
        frontendNumber: 1,
        title: 'Two Sum',
        sourceUrl: officialUrl,
        observedOn: '2026-10-24',
      },
      companies: [],
    },
  } satisfies ProblemRecord;
}

export function curriculum() {
  const planned = {
    title: null,
    slug: null,
    officialUrl: null,
    difficulty: null,
    domain: null,
    topics: [],
    status: 'planned',
    evidence: { officialQuestion: null, companies: [] },
  };
  return {
    version: 1,
    problems: [
      firstProblem(),
      ...Array.from({ length: 1999 }, (_, index) => ({
        ...planned,
        id: `leetcode:${index + 2}`,
        number: index + 2,
      })),
    ],
    lessons: [verifiedLesson()],
    paths: [pathDefinition()],
  };
}

export function problemChange(changes: Record<string, unknown>, number = 1) {
  const { problems, ...definition } = curriculum();
  return {
    ...definition,
    problems: problems.map((record) =>
      record.number === number ? { ...record, ...changes } : record,
    ),
  };
}

export function lessonChange(changes: Record<string, unknown>) {
  return { ...curriculum(), lessons: [{ ...verifiedLesson(), ...changes }] };
}
