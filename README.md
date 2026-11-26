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

Install full Chromium for the browser suite, which exercises the built response policy and the PDF.js viewer. The development command prepares content before starting Astro. It polls source paths every second, awaits watcher readiness, and refreshes open readers after successful publication. A failed content rebuild reports the offending source paths and keeps the last successful snapshot; repair the source to recover without restarting. Polling costs O(watched paths) per second. Development retains one previous asset publication for open readers; production removes stale assets.

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

### Add an ordinary note

Add UTF-8 Markdown under one of the six archive roots. Directory paths define the Source Archive hierarchy, and `README.md` is the directory landing note. A new ordinary note publishes automatically without a registry entry and appears in Source Archive and default learning search. Drafts and exclusions suppress publication. Supplemental notes remain in Source Archive and All files search.

For example, save this Markdown in `Tutorials/attention-mechanisms.md`. New notes require a nonempty frontmatter title.

```markdown
---
title: Attention mechanisms
description: Scaled dot-product attention
tags: [transformers]
---

## Why scale the scores?

Dividing by the square root of the key dimension keeps large dot products from saturating the softmax.
```

The reader is `/notes/tutorials/attention-mechanisms/`. The `tags` field describes the note. Topic browsing and topic search filters use the optional registry below.

Optional fields are `description` (string), `tags` (unique strings), `draft` (boolean), `slug` (section-relative lowercase ASCII path), `order` (finite number), `updated` (real ISO date, `YYYY-MM-DD`), `aliases` (previous absolute site paths), and `role: supplemental`. Omitted tags/aliases are empty and omitted draft is false. Omitted role means a primary learning note; supplemental course/template documents retain readers, full-text search and source links while leaving default study-note browsing, navigation and adjacency. No other role value is accepted. Legacy notes derive titles from their first H1 or filename; do not invent updated dates.

Edit `site/content/publication.json` for exclusions and path-specific overrides. Course/vendor text and notebook/resource metadata use overrides rather than rewriting upstream text. Frontmatter takes precedence over descriptive overrides; a draft in either location prevents publication. Exclusions always win, including over overrides and links. Aliases cannot shadow existing page/output paths or application assets, including `/_headers`. Markdown/notebook readers use `/notes/<section>/<path>/`; code/PDF/slides use `/resources/<section>/<path>/`.

Relative note/image/resource links are resolved from the source directory and rewritten to published routes; invalid targets, ambiguous wiki links and missing heading fragments fail with source diagnostics. Markdown supports safe HTML, tables, task lists, fenced code and math. Author scripts, event handlers, arbitrary iframes and executable MDX are forbidden. Notebooks display stored Markdown, code and supported output **without execution**. Code resources are highlighted text; course programs and their package dependencies are not run or deployed.

Referenced images and eligible PDF/slide assets are content-addressed. An individual deployed file may not exceed **25 MiB (26,214,400 bytes)**; output may not exceed **20,000 files**. Local PDFs have a responsive, in-page PDF.js preview with page and zoom controls. **Open PDF** and **Download PDF** are available at every viewport, including when JavaScript is disabled. Slides provide downloads, not a slide renderer. Oversized resources use an immutable public repository source URL or explicit HTTPS `resourceUrl` override. Declare `repositoryPublic: true` only for a genuinely public repository and configure its HTTPS `repositoryUrl`; `SOURCE_REVISION` must be an immutable commit hash (CI uses `github.sha`). Private or unavailable external sources need an explicit public resource URL or exclusion. No additional object-storage service is provisioned.

### Optionally enroll a note

Enroll a note to assign topics, a source collection or group, related readers, or a place in a learning path. Enrollment adds a stable `uid`, and builds read the registry without writing to it. The enrollment command scans all eligible sources in the worktree and proposes records for every unregistered public reader. New records start `unreviewed` with `topics: []`. The default purpose is `note` for primary Markdown and notebooks, `project-file` for code, and `reference` for other readers, including supplemental Markdown.

From `site/`, save the dry run to the ignored `.superpowers/` directory at the repository root. The plan contains the absolute worktree path, so keep it local. `--silent` keeps the npm banner out of the JSON.

```sh
mkdir -p ../.superpowers
npm run --silent content:organize -- --dry-run > ../.superpowers/organization-plan.json
```

Review the `inventory` for source hashes, dispositions and existing reader routes and anchors. Check `coverage` and the duplicate, outline and unclassified `candidates`. In `sidecars`, inspect the proposed JSON strings in `proposedBytes` and confirm which sources would be enrolled. Bare `npm run content:organize` also defaults to a read-only dry run. Run the apply command from the same worktree once you have reviewed the file.

```sh
npm run --silent content:organize -- --apply ../.superpowers/organization-plan.json
```

Apply checks current source and publication policy evidence and the prior sidecar hashes. It installs the proposed bytes in `site/content/organization/` and saves recovery evidence under `.superpowers/organization-migrations/` when there are changes. Repeating the same apply against unchanged inputs is a no-op. If source, policy or sidecar edits make a plan stale, generate and review a fresh plan.

### Classify an enrolled note

Edit the sidecars directly after enrollment. Review their diff and check the result with `npm run content:check` from `site/`. The enrollment command adds default records. Editorial choices belong in the sidecar edits. Keep organization fields out of upstream source files.

Each of the four files requires `"version": 1` and rejects unrecognized fields. The complete JSON examples below show how the attention note could be organized in a workshop. In the shared registry, add records to existing arrays, reuse matching topic and collection IDs when appropriate, and update the enrolled entry in place.

**`site/content/organization/taxonomy.json`**

```json
{
  "version": 1,
  "topics": [
    {
      "id": "attention-mechanisms",
      "title": "Attention mechanisms",
      "summary": "How attention weights combine input values."
    }
  ]
}
```

**`site/content/organization/collections.json`**

```json
{
  "version": 1,
  "collections": [
    {
      "id": "attention-workshop",
      "title": "Attention workshop",
      "summary": "Worked examples of scaled dot-product attention.",
      "type": "workshop"
    }
  ],
  "groups": [
    {
      "id": "scaled-dot-product",
      "collectionId": "attention-workshop",
      "title": "Scaled dot-product attention",
      "summary": "Compare scores before and after scaling.",
      "type": "module",
      "order": 1
    }
  ]
}
```

**`site/content/organization/entries.json`**

```json
{
  "version": 1,
  "entries": [
    {
      "uid": "doc-319b10bc3bcdebb3cf5b9420f7b66d24f2263c7d3d4d10141ca9eb4fac95d9c7",
      "sourcePath": "Tutorials/attention-mechanisms.md",
      "topics": ["attention-mechanisms"],
      "collectionId": "attention-workshop",
      "groupId": "scaled-dot-product",
      "purpose": "note",
      "status": "unreviewed"
    }
  ]
}
```

**`site/content/organization/paths.json`**

```json
{
  "version": 1,
  "paths": [
    {
      "id": "attention-workshop-introduction",
      "title": "Introduction to attention",
      "summary": "Start with score scaling, then explore related notes.",
      "steps": [
        {
          "id": "read-about-scaling",
          "title": "Why scale attention scores?",
          "summary": "Read about scaling before applying the softmax.",
          "entryUids": [
            "doc-319b10bc3bcdebb3cf5b9420f7b66d24f2263c7d3d4d10141ca9eb4fac95d9c7"
          ],
          "topicIds": ["attention-mechanisms"]
        }
      ]
    }
  ]
}
```

Use the exact normalized repository-relative `sourcePath` and keep the enrolled `uid` when a file moves. Update its `sourcePath` and preserve old reader links with an alias when the route changes. An entry can have multiple topics and appear in several paths. Its `collectionId` and `groupId` are optional. A group requires its owning collection, and a nested group’s `parentId` must be in the same collection. Topic hierarchies can have at most three levels. Use lowercase hyphenated IDs. Group IDs are unique within a collection, and step IDs are unique within a path.

Every `entryUids` reference in a path step must resolve to a public, enrolled reader. A step without entry references needs a topic with eligible learning material, including material in its descendant topics. The published path applies learning eligibility to its entries, omitting public outlines, entries with `purpose: project-file`, and supplemental readers. It displays topics that contain eligible learning material, skips steps with no visible entries or topics, and keeps the remaining steps in array order. A path gets a page only when it has a visible step.

Optional `relatedUids` records one-way relationships in the registry. For a public reader, each related UID must resolve to a public, enrolled reader.

Use `purpose` to distinguish `note`, `exercise`, `reference`, and `project-file`. Collections represent a book, university course, online course, or workshop. Groups represent chapters, modules, projects, assessments, or reference material. A `project` group exposes a file tree. Give each preserved example snapshot its own project group so its files stay together.

| `status`     | Meaning                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| `unreviewed` | No editorial review is recorded. Eligible readers still appear in learning browse and search.              |
| `outline`    | A public outline. Find it in Source Archive, All files search, and Resources where grouped.                |
| `draft`      | Withheld from public readers, navigation, search and sitemap, including when the source has no draft flag. |
| `reviewed`   | An editor has verified the document. Set this only after editorial review.                                 |

The default **Learning material** search includes eligible notes, notebooks, exercises and references. Choose **All files** to include project code, supplemental readers and outlines. Both scopes support topic, collection, section and kind filters. Topic filtering includes descendant topics. The library’s topic, collection, group and path pages link to the same canonical reader in Source Archive. Search uses the latest production build.

`npm run content:check` reports broken registry references with the owning source or record and the invalid target. For a deleted source, remove its stale entry and repair incoming path steps and related UID references. For a public reference to a draft or excluded target, update or remove that reference. For a misspelled group or topic ID, correct the reference in its sidecar. During development an invalid edit leaves the last successful snapshot available while you fix the diagnostic.

## Migration and internal reports

The reviewed metadata migration is complete and preserves original authored bodies. Its tracked audit is `site/content/migration-report.json`; generated disposition accounting is the `ledger` field in `site/.generated/current/manifest.json` and records pages, supporting assets, external resources, drafts/exclusions and unsupported files. These reports and publication configuration are not served or indexed.

The organization pilot audit records the original source inventory, hashes, canonical routes and anchors, dispositions, and reviewed sidecar hashes. It is kept outside public output. The pilot enrolled **6,279** readers and assigned organization metadata to **5,106** across Applied Science interview notes, Ian Pointer’s PyTorch book, and the Udemy React course. It defines **22 topics**, **2 source collections** with **405 groups**, and **1 learning path** with **22 steps**. The remaining **1,173 readers** have neither a topic nor a source collection. The `reviewed` editorial count is zero. [Organization pilot audit](site/content/organization-migration-report.json)

Topics were assigned to **38 readers**, including **34** of the **573** eligible for default learning search. Of the rest of that learning scope, **535** have neither a topic nor a collection and **4** have a collection only. All **5,654 code readers** remain intentionally untagged. Duplicate and outline candidates require editorial review. Further topic curation, splitting long notes, rewriting the roadmap, reconciling overlapping material, factual corrections and deduplication are deferred editorial work.

For future metadata migrations, inspect the default dry-run before applying:

```sh
npm run content:migrate -- --dry-run
# Inspect site/content/migration-report.json from the repository root.
npm run content:migrate -- --apply
```

Apply requires the exact reviewed plan and unchanged original hashes; it validates each file's body, metadata, route, render and build before proceeding. A repeated completed migration proposes zero changes. Migration does not execute notebooks. The separately approved archived Pandas-to-Polars conversion is Task 9: all fifteen examples (image CSV reader, callback CSV head, unused pipeline import, interview domain concat, Titanic column dictionary, heart feature columns, heart exercise scaffold, standalone heart pipeline, wine answer/question, multi-output Excel, both MATLAB metadata readers, time series and the cuDF tutorial CPU comparison) have mirrored parity checks. The complete conversion range has an independent specification-compliant, quality-approved review, and the configured local `npm run verify` passed archive parity, static and unit checks, production build, browser tests and final output validation. Whole-website acceptance is tracked separately from the conversion milestone; merging and live publication require separate approval. The image check uses all 1,393 real local CSV records. Callback and domain-boundary checks use explicitly synthetic inputs because the original training log and external caller frames are unavailable; they do not establish real training/classifier integration. Heart checks use the complete 303-row primary TensorFlow candidate recorded in `site/tests/fixtures/real/polars/provenance.json`; equality to the unavailable historical heart.csv remains unknown. Titanic checks use an explicitly synthetic schema because authentic input bytes are unavailable. TensorFlow/sklearn recording stubs capture only arrays and prescribed split/pipeline arguments; no model or training behavior is exercised. Exercise TODOs and the standalone script's pre-existing invalid FIXME remain intact; only selected valid tabular snippets are executed. Checks consume local inputs and never acquire datasets.

Wine checks use both complete original UCI CSVs and retain the first duplicate in source order, explicit source-row alcohol lookups, eleven ordered features and `(quality, is_red)` outputs. Full schema inference preserves the real red-wine value `40.5` that fails prefix inference. Excel checks use the complete original UCI workbook: 768 rows, eight ordered X1–X8 features, and separate Y1/Y2 outputs; its declared trailing empty rows/columns are excluded by both readers. The example reads a bounded 2 MiB workbook stream using the calamine engine. Prescribed row splits, training-only means, sample standard deviations (`ddof=1`) and normalized NumPy arrays match the original preprocessing. Null/NaN, duplicate and constant-column checks are explicitly synthetic supplements. Wine exercise TODOs, upstream licenses, model architecture and training cells remain intact; no model/training integration is claimed.

MATLAB checks use eight authentic records derived from the exact cropped metadata member, retaining default SciPy struct/cell/scalar wrappers and the unchanged 20,284-entry celebrity dictionary. Provenance records parent and fixture hashes, archive range/ETag and source IDs. Typed strings, scalar fields and bbox lists match the original metadata values and missingness; unknown gender is removed before integer casting while meaningful second-face NaNs survive. Null/NaN and empty checks supplement actual records. Builder metadata TODOs are completed only in test memory to compare selected readers; exercise placeholders, registration/extraction instructions and licenses remain intact. No crop images, real image dimensions/coordinate normalization or TFDS download/build execution are verified.

Time-series checks use the complete pinned official-course CSV: 3,235 monthly rows from 1749-01-31 through 2018-07-31. Identity with the absent historical lowercase `sunspots.csv` remains unknown. Generated month ends join unchanged Date labels, preserving calendar gaps and rejecting duplicates. Overlap Pearson correlations use pairwise null/NaN masks while retaining infinities; plotting ACF uses global centering and the full original positions. Exact lag slicing retains 3,101 double differences beginning at source position 134 (1760-03-31). Cells 48/49 intentionally correct the original label-aligned subtraction defect to positional differences; that correction is separately tested, rather than claimed as original parity. Only cell 35’s two stale saved outputs and execution count are cleared; all other saved outputs, including ARIMA, remain unchanged. The obsolete cell 47 reference is Markdown with its empty code-only fields removed. Tests adapt the removed Pandas month-end alias only in memory and execute the installed plotting function AST with recorded axes; no Matplotlib package is added. Synthetic leap/gap/off-month/duplicate, null/NaN/infinity, constant and short cases supplement real data. Rendered plot appearance, arbitrary timestamps/time zones and ARIMA execution are unverified.

CPU pageviews checks read the complete existing 34,132,641-byte CSV: 1,118,999 data rows with the original first physical row as the four ordered column names (`en.m`, `Article_51`, `1`, `0`). Full values, String/String/Int64/Int64 types and missingness match the original reader, including twelve missing page titles; explicit default NA tokens preserve the literal `None` at source row 754611. Only the exact first 257 physical lines are committed as a small fixture; they do not establish the full schema. CPU and cuDF read paths now point to the real adjacent `./pageviews_small.csv`, rather than the absent `./data/` directory. Synthetic quoted-empty, default NA, Unicode, numeric missingness and header/error cases supplement the real input. Only the CPU import/read/head is executed; GPU operations, cuDF compatibility explanations and the existing missing-image repair remain intact. cuDF/GPU behavior, performance and full notebook execution are unverified.

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

The `_headers` policy allows the exact inline theme-bootstrap hash, same-origin scripts, fonts, assets, frames and PDF.js workers, Pagefind WebAssembly compilation and controlled KaTeX/Shiki inline styles. Changing bootstrap bytes requires updating the hash and passing the actual-header browser gate. The policy also allows sanitized HTTPS archive images. Historical HTTP image URLs use native HTTPS upgrading; the local compatibility test uses deterministic image transport and does not establish upstream availability. Local tests cannot establish Cloudflare parsing, project existence, token permissions or a published URL; after authorized publication, check the actual hosted responses and reader/search/PDF behavior.

Cloudflare Free's 500 builds/month is a managed-build quota, not a measured Direct Upload deployment quota. See [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/), [CI setup](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/), [headers](https://developers.cloudflare.com/pages/configuration/headers/) and [limits](https://developers.cloudflare.com/pages/platform/limits/).
