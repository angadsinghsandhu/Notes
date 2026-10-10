# Notes Library

Personal learning notes, notebooks, code, books and course resources. The static website lives in `site/`; the archive remains the source of truth.

| Subject               | Repository              | Website               |
| --------------------- | ----------------------- | --------------------- |
| Books                 | [Books](Books/)         | `/library/books/`     |
| Classes               | [Classes](Classes/)     | `/library/classes/`   |
| Courses               | [Courses](Courses/)     | `/library/courses/`   |
| Interview preparation | [Interview](Interview/) | `/library/interview/` |
| Languages             | [Languages](Languages/) | `/library/languages/` |
| Tutorials             | [Tutorials](Tutorials/) | `/library/tutorials/` |

## Local operation

Use **Node 24.18.1** and npm (the current local runtime uses npm 11.16.0). Run application commands from `site/`:

```sh
cd site
npm ci
npx playwright install --with-deps chromium
npm run dev
```

Full Chromium is required for the native PDF viewer tests; do not install only the headless shell. The development command prepares content before starting Astro. It polls source paths every second, awaits watcher readiness, and refreshes open readers after successful publication. A failed content rebuild reports the offending source paths and keeps the last successful snapshot; repair the source to recover without restarting. Polling costs O(watched paths) per second. Development retains one previous asset publication for open readers; production removes stale assets.

Before `npm run check` or `npm run verify`, select **Python 3.12.14** and install the pinned archive parity dependencies in an isolated environment. Run this setup from the repository root:

```sh
python3 -m venv .superpowers/polars-venv
source .superpowers/polars-venv/bin/activate
python -m pip install -r site/tests/requirements-polars.txt
cd site
npm run test:polars
```

Keep that environment active for subsequent verification commands. `test:polars` rejects a base interpreter and runs explicit mirrored stdlib tests without importing whole course programs, fitting models, downloading datasets or executing GPU code. Pandas is only the original-source baseline oracle; converted examples and new Python tabular tooling use Polars. The pinned environment includes `fastexcel` for Polars' default Excel engine and `openpyxl` for the Excel baseline; running Excel examples separately requires the optional `polars[excel]` dependencies.

```sh
npm run build
npm run preview -- --port 4321 --ignore-lock
npm run verify
```

`build` validates content, builds static pages, generates Pagefind, and verifies the deployed output. `preview` serves the built site. Development search uses the last production index if present and does not refresh on note edits; use `build` then `preview` to search current content. Plain Astro preview does not apply Cloudflare `_headers`. The browser gate separately applies the built header policy to real local responses and verifies compatibility; it is not a live Cloudflare test.

`verify` builds the real output fixtures first, then runs formatting, lint, import boundaries, Astro/TypeScript checks, archive parity, unit coverage and browser tests, followed by read-only validation of the final artifact. Browser scenario cleanup preserves the incoming production URL and revision. Every covered source file must meet **90% statements, branches, functions and lines**. Browser verification owns port 4328; keep it free. Run gates serially. For foreground Astro dev/preview invocations use `--ignore-lock` so the caller owns shutdown; `npm run dev` already supplies it.

## Authoring

Add UTF-8 Markdown under one of the six archive roots. Directory paths define subject and hierarchy; `README.md` is the directory landing note. New notes require a nonempty frontmatter title:

```yaml
---
title: Attention mechanisms
description: Scaled dot-product attention
tags: [transformers]
---
```

Optional fields are `description` (string), `tags` (unique strings), `draft` (boolean), `slug` (section-relative lowercase ASCII path), `order` (finite number), `updated` (real ISO date, `YYYY-MM-DD`), `aliases` (previous absolute site paths), and `role: supplemental`. Omitted tags/aliases are empty and omitted draft is false. Omitted role means a primary learning note; supplemental course/template documents retain readers, full-text search and source links while leaving default study-note browsing, navigation and adjacency. No other role value is accepted. Legacy notes derive titles from their first H1 or filename; do not invent updated dates.

Edit `site/content/publication.json` for exclusions and path-specific overrides. Course/vendor text and notebook/resource metadata use overrides rather than rewriting upstream text. Frontmatter takes precedence over descriptive overrides; a draft in either location prevents publication. Exclusions always win, including over overrides and links. Aliases cannot shadow existing page/output paths or application assets, including `/_headers`. Markdown/notebook readers use `/notes/<section>/<path>/`; code/PDF/slides use `/resources/<section>/<path>/`.

Relative note/image/resource links are resolved from the source directory and rewritten to published routes; invalid targets, ambiguous wiki links and missing heading fragments fail with source diagnostics. Markdown supports safe HTML, tables, task lists, fenced code and math. Author scripts, event handlers, arbitrary iframes and executable MDX are forbidden. Notebooks display stored Markdown, code and supported output **without execution**. Code resources are highlighted text; course programs and their package dependencies are not run or deployed.

Referenced images and eligible PDF/slide assets are content-addressed. An individual deployed file may not exceed **25 MiB (26,214,400 bytes)**; output may not exceed **20,000 files**. Local PDFs provide a desktop native preview and an Open PDF fallback at every viewport. Slides provide downloads, not a slide renderer. Oversized resources use an immutable public repository source URL or explicit HTTPS `resourceUrl` override. Declare `repositoryPublic: true` only for a genuinely public repository and configure its HTTPS `repositoryUrl`; `SOURCE_REVISION` must be an immutable commit hash (CI uses `github.sha`). Private or unavailable external sources need an explicit public resource URL or exclusion. No additional object-storage service is provisioned.

## Migration and internal reports

The reviewed metadata migration is complete and preserves original authored bodies. Its tracked audit is `site/content/migration-report.json`; generated disposition accounting is the `ledger` field in `site/.generated/current/manifest.json` and records pages, supporting assets, external resources, drafts/exclusions and unsupported files. These reports and publication configuration are not served or indexed.

For future metadata migrations, inspect the default dry-run before applying:

```sh
npm run content:migrate -- --dry-run
# Inspect site/content/migration-report.json from the repository root.
npm run content:migrate -- --apply
```

Apply requires the exact reviewed plan and unchanged original hashes; it validates each file's body, metadata, route, render and build before proceeding. A repeated completed migration proposes zero changes. Migration does not execute notebooks. The separately approved archived Pandas-to-Polars conversion is Task 9: thirteen examples (image CSV reader, callback CSV head, unused pipeline import, interview domain concat, Titanic column dictionary, heart feature columns, heart exercise scaffold, standalone heart pipeline, wine answer/question, multi-output Excel and both MATLAB metadata readers) have mirrored parity checks; the remaining two conversions are pending. The image check uses all 1,393 real local CSV records. Callback and domain-boundary checks use explicitly synthetic inputs because the original training log and external caller frames are unavailable; they do not establish real training/classifier integration. Heart checks use the complete 303-row primary TensorFlow candidate recorded in `site/tests/fixtures/real/polars/provenance.json`; equality to the unavailable historical heart.csv remains unknown. Titanic checks use an explicitly synthetic schema because authentic input bytes are unavailable. TensorFlow/sklearn recording stubs capture only arrays and prescribed split/pipeline arguments; no model or training behavior is exercised. Exercise TODOs and the standalone script's pre-existing invalid FIXME remain intact; only selected valid tabular snippets are executed. Checks consume local inputs and never acquire datasets.

Wine checks use both complete original UCI CSVs and retain the first duplicate in source order, explicit source-row alcohol lookups, eleven ordered features and `(quality, is_red)` outputs. Full schema inference preserves the real red-wine value `40.5` that fails prefix inference. Excel checks use the complete original UCI workbook: 768 rows, eight ordered X1–X8 features, and separate Y1/Y2 outputs; its declared trailing empty rows/columns are excluded by both readers. The example reads a bounded 2 MiB workbook stream using the calamine engine. Prescribed row splits, training-only means, sample standard deviations (`ddof=1`) and normalized NumPy arrays match the original preprocessing. Null/NaN, duplicate and constant-column checks are explicitly synthetic supplements. Wine exercise TODOs, upstream licenses, model architecture and training cells remain intact; no model/training integration is claimed.

MATLAB checks use eight authentic records derived from the exact cropped metadata member, retaining default SciPy struct/cell/scalar wrappers and the unchanged 20,284-entry celebrity dictionary. Provenance records parent and fixture hashes, archive range/ETag and source IDs. Typed strings, scalar fields and bbox lists match the original metadata values and missingness; unknown gender is removed before integer casting while meaningful second-face NaNs survive. Null/NaN and empty checks supplement actual records. Builder metadata TODOs are completed only in test memory to compare selected readers; exercise placeholders, registration/extraction instructions and licenses remain intact. No crop images, real image dimensions/coordinate normalization or TFDS download/build execution are verified.

## Cloudflare Direct Upload setup

Hosting configuration is supplied in `.github/workflows/notes-site.yml`. **This work has not provisioned a Cloudflare account/project or verified a live publication.** An account owner must separately authorize setup/publication and confirm an existing Direct Upload project with production branch **master**. Direct Upload takes prebuilt files; it cannot later switch to Git integration. A command for an authorized owner to create a project is:

```sh
npx --yes wrangler@4.147.0 pages project create PROJECT --production-branch master
```

Confirm the actual project production branch and public HTTPS URL. Deploying with `--branch master` does not change a project's production branch. For an existing project with a different production branch, follow Cloudflare's documented API setup rather than assuming a dashboard switch.

Configure the GitHub repository:

| Kind     | Name                       | Purpose                                                            |
| -------- | -------------------------- | ------------------------------------------------------------------ |
| Secret   | `CLOUDFLARE_API_TOKEN`     | Account-scoped token with Account / Cloudflare Pages / Edit        |
| Variable | `CLOUDFLARE_ACCOUNT_ID`    | Intended Cloudflare account ID                                     |
| Variable | `CLOUDFLARE_PAGES_PROJECT` | Existing Direct Upload project name                                |
| Variable | `SITE_URL`                 | Actual production HTTPS URL without credentials, query or fragment |

Tokens stay in trusted readiness/publication process environments; never put them in source files, client output, build variables, command arguments or logs. Pull requests verify without a deployment token. Missing settings visibly disable publication while verification remains usable. Production URL/revision inputs are fixed during verification, so canonical/source/sitemap output matches the uploaded artifact.

Only a trusted `push` to `refs/heads/master` with successful verification and complete settings can publish. Verification uses Node 24.18.1, `npm ci`, full Chromium, Python 3.12.14 with isolated pinned parity dependencies and `npm run verify` in `site/`. It uploads only the verified `dist`. A separate job checks its exact artifact ID and SHA-256 digest, downloads it with digest mismatch treated as an error, and uses pinned Wrangler 4.147.0 without rebuilding or installing course dependencies. PRs and other branches cannot publish. Publishing runs in a workspace without checked-out course projects or a `functions` directory.

The `_headers` policy allows the exact inline theme-bootstrap hash, same-origin scripts/fonts/assets/PDF frames, Pagefind WebAssembly compilation and controlled KaTeX/Shiki inline styles. Changing bootstrap bytes requires updating the hash and passing the actual-header browser gate. It permits same-origin framing for native PDF resources and sanitized HTTPS archive images. Historical HTTP image URLs use native HTTPS upgrading; the local compatibility test uses deterministic image transport and does not establish upstream availability. Local tests cannot establish Cloudflare parsing, project existence, token permissions or a published URL; after authorized publication, check the actual hosted responses and reader/search/PDF behavior.

Cloudflare Free's 500 builds/month is a managed-build quota, not a measured Direct Upload deployment quota. See [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/), [CI setup](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/), [headers](https://developers.cloudflare.com/pages/configuration/headers/) and [limits](https://developers.cloudflare.com/pages/platform/limits/).
