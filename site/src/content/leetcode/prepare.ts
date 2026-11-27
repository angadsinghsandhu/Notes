import { createHash } from 'node:crypto';
import { constants } from 'node:fs';
import { mkdir, open, realpath, writeFile } from 'node:fs/promises';
import { isAbsolute, join, relative, sep } from 'node:path';
import { collectHeadings } from '../headings.js';
import { compareSourcePaths } from '../identifiers.js';
import { renderMarkdown } from '../render/markdown.js';
import { renderSource } from '../render/source.js';
import type { ContentEntry, Heading, RouteCatalog } from '../types.js';
import { assertCurriculumRouteOwnership } from './artifacts.js';
import { validateLearningPaths } from './paths.js';
import { validateCurriculum } from './schema.js';
import { TRACE_BYTE_LIMIT, validateTrace } from './trace.js';
import type { AlgorithmTrace, TraceFrame } from './trace.js';
import type {
  CurriculumDefinition,
  LearningPathDefinition,
  LessonApproachDefinition,
  LessonRecord,
  ProblemId,
  ProblemRecord,
} from './types.js';

const traceNamespace = '/practice-traces/';
const packageByteLimit = 25 * 1024 * 1024;
const workerFileLimit = 20_000;

interface CurriculumRoute {
  route: string;
  owner: string;
}

export interface CurriculumPrepareContext {
  rootDir: string;
  /** A new staging directory owned by the archive publication transaction. */
  outputDir: string;
  sourceCatalog: RouteCatalog;
  sourceVariants?: ReadonlyMap<string, ProblemId>;
  additionalPages?: readonly CurriculumRoute[];
}

export type PreparedProblem = Omit<ProblemRecord, 'evidence'> & {
  officialQuestionObservedOn: string | null;
  companies: {
    companyId: string;
    companyName: string;
    observedOn: string;
    reportingPeriod?: string;
    sourceUrl?: string;
  }[];
};

export interface TracePackageReference {
  url: string;
  sha256: string;
  bytes: number;
  exampleIds: string[];
}

export interface TraceTranscript {
  exampleId: string;
  steps: Pick<TraceFrame, 'stepId' | 'codeLines' | 'explanation'>[];
}

interface PreparedApproach {
  id: string;
  title: string;
  language: LessonApproachDefinition['language'];
  implementationSha256: string;
  entryPoint: string | null;
  codeHtml: string;
  trace: TracePackageReference | null;
  transcripts: TraceTranscript[];
}

export interface PreparedLesson {
  problemId: ProblemId;
  route: string;
  status: 'draft' | 'verified';
  bodyHtml: string;
  headings: Heading[];
  approaches: PreparedApproach[];
}

interface SourceVariantReference {
  sourceId: string;
  sourceRoute: string;
  problemId: ProblemId;
  lessonRoute: string;
}

export interface CurriculumSnapshot {
  version: 1;
  generation: string;
  problems: PreparedProblem[];
  /** Only verified lessons and drafts with readable prose own lesson routes. */
  lessons: PreparedLesson[];
  paths: LearningPathDefinition[];
  routes: CurriculumRoute[];
  sourceVariants: SourceVariantReference[];
}

export interface ProgressRegistry {
  version: 1;
  generation: string;
  problems: { problemId: ProblemId; revision: string }[];
}

export interface TraceAssetInventory {
  version: 1;
  generation: string;
  assets: TracePackageReference[];
}

function digest(bytes: string | Uint8Array): string {
  return createHash('sha256').update(bytes).digest('hex');
}

async function readEvidence(
  lessonDir: string,
  evidence: { path: string; sha256: string },
  trace = false,
): Promise<string> {
  const filename = await realpath(join(lessonDir, evidence.path));
  const location = relative(lessonDir, filename);
  if (
    location === '..' ||
    location.startsWith(`..${sep}`) ||
    isAbsolute(location)
  )
    throw new Error(`${evidence.path} resolves outside its lesson root`);

  const file = await open(
    filename,
    constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK,
  );
  try {
    const info = await file.stat();
    if (!info.isFile())
      throw new Error(`${evidence.path} must be a regular file`);
    const limit = trace ? TRACE_BYTE_LIMIT : packageByteLimit;
    const limitMessage = trace ? '1 MiB trace limit' : '25 MiB evidence limit';
    if (info.size > limit)
      throw new Error(`${evidence.path} exceeds the ${limitMessage}`);
    const bytes = await file.readFile();
    if (bytes.length > limit)
      throw new Error(`${evidence.path} exceeds the ${limitMessage}`);
    if (digest(bytes) !== evidence.sha256)
      throw new Error(`${evidence.path} does not match its SHA256 evidence`);
    return new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(
      bytes,
    );
  } finally {
    await file.close();
  }
}

function checkTrace(
  raw: string,
  problemId: ProblemId,
  approachId: string,
  evidence: LessonApproachDefinition['traces'][number],
  lineCount: number,
): { trace: AlgorithmTrace; compact: string } {
  let value: unknown;
  try {
    value = JSON.parse(raw);
  } catch (error) {
    throw new Error(`${evidence.path} contains invalid trace JSON`, {
      cause: error,
    });
  }
  if (
    typeof value !== 'object' ||
    value === null ||
    Reflect.get(value, 'problemId') !== problemId ||
    Reflect.get(value, 'approachId') !== approachId ||
    Reflect.get(value, 'exampleId') !== evidence.exampleId ||
    Reflect.get(value, 'implementationSha256') !== evidence.implementationSha256
  )
    throw new Error(`${evidence.path} has inconsistent trace identity`);
  try {
    const trace = validateTrace(value);
    for (const { stepId, codeLines } of trace.frames)
      for (const line of codeLines)
        if (line > lineCount)
          throw new Error(
            `Step ${stepId} references source line ${line}, beyond ${lineCount} lines`,
          );
    return { trace, compact: JSON.stringify(value) };
  } catch (error) {
    throw new Error(`${evidence.path}: ${(error as Error).message}`, {
      cause: error,
    });
  }
}

async function prepareApproaches(
  record: LessonRecord,
  lessonDir: string,
  assets: TracePackageReference[],
  assetDir: string,
  published: boolean,
): Promise<PreparedApproach[]> {
  const prepared: PreparedApproach[] = [];
  for (const {
    id,
    title,
    language,
    implementation,
    traces,
  } of record.approaches) {
    const originalCode = await readEvidence(lessonDir, implementation);
    const code = originalCode.replace(/\r\n?/g, '\n');
    const lineCount = code
      ? code.split('\n').length - Number(code.endsWith('\n'))
      : 0;
    const prefix = '{"version":1,"traces":[';
    const suffix = ']}\n';
    let byteCount = prefix.length + suffix.length;
    const packaged: string[] = [];
    const transcripts: TraceTranscript[] = [];
    for (const evidence of traces) {
      const raw = await readEvidence(lessonDir, evidence, true);
      const {
        trace: { exampleId, frames },
        compact,
      } = checkTrace(raw, record.problemId, id, evidence, lineCount);
      byteCount +=
        Math.max(Buffer.byteLength(raw), Buffer.byteLength(compact)) +
        Number(packaged.length > 0);
      if (byteCount > packageByteLimit)
        throw new Error(
          `${record.problemId}/${id} exceeds the 25 MiB trace package limit`,
        );
      packaged.push(compact);
      if (published)
        transcripts.push({
          exampleId,
          steps: frames.map(({ stepId, codeLines, explanation }) => ({
            stepId,
            codeLines,
            explanation,
          })),
        });
    }
    if (!published) continue;

    let trace: TracePackageReference | null = null;
    if (packaged.length) {
      const bytes = Buffer.from(prefix + packaged.join(',') + suffix);
      const sha256 = digest(bytes);
      const url = `${traceNamespace}${sha256}.json`;
      trace = {
        url,
        sha256,
        bytes: bytes.length,
        exampleIds: traces.map(({ exampleId }) => exampleId),
      };
      if (assets.length >= workerFileLimit)
        throw new Error('Worker trace assets exceed 20,000 files');
      await writeFile(join(assetDir, `${sha256}.json`), bytes);
      assets.push(trace);
    }
    const { html: codeHtml } = await renderSource(
      code,
      language === 'shell' ? 'bash' : language,
    );
    prepared.push({
      id,
      title,
      language,
      codeHtml,
      implementationSha256: implementation.sha256,
      entryPoint: implementation.entryPoint,
      trace,
      transcripts,
    });
  }
  return prepared;
}

function lessonRoute(number: number): string {
  return `/practice/leetcode/${number}/`;
}

function publicProblem(record: ProblemRecord): PreparedProblem {
  const { evidence, ...summary } = record;
  const companies = evidence.companies.map(
    ({ source, companyId, companyName, observedOn, reportingPeriod }) => {
      const company = {
        companyId,
        companyName,
        observedOn,
        ...(reportingPeriod === undefined ? {} : { reportingPeriod }),
      };
      if (source.type === 'public') {
        const url = new URL(source.url);
        if (url.username || url.password)
          throw new Error(
            `${record.id} company source URL contains credentials`,
          );
        return { ...company, sourceUrl: source.url };
      }
      return company;
    },
  );
  return {
    ...summary,
    officialQuestionObservedOn: evidence.officialQuestion?.observedOn ?? null,
    companies,
  };
}

// The existing resolver needs entry metadata for route and fragment lookups.
function linkTarget(
  route: string,
  title: string,
  lesson?: { id: ProblemId; sourcePath: string; prose: string },
): ContentEntry {
  return {
    id: lesson?.id ?? route,
    route,
    sourcePath: lesson?.sourcePath ?? route,
    kind: 'markdown',
    section: 'interview',
    groupSegments: [],
    bytes: lesson ? Buffer.byteLength(lesson.prose) : 0,
    headings: lesson ? collectHeadings(lesson.prose) : [],
    title,
    description: '',
    tags: [],
    draft: false,
    aliases: [],
  };
}

export async function prepareCurriculum(
  definition: CurriculumDefinition,
  context: CurriculumPrepareContext,
): Promise<CurriculumSnapshot> {
  const validated = validateCurriculum(definition);
  const paths = [
    ...validateLearningPaths(validated.paths, validated.problems).values(),
  ];
  const problems = validated.problems
    .toSorted((a, b) => a.number - b.number)
    .map(publicProblem);
  const byId = new Map(problems.map((problem) => [problem.id, problem]));
  const root = await realpath(context.rootDir);
  const routes: CurriculumRoute[] = [
    { route: '/practice/leetcode/', owner: 'LeetCode library' },
    { route: '/practice/paths/', owner: 'practice paths' },
  ];
  const linkRoutes = new Map(context.sourceCatalog.routes);
  for (const { route, owner } of routes)
    linkRoutes.set(route, linkTarget(route, owner));
  const pathRoutes = paths.map(({ id, title }) => {
    const route = `/practice/paths/${id}/`;
    linkRoutes.set(route, linkTarget(route, title));
    return { route, owner: `practice path ${id}` };
  });
  const inputs = [];
  for (const record of validated.lessons) {
    const problem = byId.get(record.problemId);
    if (!problem || problem.status === 'planned')
      throw new Error(`Unexpected lesson ${record.problemId}`);
    const lessonDir = join(root, 'problems', String(problem.number));
    if ((await realpath(lessonDir)) !== lessonDir)
      throw new Error(
        `${problem.id} lesson directory must stay within its original lesson root`,
      );
    const prose = record.prose
      ? await readEvidence(lessonDir, record.prose)
      : null;
    if (record.examples) await readEvidence(lessonDir, record.examples);
    const route = lessonRoute(problem.number);
    let linkEntry: ContentEntry | undefined;
    if (prose !== null) {
      routes.push({ route, owner: problem.id });
      linkEntry = linkTarget(route, problem.title ?? problem.id, {
        id: problem.id,
        sourcePath: `problems/${problem.number}/${record.prose?.path}`,
        prose,
      });
      linkRoutes.set(route, linkEntry);
    }
    inputs.push({
      record,
      status: problem.status,
      lessonDir,
      prose,
      linkEntry,
    });
  }
  routes.push(...pathRoutes);
  assertCurriculumRouteOwnership(
    [...(context.additionalPages ?? []), ...routes],
    [...context.sourceCatalog.sources.values()],
  );

  const assetDir = join(context.outputDir, 'worker-assets', traceNamespace);
  await mkdir(assetDir, { recursive: true });
  const assets: TracePackageReference[] = [];
  const lessons: PreparedLesson[] = [];
  const progress: ProgressRegistry['problems'] = [];
  for (const { record, status, lessonDir, prose, linkEntry } of inputs) {
    const approaches = await prepareApproaches(
      record,
      lessonDir,
      assets,
      assetDir,
      prose !== null,
    );
    if (prose === null || !linkEntry) continue;
    const catalog = { ...context.sourceCatalog, routes: linkRoutes };
    // Fragment-only links resolve against this lesson for the duration of its render.
    linkRoutes.set('', linkEntry);
    const { html: bodyHtml, headings } = await renderMarkdown(prose, {
      sourcePath: linkEntry.sourcePath,
      catalog,
    });
    const { problemId } = record;
    lessons.push({
      problemId,
      route: linkEntry.route,
      status,
      bodyHtml,
      headings,
      approaches,
    });
    if (status === 'verified' && record.review)
      progress.push({ problemId, revision: record.review.contentSha256 });
  }

  const publishedById = new Map(
    lessons.map(({ problemId, route }) => [problemId, route]),
  );
  const sourceVariants: SourceVariantReference[] = [];
  const sortedVariants = [...(context.sourceVariants ?? [])].sort(
    ([left], [right]) => compareSourcePaths(left, right),
  );
  for (const [sourcePath, problemId] of sortedVariants) {
    const source = context.sourceCatalog.sources.get(sourcePath);
    if (!source || source.draft || !byId.has(problemId))
      throw new Error(`Invalid source variant ${sourcePath} for ${problemId}`);
    const lessonRoute = publishedById.get(problemId);
    if (lessonRoute)
      sourceVariants.push({
        sourceId: source.id,
        sourceRoute: source.route,
        problemId,
        lessonRoute,
      });
  }

  const payload = {
    version: 1 as const,
    problems,
    lessons,
    paths,
    routes,
    sourceVariants,
  };
  const generation = digest(JSON.stringify({ payload, progress, assets }));
  const snapshot = { ...payload, generation };
  const registry: ProgressRegistry = {
    version: 1,
    generation,
    problems: progress,
  };
  const inventory: TraceAssetInventory = { version: 1, generation, assets };
  for (const [filename, contents] of [
    ['curriculum.json', snapshot],
    ['progress-registry.json', registry],
    ['trace-assets.json', inventory],
  ] as const)
    await writeFile(
      join(context.outputDir, filename),
      JSON.stringify(contents) + '\n',
    );
  return snapshot;
}
