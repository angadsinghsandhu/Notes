# LeetCode Learning Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend Notes with deep algorithm lessons, per-approach playback, reusable learning-path trees and private cross-device studied progress.

**Architecture:** Keep Astro static readers and the existing prepared catalog. Prepare a separate curriculum snapshot in the same atomic publication generation; load lesson-specific traces on demand. A same-origin Cloudflare Worker protected by Access stores owner progress in D1.

**Tech Stack:** Existing Astro/TypeScript/Zod/Markdown/Pagefind/Vitest/Playwright; Python 3.12 curriculum checks; SQL/shell where required; Cloudflare Workers, D1 and Access; pinned Wrangler and a maintained JWT library selected after a compatibility check.

**Spec:** `docs/superpowers/specs/2026-10-24-leetcode-learning-library-design.md` — user approved 2026-10-24. Companion content plan: `docs/superpowers/plans/2026-10-24-leetcode-curriculum.md`.

## Global Constraints

- Work only in `/Users/angad/.codex/worktrees/notes-website/Notes`; app boundary `site/`. Preserve all existing uncommitted organization work and archive bytes.
- Public target is exactly frontend problem numbers 1–2000, inclusive; immutable identity `leetcode:<frontend-number>`; Python default, SQL/shell for native questions.
- Proposed canonical routes: `/practice/leetcode/`, `/practice/leetcode/<number>/`, `/practice/paths/`, `/practice/paths/<id>/`; preserve source readers and routes.
- Every distinct approach needs checked code, explanation/proof/complexity, tests and at least one curated visualization. No custom-input editor or arbitrary code execution.
- Maximum 2000 trace frames and 1 MiB uncompressed trace per example. No silent truncation, autoplay, whole-corpus trace bundle or animation-only explanation.
- Completed means studied. Only one configured owner; private data never enters static output, Pagefind or public caches. Anonymous reading works without the API.
- Content states `planned`, `draft`, `verified` remain distinct. Company associations require source/date; unknown evidence stays unknown.
- Keep Node 24.18.1 and existing project Python environment; no archived notebook/course execution. No speculative framework.
- Mirror source paths under `site/tests/`; source files under approximately 500 lines. Preserve at least 90% per-file statements/branches/functions/lines; no ignores/skips/retries to make a gate pass.
- Targeted tests and scoped static checks while editing; necessary real UI builds; one full serialized `npm run verify` after final fixes and before final feature readiness. Do not repeatedly run full suites per task.
- Main agent alone handles exact-path commits, pushes and PRs; no destructive Git commands, merges, provisioning, remote migrations or deployment without separate authorization. Feature PRs remain draft until applicable final gates pass.

## Review Focus

1. Two devices toggle the same problem concurrently: reject stale writes, preserve intent, show current server state (Task 9/10).
2. A forged Access header, alternate Worker origin or expired HTML login redirect must never grant identity or appear as successful synchronization (Task 9/10/13).
3. A recursion/mutation-heavy visualization must represent the tested code's actual intermediate state, including backtracking and input changes (Task 4/5 and content C2).
4. A problem repeated in multiple branches must count once; pending lessons must not make a path look complete (Task 7).
5. A source rename or metadata refresh during development must not combine an old lesson body with a new registry/trace or lose a legacy reader (Task 3/12).

## Work breakdown and file placement

This plan covers software; the companion plan covers source research, the eight-lesson pilot and all remaining content. Execute sequentially against these interfaces. No parallel source writers. When a file exceeds the size cap, split along the named responsibilities and record the exact extra paths before editing.

| Surface           | Files and responsibility                                                                                                                                                                                                                                                          |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Content contracts | `site/src/content/leetcode/{types,schema,paths,prepare}.ts`: validated identities, lesson readiness, DAGs and generation outputs; exports via `site/src/content/index.ts`                                                                                                         |
| Publication       | Existing `prepare.ts`, `publication.ts`, `identifiers.ts`, `watcher.ts`, `types.ts` only where reconciliation shows required changes; maintain archive Manifest v1 and use a versioned companion curriculum artifact                                                              |
| Read facade       | `site/src/lib/leetcode.ts`, existing `catalog.ts`: same-generation indexed selectors and safe public copies                                                                                                                                                                       |
| Trace preparation | `site/scripts/curriculum.py`, `site/scripts/curriculum_trace.py`: reviewed bounded implementation verification; no archive imports                                                                                                                                                |
| Playback          | `site/src/client/leetcode/{trace,playback,renderers}.ts`, `site/src/components/AlgorithmPlayer.astro`: pure state/frame selection, lifecycle and semantic rendering                                                                                                               |
| Readers           | `site/src/layouts/LessonLayout.astro`, `site/src/components/{LessonApproach,CompanyEvidence,StudyProgress,LearningPathTree}.astro`, `site/src/pages/practice/leetcode/{index,[number]}.astro`, `site/src/pages/practice/paths/{index,[id]}.astro`, `site/src/styles/leetcode.css` |
| Discovery/search  | Existing `Navigation.astro`, `Search.astro`, `src/client/search.ts`, source resource route, sitemap and output/Pagefind verifiers                                                                                                                                                 |
| Progress          | `site/src/lib/progress-types.ts`, `site/src/client/progress.ts`; `site/worker/{index,auth,progress,export}.ts`, `site/worker/migrations/0001_progress.sql`, `site/wrangler.progress.jsonc`, `site/tsconfig.worker.json`                                                           |
| Local/config/docs | Existing package/lock/eslint/vitest/tsconfig and CI as needed; `site/scripts/progress-dev.ts`, `site/tests/scripts/progress-dev.test.ts`, `site/README.md`, repo README and mirrored steering                                                                                     |

Every `.ts` above has its same relative `.test.ts` under `site/tests/`. Every Astro page/component/layout has a mirrored Playwright `.test.ts`. Python tools use `site/tests/scripts/test_curriculum.py` and `test_curriculum_trace.py`; content implementation cases mirror their directory under `site/tests/content/leetcode/`. Worker migrations are exercised by Worker repository integration tests under `site/tests/worker/progress.test.ts`, not a pretend SQL text assertion. Add new test roots to the real runners without diluting existing coverage.

## Execution sequence

### Task 0: Reconcile the prerequisite and freeze preservation evidence

**Files:** Existing organization ledger `.superpowers/sdd/2026-10-21-library-information-architecture/{progress,SESSION_CONTEXT}.md`; `tasks/todo.md`; this plan. No new product source during reconciliation.

**Interfaces:** Consumes the approved organization spec/plan and all current partial files. Produces a recorded reviewed base SHA, current archive hash/route inventory, applicable catalog signatures and a clean separation of unfinished prerequisite work.

- [ ] Read current Git status, ledger, live agent state and reports; never repeat organization Tasks 1–4 or discard Tasks 5–8 partial work. Reconcile changes since this plan was written.
- [ ] Finish/review the remaining organization tasks under their existing approved plan before extending their reader/catalog contracts. Record completion evidence; do not claim the current uncommitted UI is reviewed.
- [ ] Save a read-only source hash, source identity/route/headings and publication baseline with actual UTC time under a new ignored curriculum ledger. Keep preview 4330 on its reviewed snapshot.
- [ ] Record task dependencies/checkpoints in `tasks/todo.md`; main creates a `codex/leetcode-platform` branch from the reviewed base without resetting files.

### Task 1: Define strict curriculum contracts

**Files:** Create content `leetcode/types.ts`, `schema.ts`; mirrored tests; modify content barrel. Content plan C1 supplies real manifest records.

**Interfaces:** `ProblemId = \`leetcode:${number}\``(runtime constrained integer 1..2000);`LessonStatus = 'planned' | 'draft' | 'verified'`; `readCurriculum(rootDir: string): Promise<CurriculumDefinition>`; `validateCurriculum(input: unknown): CurriculumDefinition`. Definition version 1 contains problems, lesson records and paths. `ProblemRecord` includes number, id, official URL/slug, domain, topics, difficulty, evidence and status; readiness may not depend on an unvalidated claim in prose.

- [ ] Write mirrored red tests `rejects_missing_or_duplicate_frontend_ids`, `rejects_url_identity_mismatch`, `requires_company_source_and_observation_date`, `rejects_escape_paths_and_unknown_keys`, `rejects_verified_lesson_without_approach_evidence`. Assert exact 1..2000 coverage, not only length 2000.
- [ ] Run `npx vitest run tests/src/content/leetcode/schema.test.ts` and observe intended missing-module/API failures.
- [ ] Implement strict Zod contracts, bounded local file references, separate catalog metadata vs prose/code/trace evidence. Allow planned records with explicitly absent unverified metadata; never make up slugs/titles to satisfy schemas.
- [ ] Run named tests and scoped formatter/linter/boundary checks plus typecheck; main reviews/stages only listed files and commits `feat: define curriculum content contracts` after independent review.

### Task 2: Validate reusable learning-path graphs

**Files:** Content `leetcode/paths.ts`, mirrored test; types/schema/barrel only for this public contract.

**Interfaces:** `validateLearningPaths(paths: LearningPathDefinition[], problems: ProblemRecord[]): LearningPathIndex`; `pathProgress(path: LearningPathDefinition, studied: ReadonlySet<ProblemId>, problems: ReadonlyMap<ProblemId, ProblemRecord>): PathProgress`. Nodes have stable ID, kind stage/problem, ordered children and prerequisites; `PathProgress` separates unique required/available/verified/studied counts.

- [ ] Add red `rejects_cycles_and_dangling_prerequisites`, `rejects_out_of_range_problem`, `shared_problem_counts_once`, `pending_targets_prevent_full_completion`, `next_ready_skips_pending_without_locking_navigation` cases with explicit small graphs.
- [ ] Run mirrored tests red; implement deterministic DAG validation, stable ordering and distinct-ID counters. Reuse existing organization path presentation where compatible; do not change its UID/source identity contract to fit curriculum IDs.
- [ ] Run named tests and scoped gates; independently review and main commit `feat: validate curriculum learning paths`.

### Task 3: Prepare and read generation-bound curriculum snapshots

**Files:** Content `leetcode/prepare.ts`, existing preparation/publication/watcher/identifiers/types/barrel; lib `leetcode.ts` and `catalog.ts`; all respective mirrored tests; scripts/content.ts if wiring requires it.

**Interfaces:** `prepareCurriculum(definition: CurriculumDefinition, context: CurriculumPrepareContext): Promise<CurriculumSnapshot>`; context contains source catalog and isolated generation output directory. Snapshot v1 holds canonical metadata, routes and body/trace references. Add `catalog.curriculum: CurriculumCatalog` with `listProblems(filter?: ProblemFilter): ProblemSummary[]`, `getLesson(id: ProblemId): PreparedLesson | undefined`, `listPaths(): PathSummary[]`, `getPath(id: string): PreparedLearningPath | undefined`; all results safe copies bound to the selected catalog generation. Prepared lesson includes body HTML and approach code/trace references, never raw filesystem paths publicly. Also emit a minimal nonprivate `progress-registry.json` of published problem IDs/revisions for the Worker build; it must not import the Node catalog or bundle lesson bodies.

- [ ] Add red tests `claims_new_routes_against_aliases_and_source_folders`, `invalid_lesson_keeps_last_good_snapshot`, `draft_body_not_reported_verified`, `old_catalog_keeps_old_lesson_and_trace`, `source_variants_link_without_rewriting_archive`. Include normalized/case-folded collisions.
- [ ] Implement companion artifact inside the existing atomic publication transaction; reuse sanitized Markdown/heading/render helpers. No new parallel content watcher or per-page reparsing of the large archive manifest.
- [ ] Expose lesson routes to the sitemap/output ownership inventory. Watch curriculum metadata/prose/code/trace changes through the existing awaited queue with errors retaining last successful output.
- [ ] Run direct-dependent content/catalog tests and scoped gates. Review/commit `feat: publish curriculum snapshots with archive preservation`.

### Task 4: Build deterministic trace verification and bounded execution

**Files:** `site/scripts/curriculum.py`, `curriculum_trace.py`, mirrored Python tests; content `leetcode/trace.ts` plus mirrored TypeScript test/barrel; package/lock/test configuration only for the real gate and selected tooling.

**Interfaces:** Trace v1 `{problemId, approachId, implementationSha256, exampleId, result, frames}`; each frame `{stepId, codeLines, explanation, state, highlights}` with renderer-discriminated validated state. `validateTrace(trace: unknown): AlgorithmTrace` enforces 2000 frames and 1048576 UTF-8 JSON bytes. CLI `python3 -B scripts/curriculum.py check --ids 1,64` verifies code/results/traces; `... inventory` reports exact pending/verified IDs; default `check` checks all published implementation inputs. Tool exits nonzero on mismatch, timeout or absent evidence.

- [ ] Write red tests for wrong intermediate state, mismatched implementation hash, duplicated step IDs, invalid code-line references, missing text explanation, 2001 frames and 1048577 bytes. Pin exact accepted boundaries too.
- [ ] Implement reviewed subprocess execution with deterministic seeds/timeouts and fail-closed network/filesystem restrictions appropriate to trusted repo implementations. Not an untrusted-code sandbox: never expose a browser/HTTP execution endpoint. Run only explicitly enrolled curriculum modules through explicit call adapters, never archive imports.
- [ ] Generate traces from the tested instrumented algorithm, not a disconnected animation; check every state transition against per-approach invariants and independent small-input oracle where justified. Preserve input mutation semantics and result parity.
- [ ] Run `python3 -B -m unittest discover -s tests/scripts -p 'test_curriculum*.py'` and mirrored trace Vitest tests. Wire curriculum checks into the real final gate; add lint/type/format tooling for these Python files using existing Python conventions without reformatting archive files.
- [ ] Independent review/commit `feat: verify deterministic algorithm traces`. Coordinate companion C2 for real eight-domain fixtures before calling the framework complete.

### Task 5: Build accessible per-approach playback

**Files:** Client `leetcode/{trace,playback,renderers}.ts`, `AlgorithmPlayer.astro`, `leetcode.css`; exact mirrored unit/component browser tests.

**Interfaces:** `createPlayback(trace: AlgorithmTrace): PlaybackController`; controller `getFrame()`, `next()`, `previous()`, `reset()`, `play()`, `pause()`, `setSpeed(rate: number)`, `destroy()`. `mountAlgorithmPlayer(root: HTMLElement): () => void` fetches only the selected trace and returns cleanup. UI consumes types only from content barrel and pre-rendered trace URLs, no content runtime imports.

- [ ] Add red tests `backtracking_restores_full_state`, `reset_cancels_timer`, `example_switch_pauses`, `hidden_document_and_cleanup_pause`, `reduced_motion_defaults_to_manual_steps`, `trace_load_failure_keeps_transcript`. Use deterministic fake timers, no sleeps.
- [ ] Implement reusable array/pointer, matrix, node/edge and stack/queue/call-tree views as required by the pilot. SQL row transformations use semantic tables. Keep initial page free of trace fetch until activation; bound frame work and never load every approach's trace together.
- [ ] Add mirrored Playwright cases: keyboard/touch controls, no autoplay, code-step linkage, non-color labels, screen-reader transcript, narrow screen containment, reduced motion, request count/bytes. Use pilot trace outputs, not only synthetic frames.
- [ ] Run direct units/browser cases plus necessary configured real UI build; independent review/commit `feat: add accessible algorithm visualization playback`.

### Task 6: Deliver canonical lessons and discovery

**Files:** Lesson layout, LessonApproach, CompanyEvidence, problem index/detail routes, source resource route, Navigation/Search/client search, sitemap; corresponding mirrored tests; existing output/Pagefind verifiers and tests.

**Interfaces:** Pages consume only `Catalog.curriculum` from Task 3. A source variant maps to canonical `ProblemId`; official link/company display uses validated metadata, never prose scraping. `ProblemFilter` supports query, topic, difficulty, company, status with URL state. Add a distinct canonical lesson search scope while retaining source-file search.

- [ ] Write red real-build/browser assertions: #64 contains statement, constraints, each approach/proof/complexity/code/player, official URL, evidence date or honest unknown; original #64 resource still renders and links to lesson; SQL #175 is labeled SQL; a planned lesson shows pending rather than fabricated prose.
- [ ] Implement readable long-form desktop/mobile layout and consistent breadcrumbs. Keep one canonical index body per lesson and no listing duplicates; display drafts visibly and count only verified lessons as finished curriculum.
- [ ] Add no-JS reading, semantic headings/anchors, visible focus, dark/light/reduced-motion, 320px and desktop tests. Search uses current native Pagefind API and pinned generated fixture, verifies filters intersect without whole-corpus downloads.
- [ ] Run scoped units/browser/output checks against one frozen required build. Review/commit `feat: add canonical LeetCode lesson readers`.

### Task 7: Deliver learning-path trees

**Files:** LearningPathTree component, path index/detail pages, client `leetcode/path-tree.ts`, respective mirrored tests; catalog facade only as necessary for precomputed paths.

**Interfaces:** Render Task 2 `PreparedLearningPath` with unique progress aggregates from Task 10. Tree state is local presentation only; canonical studied state lives once per problem. Start with editorial full-coverage route; future named subsets are unsupported until exact membership is curated.

- [ ] Add red tests for a shared problem under two stages, prerequisite edges, expand/collapse keyboard controls, deterministic next-ready recommendation and unavailable lesson labels. Assert 2000 unique targets is not presented as 2000 verified lessons.
- [ ] Implement expandable tree/forest with equivalent ordered outline, usable links even without JS, mobile nested lists instead of a squashed wide graph. Never lock access based on prerequisites.
- [ ] Verify real pilot path, mixed planned/verified targets, deep branch and keyboard/reduced-motion layouts. Review/commit `feat: add reusable curriculum learning paths`.

### Task 8: Add a locally tested D1 progress repository

**Files:** Shared `progress-types.ts`; Worker `progress.ts`, migration SQL, Wrangler config, Worker tsconfig; mirrored shared/Worker tests; package/lock/config for pinned local tooling.

**Interfaces:** `StudyProgress = {problemId: ProblemId, studied: boolean, studiedRevision: string | null, studiedAt: string | null, updatedAt: string, version: number}`; `ProgressWrite = {studied: boolean, lessonRevision: string, expectedVersion: number}`. `readProgress(db, ownerKey): Promise<StudyProgress[]>`; `writeProgress(db, ownerKey, problemId, input): Promise<{kind:'saved';progress:StudyProgress}|{kind:'conflict';progress:StudyProgress}>`. Missing row has logical version 0. Owner key comes only from authenticated server context, not request JSON.

- [ ] Red tests against actual local D1 binding: migrations create unique owner/problem row, version 0 insert race has one winner, stale update conflicts, repeated identical intended state returns stable saved state, different problems do not conflict, unstudy clears studied timestamp/revision, timestamps are server-assigned.
- [ ] Implement prepared SQL, conditional writes/transactions and explicit read consistency using supported D1 behavior. Conflict response includes authoritative current state; clients never use clock time as ordering.
- [ ] Run focused Worker integration tests under Wrangler/Cloudflare test runtime. Extend real coverage/static gates for Worker files and SQL behavior without adding a second ignored product test tree. Review/commit `feat: store versioned owner study progress in D1`.

### Task 9: Secure the same-origin owner API and export

**Files:** Worker `index.ts`, `auth.ts`, `export.ts`, repository, Wrangler config; mirrored tests; no live Cloudflare configuration changes.

**Interfaces:** `authenticateOwner(request: Request, env: AuthEnv): Promise<OwnerIdentity>` validates JWT then configured allowed identity. API: `GET /api/progress` → `{schemaVersion:1,progress:StudyProgress[]}`; `PUT /api/progress/<number>` accepts `ProgressWrite`, returns saved row or HTTP 409 current row; `GET /api/progress/export` → versioned JSON attachment. `/account/` implements safe relative return and sign-in/logout handoff. Unknown/unpublished identity fails 404; allow studying published drafts but retain their revision/status distinction, never mark their content verified.

- [ ] Red tests for signed allowed owner, wrong owner, expired/incorrect-audience/issuer/signature JWT, forged email header, missing env, alternate ingress, cross-origin mutation, oversized/unknown JSON, SQL payload, unknown ID and malicious return URL. Use local signed fixtures, never real private tokens in tests.
- [ ] Implement supported JWKS verification with bounded caching/rotation and signature checks. Require exact origin on mutations and CSRF defense; private JSON no-store; strict methods/body limits, no permissive CORS, no raw auth diagnostics or private values in logs. Exact email allowlist is an environment setting.
- [ ] Test parallel conflicting writes over actual Worker HTTP and ensure private endpoints never use the public static cache. Export schema includes revisions/versions and only authenticated owner's records; versioned export is recovery, not public build input.
- [ ] Load the Task 3 generated public progress registry during the Worker build; test unknown/planned IDs against that registry rather than accepting any integer in range. Record matching site/Worker curriculum revision in delivery instructions and handle a stale deployment as an explicit unavailable action, never an invented successful save.
- [ ] Run scoped auth/API/D1 checks; independent security/correctness review and commit `feat: protect private progress with Cloudflare Access`.

### Task 10: Add private studied state to lessons, cards and trees

**Files:** Client progress.ts, StudyProgress component; problem/path pages/cards and mirrored tests; pure path aggregate code only for shared-ID projection.

**Interfaces:** `createProgressClient(options: {baseUrl: string}): ProgressClient` with `load()`, `setStudied(id, studied, lessonRevision)`, `export()`, `logout()`, `destroy()`; `ProgressView` discriminates anonymous/loading/synced/saving/unsaved/conflict/error. Never return success until acknowledged by API. Use server version from latest state.

- [ ] Red tests for offline write, expired Access returning HTML/redirect, focus refresh, updated-since-studied, two-device conflict, reload persistence and sign-out cleanup. Assert completing #64 updates every visible path occurrence exactly once in totals.
- [ ] Implement explicit sign-in from public readers; pending intent stays in live view but needs confirmation after sign-in. Toggle studied reversibly. No passive scroll completion, persistent offline queue or feature creep into personal notes/submission tracking.
- [ ] Add real local Worker + two separate browser-context acceptance test for login fixture, cross-device save/read/conflict, retry, export, API unavailable and local public reading. Browser contexts must share D1, not localStorage pretending to sync.
- [ ] Scoped client/API/browser checks; review/commit `feat: synchronize private studied progress across devices`.

### Task 11: Integrate pilot curriculum and independent teaching review

**Files:** Companion content C2 exact eight problem folders, manifest/path/report; no new unlisted software paths unless pilot finds a reproduced defect.

**Interfaces:** Consume Tasks 1–10 plus C2 code/trace/content fixtures; produce eight verified lessons and a pilot acceptance report with exact evidence hashes and unresolved IDs.

- [ ] Complete C2 and cross-check at least one lesson for each renderer/algorithm family against actual code and trace. Run per-lesson, source-mapping and direct UI checks; never run full 2000 scripts to validate eight changes.
- [ ] Require fresh independent code/trace/correctness/teaching review. Resolve findings in smallest scoped fixes with regression and re-review. No lesson is promoted by the author alone.
- [ ] Main commit coherent pilot sub-batches after review; create a curriculum feature PR stacked on the platform branch. Do not mark remaining targets completed.

### Task 12: Preserve publishing, hot reload and end-to-end output safety

**Files:** Existing `site/scripts/verify-output.ts`, `verify-pagefind.ts`, `site/tests` mirrors; existing actual-dev lifecycle browser test; prepared watcher/curriculum files only for reproduced defects.

- [ ] Add failing real `npm run dev` acceptance with owned temporary curriculum files: add unregistered lesson, change prose/trace, invalid metadata → last good output, repair, draft/verified change, remove, legacy source rename mapping. Await HTTP generation identity, not arbitrary sleeps. Restore owned fixtures exactly on failures.
- [ ] Verify every original source SHA/route/heading/anchor and source resource action against Task 0 baseline. Validate all canonical curriculum routes, IDs, trace hashes/bounds and official-link metadata; stream/retain minimal evidence so default memory handles large output.
- [ ] Test native Pagefind canonical lesson scope and nonduplicate listings, all future 2000 manifest identities without body loading, and public output contains neither owner state, auth config, local paths nor private database files.
- [ ] Run only named lifecycle/output/browser tests and a necessary frozen build; review/commit `test: verify curriculum publishing and archive preservation`.

### Task 13: Document local use and deployment readiness

**Files:** Local dev script and mirror, package/config/CI, site/root README, mirrored CLAUDE.md/codex.md, tasks/todo.md; worker environment example contains names only.

- [ ] Add red startup test that a production hostname can never enable development fixture identity; local D1 stays local; missing production auth fails closed. One documented local command starts needed local dependencies and cleans up only its owned process tree.
- [ ] Document authoring/verification commands, statuses, paths, company evidence, adding an approach/example, progress export and version conflicts. Test exact commands on owned local fixture; preserve current preview and original mutable caches.
- [ ] Document custom domain, Access exact owner allow policy + OTP, JWT audience/team, protected path scope, alternate ingress disabled, Worker/D1 bindings, local/remote migration separation and artifact workflow. Read current Cloudflare limits at execution; report costs/constraints honestly. No automatic provisioning or remote DB writes.
- [ ] Update CI to exercise Worker/curriculum gates and existing website gates with isolated local DB. Keep deployment opt-in rules; public static success is not claimed as live auth success.
- [ ] Run scoped docs/startup/config tests and mirror checks; independently review and commit `docs: document curriculum authoring and private progress operation`.

### Task 14: Final platform review and release-candidate evidence

**Files:** No planned new source; any review fix has named paths and a new scoped regression before editing.

- [ ] Self-audit spec coverage, exact diff, staged/untracked ownership, no coverage suppressions/gate weakening, all task evidence and no false full-library claims. Fresh whole-branch reviewer inspects auth, D1 races, trace/code parity, original preservation, accessible reading and loading costs.
- [ ] Fix/re-review all findings; run scoped checks after each fix. Once product/test bytes are frozen, run complete serialized `npm run verify` under documented matching URL/revision and pinned runtime, including Worker/curriculum checks. Preserve real exits and logs. A failure requires root cause, scoped fix and revalidation, not rerunning for luck.
- [ ] Inspect desktop/mobile screenshots and manual playback/progress pilot. Confirm final output checker remains read-only. Refresh preview 4330 only from reviewed immutable final output after all browser/build tasks finish; preserve old snapshot.
- [ ] Main pushes final commits, updates/attaches feature PRs, records actual CI status and unverified live Cloudflare/physical-device constraints. Never merge/deploy. Platform complete means tested software + pilot; curriculum remains open until companion C3 reaches 2000/2000 verified.

## Verification commands and evidence discipline

From `site/`, scoped TypeScript units use `npx vitest run <mirrored-tests>` (add changed-source coverage selection when measuring the per-file floor); browser tests use `npx playwright test <mirrored-tests> --workers=1`. Scoped formatting/lint/boundaries use existing configs; `npm run typecheck` remains project-wide. New Wrangler Worker integration runner is pinned and wired into `npm run check` in Task 8; the exact installed command is recorded there before dispatching dependents. Python scoped tools use the pinned project environment and commands in Task 4. Do not assume a plain Vitest Node run proves D1 compatibility.

After any formatting/autofix, recheck affected files. Log UTC clock stamps, commands, source fingerprint, real exit and exact failures; retained evidence and task reports live in an ignored curriculum ledger. Independent reviewers read a frozen complete diff and reports, not just a summary or a green test count. No full-suite rerun solely because a reviewer hit a usage limit.

## Self-review

All spec surfaces have owners: identity/provenance/content C1/C2/C3; archive preservation 0/3/12; traces 4/5; lesson/search 6; trees 2/7; D1/auth 8/9; UI sync 10; pilot 11; hosting/local/docs 13; final validation 14. All five Review Focus conditions have named tests. Deferred named subsets, custom inputs and public registration are not silently implemented. User design approval is recorded; this plan awaits user review before implementation.
