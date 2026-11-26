# Library Information Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (the user's established execution method) or superpowers:executing-plans only if the user changes that preference. Steps use checkbox syntax for tracking.

**Goal:** Add Topics, Collections and Learning Paths while preserving every existing reader, archive source and publishing safeguard.

**Architecture:** Build and validate an organization snapshot from versioned JSON sidecars during content preparation. Expose indexed selectors through the existing catalog facade; Astro pages and Pagefind consume that prepared snapshot. Curate three pilots before extending classification across the archive.

**Tech Stack:** Existing Astro/TypeScript, Zod, Pagefind, Vitest and Playwright; Node 24.18.1. No new production dependency, service or database.

**Spec:** [2026-10-21-library-information-architecture-design.md](../specs/2026-10-21-library-information-architecture-design.md)

**Status:** User approved implementation of all tasks on 2026-10-21 and selected subagent-driven development. Merging and deployment remain unauthorized.

## Global Constraints

- Preserve the original six archive roots, archive bytes, canonical reader routes and heading anchors; no prose rewrites, physical moves or duplicate deletion.
- Keep the current `ContentEntry.id`, body paths, and `Manifest.version: 1` intact.
- Keep Astro/TypeScript, Node 24.18.1, Pagefind, and the existing verified Cloudflare Direct Upload workflow.
- Individual output files remain at most 26,214,400 bytes and total output at most 20,000 files.
- Existing per-file statements, branches, functions and lines stay at least 90%; no new suppression, skip, retry policy, or reduced threshold masks a failure.
- Never execute course programs, notebooks, training, or GPU code.
- Only the main agent makes Git/remote writes. No destructive Git commands, including in scratch repositories; preserve unrelated edits and all evidence.
- Never merge, release, provision, or deploy without separate human authorization.
- Keep the reviewed preview on port 4330 available; stateful gates run serially and browser verification owns 4328.
- Respect content/public-barrel boundaries and the catalog facade; keep focused source files below approximately 500 lines.

## Review Focus

1. Source-path-derived IDs must not be mistaken for persistent UIDs: a registered source-path change preserves UID without breaking prepared body validation (Tasks 1–3).
2. Draft/excluded items must not leak through path steps, topic counts, Pagefind, sitemap or copied assets (Tasks 2, 4, 6).
3. Conflicting category/alias/folder routes and invalid sidecar updates must fail before publication while development retains a good snapshot (Tasks 2, 4, 7).
4. Shared multi-topic entries and deeply nested project snapshots must not duplicate readers/counts or load the complete source tree into every page (Tasks 3–6).
5. Existing unclassified notes and no-JavaScript/mobile users must retain access; outline/project suppression only changes default curated browsing/search (Tasks 3–7).

## File and responsibility map

Paths below are repository-relative. Existing files were inspected at baseline `19aee37`; recheck any externally updated base before execution. Existing feature PRs are dependencies: do not silently merge them.

| Unit                  | Files                                                                                             | Responsibility                                         |
| --------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Organization contract | `site/src/content/organization-types.ts`, `organization-schema.ts`, `organization.ts`             | Strict schemas, resolution, public snapshot            |
| Source integration    | `site/src/content/types.ts`, `index.ts`, `prepare.ts`; `site/scripts/dev.ts`                      | One atomic publication, draft timing, sidecar watching |
| Indexed browsing      | `site/src/lib/organization.ts`, `catalog.ts`                                                      | Prepared public selectors and indexes                  |
| Reviewed metadata     | `site/content/organization/{taxonomy,collections,entries,paths}.json`                             | Vocabulary, source/group membership, ordered paths     |
| Migration             | `site/src/content/organization-migrate.ts`; `site/scripts/organize.ts`                            | Read-only plan and hash-checked atomic apply           |
| UI                    | `site/src/components/Organization*.astro`; `site/src/pages/library/{topics,collections,paths}/**` | Curated indexes/details and collection groups          |
| Integration           | Existing library index, Navigation, ReaderLayout, Search, search client and reader styles         | Navigation, metadata links, Pagefind scopes            |
| Output safety         | Existing identifiers/folder route owners, sitemap route and output validator                      | Route ownership, sitemap, canonical preservation       |

Every new source gets a same-relative-path mirrored test under `site/tests/`; new Astro pages get component/source tests and applicable Playwright coverage using the existing test conventions. Do not introduce a second test root.

## Shared interface decisions

Define `OrganizationDefinition` from the four strict versioned sidecar schemas in the spec. Export its types and schema/resolver functions through `site/src/content/index.ts`. Keep I/O separate from pure validation/resolution.

`OrganizationSnapshot` contains public `topics`, `collections`, `groups`, `paths`, and resolved `memberships`. Each membership is `{entryId, uid?, topics, collectionId?, groupId?, purpose, status, summary, relatedUids}`. Use spec enums, immutable array inputs and no absolute paths. Registered UIDs are `doc-<64 lowercase hex>`; unregistered memberships omit UID. `summary` uses the organization summary, then original description, then an empty string; no generated prose at runtime.

Interfaces to implement:

```typescript
readOrganization(directory: string): Promise<OrganizationDefinition>
validateOrganization(value: unknown): OrganizationDefinition
resolveOrganization(entries: readonly ContentEntry[], definition: OrganizationDefinition): OrganizationSnapshot
buildOrganizationIndex(entries: readonly ContentEntry[], snapshot?: OrganizationSnapshot): OrganizationIndex
```

Use one discriminated `LibraryNode` union (`topic | collection | group | path`) with `{type, id, title, summary, route}` and its type-specific record data. Group keys are `<collectionId>/<groupId>`. `OrganizationIndex` supplies:

```typescript
listNodes(type: LibraryNode['type'], parentKey?: string): LibraryNode[]
getNode(type: LibraryNode['type'], key: string): LibraryNode | undefined
getMembership(entryId: string): Membership
getEntryByUid(uid: string): ContentEntry | undefined
listNodeEntries(type: 'topic' | 'collection' | 'group', key: string,
  options?: { descendants?: boolean; scope?: 'learning' | 'files' }): ContentEntry[]
```

Defaults: descendants false, scope learning. Topic child cards/counts explicitly request descendants true; group document lists request false. `listNodes` omits publicly empty branches; a topic parent with populated descendants is populated. A collection/group with only project files is populated in browsing even though its learning-entry count is zero. Path nodes expose resolved steps in stored order. `Catalog` gains `organization: OrganizationIndex`; existing methods retain behavior. New selectors return safe public copies.

### Task 1: Organization schema and persistent identity

**Files:** Create the three organization content modules above; modify `types.ts` and `index.ts`; create mirrored `organization-schema.test.ts` and `organization.test.ts`.

**Consumes:** Existing `ContentEntry`, publication rules and canonical routes. **Produces:** Strict definitions, membership types and pure resolver interfaces from Shared interface decisions. Add optional `Manifest.organization` without changing `version` or body identity.

- [ ] Write `rejects_invalid_registry_graphs`: duplicate/case-colliding IDs, unknown fields/enums, invalid UID/source paths, topic cycles/depth >3, group cycles/cross-collection parents, missing topics/UIDs, and groups without collection membership all fail with the offending record.
- [ ] Write `preserves_registered_uid_when_source_path_changes`: resolving the same recorded UID at a new explicit source path preserves UID, while `ContentEntry.id` and body identity remain their existing values.
- [ ] Write `resolves_unregistered_defaults`: code → project-file; primary Markdown/notebook → note; other/supplemental → reference; status unreviewed; UID absent; no I/O writes.
- [ ] Run `npx vitest run tests/src/content/organization-schema.test.ts tests/src/content/organization.test.ts` from `site/`; confirm intended failures, then implement only the specified contract and make tests pass.
- [ ] Run format/lint/boundaries/typecheck/build and targeted tests; main commits `feat(content): define library organization contracts` after review. Keep strict versioned empty sidecars with this deliverable only if the loader requires them; the baseline with absent organization must remain supported.

### Task 2: Atomic preparation, exclusions and route safety

**Files:** Modify `prepare.ts`, `identifiers.ts`, `types.ts`, `index.ts`, `site/scripts/dev.ts`, and corresponding mirrored tests. Add focused helper modules/tests if required by the 500-line cap.

**Consumes:** Task 1 definitions/resolver. **Produces:** Optional prepared organization snapshot and watcher support. `PrepareOptions` gains `organizationDir?: string`; production CLI supplies `site/content/organization`. Synthetic callers without it use an empty definition.

- [ ] Write `organization_drafts_are_filtered_before_render_and_assets`: an organizational draft's body, assets, links and outgoing public references cannot be published; path/related references to it fail clearly. Existing frontmatter/policy draft/exclusion behavior remains stronger.
- [ ] Write `organization_routes_share_central_ownership`: topic/collection/path/group routes collide with a canonical route, alias differing only in case, source folder route, and reserved output endpoint before swap.
- [ ] Write `organization_and_bodies_publish_one_generation`: malformed configuration or dangling reference yields diagnostics, leaves previous generation intact, and does not leak partially resolved memberships.
- [ ] Write watcher service tests for edits/atomic replacements to each of four sidecars, recovery from invalid JSON, and awaited shutdown; preserve serialized acquisition and 1s polling.
- [ ] Run mirrored prepare/identifiers/dev tests red, integrate early filtering and final snapshot resolution, then green. Account organizational drafts in the ledger using the existing excluded disposition with a precise reason.
- [ ] Run applicable full static/build gates; main commits `feat(content): publish validated organization snapshots` after independent review.

### Task 3: Indexed public catalog selectors

**Files:** Create `site/src/lib/organization.ts`, `site/tests/src/lib/organization.test.ts`; modify catalog and its mirrored tests.

**Consumes:** Snapshot and public entries from Task 2. **Produces:** `OrganizationIndex` and `Catalog.organization` exactly as specified above.

- [ ] Write `topic_descendants_deduplicate_shared_entries`: an entry assigned to two sibling topics counts once in their parent and links only to its canonical route.
- [ ] Write `group_children_do_not_flatten_projects`: only direct documents appear by default, nested snapshots remain distinct, and an explicit descendant query includes them once.
- [ ] Write `catalog_organization_is_generation_bound`: the cached manifest is parsed once per generation, a new generation refreshes organization, selectors cannot mutate internal records, and returned public data excludes ledger/hashes/absolute paths.
- [ ] Write `unregistered_and_outline_access_remains`: ordinary new notes remain in archive/files; outline/project/supplemental entries leave learning scope; resources remain accessible. Path step order is preserved and existing reader adjacency is unchanged.
- [ ] Run targeted tests red; implement indexes and selectors; run them green plus existing catalog/body-binding tests and static/build gates. Main commits `feat(site): expose indexed topic and collection browsing` after review.

### Task 4: Reviewed migration and three pilot collections

**Files:** Create organization sidecar JSON, `organization-migrate.ts`, `site/scripts/organize.ts`, mirrored migration/CLI tests; modify content barrel and `site/package.json`. Store the reviewed audit at `site/content/organization-migration-report.json`, outside public output.

**Consumes:** Contracts, resolver and baseline entries. **Produces:** `planOrganizationMigration(rootDir: string, definition: OrganizationDefinition): Promise<OrganizationMigrationPlan>` and `applyOrganizationMigration(plan: OrganizationMigrationPlan): Promise<void>`. Plan contains version, ordered source SHA256/route/anchor inventory, previous sidecar hashes, proposed complete sidecar bytes, coverage and candidates. Apply verifies both source and destination preconditions before any atomic replace and preserves previous bytes for recovery.

- [ ] Write `dry_run_never_writes_and_apply_rejects_changed_inputs`, `apply_is_idempotent`, and `partial_write_failure_restores_previous_sidecars`. Do not run the existing title-migration apply command.
- [ ] Implement `npm run content:organize -- --dry-run` as default; `--apply <reviewed-plan.json>` applies that exact plan. Split status/report generation from CLI I/O; explicit paths remain under the verified organization directory.
- [ ] Capture the current complete baseline, enroll every public entry with persistent UID/default purpose/unreviewed status, and emit unclassified/duplicate/outline candidates without guessing. Do not apply until the main agent reviews the exact proposed diff and hashes.
- [ ] Curate all Applied Science documents into the appropriate controlled topics and ordered applied-scientist path; link existing notes, preserving bodies/anchors and leaving unsupported subject gaps absent.
- [ ] Curate the PyTorch book into chapter groups with associated notebooks/code/PDF and verified order. Curate React into modules and distinct project snapshot groups; inspect real directory boundaries before writing explicit assignments. All raw code has project-file purpose unless a reviewed record explicitly classifies an exercise.
- [ ] Write pilot fixture tests asserting exact reviewed membership UID sets, every React code entry's purpose, chapter ordering, path order, and no missing registered sources. Topic placeholders with no material stay hidden. Source acronym expansions require evidence in the audit.
- [ ] Run migration tests red/green, inspect dry-run, apply reviewed sidecars, compare every archive hash and baseline route/anchor/disposition, then run static/build/output gates. Main commits `feat(content): organize three pilot learning collections` after independent metadata review. Record unclassified remainder and outline candidates explicitly.

### Task 5: Curated pages, trees and reader links

**Files:** Create page index/detail pairs under `site/src/pages/library/topics/`, `collections/`, `paths/`; collection groups at `collections/[collectionId]/groups/[groupId].astro` (use `collections/[id].astro` for collection detail, `[id].astro` for topic/path detail). Create focused `OrganizationCards.astro`, `OrganizationTree.astro`, `OrganizationMetadata.astro`, plus mirrored tests. Modify existing library index, Navigation, ReaderLayout, reader styles and their tests. Do not replace the source FolderTree.

**Consumes:** Catalog organization selectors. **Produces:** Static routes and responsive browsing matching the spec; no duplicate readers.

- [ ] Write tests for populated-only topic trees, provider/type collection grouping, immediate group cards, Notes/Exercises/Resources sections, ordered path steps, empty-note resource-only groups and canonical links. Listing pages are outside Pagefind indexing.
- [ ] Write browser cases in `site/tests/src/pages/library/organization.test.ts`: transformer-topic links to real pilot sources; book chapter/resource navigation; React module → snapshot → source file; source archive and full tree remain reachable.
- [ ] Write mobile/keyboard/no-JS tests at 320/375/768/1280px, long titles, theme variants, visible focus and 44px controls; assert no page-wide overflow and breadcrumb row alignment. Run new tests red before markup changes.
- [ ] Implement pages through the facade only. Reader metadata exposes curated topic/collection links without replacing source breadcrumb or adjacency. Only the active collection group tree is included; unrelated project trees are absent from reader HTML.
- [ ] Run mirrored tests, targeted browsers and static/build gates; inspect real pilot screenshots and scoped Axe results. Main commits `feat(site): browse topics collections and learning paths` after independent UI review.

### Task 6: Learning/file search scopes and metadata filters

**Files:** Modify ReaderLayout, Search, `site/src/client/search.ts`, corresponding mirrored tests, and page search browser tests.

**Consumes:** Membership purpose/status plus topic/collection indexes. **Produces:** Pagefind `scope`, `topic`, `collection` filters without duplicate indexed readers. An eligible learning reader has scope values `learning` and `files`; all other public readers have only `files`. Topic filters include assigned topic IDs and deduplicated ancestors. Collection filter is its ID or absent.

- [ ] Write unit tests for the exact default `learning` scope, explicit `files` scope, section/kind compatibility, topic/collection selection and reset behavior. Changing filters resets result pagination and retains an intelligible empty state.
- [ ] Write actual generated Pagefind tests: a real React App/source entry is absent from learning and present in files; a pilot conceptual note is in both; supplemental/outline entries are files-only; drafts/exclusions are in neither. Listing pages are not indexed duplicates.
- [ ] Implement filter markup and existing-client integration using current pinned Pagefind API; verify its installed documentation/types locally rather than assuming multivalue filter syntax. Keep the development stale-index notice accurate.
- [ ] Build and run search tests red/green, actual production filter/browser checks, and static/build gates. Main commits `feat(search): prioritize learning material with explicit file scope` after review.

### Task 7: Full output and live development acceptance

**Files:** Modify `site/scripts/verify-output.ts`, `site/tests/scripts/verify-output.test.ts`, existing sitemap tests/route, and `site/tests/src/lib/catalog.browser.test.ts`; create focused acceptance fixture helpers/tests only as needed. Extend current actual-archive content integration assertions.

**Consumes:** Complete routes, curated snapshot and native Pagefind index. **Produces:** Enforced preservation/organization validation within existing build/verify gates.

- [ ] Add output assertions for every category/group route, canonical link, path step, UID resolution, draft exclusion, sitemap inclusion and listing search exclusion. Extend existing route ownership/fragment checks rather than building a second validator.
- [ ] Compare all baseline canonical routes and heading anchors: zero removals; compare all archive hashes and recorded dispositions. Report category counts and final output bytes/files against existing hard limits.
- [ ] Extend the actual npm-dev HTTP test with organization enrollment/edit/draft/invalid/recovery cases: new unclassified note works before enrollment; changing JSON updates without restart; stale-record deletion keeps the good snapshot and becomes 404 after repairing the record. Preserve/restore source fixtures and all four sidecars even on failure.
- [ ] Exercise rename via an explicit updated source mapping with preserved UID and preserved old reader route/alias; verify body generation is bound correctly. This is a temporary owned test fixture, not authorization to move originals.
- [ ] Preserve logs and use the existing serialized browser harness; run new targeted acceptance red/green. Investigate first real failures and reproduce causes; do not rerun repeatedly hoping green or increase budgets without measured evidence.
- [ ] Run full configured `npm run verify` from site with the pinned isolated Python environment and immutable SOURCE_REVISION; preserve the incoming SITE_URL/revision through sitemap tests. Main commits verified acceptance changes after independent review.

### Task 8: Authoring guide, final review and feature delivery

**Files:** Modify root README, `docs/deployment.md` only if its actual authoring/artifact instructions change, and `tasks/todo.md`. Modify both `CLAUDE.md` and `codex.md` identically only for durable new organization rules; keep AGENTS symlink intact. Reconcile the README's obsolete native-PDF sentence with the already shipped PDF.js behavior as a separate explicit documentation correction.

**Consumes:** Verified implementation and pilot audit. **Produces:** Operator/author instructions, exact coverage report and reviewed feature PRs, without deployment.

- [ ] Document adding an ordinary Markdown note versus enrolling/classifying it, exact JSON examples, dry-run review/apply, status semantics, collection/project grouping, search scopes, and broken-reference diagnostics. Explain the unclassified remainder and deferred editorial work.
- [ ] Check every documented command against actual package scripts/schema. Test the complete authoring example through a temporary fixture, with source/registry cleanup and no archive program execution.
- [ ] Compare each spec requirement against task evidence; independently review the entire branch and fix/re-review actual findings. Re-run appropriate checks after fixes; a changed formatter output also requires rechecking gates.
- [ ] Main commits documentation, pushes coherent feature branches and opens/updates PRs at verified milestones. Stacked PRs may be used without merging dependencies. Attach every created PR to the task.
- [ ] Refresh the port 4330 preview only from final reviewed output, preserving prior snapshot and validating PDF, tree, search and real pilots. Record immutable snapshot path, source revision and current CI state.
- [ ] Deliver links, actual test totals, classification coverage, remaining editorial scope, PR/CI status and limitations. Do not claim live hosting or physical-device testing without evidence. Do not merge or deploy.

## Verification commands and execution handoff

From absolute worktree `site/`, run targeted `npx vitest run <mirrored tests>` without the project-wide coverage floors, then the complete gates before committing a milestone. The complete gate remains:

```sh
npm run verify
```

Use Node 24.18.1, the existing isolated pinned Python environment, configured `SITE_URL`, immutable `SOURCE_REVISION`, serialized gates and port 4328 availability as documented in project steering. Tests and build must use matching environment values. Do not copy output while sitemap/browser rebuild tests are active. Do not change the existing verification order.

Self-review: all spec sections map to Tasks 1–8; shared identifiers/selectors are defined above; all five review-focus cases have owning tests. The plan intentionally excludes content rewriting and physical moves. Before execution, the user reviews this spec/plan and confirms they capture the desired scope; preserve their established subagent-driven method. Assign each implementer an explicit file list; forbid all Git/remote writes and destructive commands in every dispatch. Main audits out-of-scope diffs after each assignment, runs fresh serialized milestone verification, commits and completes independent review/fix loops before marking a task complete.
