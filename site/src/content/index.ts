export type {
  AssetRecord,
  ContentEntry,
  ContentKind,
  Diagnostic,
  Disposition,
  Heading,
  Manifest,
  Metadata,
  MigrationRow,
  PreparationResult,
  PublicationPolicy,
  RenderContext,
  RenderResult,
  RouteCatalog,
  Section,
  SourceEntry,
} from './types.js';
export { discoverEntries, publicationExclusion } from './discover.js';
export {
  assertUniqueRoutes,
  compareSourcePaths,
  sourceFolderRoute,
  publicationPages,
  createEntry,
} from './identifiers.js';
export { readMetadata, readPolicy } from './schema.js';

export {
  collectHeadings,
  collectExplicitAnchors,
  collectMarkdownLinks,
  createHeadingSlugger,
  parseMarkdown,
} from './headings.js';
export type { HeadingSlugger, MarkdownLink } from './headings.js';
export { createRouteCatalog, resolveLink, publicSourceUrl } from './links.js';
export {
  planAssets,
  copyLocalAssets,
  planRasterAsset,
  MAX_LOCAL_ASSET_BYTES,
} from './assets.js';
export type { RasterAsset } from './assets.js';
export { renderMarkdown } from './render/markdown.js';
export { renderNotebook } from './render/notebook.js';
export { renderSource } from './render/source.js';
export { sanitizeAuthorHtml } from './render/sanitize.js';

export { prepareContent } from './prepare.js';
export type { PrepareOptions } from './prepare.js';
export { writeManifest } from './manifest.js';
export { readPlannedLocalAsset } from './assets.js';
export { applyMigration, planMigration } from './migrate.js';
export type { MigrationPlan } from './migrate.js';

export type {
  Purpose,
  EditorialStatus,
  Topic,
  Collection,
  Group,
  OrganizationRecord,
  PathStep,
  LearningPath,
  OrganizationDefinition,
  Membership,
  OrganizationSnapshot,
} from './organization-types.js';
export {
  readOrganization,
  validateOrganization,
} from './organization-schema.js';
export { resolveOrganization, isLearningEntry } from './organization.js';
export {
  planOrganizationMigration,
  applyOrganizationMigration,
} from './organization-migrate.js';
export type { OrganizationMigrationPlan } from './organization-migrate.js';

export { organizationPageRoutes } from './organization-routes.js';

export type {
  ProblemId,
  LessonStatus,
  ProblemRecord,
  CompanyAssociation,
  LessonApproachDefinition,
  LessonRecord,
  LearningPathNode,
  LearningPathDefinition,
  CurriculumDefinition,
} from './leetcode/types.js';
export {
  hashLessonForReview,
  readCurriculum,
  validateCurriculum,
} from './leetcode/schema.js';

export { pathProgress, validateLearningPaths } from './leetcode/paths.js';
export type { LearningPathIndex, PathProgress } from './leetcode/paths.js';

export { readPublishedCurriculum } from './leetcode/publication.js';
export type {
  CurriculumSnapshot,
  PreparedLesson,
  PreparedProblem,
  TracePackageReference,
} from './leetcode/prepare.js';
export {
  assertCurriculumRouteOwnership,
  verifyCurriculumArtifacts,
} from './leetcode/artifacts.js';

export { validateTrace } from './leetcode/trace.js';
export type {
  AlgorithmTrace,
  TraceFrame,
  TraceHighlight,
  TraceState,
} from './leetcode/trace.js';
