# Library information architecture refactor

Date: 2026-10-21 (America/Los_Angeles)
Status: approved for implementation by the user on 2026-10-21; subagent-driven execution is in progress.
Baseline: `19aee3713aaa34f03aad8679b09c6793a4111209`.

## Intent and scope

Make the archive useful as a learning library: find a concept across sources, follow a book/course in order, and follow a preparation path without digging through implementation files. Preserve Markdown-in-Git authoring, local operation, static Cloudflare Pages hosting, mobile access, existing readers, and the original archive.

The user requested a refactor specification and plan following the archive review. This proposal interprets that as a navigation, classification, and publishing refactor. It does not authorize bulk prose rewriting, physical moves, duplicate deletion, merging, or deployment. The user subsequently approved both artifacts by requesting implementation of all tasks on 2026-10-21. That approval preserves the exclusions above.

## Evidence and limitations

The prepared catalog contains 6,279 entries: 220 Markdown documents, 154 notebooks, 5,654 code resources, 215 PDFs, and 36 slide resources. The ledger accounts for 10,031 source files, including supporting assets, unsupported files, and exclusions. One Udemy React collection accounts for 5,071 published entries. There are 49 supplemental documents and no populated tags or descriptions in the prepared entries.

All published paths and catalog metadata were inventoried; document headings and bodies were sampled. PDFs and notebooks have not all received factual/editorial review. Ten byte-identical Markdown/notebook/PDF groups contain 44 additional copies, including templates and placeholders: byte equality alone does not establish that a document should be deleted.

Examples motivating the design:

- Related ML material is spread across Books, Classes, Courses, Interview, and Tutorials.
- React project snapshots expose thousands of individual code files as peer resources.
- The applied-science roadmap has 815 lines; several breadth notes exceed 1,000 lines.
- French/Japanese unit landing pages contain only frontmatter.
- JHU semester/acronym paths obscure descriptive course names.
- Parallel TensorFlow directories require comparison, not an assumed automatic merge.

## Alternatives and decision

1. **Recommended: preserve sources; add curated views.** Topics, Collections, and Learning Paths reference one canonical reader per entry. Lowest migration risk and keeps course context.
2. Move everything into topic folders. Simpler physical taxonomy but disrupts projects, relative links, course order, and cross-topic documents.
3. Keep the six roots and improve labels only. Cheap, but does not connect subjects across sources or solve project-file noise.

Choose option 1. Physical reorganization and editorial splitting are later, separately reviewed projects. No new database, server, CMS, graph engine, or runtime classification service is required.

## Website structure

`/library/` becomes a landing page with three equal entry points plus an explicit link to the existing source archive.

```text
Library
├── Topics                         /library/topics/
│   ├── Mathematics & Statistics
│   │   ├── Linear Algebra
│   │   ├── Calculus & Optimization
│   │   ├── Probability
│   │   └── Statistics & Experimentation
│   ├── Algorithms & Data Structures
│   │   ├── Arrays, Strings & Hashing
│   │   ├── Linked Lists, Stacks & Queues
│   │   ├── Trees, Tries & Heaps
│   │   ├── Graphs
│   │   ├── Searching & Sorting
│   │   ├── Recursion & Backtracking
│   │   ├── Dynamic Programming
│   │   └── Greedy Algorithms
│   ├── Machine Learning
│   │   ├── Foundations & Data Preparation
│   │   ├── Supervised Learning
│   │   ├── Unsupervised Learning
│   │   ├── Probabilistic Models
│   │   ├── Training & Regularization
│   │   ├── Evaluation & Validation
│   │   └── Deployment
│   ├── Deep Learning
│   │   ├── Neural Networks
│   │   ├── Computer Vision
│   │   ├── Natural Language Processing
│   │   ├── Attention, Transformers & Language Models
│   │   ├── Audio & Speech
│   │   ├── Reinforcement Learning
│   │   └── Frameworks & GPU Computing
│   ├── Web Development
│   │   ├── JavaScript & TypeScript
│   │   ├── React
│   │   ├── Next.js
│   │   ├── CSS & Tailwind
│   │   ├── Data Visualization
│   │   └── Testing & Deployment
│   ├── Software Design & Systems
│   │   ├── Object-Oriented Design & SOLID
│   │   ├── Design Exercises
│   │   ├── Containers & Docker
│   │   └── Conversational Interfaces
│   ├── Cryptography & Blockchains
│   │   ├── Foundations
│   │   ├── Consensus
│   │   ├── Smart Contracts
│   │   └── Privacy & Zero Knowledge
│   └── Human Languages
│       ├── German
│       ├── French
│       └── Japanese
├── Collections                    /library/collections/
│   ├── Books
│   ├── University Courses         institution → named course
│   ├── Online Courses             provider → named course
│   └── Workshops & Tutorials      author/provider → named work
├── Learning Paths                 /library/paths/
│   ├── Coding Interview Preparation
│   ├── Applied Scientist Interview Preparation
│   ├── Low-Level Design Preparation
│   └── Behavioral Interview Preparation
└── Source Archive                 existing sections and /library/tree/
```

This is the controlled vocabulary, not a promise of content under every branch. Empty branches are omitted from public navigation. Topic IDs are unique lowercase hyphenated strings; parent IDs define a tree of at most three levels below Topics. Topic routes use `/library/topics/<id>/`, independent of ancestry. Collections and paths similarly use flat stable IDs under their own namespaces. Renaming a display label or moving a topic under another parent does not change its route.

An entry can belong to several topics and paths, but has at most one primary source collection and one collection group. Semester, year, edition, and course code are optional collection metadata; descriptive course names are the labels. Do not infer acronym expansions from filenames without source evidence.

## Collection and project model

A collection overview contains a real summary, source attribution, and ordered groups. Group types are `chapter`, `module`, `project`, `assessment`, and `reference`. Each group belongs to exactly one collection; groups have optional same-collection parents, with cycles rejected. Group routes are `/library/collections/<collection-id>/groups/<group-id>/`.

Readers see direct child group cards, then direct documents divided into Notes, Exercises, and Resources. Descendant groups are not flattened into every ancestor. Group order uses explicit numeric order, then the existing natural title/path comparator as a deterministic tie-breaker. Resource file format is a badge/filter, not the main hierarchy.

For React, each example snapshot becomes a project group containing its own source tree. Distinct starting/completed/intermediate snapshots remain distinct; no source versions are deduplicated. The project page is the discoverable unit; individual code readers remain accessible through its file tree, source archive, and an explicit file search scope. No project code is executed.

The PyTorch book preserves its chapter order. Its PDFs, notebooks, and code appear beside the relevant chapter notes. A group with no notes still exposes its resources without suggesting that an authored explanation exists.

## Metadata and identity contract

Use reviewed JSON sidecars under `site/content/organization/`; do not insert organizational metadata into upstream course files or notebooks. Existing title/description/frontmatter/publication override rules remain authoritative. Existing `role: supplemental` is preserved and is separate from the new purpose field.

The sidecars have strict schemas, `version: 1`, and reject unknown properties:

- `taxonomy.json`: `topics` with `{id, title, summary, parentId?, order?}`.
- `collections.json`: `collections` with `{id, title, summary, type, provider?, courseCode?, edition?, year?, semester?}`; `type` is `book | university-course | online-course | workshop`. Also `groups` with `{id, collectionId, parentId?, title, summary, type, order?}`. Group IDs are unique within a collection.
- `entries.json`: `entries` with `{uid, sourcePath, topics, collectionId?, groupId?, purpose, status, summary?, relatedUids?}`. `purpose` is `note | exercise | reference | project-file`; `status` is `unreviewed | outline | draft | reviewed`.
- `paths.json`: `paths` with `{id, title, summary, steps}`; steps are `{id, title, summary, entryUids, topicIds}` in array order. Step IDs are unique within the path. A step needs at least one entry or populated topic; it is not a second copy of the content.

All ID references must resolve, paths must be normalized repository-relative sources under existing roots, and each published source can have only one organization record. A `groupId` requires its owning `collectionId`. Topic assignments are direct; ancestor membership is derived. Ancestor counts deduplicate entries by UID. Summaries are plain text, never executable markup. `relatedUids` is a curated directed list; no inferred graph or automatic reciprocal edges.

**Keep the current `ContentEntry.id`, body paths, and `Manifest.version: 1` intact.** Today that ID is SHA-256 of sourcePath and is validated by the body loader. Add an optional `organization` block on the manifest containing the validated organization snapshot; do not overload `id`.

`uid` is a persistent `doc-` plus 64 lowercase hexadecimal characters. Initial enrollment copies the current entry ID with that prefix. Once recorded, a UID never changes merely because a path changes. A future move must update the record's sourcePath and explicitly preserve routes/aliases; file moves are outside this phase.

New Markdown files continue to be discovered automatically. An unregistered entry remains accessible in its original section/tree/search with a derived fallback purpose (`project-file` for code, `note` for primary Markdown/notebooks, otherwise `reference`) and `unreviewed` status. It has no curated UID and cannot be referenced by a path until enrolled. There are no build-time writes to the registry. Authors use the migration dry-run/apply tool to enroll and classify it. This avoids making automatic publishing depend on hidden database mutations.

Publication exclusions and existing draft flags always win. Organizational `status: draft` additionally suppresses an entry before links, body publication, search, sitemap, and assets are planned. Organization records may classify a draft, but no public path step or related-entry link may reference a missing, excluded, or draft target: those references are errors, not dangling links. A stale entry record after a deletion is reported as an error; the last successful development snapshot remains served until the record is repaired.

`outline` documents remain explicitly labeled and available in the archive/file scope; omit them from default topic/path learning lists. `unreviewed` means no editorial judgment was made, not that the content is incorrect. Never mark existing notes reviewed or invent update dates during mechanical migration.

## Public catalog and rendering

Content preparation reads and validates sidecars once, resolves organization against discovered entries, and publishes it atomically with bodies and assets. UI reads prepared data only through `site/src/lib/catalog.ts`. Build UID/topic/collection/group indexes once per catalog generation, not by reparsing the manifest in each page.

Expose typed methods to list populated topics, collections, paths and groups, fetch their records, and select direct or descendant entries. Public selectors exclude drafts and return copies; do not expose internal ledgers, absolute paths, original hashes, migration reports, or generated body storage in page props. Counts distinguish learning documents, project groups, and supporting resources.

Topic pages show a summary, child topics, learning notes/exercises, related collections, and an optional Resources section. Do not emit a duplicate reader under a topic URL: every document link targets its existing canonical reader. Add topic/collection links to reader metadata without changing the original-source breadcrumb or its same-row alignment.

Learning-path steps preserve explicit order. Entry links always point to canonical readers. Path progress is expressed as a study sequence, with no login, completion tracking, or saved personal state in this phase. Reader adjacency remains source-context adjacency; do not change next/previous merely because a note appears in a path.

## Search and navigation

Keep Pagefind and its existing production-build lifecycle. Index canonical readers once. Mark category/group/path listing pages as outside Pagefind indexing to prevent duplicate results.

Add topic and collection filters and a search scope with two values: `learning` (default) and `files`. Learning scope indexes primary notes/notebooks and non-project references/exercises. It excludes `project-file`, supplemental, and outline entries. Files scope searches all public readers, including project files, supplemental material, and outlines. Exclusions and drafts are never searchable. Existing section and file-kind filters continue to work in both scopes.

Project group pages are navigable browsing pages, not duplicated indexed readers. Consequently they are found through collection/topic browsing in this phase. Do not invent an untested search-weight algorithm to make code less prominent: the explicit scope is the contract.

Desktop navigation exposes Topics, Collections, Paths, and Source Archive. Mobile uses the existing accessible navigation mechanism. Retain the complete source tree and add a server-rendered topic tree; show the active collection's group tree on collection/group pages. Do not load all project source trees into every reader. Controls meet the existing 44px target, visible focus, keyboard, theme, and no-JavaScript browsing expectations. At 320px, 375px, 768px and 1280px there is no page-wide horizontal overflow; long labels wrap and breadcrumbs align within each row.

## Migration strategy and scope boundary

Implement a separate organization migration tool, leaving the completed title migration untouched. Default mode is read-only dry-run. Its output records baseline source hashes, old canonical routes/anchors, dispositions, proposed organization records, duplicate candidates, and classification coverage. Apply requires the exact reviewed plan and unchanged hashes; it writes only sidecar JSON with atomic replacement and preserved prior copies. Re-running an applied plan makes no changes.

Initial enrollment covers all published entries, with unreviewed status and no guessed topic labels. Initial purpose is `project-file` for code, `note` for primary Markdown/notebooks, and `reference` otherwise; explicitly reviewed exercises can override it. Curated pilot scope is:

1. `Interview/Applied Science/**`: topic assignments and an applied-scientist path linking existing documents. Preserve all prose and existing section anchors.
2. `Books/Programming PyTorch for Deep Learning - Ian Pointer/**`: book/chapter groups and resource relationships.
3. `Courses/Udemy/React/**`: course/module/project-snapshot groups, with code assigned `project-file`; preserve each example version and path. Supplemental templates stay supplemental.

Outside the pilot, a reviewed directory-to-collection mapping may establish source collections, but unknown topics remain unassigned. A course directory is not sufficient evidence of every file's subject. The migration report lists unclassified and outline candidates; unresolved candidates do not silently acquire classifications.

The first delivery is complete when these three pilots and the infrastructure work. Full corpus topic curation, splitting long notes, rewriting the roadmap, fixing factual content, deleting duplicates, and physical restructuring are explicitly later editorial work. The report must say how much remains rather than claim the whole archive is curated.

## Route, watcher, and deployment safety

All new category and group routes enter the existing central, case-insensitive route/output ownership checks, including collisions with aliases, reserved paths, generated files, and folder routes. Source-archive routes remain unchanged. Compare every baseline canonical route and anchor after migration; this phase permits zero removals.

Watch all organization sidecars alongside publication policy. Source and organization edits publish one consistent generation; invalid configuration retains the last successful snapshot with source-specific diagnostics. Production search still updates only after a build, and development continues to disclose that limitation. Changing organization files must not require restarting development.

Keep Astro/TypeScript, Node 24.18.1, Pagefind, and the existing verified Cloudflare Direct Upload workflow. No new production dependency is required. Individual output files remain at most 26,214,400 bytes and total output at most 20,000 files. Existing PDF support-file validation, restrictive response policy, and resource fallbacks stay intact. Never execute course programs, notebooks, training, or GPU code.

## Acceptance and release evidence

- Inventory every published entry and ledger disposition; archive bytes, canonical routes, and anchors match the baseline. Record the actual baseline at execution rather than hard-code today's counts.
- The three pilots have reviewed titles, collection/group relationships, intended topic assignments and linked resources, with explicit unreviewed/outline status where applicable.
- A transformer topic reaches applicable pilot interview and book material through canonical links; no copies are created.
- React code files leave default learning search and remain discoverable through files scope, source archive, and project groups.
- Registry/reference/cycle/duplicate-ID/route collisions fail before a snapshot swap. New unclassified notes still publish automatically; deletions with stale records produce actionable errors.
- Actual HTTP development tests exercise source addition, registry enrollment, label/topic edits, draft transition, rename mapping and deletion cleanup without restart; validate old snapshot retention on errors.
- Browser tests cover the real pilots, native Pagefind scopes/filters, 320/375/768/1280 layouts, keyboard, no-JavaScript browsing, themes, scoped accessibility, PDF controls and resource links.
- Existing per-file statements, branches, functions and lines stay at least 90%; no new suppression, skip, retry policy, or reduced threshold masks a failure.
- Final serialized `npm run verify` passes, followed by independent review/fix loops. Commit verified milestones and create feature PRs; only the main agent makes Git/remote writes. Never merge, release, provision, or deploy without separate human authorization.

## Deferred editorial refactor

After the pilot is reviewed, prepare a separate content-editing spec: split the largest applied-science notes by learning question, reduce the roadmap to a linked sequence, reconcile overlapping TensorFlow sources, repair mislabeled documents, and review repeated PDFs. Every proposed move/split needs a source-to-destination mapping, preserved anchors/aliases, provenance, and review of original bytes. It is not part of the implementation plan accompanying this spec.
