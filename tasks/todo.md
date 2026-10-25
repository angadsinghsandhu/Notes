# Notes website

## Design and planning

- [x] Inspect the archive, representative notes, and existing project guidance.
- [x] Confirm authoring: Markdown in this repository, published after a Git push.
- [x] Record the initial content scope and publication assumptions for review.
- [x] Compare architecture and free hosting options.
- [x] Draft the publishing pipeline, artifact handling, responsive interface, and verification design.
- [x] Write and self-review the design specification.
- [x] Obtain review of the written specification (user authorized implementation).
- [x] Write and self-review the implementation plan.
- [x] Obtain plan review and execution-method selection (subagent-driven development).

## Implementation and verification

- [x] Implement the approved pipeline and website with appropriate tests and quality gates.
- [x] Adapt existing content and verify internal links and artifact rendering.
- [x] Verify local development, production output, mobile and desktop layouts, and deployment configuration.
- [x] Document authoring, local startup, and deployment.

## Review

Exploration found about 10,000 files and 1.9 GB of material. The archive mixes authored Markdown with course examples, PDFs, slide decks, notebooks, datasets, and model checkpoints.

The user requested both specification and plan creation. Wrote `docs/superpowers/specs/2026-10-04-notes-website-design.md` and `docs/superpowers/plans/2026-10-04-notes-website.md`. The design proposes Astro/TypeScript, a build-time publishing backend, Pagefind search, and verified Cloudflare Pages deployment. The eight-task implementation plan covers runtime/gates, discovery, links/assets, rendering, pipeline, responsive interface, migration, and delivery.

Review assumptions are public readership, rendered notebooks/code with PDF/slide resource pages, the name Notes Library, and the dedicated `site/` application boundary. Both documents were checked for placeholders, link validity, consistent interfaces, hosting limits, draft exclusions, and specification coverage. Documentation checks passed; product tests are not applicable because no product code exists yet. The user approved implementation, task commits, and frequent feature PRs on 2026-10-04. Work runs in the managed notes-website worktree with fresh implementers and task reviews. Commits and remote feature-branch/PR writes are performed only by the controller. No merging or live publishing is authorized.

## Implementation milestones

- [x] Task 1: runtime and quality gates (reviewed; commits 7d6755d, 8dbda44).
- [x] Task 2: automatic discovery and metadata/URL validation (reviewed; commit 497438f).
- [x] Task 3: links, headings, and assets (reviewed; commits d9c54e4, f7fbe87).
- [x] Task 4: safe Markdown/notebook/code rendering (reviewed; commits 681bf6b, 80e4759).
- [x] Task 5: content pipeline and development watcher (reviewed; commits 99c9718, 0272436; 188 units and all gates pass).
- [x] Task 6: responsive reader and search (reviewed; commit 1fb53b5; 270 units/all gates/52 browsers; 2 minor follow-ups recorded).
- [x] Task 7: full archive migration and output verification (reviewed; commits bef12de, 992e0f6; 398 units/all gates/56 browsers).
- [x] Task 8: deployment and operating documentation.
- [x] Task 9: approved archived Pandas → Polars conversion (15 files; isolated real-data parity).

Task 7 migrated 171 authored titles without changing source bodies, classified 49 upstream supplemental documents, and accounted for all 10,031 archive files. Production validation checks routes, assets, source actions, exclusions and native Pagefind output. Source polling and serialized watcher readiness passed the original live HTTP lifecycle. Fresh controller verification passed 398 units, all four per-file coverage floors of at least 90%, all static/build/output gates and 56 browser tests. Independent review and scoped re-review resolved all three P2 findings; two Zod deprecation hints remain deferred for final review. No deployment was performed.

## Approved folder navigation correction (2026-10-19)

- [x] Implement aligned clickable breadcrumbs, folder pages/cards and full-tree navigation.
- [x] Verify real archive, mobile/desktop, keyboard/no-JS and existing quality gates.
- [x] Independently review and commit verified navigation; refresh the local preview.

User approved the short design in chat. Folder cards show immediate children; the complete 2,300-folder tree is a shared page linked from the desktop sidebar and mobile drawer. Generated navigation routes participate in existing alias and case-insensitive output ownership checks.

Review: independent review and scoped re-review approved. Final checks passed 75 Python tests, 463 unit tests, all per-file coverage floors, format/lint/boundaries/typecheck/build/output validation, and 69 production browser tests after the final guard. The earlier full 73-browser run also passed the four real development/publication fixtures. All non-Pagefind output is byte-identical to that full browser artifact; native Pagefind metadata/filter semantics are unchanged, and fresh search/response-policy browser checks passed on the final configured build. Archive files remain unchanged. Local preview runs at http://127.0.0.1:4330/library/books/. No merge or deployment was performed.

## Approved responsive PDF viewer (2026-10-19)

- [x] Implement self-hosted PDF.js pages, zoom/fit-width, selectable text and fallbacks.
- [x] Verify real PDFs, mobile/desktop, keyboard, lazy loading and response policy.
- [x] Independently review and commit verified viewer; refresh local preview.

User approved the short design in chat.

Review: the PDF reader passed independent task review, scoped re-review and final integration review. Fresh complete verification passed 75 archive parity checks, 482 unit tests, all four per-file coverage floors, format/lint/boundaries/typecheck/build/output checks, and 77 browser tests. Actual seven-page and 220-page documents cover pixels, selectable text, page controls, zoom, keyboard scrolling, mobile layouts and response policy. New pages reset reading offsets while same-page zoom preserves position. The reviewed immutable preview is available at http://127.0.0.1:4330/. Tasks 8 and 9 were already independently completed before these navigation/PDF follow-ups; their checkboxes now reflect that recorded completion. No merge or deployment was performed. Live Cloudflare hosting, real encrypted PDF browser fixtures, physical mobile browsers and full model training remain unverified.

## Proposed library information architecture (2026-10-21)

- [x] Inventory published paths and metadata; sample document content and identify structural problems.
- [x] Write the requested refactor specification and implementation plan.
- [x] Self-review contracts, compatibility, pilot scope and verification coverage.
- [x] Obtain user review of both documents before implementation (user requested implementing all tasks on 2026-10-21).
- [ ] Execute the reviewed plan with the established subagent-driven method.

Review: the proposal adds Topics, Collections and Learning Paths over the existing six-root archive. It preserves canonical readers, source bodies, prepared body IDs, PDF functionality and the complete source tree. A separate persistent UID registry supports curated references. The initial curation pilots are Applied Science, the PyTorch book and the Udemy React course; full-corpus editorial rewriting, duplicate deletion and physical moves are deferred. The plan defines eight testable milestones, strict metadata/reference validation, learning/file search scopes, live-update acceptance and route/hash preservation. Both artifacts are proposals for joint review as explicitly requested; no product code, archive material or running preview changed.

### Organization implementation milestones

- [x] Task 1: strict organization schema and persistent identity (8325343; independent review approved).
- [x] Task 2: atomic preparation, draft/route safety and sidecar watcher (9fa6fb0; independent review approved).
- [x] Task 3: indexed public catalog selectors (540dfa4; independent review approved).
- [x] Task 4: reviewed metadata migration and three pilots (targeted checks/build and independent review approved; final full gate remains for delivery).
- [ ] Task 5: responsive curated pages, trees and reader links.
- [ ] Task 6: learning/file search scopes and metadata filters.
- [ ] Task 7: full output preservation and live development acceptance.
- [ ] Task 8: authoring guide, whole-branch review and feature delivery.

Execution: isolated notes-website worktree; ledger `.superpowers/sdd/2026-10-21-library-information-architecture/progress.md`. Source/body identities and the reviewed port-4330 snapshot remain preserved. Main alone handles Git/remote writes; no merge or deployment is authorized.

## LeetCode interactive curriculum (2026-10-24)

- [x] Inspect current solutions and the source-reader pipeline; inventory numbered coverage and duplicates.
- [x] Create clickable library/lesson mockups in ignored brainstorming space.
- [x] Confirm deep lessons for problems 1–2000, every distinct approach visualized, curated inputs and future custom-input compatibility.
- [x] Confirm Cloudflare-only hosting, owner-only cross-device studied progress, official links, sourced company information and reusable learning trees.
- [x] Write the full design, obtain independent builder check and user approval.
- [x] Write and self-review separate platform and complete-curriculum implementation plans.
- [ ] Obtain user review of the implementation plans before execution; retain the established subagent-driven method.
- [ ] Reconcile and complete the prerequisite organization refactor without discarding its partial files.
- [ ] Implement and independently review platform Tasks 1–14 and curriculum inventory/pilot C1–C2.
- [ ] Complete all 40 coverage waves in C3 with exact IDs, bounded sub-batches and independent per-lesson review.
- [ ] Complete final integration/coverage review and the applicable serialized full gate; update PRs without merging or deploying.

Review: approved specification `docs/superpowers/specs/2026-10-24-leetcode-learning-library-design.md`; plans `docs/superpowers/plans/2026-10-24-leetcode-learning-platform.md` and `docs/superpowers/plans/2026-10-24-leetcode-curriculum.md`. Initial filename inventory found 360 Python files, 250 distinct numbered problems, 240 in range and 79 duplicate numbers; identity/correctness reconciliation remains implementation work. The plans distinguish software/pilot readiness from all 2000 verified lessons, preserve original archive URLs/bytes and private progress, and defer actual deployment authorization. This milestone changes documentation only; no curriculum lessons, progress backend or production UI have been implemented.
