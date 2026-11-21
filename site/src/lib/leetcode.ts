import type {
  CurriculumSnapshot,
  LearningPathDefinition,
  PreparedLesson,
  PreparedProblem,
  ProblemId,
} from '../content/index.js';

export type ProblemSummary = PreparedProblem;
export type PreparedLearningPath = LearningPathDefinition;
export type PathSummary = Pick<
  PreparedLearningPath,
  'id' | 'title' | 'description'
>;
export type ProblemFilter = {
  status?: ProblemSummary['status'];
  difficulty?: NonNullable<ProblemSummary['difficulty']>;
  domain?: NonNullable<ProblemSummary['domain']>;
  topic?: string;
};

export type CurriculumCatalog = {
  listProblems(filter?: ProblemFilter): ProblemSummary[];
  getLesson(id: ProblemId): PreparedLesson | undefined;
  listPaths(): PathSummary[];
  publishedRoutes(elected?: readonly string[]): string[];
  getPath(id: string): PreparedLearningPath | undefined;
};

export function createCurriculumCatalog(
  snapshot?: CurriculumSnapshot,
): CurriculumCatalog {
  const problems = snapshot?.problems ?? [];
  const lessons = new Map(
    snapshot?.lessons.map((lesson) => [lesson.problemId, lesson]),
  );
  const paths = new Map(snapshot?.paths.map((path) => [path.id, path]));
  return {
    publishedRoutes: (elected) =>
      selectCurriculumRoutes(snapshot?.routes ?? [], elected),
    listProblems: (filter = {}) =>
      structuredClone(
        problems.filter(
          (problem) =>
            (!filter.status || filter.status === problem.status) &&
            (!filter.difficulty || filter.difficulty === problem.difficulty) &&
            (!filter.domain || filter.domain === problem.domain) &&
            (!filter.topic || problem.topics.includes(filter.topic)),
        ),
      ),
    getLesson: (id) => structuredClone(lessons.get(id)),
    listPaths: () =>
      [...paths.values()].map(({ id, title, description }) => ({
        id,
        title,
        description,
      })),
    getPath: (id) => structuredClone(paths.get(id)),
  };
}

// Curriculum page renderers register their elected routes here when added.
const rendererRoutes: readonly string[] = [];

export function selectCurriculumRoutes(
  claims: CurriculumSnapshot['routes'],
  elected: readonly string[] = rendererRoutes,
): string[] {
  const requested = new Set(elected);
  if (requested.size !== elected.length)
    throw new Error('Duplicate elected curriculum route');
  const routes = claims
    .map(({ route }) => route)
    .filter((route) => requested.delete(route));
  if (requested.size)
    throw new Error(
      `Unclaimed elected curriculum routes: ${[...requested].join(', ')}`,
    );
  return routes;
}
