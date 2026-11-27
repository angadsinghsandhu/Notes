import { createHash } from 'node:crypto';
import { readFile, realpath, stat } from 'node:fs/promises';
import { isAbsolute, join, relative, sep } from 'node:path';
import { z } from 'zod';
import { readShards, shardIndex } from './catalog-shards.js';
import type {
  CurriculumDefinition,
  LessonRecord,
  LessonStatus,
  ProblemId,
  ProblemRecord,
} from './types.js';

const lastProblem = 2000;
const frontendNumber = z.number().int().min(1).max(lastProblem);
const problemId = z.custom<ProblemId>(
  (value) =>
    typeof value === 'string' &&
    /^leetcode:[1-9][0-9]{0,3}$/.test(value) &&
    Number(value.slice('leetcode:'.length)) <= lastProblem,
  'Expected leetcode:<frontend number> from 1 through 2000',
);
const slug = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
const label = z.string().trim().min(1);
const status = z.enum([
  'planned',
  'draft',
  'verified',
]) satisfies z.ZodType<LessonStatus>;
const date = z.iso.date();
export const sha256 = z.string().regex(/^[a-f0-9]{64}$/);
const canonicalQuestionUrl = z
  .string()
  .regex(/^https:\/\/leetcode\.com\/problems\/[a-z0-9]+(?:-[a-z0-9]+)*\/$/);
const languages = {
  algorithm: 'python',
  sql: 'sql',
  shell: 'shell',
  concurrency: 'python',
} as const;
const extensions = { python: 'py', sql: 'sql', shell: 'sh' } as const;

export const companyAssociation = z.strictObject({
  companyId: slug,
  companyName: label,
  source: z.discriminatedUnion('type', [
    z.strictObject({
      type: z.literal('public'),
      url: z.url({ protocol: /^https$/ }),
    }),
    z.strictObject({ type: z.literal('user-supplied'), reference: label }),
  ]),
  observedOn: date,
  reportingPeriod: label.optional(),
});

const officialQuestion = z.strictObject({
  frontendNumber,
  title: label,
  sourceUrl: canonicalQuestionUrl,
  observedOn: date,
});

export const problem = z.strictObject({
  number: frontendNumber,
  id: problemId,
  title: label.nullable(),
  slug: slug.nullable(),
  officialUrl: canonicalQuestionUrl.nullable(),
  domain: z.enum(['algorithm', 'sql', 'shell', 'concurrency']).nullable(),
  difficulty: z.enum(['easy', 'medium', 'hard']).nullable(),
  topics: z.array(slug),
  evidence: z.strictObject({
    officialQuestion: officialQuestion.nullable(),
    companies: z.array(companyAssociation),
  }),
  status,
});

const localPath = z
  .string()
  .max(240)
  .regex(
    /^(?:[a-z0-9_-][a-z0-9._-]*\/)*[a-z0-9_-][a-z0-9._-]*$/,
    'Expected a normalized lesson-relative file path',
  );
const fileEvidence = z.strictObject({ path: localPath, sha256 });
const traceEvidence = fileEvidence.extend({
  exampleId: slug,
  implementationSha256: sha256,
});

const entryPoint = z
  .string()
  .regex(/^[a-zA-Z_][a-zA-Z_0-9]*$/)
  .nullable();

export const approach = z.strictObject({
  id: slug,
  title: label,
  language: z.enum(['python', 'sql', 'shell']),
  implementation: fileEvidence.extend({ entryPoint }),
  traces: z.array(traceEvidence),
  verification: z
    .strictObject({
      implementationSha256: sha256,
      entryPoint,
      examplesSha256: sha256,
      passedExampleIds: z.array(slug).min(1),
      checkedOn: date,
    })
    .nullable(),
});

const reviewableLesson = z.strictObject({
  problemId,
  prose: fileEvidence.extend({ path: localPath.regex(/\.md$/) }).nullable(),
  examples: fileEvidence
    .extend({ path: localPath.regex(/\.json$/) })
    .nullable(),
  approaches: z.array(approach),
});

export const lesson = reviewableLesson.extend({
  review: z
    .strictObject({
      reviewer: label,
      reviewedOn: date,
      contentSha256: sha256,
    })
    .nullable(),
});

const nodeFields = {
  id: slug,
  title: label,
  childIds: z.array(slug),
  prerequisiteIds: z.array(slug),
};
const stageNode = z.strictObject({ ...nodeFields, kind: z.literal('stage') });
const problemNode = z.strictObject({
  ...nodeFields,
  kind: z.literal('problem'),
  problemId,
});
export const pathNode = z.discriminatedUnion('kind', [stageNode, problemNode]);
export const learningPath = z.strictObject({
  id: slug,
  title: label,
  description: label,
  rootIds: z.array(slug),
  nodes: z.array(pathNode),
});
const pathCatalog = learningPath.extend({
  nodes: z.union([learningPath.shape.nodes, shardIndex]),
});
const authoredPathNode = z.discriminatedUnion('kind', [
  stageNode.extend({
    childIds: z.union([nodeFields.childIds, shardIndex]),
  }),
  problemNode,
]);

const manifest = z.strictObject({
  version: z.literal(1),
  problems: z.array(problem),
  lessons: z.array(problemId),
  paths: z.array(slug),
});
const manifestCatalog = manifest.extend({
  problems: z.union([manifest.shape.problems, shardIndex]),
});

export const curriculum = manifest.extend({
  lessons: z.array(lesson),
  paths: z.array(learningPath),
});

function indexUnique<Key, Record>(
  records: readonly Record[],
  key: (record: Record) => Key,
  label: string,
): Map<Key, Record> {
  const entries = new Map<Key, Record>();
  for (const record of records) {
    const id = key(record);
    if (entries.has(id)) throw new Error(`Duplicate ${label} ${String(id)}`);
    entries.set(id, record);
  }
  return entries;
}

function validateIdentity(record: ProblemRecord): void {
  const { number, id, slug, officialUrl, title, evidence } = record;
  if (id !== `leetcode:${number}`)
    throw new Error(`${id} must match frontend number ${number}`);

  const question = evidence.officialQuestion;
  if (
    slug === null &&
    officialUrl === null &&
    question === null &&
    title === null
  )
    return;
  if (
    slug === null ||
    officialUrl !== `https://leetcode.com/problems/${slug}/` ||
    question?.sourceUrl !== officialUrl ||
    question.frontendNumber !== number ||
    question.title !== title
  ) {
    throw new Error(
      `${id} has inconsistent official question identity or evidence`,
    );
  }
}

function validateApproaches(record: LessonRecord): void {
  const { problemId, approaches, examples } = record;
  indexUnique(approaches, ({ id }) => id, `approach in lesson ${problemId}`);
  indexUnique(
    approaches,
    ({ implementation }) =>
      `${implementation.path}#${implementation.entryPoint ?? ''}`,
    `implementation in lesson ${problemId}`,
  );
  const digestsByPath = new Map<string, string>();
  for (const {
    id,
    language,
    implementation,
    traces,
    verification,
  } of approaches) {
    const { path, sha256 } = implementation;
    const previousDigest = digestsByPath.get(path);
    if (previousDigest !== undefined && previousDigest !== sha256)
      throw new Error(
        `${problemId} has conflicting implementation digests for ${path}`,
      );
    digestsByPath.set(path, sha256);

    if (!implementation.path.endsWith(`.${extensions[language]}`)) {
      throw new Error(
        `${problemId} approach ${id} requires a ${language} implementation file`,
      );
    }
    if ((language === 'python') !== (implementation.entryPoint !== null)) {
      throw new Error(
        `${problemId} approach ${id}: Python requires a named entry point and native implementations use a file`,
      );
    }
    indexUnique(
      traces,
      ({ exampleId }) => exampleId,
      `example for approach ${id} in lesson ${problemId}`,
    );
    for (const trace of traces) {
      if (
        trace.implementationSha256 !== implementation.sha256 ||
        trace.path !== `traces/${id}/${trace.exampleId}.json`
      ) {
        throw new Error(
          `${problemId} approach ${id} has inconsistent trace evidence for ${trace.exampleId}`,
        );
      }
    }
    if (verification) {
      const passedExamples = indexUnique(
        verification.passedExampleIds,
        (exampleId) => exampleId,
        `passed example for approach ${id} in lesson ${problemId}`,
      );
      if (
        verification.implementationSha256 !== implementation.sha256 ||
        verification.entryPoint !== implementation.entryPoint ||
        verification.examplesSha256 !== examples?.sha256 ||
        traces.some(({ exampleId }) => !passedExamples.has(exampleId))
      ) {
        throw new Error(
          `${problemId} approach ${id} has inconsistent verification evidence`,
        );
      }
    }
  }
}

const reviewableProblem = problem
  .pick({
    number: true,
    id: true,
    title: true,
    slug: true,
    officialUrl: true,
    domain: true,
    difficulty: true,
    topics: true,
  })
  .strip();

/** Compute the versioned digest recorded by a reviewer after inspecting the lesson evidence. */
export function hashLessonForReview(
  metadata: ProblemRecord,
  evidence: Omit<LessonRecord, 'review'>,
): string {
  const payload = {
    version: 1,
    problem: reviewableProblem.parse(metadata),
    lesson: reviewableLesson.parse(evidence),
  };
  const canonicalJson = JSON.stringify(payload, (_key, value: unknown) => {
    if (value === null || typeof value !== 'object' || Array.isArray(value))
      return value;
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, Reflect.get(value, key)]),
    );
  });
  return createHash('sha256').update(canonicalJson).digest('hex');
}

function validateVerified(problem: ProblemRecord, lesson: LessonRecord): void {
  const { id, slug, difficulty, domain, topics } = problem;
  if (!slug || !difficulty || !domain || topics.length === 0)
    throw new Error(`${id} verified lesson requires complete catalog metadata`);

  const { review, ...content } = lesson;
  const { prose, examples, approaches } = content;
  if (
    !prose ||
    !examples ||
    !review ||
    approaches.length === 0 ||
    approaches.some(
      ({ traces, verification }) => traces.length === 0 || !verification,
    )
  )
    throw new Error(
      `${id} verified lesson requires prose, examples, editorial review, and verification and trace evidence for each approach`,
    );

  if (!approaches.some(({ language }) => language === languages[domain]))
    throw new Error(
      `${id} verified lesson requires a ${languages[domain]} implementation`,
    );

  if (review.contentSha256 !== hashLessonForReview(problem, content))
    throw new Error(`${id} has stale editorial review evidence`);
}

export function validateCurriculum(input: unknown): CurriculumDefinition {
  const result = curriculum.safeParse(input);
  if (!result.success)
    throw new Error(`Invalid curriculum:\n${z.prettifyError(result.error)}`);
  const definition = result.data;
  const { problems, lessons, paths } = definition;
  const byNumber = indexUnique(
    problems,
    ({ number }) => number,
    'frontend number',
  );
  const byProblemId = indexUnique(
    lessons,
    ({ problemId }) => problemId,
    'lesson for',
  );
  indexUnique(paths, ({ id }) => id, 'path');

  for (let number = 1; number <= lastProblem; number++) {
    if (!byNumber.has(number))
      throw new Error(`Missing frontend number ${number}`);
  }

  const officialUrls = new Set<string>();
  for (const record of problems) {
    validateIdentity(record);
    if (record.officialUrl !== null) {
      if (officialUrls.has(record.officialUrl))
        throw new Error(`Duplicate official question ${record.officialUrl}`);
      officialUrls.add(record.officialUrl);
    }
    const lesson = byProblemId.get(record.id);
    if (record.status === 'planned') {
      if (lesson)
        throw new Error(`Planned problem ${record.id} has a lesson record`);
      continue;
    }
    if (!lesson) throw new Error(`${record.id} requires a lesson record`);
    validateApproaches(lesson);
    if (record.status === 'verified') validateVerified(record, lesson);
  }
  return definition;
}

async function readJson<Schema extends z.ZodType>(
  root: string,
  filename: string,
  schema: Schema,
): Promise<z.infer<Schema>> {
  try {
    const file = await realpath(join(root, filename));
    const fromRoot = relative(root, file);
    if (
      fromRoot === '..' ||
      fromRoot.startsWith(`..${sep}`) ||
      isAbsolute(fromRoot)
    )
      throw new Error('File resolves outside the curriculum root');
    if (!(await stat(file)).isFile())
      throw new Error('Expected a regular file');
    const value: unknown = JSON.parse(await readFile(file, 'utf8'));
    return schema.parse(value);
  } catch (error) {
    throw new Error(
      `${join(root, filename)}: cannot read curriculum JSON: ${String(error)}`,
      { cause: error },
    );
  }
}

async function readPathNodes(
  root: string,
  filename: string,
  nodes: z.infer<typeof pathCatalog>['nodes'],
): Promise<z.infer<typeof learningPath>['nodes']> {
  if (Array.isArray(nodes)) return nodes;
  const resolved: z.infer<typeof pathNode>[] = [];
  for (const node of await readShards(
    root,
    filename,
    nodes,
    authoredPathNode,
  )) {
    const { childIds } = node;
    resolved.push({
      ...node,
      childIds: Array.isArray(childIds)
        ? childIds
        : await readShards(root, filename, childIds, slug),
    });
  }
  return resolved;
}

export async function readCurriculum(
  rootDir: string,
): Promise<CurriculumDefinition> {
  const root = await realpath(rootDir);
  const {
    version,
    problems: authoredProblems,
    lessons: lessonIds,
    paths: pathIds,
  } = await readJson(root, 'manifest.json', manifestCatalog);
  const problems = Array.isArray(authoredProblems)
    ? authoredProblems
    : await readShards(root, 'manifest.json', authoredProblems, problem);
  const lessons = [];
  for (const id of lessonIds) {
    const filename = `problems/${id.slice('leetcode:'.length)}/metadata.json`;
    const record = await readJson(root, filename, lesson);
    if (record.problemId !== id)
      throw new Error(
        `${filename}: expected problemId ${id}, found ${record.problemId}`,
      );
    lessons.push(record);
  }

  const paths = [];
  for (const id of pathIds) {
    const filename = `paths/${id}.json`;
    const record = await readJson(root, filename, pathCatalog);
    if (record.id !== id)
      throw new Error(
        `${filename}: expected path ID ${id}, found ${record.id}`,
      );
    paths.push({
      ...record,
      nodes: await readPathNodes(root, filename, record.nodes),
    });
  }

  return validateCurriculum({ version, problems, lessons, paths });
}
