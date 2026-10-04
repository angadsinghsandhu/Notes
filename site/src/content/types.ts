export type Section =
  'books' | 'classes' | 'courses' | 'interview' | 'languages' | 'tutorials';
export type ContentKind = 'markdown' | 'notebook' | 'code' | 'pdf' | 'slides';
export type Heading = { id: string; text: string; depth: number };
export type SourceEntry = {
  sourcePath: string;
  absolutePath: string;
  section: Section;
  kind: ContentKind;
  bytes: number;
};
export type Metadata = {
  title: string;
  description: string;
  tags: string[];
  draft: boolean;
  slug?: string;
  order?: number;
  updated?: string;
  aliases: string[];
};
export type ContentEntry = Metadata & {
  id: string;
  sourcePath: string;
  section: Section;
  kind: ContentKind;
  bytes: number;
  groupSegments: string[];
  route: string;
  headings: Heading[];
  anchors?: string[];
  bodyFile?: string;
  assetUrl?: string;
  sourceUrl?: string;
};
export type Diagnostic = {
  sourcePath: string;
  message: string;
  cellIndex?: number;
};
export type Disposition =
  | 'page'
  | 'supporting-asset'
  | 'external-resource'
  | 'excluded'
  | 'unsupported';
export type MigrationRow = {
  sourcePath: string;
  disposition: Disposition;
  reason: string;
  destination?: string;
};
export type AssetRecord = {
  sourcePath: string;
  bytes: number;
  url: string;
  mode: 'local' | 'external';
};
export type Manifest = {
  version: 1;
  entries: ContentEntry[];
  assets: AssetRecord[];
  ledger: MigrationRow[];
};
export type PublicationPolicy = {
  roots: string[];
  exclude: string[];
  overrides: Record<string, Partial<Metadata> & { resourceUrl?: string }>;
  repositoryPublic: boolean;
  repositoryUrl?: string;
  revision?: string;
  siteUrl?: string;
};
export type RouteCatalog = {
  sources: Map<string, ContentEntry>;
  routes: Map<string, ContentEntry>;
  assets: Map<string, AssetRecord>;
  policy?: PublicationPolicy;
};
export type RenderContext = { sourcePath: string; catalog: RouteCatalog };
export type RenderResult = { html: string; headings: Heading[] };
export type PreparationResult = {
  manifest: Manifest;
  diagnostics: Diagnostic[];
};
