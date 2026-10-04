# Notes Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the existing learning archive as a searchable, responsive website that automatically discovers new Markdown notes and publishes verified output after a Git push.

**Architecture:** Keep the six learning folders as the source of truth. A TypeScript build pipeline emits normalized metadata, sanitized rendered content, and approved assets; Astro generates static pages and Pagefind indexes those pages. GitHub Actions verifies the application before uploading the built artifact to Cloudflare Pages.

**Tech Stack:** Astro, TypeScript, npm, Zod, unified/remark/rehype, KaTeX, Shiki, Pagefind, Vitest, Playwright, axe-core, ESLint, Prettier, and Cloudflare Pages. Use native CSS with semantic tokens; React is not required. Resolve compatible stable package versions during Task 1 and commit their lockfile as part of the user's eventual commit, not an agent commit.

**Spec:** [Notes website specification](../specs/2026-10-04-notes-website-design.md). Read it before executing any task. The three publication assumptions and application placement remain subject to user review.

## Global Constraints

- This repository remains the content source of truth.
- Authoring uses Markdown files; publishing follows a Git push.
- The user approved implementation on 2026-10-04 and explicitly authorized commits after each task and frequent feature PRs. Only the controller performs Git or remote writes; never merge or publish without further authorization.
- Keep content in the existing six folders. The new application lives under `site/`, with its own package manifest and lockfile.
- Content code must not import UI or CLI modules. UI code consumes the manifest through `catalog.ts` and never scans the archive. CLI modules call content modules. Do not execute course programs or import course package dependencies.
- Required field: nonempty `title`. Optional fields: `description` (string), `tags` (unique strings, default empty), `draft` (boolean, default false), `slug` (section-relative lowercase ASCII path), `order` (finite number), `updated` (ISO date supplied by the author), and `aliases` (previous absolute website paths).
- Exclusions always win; a draft cannot be published by an override or by being linked from another note.
- Output contains at most 20,000 files and no deployed asset larger than 26,214,400 bytes.
- All controls have visible focus indicators and accessible names. Touch targets are at least 44 by 44 px.
- The page itself has no horizontal overflow at 320 px, including long URLs, math, breadcrumbs, and resource filenames.
- Never execute notebooks.

After every implementation/configuration file edit, run the applicable targeted test and the application format, lint, boundary, type, and build checks before treating that file as done or moving to another implementation file. An intentional failing TDD test is a temporary red stage, not a finished file. Preserve all existing changes. Never run `git restore`, `git checkout --`, `git stash`, `git reset --hard`, or `git clean`.

If execution uses subagents, give each agent an explicit assigned file list. Forbid all Git writes and all remote/network writes, including push, PR creation/comments/merges, non-GET API calls, tagging, releases, and deployment. State that an assignment is not authorization for these actions. Every shell script starts with `cd /Users/angad/Code/Notes || exit 1`. Audit `git status --short` and source diffs after every delegated batch. Serialize test runs and use isolated browser ports/output directories when needed. Model names in the supplied global instructions are not available in this harness; resolve that mismatch before dispatching rather than passing an unsupported model ID.

## Review Focus

1. Spaces, apostrophes, Unicode filenames, case-only README variants, and duplicate normalized routes must resolve predictably or fail with both paths — Task 2.
2. Draft/excluded content reachable through a Markdown link, notebook attachment, alias, or symlink must not leak into pages/assets/search — Tasks 2, 3, 5, and 7.
3. Malformed notebooks, unsafe rich HTML, and unsupported MIME-only outputs must preserve readable content or report the exact cell — Task 4.
4. A deleted or renamed source must not leave an old page, copied asset, or search result; a failed hot rebuild must retain only the last successful snapshot — Tasks 5 and 7.
5. Oversized PDF resources and long math/code/tables must have working source actions and a usable phone layout — Tasks 3, 6, and 7.

## File and interface map

All application paths below are relative to `site/` unless a root path is explicitly shown. Tests mirror the relative source/script path under `tests/`; browser tests mirror their component/page/client files too. Configuration is verified by the gates and integration tests, not by tautological tests of its contents. Keep non-vendored source modules below approximately 500 lines.

| Files | Ownership |
| --- | --- |
| `package.json`, `package-lock.json`, `.node-version`, Astro/TypeScript/Vitest/Playwright/ESLint/Prettier configs | Task 1 runtime and quality gates |
| `src/content/types.ts`, `schema.ts`, `discover.ts`, `identifiers.ts`; `content/publication.json` | Task 2 canonical data contract and discovery |
| `src/content/assets.ts`, `links.ts`, `headings.ts` | Task 3 URL and asset preparation |
| `src/content/render/markdown.ts`, `notebook.ts`, `source.ts`, `sanitize.ts` | Task 4 content rendering |
| `src/content/prepare.ts`, `manifest.ts`; `scripts/content.ts`, `dev.ts`; `src/lib/catalog.ts` | Task 5 pipeline, watcher, and reader query API |
| `src/layouts/LibraryLayout.astro`, `ReaderLayout.astro`; components/pages/styles/client modules | Task 6 reading interface and routes |
| `src/content/migrate.ts`; `scripts/migrate.ts`, `verify-output.ts`; `content/migration-report.json` | Task 7 archive migration and output validation |
| Root `.github/workflows/notes-site.yml`, `README.md`, `.gitignore`, `CLAUDE.md`, `codex.md`, `AGENTS.md`; `public/_headers`, `scripts/deploy.ts` | Task 8 delivery/documentation/project steering |

Define and export these shared types in Task 2; later tasks use the same names:

```ts
type Section = 'books' | 'classes' | 'courses' | 'interview' | 'languages' | 'tutorials';
type ContentKind = 'markdown' | 'notebook' | 'code' | 'pdf' | 'slides';
type Heading = { id: string; text: string; depth: number };
type SourceEntry = {
  sourcePath: string; absolutePath: string; section: Section;
  kind: ContentKind; bytes: number;
};
type Metadata = {
  title: string; description: string; tags: string[]; draft: boolean;
  slug?: string; order?: number; updated?: string; aliases: string[];
};
type ContentEntry = Metadata & {
  id: string; sourcePath: string; section: Section; kind: ContentKind;
  bytes: number; groupSegments: string[]; route: string; headings: Heading[];
  bodyFile?: string; assetUrl?: string; sourceUrl?: string;
};
type Diagnostic = { sourcePath: string; message: string; cellIndex?: number };
type Disposition = 'page' | 'supporting-asset' | 'external-resource' | 'excluded' | 'unsupported';
type MigrationRow = {
  sourcePath: string; disposition: Disposition; reason: string; destination?: string;
};
type AssetRecord = {
  sourcePath: string; bytes: number; url: string; mode: 'local' | 'external';
};
type Manifest = {
  version: 1; entries: ContentEntry[]; assets: AssetRecord[]; ledger: MigrationRow[];
};
```

`PublicationPolicy` has `roots` (the six original case-sensitive root paths), `exclude` (glob strings), `overrides` (`Record<string, Partial<Metadata> & { resourceUrl?: string }>`), `repositoryPublic` (boolean, default false), and optional HTTPS `repositoryUrl`, immutable `revision`, and HTTPS `siteUrl`. Environment values `REPOSITORY_URL`, `SOURCE_REVISION`, and `SITE_URL` override deployment-specific defaults without altering note metadata. Frontmatter wins over overrides for descriptive fields; any source of `draft: true` wins over `draft: false`.

`RouteCatalog` maps original source paths and unique routes/aliases to entries and their headings, and maps asset source paths to `AssetRecord`. `RenderContext` contains `sourcePath` and `catalog`. `RenderResult` contains `html` and `headings`. `PreparationResult` contains `manifest` and `diagnostics`. Store source paths with repository-relative POSIX separators; absolute filesystem paths never appear in rendered output.

## Task 1: Establish a working application and quality gates

**Files:** Create the runtime/configuration files in the map; `src/pages/index.astro`, `src/styles/tokens.css`, and `tests/src/pages/index.test.ts`. Modify root `.gitignore` only to ignore application dependencies, output, generated content/assets, and test artifacts. Do not alter course ignores or package files.

**Interfaces:** Produces the local npm commands `dev`, `check`, `build`, `preview`, `test:unit`, `test:e2e`, and `verify`. During this task, `build` generates the minimal homepage; Task 5 extends it with content and Task 6 with Pagefind. Browser tests use production output. `check` chains format-check, lint, boundary-check, typecheck, and unit tests; `verify` adds build and browser tests serially.

- [x] Write `test_homepage_is_a_readable_document` in the mirrored page test: visiting `/` returns 200, document language is `en`, there is exactly one H1 named `Notes Library`, and a skip link reaches `main`.
- [x] Bootstrap only the dependencies/configuration necessary to run that test. Resolve mutually compatible stable versions; select a supported Node LTS patch from official runtime/framework requirements and record the same patch in `.node-version`, CI setup, and README. Run the browser test and observe the absent homepage failure.
- [x] Implement the minimal Astro document and tokens. Add strict Astro/TypeScript checking for source, CLI, and test code. Vitest owns content/lib/script tests; Playwright owns component/layout/page/client tests, with explicit non-overlapping test globs.
- [x] Configure ESLint import restrictions to enforce the three boundaries from the spec, expose them through `check:boundaries`, and verify that a temporary forbidden UI import in a content-module test fixture fails the boundary checker. Remove only that deliberate fixture violation afterward.
- [x] Run `npm run check`, `npm run build`, and `npm run test:e2e`. Expected: all exit zero, the production homepage assertion passes, and no course application is built or executed.

## Task 2: Discover content and validate canonical identities

**Files:** Create `src/content/types.ts`, `schema.ts`, `discover.ts`, `identifiers.ts`, `content/publication.json`, and mirrored `tests/src/content/{schema,discover,identifiers}.test.ts`. Add small copied real-input fixtures under `tests/fixtures/`; retain original source paths in fixture metadata.

**Interfaces:** `readPolicy(policyPath: string): Promise<PublicationPolicy>`; `discoverEntries(rootDir: string, policy: PublicationPolicy): Promise<{ sources: SourceEntry[]; ledger: MigrationRow[] }>`; `readMetadata(source: SourceEntry, policy: PublicationPolicy): Promise<Metadata>`; `createEntry(source: SourceEntry, metadata: Metadata): ContentEntry`; `assertUniqueRoutes(entries: ContentEntry[]): void`. `id` is SHA-256 of the normalized relative source path; route generation and non-ASCII fallback follow spec section 6. Draft entries remain in the ledger but are excluded from the publishable entries.

- [x] Write `discover_new_markdown_without_registration`: copy a real note into an allowed root, add another note, and assert both are found without adding them to policy overrides. Write `reject_symlink_escape_and_excluded_targets` and assert outside-root symlinks, `.kiro`, `env.json`, checkpoints, dependencies, and caches are absent.
- [x] Write schema tests asserting title is required for frontmatter-bearing notes; legacy H1/filename fallback works; `draft: true` cannot be overridden false; invalid dates/types, duplicate tags, traversal slugs, and nonfinite order values fail with source paths.
- [x] Write identifier tests asserting case-insensitive README landing paths, stable routes with spaces/apostrophes, the exact `item-<8 hex>` fallback, collision diagnostics containing both paths, alias collisions, and natural numeric sorting inputs. Test the actual empty Japanese READMEs without inventing their content; add an explicitly labeled synthetic Unicode fixture and use actual archive path shapes.
- [x] Run `npm run test:unit -- tests/src/content/schema.test.ts tests/src/content/discover.test.ts tests/src/content/identifiers.test.ts` and observe the new behavior tests fail before implementation.
- [x] Implement discovery with sorted traversal and an explicit supported-extension table. Account for every discovered source file, including unsupported/excluded material. The full manifest/ledger is a build-time input and internal migration report, never a deployed JSON endpoint or client import. UI props contain only selected published entry fields.
- [x] Run the targeted tests, `npm run check`, and `npm run build`. Expected: zero exit statuses and deterministic source/route output.

## Task 3: Resolve links, headings, and publishable assets

**Files:** Create `src/content/headings.ts`, `links.ts`, `assets.ts`; mirrored `tests/src/content/{headings,links,assets}.test.ts`.

**Interfaces:** `collectHeadings(markdown: string): Heading[]`; `planAssets(rootDir: string, sources: string[], policy: PublicationPolicy): Promise<AssetRecord[]>`; `createRouteCatalog(entries: ContentEntry[], assets: AssetRecord[]): RouteCatalog`; `resolveLink(href: string, sourcePath: string, catalog: RouteCatalog): string`; `copyLocalAssets(rootDir: string, assets: AssetRecord[], targetDir: string): Promise<void>`. Use one shared heading slugger implementation for collection/rendering, including duplicate headings and notebook-wide ordering.

- [ ] Write `rewrite_real_relative_links_and_fragments`: retain a real linked-note/image pair and assert page/asset rewriting, percent-encoded names, query/fragment preservation, duplicate heading anchors, and directory README links. Missing targets and fragments must name the referring source and target.
- [ ] Write `resolve_wikilink_only_when_unique`: a unique source/title match resolves, while duplicate titles list candidates. Add external HTTP/mailto passthrough and javascript/data scheme rejection tests. Known repository HTTP links are resolved against publication policy too, so a draft/excluded target is rejected rather than bypassing the local-link check. Notebook-generated image data becomes an extracted asset rather than an arbitrary URL.
- [ ] Write asset tests asserting a referenced file of 26,214,400 bytes can be local, one of 26,214,401 bytes becomes external, equal bytes deduplicate by hash, unreferenced images are not copied, and excluded/symlink targets fail. Use sparse temporary files to test size boundaries without large fixtures.
- [ ] Write `require_accessible_source_url_for_external_resource`: a missing/private public-source configuration cannot silently produce a valid hosted action; explicit HTTPS resource URLs work. Test source URL path encoding and immutable revision handling.
- [ ] Run these targeted unit tests, observe the intended failures, then implement the resolvers and asset planner. Preserve external links without probing third-party availability.
- [ ] Run targeted tests, `npm run check`, and `npm run build`. Expected: valid rewrites and no asset copied outside the designated generated asset directory.

## Task 4: Render Markdown, notebooks, and code safely

**Files:** Create `src/content/render/markdown.ts`, `notebook.ts`, `source.ts`, `sanitize.ts`, and the mirrored renderer tests.

**Interfaces:** `renderMarkdown(markdown: string, context: RenderContext): Promise<RenderResult>`; `renderNotebook(json: unknown, context: RenderContext): Promise<RenderResult>`; `renderSource(code: string, language: string): Promise<RenderResult>`; `sanitizeAuthorHtml(html: string): string`. Notebook parsing/schema validation belongs to the notebook module. Attachment extraction adds known asset targets to the context before Markdown link resolution.

- [ ] Write `render_transformer_note_with_math_and_code` from the actual transformer note and another real math-bearing note: headings agree with collection, fenced code is highlighted, equations render through KaTeX, and tables/details remain usable. Assert Japanese characters in the labeled Unicode fixture survive unchanged; the actual Japanese README placeholders are empty.
- [ ] Write `preserve_gpu_and_pytorch_notebook_cells` using real archived notebooks: Markdown and code order is preserved and no execution occurs. Add regression inputs for stored output, attachment images, unsupported MIME-only output, invalid nbformat, malformed cell/source fields, unknown cell type, and error output with escaped text.
- [ ] Write sanitization tests asserting script tags, event attributes, unsafe URLs, active SVG content, iframes, and executable notebook HTML are absent; supported details/summary/images remain. Verify trusted KaTeX/Shiki output is generated after sanitizing author HTML rather than stripped accidentally.
- [ ] Write source rendering tests using `Interview/leetcode/Solutions/78_Subsets.py` and literal HTML/JS input: displayed code is escaped and highlighted, and no source is executed. Do not import the code fixture as a program.
- [ ] Run renderer tests and observe red. Implement unified AST processing, a narrow HTML allowlist, controlled KaTeX/Shiki transforms, nbformat-4 cell rendering, and the MIME preference from the spec. Unsupported rich output receives a visible placeholder with the cell index.
- [ ] Run renderer tests, `npm run check`, and `npm run build`. Expected: all pass and collected/rendered heading IDs agree.

## Task 5: Assemble a deterministic pipeline and local watcher

**Files:** Create `src/content/manifest.ts`, `prepare.ts`, `src/lib/catalog.ts`, `scripts/content.ts`, `scripts/dev.ts`, and mirrored tests for each behavior-bearing module. Modify `package.json` scripts to expose content validation and integrate preparation into dev/build.

**Interfaces:** `prepareContent(options: { rootDir: string; outputDir: string; policyPath: string; hosted: boolean }): Promise<PreparationResult>`; `writeManifest(manifest: Manifest, outputDir: string): Promise<void>`; `loadCatalog(manifest: Manifest): Catalog`, exposing `getEntry(route: string)`, `listEntries(filters?: { section?: Section; kind?: ContentKind })`, and `getAdjacentNotes(id: string)`. `startContentWatcher(options: PrepareOptions, onSuccess: () => void): Promise<{ close(): Promise<void> }>` serializes builds and coalesces intervening changes. CLI exits nonzero on diagnostics.

- [ ] Write `prepare_real_mixed_archive_subset`: assert all selected Markdown/notebook/code/PDF/slide inputs produce the correct kind/route/body/resource metadata, and every original file has an internal ledger row. Repeated preparation with fixed inputs/revision produces identical manifest/body bytes.
- [ ] Write `do_not_publish_draft_bodies_or_internal_ledger`: drafts have no rendered body/assets and the full manifest/ledger is not emitted into `dist` or imported by client modules. Published links to drafts fail. Public page props cannot contain absolute filesystem paths.
- [ ] Write `remove_deleted_pages_assets_and_aliases`: prepare, delete/rename a fixture with declared aliases, prepare again, and assert stale outputs are gone while the explicit alias resolves. Cleanup must reject any output directory outside `site/.generated` and `site/public/content-assets`.
- [ ] Write watcher tests with deterministic events, not sleeps: concurrent file changes serialize; a failed rebuild keeps the prior successful manifest; fixing the source triggers the latest successful update. Verify `close()` terminates watchers/server children.
- [ ] Write catalog tests asserting sections/groups and natural numeric ordering, note-only previous/next adjacency, and draft exclusion. Run all targeted tests to observe red.
- [ ] Implement a two-pass pipeline: discover/normalize all entries and collect document headings; construct the complete route/asset catalog; render/validate all bodies; atomically replace generated output only after success. Keep source files unchanged. Build commands re-create the exact publishable asset set.
- [ ] Run targeted tests, `npm run content:check`, `npm run check`, and `npm run build`. Add a new temporary note locally and prove the development URL appears without restarting; remove only that explicitly created temporary note afterward.

## Task 6: Build the responsive library, reader, resources, and search

**Files:** Create `src/layouts/{LibraryLayout,ReaderLayout}.astro`; `src/components/{Navigation,Breadcrumbs,TableOfContents,ResourceViewer,Search}.astro`; `src/client/{navigation,theme,copy-code,search}.ts`; `src/styles/{tokens,global,reader}.css`; pages `library/index.astro`, `library/[section].astro`, `notes/[...slug].astro`, `resources/[...slug].astro`, `search.astro`, `404.astro`. Extend the homepage. Add matching browser tests under `tests/src/` for those paths and catalog query tests if new queries are needed.

**Interfaces:** Route generation consumes `Catalog` and `ContentEntry`. Layout props are `{ title: string; description: string; entry?: ContentEntry }`; resource props are `{ entry: ContentEntry }`; reader props are `{ entry: ContentEntry; html: string }`, with HTML exclusively from Task 4. Search exposes section/kind filters and runs against Pagefind's generated index. Client interactions initialize once per document and require no application server.

- [ ] Write browser assertions for homepage/library/section browsing; direct note/resource URLs; breadcrumbs; numeric previous/next; working 404 recovery; code-copy feedback; and links to original source. Test initial notes-only browsing and deliberate switching to resources.
- [ ] Write responsive tests at 320, 375, 768, 1024, and 1440 px. Assert `document.documentElement.scrollWidth <= window.innerWidth`, including real long code/table/math and filenames. Test drawer keyboard focus trapping/return/Escape, contents disclosure, touch targets, and no-JavaScript article navigation.
- [ ] Write light/dark/system theme and reduced-motion browser tests. Run axe against homepage, library, reader, resource, and search in both explicit themes, with no serious/critical violations. Check actual text contrast and focus visibility manually as well.
- [ ] Write resource tests for local PDF preview plus Open PDF fallback, slide download/source action, escaped code page, and a large resource that offers a labeled external source action without a broken local embed.
- [ ] Write search tests against built output: a phrase from the real transformer note returns its page; filters affect results; a draft phrase is absent; empty and unavailable-index states display useful feedback. Test the visible local-development search limitation separately.
- [ ] Run browser tests to observe red. Implement static semantic layouts, styles, and small client modules using the exact tokens, breakpoints, 72-character reading width, 16 px text floor, 1.6 line height, and 44 px targets from the spec. Use SVG icons with accessible labels; do not add a React dependency for these controls.
- [ ] Extend `build` to run preparation, Astro, then Pagefind on article/resource bodies only. Generate aliases as small static redirect pages excluded from indexing. Generate canonical/sitemap output only with configured HTTPS production URL. Add tests for a known alias and sitemap URL.
- [ ] Run `npm run check`, `npm run build`, and `npm run test:e2e`. Inspect screenshots at all required widths, both themes, and a notebook/math note. Fix overflow/accessibility defects before completing the task.

## Task 7: Migrate the complete archive and validate production output

**Files:** Create `src/content/migrate.ts`, `scripts/migrate.ts`, `scripts/verify-output.ts`, `content/migration-report.json`, and mirrored tests. Modify only authored Markdown requiring frontmatter or necessary internal-link repairs. Use policy overrides for course/vendor example files. Record the concrete source-file list from dry run before edits.

**Interfaces:** `planMigration(rootDir: string, policy: PublicationPolicy): Promise<MigrationPlan>` where `MigrationPlan` contains `changes: { sourcePath: string; originalHash: string; proposedText: string }[]` and `ledger: MigrationRow[]`; `applyMigration(plan: MigrationPlan): Promise<void>` rejects a source whose hash changed after planning. `verifyOutput(distDir: string): Promise<Diagnostic[]>` verifies deployed size/count, page/asset/fragment links, aliases, source-action structure, and exclusion rules using the generated manifest.

- [ ] Write migration tests proving a real legacy note gets metadata without body changes; obsolete internal links are repaired against actual targets; protected course examples get overrides; dry run writes no source; a second apply has zero changes; and concurrent source edits fail rather than being overwritten.
- [ ] Write output tests asserting the exact 20,000/20,001 file and 26,214,400/26,214,401 byte boundaries, missing assets/fragments, excluded content, malformed source actions, and stale search/page remnants. Generated cleanup must stay within the application output tree.
- [ ] Run targeted tests to observe red; implement migration and output validation. Wire `content:migrate`, `content:check`, and `check:output` commands; make output validation the final `build` step.
- [ ] Run `npm run content:migrate -- --dry-run`; inspect dispositions and the full proposed source-file list. Fix misclassified authored/vendor content in policy before applying. Apply only the scoped changes with `npm run content:migrate -- --apply` and verify each edited note via content validation/build before moving to the next source edit.
- [ ] Run migration again and require zero proposed changes. Run the complete archive build; compare discovery inventory with the internal ledger so every original file is accounted for, and review all unsupported/excluded reasons. The full ledger stays out of deployed output.
- [ ] Run `npm run verify` serially. Establish line/function/statement/branch coverage floors of at least 90% for behavior-bearing application TypeScript; improve tests until met. Measure twice serially before pinning the measured floors on the actual `test:unit` gate. Do not use suppressions or skipped tests to meet them; do not demand coverage of course/vendor source.
- [ ] Produce screenshot/verification evidence for real Markdown, Japanese placeholders plus labeled Unicode fixture, both notebook families, LeetCode source, PDF, slide, and oversized source resource. Confirm every selected page builds and all local targets/fragments resolve. Preserve original artifacts and model files in the repo.

## Task 8: Configure verified deployment and document operation

**Files:** Create root `.github/workflows/notes-site.yml`; create `site/scripts/deploy.ts`, its mirrored unit test, and `site/public/_headers`; update root README and `.gitignore` as needed. Create root `CLAUDE.md` and byte-identical `codex.md` for website placement/quality-gate rules; make `AGENTS.md` a symlink to `CLAUDE.md`. Preserve any such files that appear during implementation and reconcile them rather than overwriting.

**Interfaces:** `getDeploymentDecision(input: { eventName: string; ref: string; gatesPassed: boolean; projectName?: string; accountId?: string; hasToken: boolean }): { deploy: boolean; reason: string }`. Only `push`, `refs/heads/master`, passing gates, and complete deployment configuration can produce `deploy: true`. This decision is also enforced by workflow job conditions, not only a script convention.

- [ ] Write tests asserting failed gates, pull requests, non-master branches, and missing project/account/token settings cannot deploy; a configured trusted master push can. Diagnostics must not expose tokens.
- [ ] Run the decision tests to observe red, then implement deployment gating and the workflow. Verification uses an explicit `site/` working directory, locked install, matching Node runtime, production URL/revision configuration, Playwright browser install, and `npm run verify`. Keep token-bearing deploy jobs separate from pull-request execution.
- [ ] Upload the verified `dist` artifact from the verification job and download that exact artifact in the deployment job; invoke the pinned Wrangler CLI for the configured Direct Upload project. Do not rebuild with different dependencies or inputs during deployment. Missing settings report that publication is disabled while verification still succeeds.
- [ ] Add response headers appropriate to the chosen static assets, without a policy that breaks generated math, Pagefind, or permitted PDF previews. Browser-test the actual headers under the deployment-compatible local preview when feasible; do not claim a live-host check from local preview.
- [ ] Replace README placeholders with real subject navigation and document frontmatter, policy/drafts, overrides, notebooks/resources, Node/npm setup, `dev`, `build`, `preview`, `verify`, migration, and search's development limitation. Document Cloudflare Direct Upload setup and the required `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_PAGES_PROJECT`, and `SITE_URL` configuration; require a public repository/resource URL for external artifacts.
- [ ] Add the placement and command rules to project steering only. Check `CLAUDE.md` and `codex.md` byte equality and the AGENTS symlink. No global steering edits are needed for this feature.
- [ ] Run `npm run verify`, inspect the workflow conditions, and confirm no credentials appear in tracked files or generated client output. Run `git status --short` and audit all source diffs for changes outside the dry-run migration list and application/docs/config scope.
- [ ] Deliver the working local website, migration ledger, verification results, and deployment setup instructions. Provisioning/publishing to the user's account requires their explicit authorization and available credentials; perform no remote writes from a delegated worker. Report deployment as configured/unconfigured/published based on evidence, never inference.

## Final acceptance and execution handoff

The first release is complete only when all nine specification acceptance criteria have direct evidence: new-note pickup, update/delete behavior, migration accounting, real artifact rendering, error/sanitization behavior, responsive usability, complete green gates, hosting limits/search, and local/deployment behavior. Where Cloudflare account access is unavailable, local and configuration verification can finish, but a live deployment is explicitly unverified.

Selected execution method: **subagent-driven development**, explicitly requested by the user on 2026-10-04. Use one fresh implementer per task, a task reviewer, and a final whole-branch reviewer. Source migration and full browser/test runs remain serialized. The controller performs commits and feature PR creation after verification.

Plan self-review: all specification sections map to Tasks 1–8; shared types/signatures are named before consumption; all five Review Focus items have assigned tests; artifact limitations and draft exclusions are explicit. Product implementation, commits, and remote writes are not authorized by creating this document; Task 8 describes future deployment after user authorization. The user approved implementation with subagent-driven development on 2026-10-04. Controller commits and feature PRs are authorized; merging and live publication are not.
