# Notes website specification

Date: 2026-10-04
Status: Approved for subagent-driven implementation on 2026-10-04.

## 1. Intended outcome and decisions

Turn this repository into a readable, searchable learning library. A reader can browse the existing subject hierarchy, open a note or notebook, inspect accompanying code, and find supporting resources on a phone or desktop. The author adds Markdown to the repository, previews locally, and publishes by pushing to Git.

Confirmed requirements:

- This repository remains the content source of truth.
- Authoring uses Markdown files; publishing follows a Git push.
- Existing material must be adapted for the website.
- Local development and free hosted deployment are supported.
- Mobile and desktop layouts are first-class requirements.
- The user approved implementation on 2026-10-04 and explicitly authorized commits after each task and frequent feature PRs. Only the controller performs Git or remote writes; never merge or publish without further authorization.

Working assumptions requiring review:

- The hosted website is publicly readable. There are no reader accounts or access controls.
- Render existing notebooks and source code. PDFs have resource pages with previews where supported; slides have resource pages and download/source actions. PDF/slide text extraction is outside this release.
- Use the product name **Notes Library** until the author supplies another name.
- Add a dedicated `site/` application directory. This is the proposed placement rule for this new subsystem; existing learning folders remain in place.

## 2. Repository findings

Read-only inventory found 10,036 files excluding `.git`, approximately 1.9 GB of material, 224 Markdown files, 215 PDFs, 159 notebooks, and 36 slide decks. Counts describe the checkout, not the final publication set. Three Markdown files are internal `.kiro` guidance. Other Markdown files include both authored notes and course example READMEs.

The six content roots are `Books`, `Classes`, `Courses`, `Interview`, `Languages`, and `Tutorials`. Notes contain mathematics, fenced code, tables, relative images, some raw HTML, and possible wiki-style links. No Markdown files currently start with YAML frontmatter. The root README has placeholders and obsolete `University`/`Youtube` links. The current branch is `master`; there is no root website application or shared quality-gate configuration.

Examples that verification must use include the transformer note in `Interview/Applied Science/breadth/6.6.2-transformers.md`, the Japanese unit READMEs, GPU workshop notebooks, a PyTorch book notebook, and LeetCode solution source files.

## 3. Architecture and hosting

Choose **Astro + TypeScript + Cloudflare Pages**. The backend is a deterministic content-processing pipeline running locally and in CI. It discovers files, validates metadata, resolves links, renders content, and emits a manifest. Astro generates static HTML from that manifest. Pagefind indexes the completed HTML and supplies client-side full-text search.

There is no always-running API or database in this release. Git provides storage and revision history. This architecture fulfills the selected file-based workflow without introducing hosted state. It does not claim to provide a conventional database-backed application.

Alternatives considered:

| Option | Benefit | Trade-off |
| --- | --- | --- |
| Astro and a custom content pipeline | Fits mixed artifacts and a tailored reading interface | Requires explicit migration and renderer tests |
| Docusaurus | Established documentation navigation and Markdown features | Mixed notebooks/resources still need custom ingestion; stronger documentation theme conventions |
| Application server and database | Browser editing, accounts, live mutations | Extra hosting, authentication, and synchronization absent from the chosen workflow |

Cloudflare Pages is the primary deployment target. Use GitHub Actions to run checks, build once, and upload the successful output to a Cloudflare Pages Direct Upload project. This avoids a separate unchecked hosting build. Pushes to `master` publish only after the deployment is configured; pull requests run verification without deployment credentials. The output remains an ordinary static site portable to other hosts.

Cloudflare's documented Free limits are 500 builds/month, 20,000 deployed files, and 25 MiB per asset. GitHub Pages has a 1 GB published-site limit. Several current PDFs/slides exceed Cloudflare's asset limit; they remain external source resources rather than being copied into the deployment. Do not add R2 or another billed/storage service to the first release.

## 4. Application layout and boundaries

Keep content in the existing six folders. The new application lives under `site/`, with its own package manifest and lockfile. Root `README.md` documents the application commands.

| Area | Responsibility |
| --- | --- |
| `site/src/content/` | Discovery, schemas, identifiers, asset/link resolution, renderers, migration reporting |
| `site/src/lib/catalog.ts` | Read the generated manifest and answer UI queries; no filesystem writes |
| `site/src/components/`, `site/src/layouts/`, `site/src/pages/` | Static reader interface and route generation |
| `site/src/client/` | Navigation, theme, code-copy, and search interactions |
| `site/scripts/` | CLI orchestration, local watcher, migration, output verification |
| `site/tests/` | Tests mirroring source/script/component/page paths |
| `site/content/` | Publication policy, metadata overrides, migration ledger |
| `site/.generated/` | Disposable manifest and rendered bodies, ignored by Git |
| `site/public/content-assets/` | Only referenced, approved, publishable local assets, ignored by Git |

Content code must not import UI or CLI modules. UI code consumes the manifest through `catalog.ts` and never scans the archive. CLI modules call content modules. Do not execute course programs or import course package dependencies.

## 5. Content contract and authoring

A new note is a UTF-8 `.md` file under a content root, with YAML frontmatter:

```yaml
---
title: Transformer Architecture
description: Attention, encoder and decoder stacks, and common variants.
tags: [machine-learning, transformers]
draft: false
---
```

Required field: nonempty `title`. Optional fields: `description` (string), `tags` (unique strings, default empty), `draft` (boolean, default false), `slug` (section-relative lowercase ASCII path), `order` (finite number), `updated` (ISO date supplied by the author), and `aliases` (previous absolute website paths). Section and hierarchy come from the file path. Do not fabricate updated dates.

Legacy notes remain loadable before migration: derive the title from the first H1, then the filename; infer hierarchy from the original directories. Migration adds frontmatter to authored Markdown without rewriting its body. Course/vendor example files use metadata overrides instead of edits to upstream text. The site does not require MDX or executable content.

`site/content/publication.json` defines the six allowed roots, excluded patterns, and per-path overrides. Each eligible new note is discovered automatically without a manually maintained page list. Notebook and resource metadata uses the same override map; resource overrides may additionally specify an HTTPS `resourceUrl`. A `repositoryPublic` boolean explicitly declares whether repository source links are publicly usable, defaulting to false when omitted. Exclusions always win; a draft cannot be published by an override or by being linked from another note.

Exclude `.git`, `.kiro`, application internals, dependencies, caches, build outputs, checkpoints, binary archives, environment/credential files, and unsupported datasets from automatic publication. Images are supporting assets, not standalone articles. Source code includes `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.css`, `.html`, `.java`, `.kt`, and `.cpp`; code is displayed as escaped source, never run. JSON configuration files are not automatically exposed.

Every original file receives a migration-ledger disposition: page, supporting asset, external resource, draft/excluded, or unsupported. The ledger records its source path, reason, and destination where applicable. This provides a checkable accounting of material rather than pretending all 10,036 files are notes.

## 6. URLs, links, and assets

Website routes:

- `/`: library overview and search entry point.
- `/library/`: browse all published entries, with section and kind filters.
- `/library/<section>/`: section hierarchy, with notes and resources distinguished.
- `/notes/<section>/<path>/`: Markdown and notebook reader pages.
- `/resources/<section>/<path>/`: source code, PDFs, and slide resource pages.
- `/search/`: full-text search.
- `/404.html`: useful recovery links and search entry point.

Generate lowercase ASCII path segments from NFC-normalized source paths. Treat directory `README.md` case-insensitively as the directory landing note. If a segment contains no ASCII letters/digits, use `item-` followed by the first eight SHA-256 hex characters of that original segment. Preserve identity with explicit slugs and aliases when renaming content. Detect all route collisions, including case-only collisions and aliases, and fail with both source paths; never silently choose a winner.

Build a complete source-to-route map before resolving links. Resolve relative links against the source file's directory, preserving query strings and fragments. Rewrite links to published Markdown/notebooks/code/resources to their website routes. Validate heading fragments against generated heading IDs, including duplicate headings. Support unambiguous wiki links to a published entry's title or source path; ambiguous matches fail with candidates. Fix obsolete internal repository links during migration using actual target files. External HTTP(S)/mailto links remain external; CI does not depend on third-party network availability.

Local links cannot traverse outside the allowed repository roots or bypass exclusions through symlinks. A missing local target, broken fragment, link to an excluded file, unsafe URL scheme, or unresolved old internal link is a publication error. A draft target is unavailable in production.

Copy only referenced publishable images and PDF/slide attachments at or below 25 MiB. Name copied assets by content hash and preserve an appropriate extension. Local SVGs are sanitized before use. Reserve image dimensions, use lazy loading below the fold, and constrain images to their container. Referenced assets larger than 25 MiB get a clearly labeled source action using an HTTPS repository URL and source revision; do not silently omit them or create broken embeds. If the repository is private or a public source URL is unavailable, require an explicit public resource URL or exclude the resource before deployment.

Resource pages always show title, kind, original filename, size, and source action. Locally hosted PDFs offer a desktop preview with an Open PDF fallback available on every viewport. Slides offer download/source actions; do not promise an in-browser PPT/PPTX preview. External-only large resources show a source action without a nonfunctional local download. Local development follows this same policy; a public repository declaration or explicit resource URL is necessary for the large-resource fallback. Source links to unpublished/draft targets remain forbidden even when expressed as known repository HTTP URLs.

## 7. Rendering and search

Markdown supports headings, lists, links, GitHub-style tables/task lists, code highlighting, KaTeX math, images, and safe `details`/`summary` markup. Process input through Markdown/HTML ASTs, sanitize author-provided HTML, then apply controlled highlighting/math transforms. Never enable arbitrary scripts, event handlers, iframes, or MDX execution. Any final HTML inserted into a page comes only from these controlled renderers.

Notebook support targets nbformat 4. Preserve cell order; render Markdown cells through the shared Markdown renderer and code cells as highlighted source. Render stored stream/error/text output as escaped text, and stored PNG/JPEG outputs as bounded images. For rich outputs choose PNG/JPEG first, then `text/plain`; show a labeled unsupported-output placeholder when no supported representation exists. Resolve notebook Markdown attachments into supporting assets. Never execute notebooks. Malformed notebooks or unknown cell types report file and cell index and fail validation rather than disappearing.

Use Pagefind on built reader/resource bodies. Exclude navigation, raw notebook metadata, drafts, and internal reports. Resource search indexes metadata and displayed code, not extracted PDF/slide text. Filters cover section and content kind. Search has loading, empty, error, and result states; each result shows title, breadcrumb, kind, and excerpt.

`npm run dev` watches eligible files and policy/metadata changes, serializes rebuilds, and updates pages without restarting the server. Search uses the most recent production index when available; otherwise the development search page visibly instructs the author to run `npm run build` and `npm run preview`. Never claim the Pagefind index updates with every Markdown hot reload. Production preview is the authoritative search test.

## 8. Responsive interface and design system

Design direction: a quiet, content-focused library with prominent search, a clear subject hierarchy, and restrained color. Avoid marketing sections, decorative dashboards, and animated background effects.

Use semantic tokens: light background `#F8FAFC`, surfaces `#FFFFFF`, primary text `#1E293B`, secondary text `#475569`, accent `#2563EB`, borders `#E2E8F0`. Dark mode uses background `#0F172A`, surfaces `#1E293B`, text `#F1F5F9`, secondary text `#CBD5E1`, accent `#93C5FD`, and borders `#475569`. Check actual token combinations for contrast. Use a system sans-serif stack for UI/body and a system monospace stack for code; no external font request is required.

At widths below 768 px, use one reading column, an accessible navigation drawer, and a collapsed on-page contents disclosure. From 768 to 1199 px, show the section sidebar and keep contents collapsible. At 1200 px and above, provide sidebar, readable article column, and on-page contents rail. Article width is capped at 72 characters. Use at least 16 px body text and 1.6 line height.

Navigation includes breadcrumbs, current-section highlighting, nested groups, a source link, and previous/next notes in natural numeric order within the same group. Library lists distinguish learning notes from course code/resources so snapshots do not overwhelm the default notes view. Theme selection supports system/light/dark and persists locally.

All controls have visible focus indicators and accessible names. Touch targets are at least 44 by 44 px. Include a skip link; drawer focus returns to its trigger and Escape closes it. Code-copy has success/failure feedback. Table and code overflow is confined to labeled, keyboard-accessible containers. The page itself has no horizontal overflow at 320 px, including long URLs, math, breadcrumbs, and resource filenames. Respect reduced motion. Reading/navigation work without JavaScript; search and convenience controls may require it.

## 9. Local commands and delivery contract

Use npm with a committed `site/package-lock.json`. Pin a supported Node LTS version in `site/.node-version`, CI, and documentation when scaffolding; pin resolved dependency versions in the lockfile. All commands below run from `site/`:

| Command | Contract |
| --- | --- |
| `npm ci` | Install exactly the locked dependencies |
| `npm run dev` | Prepare content, watch the archive, run Astro locally |
| `npm run content:check` | Validate policy, metadata, routes, artifacts, and local links without rewriting source |
| `npm run content:migrate -- --dry-run` | Emit a proposed migration report without editing original notes |
| `npm run content:migrate -- --apply` | Apply the reviewed metadata/link migration, retaining source bodies |
| `npm run check` | Format, lint, import boundaries, types, and unit tests |
| `npm run build` | Prepare content, generate Astro HTML, run Pagefind, verify output limits/links |
| `npm run preview` | Serve the completed production output locally |
| `npm run test:e2e` | Browser verification against production output |
| `npm run verify` | Run `check`, `build`, and `test:e2e` serially |

CI runs `npm ci` and `npm run verify`. The deploy job depends on verification and only runs on trusted pushes to `master`. Provisioning a Cloudflare project and supplying deployment credentials are setup actions, not prerequisites for local use or CI checks. Missing deployment configuration results in a clearly reported non-deployment, not a claim that a site was published. No external project or remote write is part of specification/plan creation.

Configure repository/source URL, source revision, and production site URL explicitly. Local builds may omit production URL; hosted builds require an HTTPS site URL for sitemap/canonical output. Deployment credentials remain CI secrets; never put tokens in Markdown, client code, build output, or the repository.

## 10. Failure behavior, migration, and verification

Content errors include source path and a specific reason, with nonzero exit status. Production never deploys partial output. Development keeps the last successful content snapshot after a failed rebuild and prints the failing paths; the next successful edit replaces it. Rebuilding is deterministic for identical content/configuration and a fixed source revision. Generated cleanup is restricted to the application's generated directories; never run destructive Git commands to reset source.

Migration proceeds through inventory, classification, metadata/URL normalization, link and asset fixes, and complete rendering verification. Migration is idempotent and preserves note bodies except explicit necessary link repairs. Test the dry run first, and run twice after apply to prove the second run has no changes. Record excluded and unsupported artifacts in `site/content/migration-report.json`; do not delete them from the repository. Replace root README placeholders with real navigation and authoring/startup/deployment instructions.

Acceptance criteria:

1. A new Markdown note in any allowed root appears in local browsing automatically and in production HTML/search after a build, with no hand-edited routing list.
2. A published note changed, renamed with aliases, or deleted produces updated pages/indexes without stale routes/assets. Drafts are absent from production HTML, downloads, and search.
3. Every file in the six roots is accounted for in the migration ledger; every selected entry renders and every internal page/asset/fragment link resolves.
4. Real transformer/math notes, Japanese text, GPU/PyTorch notebooks, LeetCode code, local PDFs, slides, and an oversized resource have verified representations.
5. Malformed metadata/notebooks, duplicate routes, ambiguous wiki links, excluded targets, escaping paths, and unsafe HTML/URLs fail or are sanitized as specified.
6. At 320, 375, 768, 1024, and 1440 px, navigation, search, articles, code, math, tables, and resources remain usable with no page-wide horizontal scroll. Verify light and dark themes, keyboard operation, and reduced motion.
7. A clean dependency installation passes format, lint, import boundaries, TypeScript/Astro checks, unit tests, production build, internal-output validation, accessibility checks, and browser tests. Establish a measured coverage floor; never hide reachable branches with suppressions or skipped tests.
8. Output contains at most 20,000 files and no deployed asset larger than 26,214,400 bytes. Search finds a known phrase in a real note; excluded content is absent. No reader action executes repository source or notebooks.
9. Local startup and production preview are reproducible from documented commands. A configured trusted Git push publishes the already-verified artifact; a failed gate prevents deployment.

## 11. Scope boundaries

This release includes discovery, validated rendering, metadata migration, browsing, search, responsive design, authoring documentation, and deployment configuration. It excludes accounts, browser editing, a database, notebook execution, PDF OCR/text extraction, slide-to-HTML conversion, AI chat, comments, cloud object-storage provisioning, and automatic execution/deployment of course demo projects. Those require separate requirements rather than being hidden inside this migration.

## 12. Sources and review record

Platform choices were checked against primary documentation on 2026-10-04:

- [Astro content collections](https://docs.astro.build/en/guides/content-collections/): filesystem loading and structured content.
- [Astro Markdown](https://docs.astro.build/en/guides/markdown-content/): Markdown processing and integrations.
- [Pagefind documentation](https://pagefind.app/docs/): indexes generated HTML after a build; static search output.
- [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/): free plan and asset limits.
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits): alternative hosting constraints.

Self-review checked intent, scope, publication assumptions, artifact fallback behavior, local search limitations, hosting limits, URL collisions, failure modes, and acceptance criteria. The user subsequently approved implementation with subagents, commits after each task, and frequent feature PRs. That authorization supersedes earlier no-commit instructions. Merging and live publication remain outside the authorized scope.
