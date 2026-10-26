# LeetCode 1–2000 Curriculum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver exactly 2000 deep, independently checked lessons, each with every meaningful approach tested and visualized.

**Architecture:** Original lesson prose and reviewed executable approaches live in strict per-problem content folders. The platform plan prepares these through the existing atomic content pipeline. Drafting, algorithm tests, deterministic traces and independent review precede verified publication; a manifest accounts for all targets at every stage.

**Tech Stack:** Markdown/strict JSON metadata, Python 3.12, SQL/shell for native domains, bounded local verification tools, shared TypeScript trace renderers, existing Astro publishing.

**Spec:** `docs/superpowers/specs/2026-10-24-leetcode-learning-library-design.md`. Platform dependencies/interfaces: `docs/superpowers/plans/2026-10-24-leetcode-learning-platform.md`.

## Global Constraints

- The target is frontend numbers 1–2000 inclusive, not the first 2000 files or internal IDs; do not count pending records as lessons.
- Preserve all original archive files and existing URLs; new canonical lessons may consolidate teaching without deleting source variants.
- Original self-contained statements/explanations, legitimately sourced constraints and company associations with dates. No paid-content bypass, invented frequency or undisclosed copied editorials.
- Every distinct approach has explanation, proof, commented implementation, complexity assumptions, tests and a checked curated visualization; time/memory tradeoffs are explicit.
- Traces stay within 2000 frames and 1 MiB per example; no silent truncation, custom-input editor or arbitrary execution.
- A verified lesson is independently reviewed and passes its actual code/trace/content tests. Planned/draft/verified are separate and auditable.
- Main alone makes Git/remote writes, stages exact files and creates focused feature PRs. No destructive Git, merges, provisioning or deployment. All unrelated partial work survives.
- Mirrored tests, source size limits and existing quality floors remain. Targeted batch checks during work; full repository gate once before final readiness of the delivered change, not per individual problem. Revalidate only when changed bytes invalidate evidence.

## Review Focus

1. A filename uses the wrong problem number/title: investigate actual function/statement and retain a mismatch record; never blindly overwrite identity (C1).
2. Two variants differ on duplicates/empty/mutation cases: small exhaustive tests and explicit contracts decide valid reuse, not a passing sample (C2/C3).
3. A claimed company association has no source/date or only a path name: omit the claim and show missing evidence (C1/C3).
4. A DP/recursive walkthrough reaches the correct final answer but shows impossible intermediate state: compare execution events/invariants frame by frame (C2/C3).
5. An unavailable premium/native-domain source leaves a gap: keep the target visibly pending and preserve the full denominator until legitimate evidence resolves it (C1/C3).

## File map and shared interfaces

- `site/content/leetcode/manifest.json`: schema v1, exactly 2000 identities and their source/readiness metadata.
- `site/content/leetcode/source-map.json`: each existing solution path/hash mapped to its reconciled canonical identity, variant and provenance; mismatches recorded explicitly.
- `site/content/leetcode/coverage-report.json`: deterministic sorted verified/draft/planned IDs, evidence hashes and unresolved reasons; no private user data/local absolute paths.
- `site/content/leetcode/problems/<number>/lesson.md`: original self-contained prose with stable section/approach anchors.
- `site/content/leetcode/problems/<number>/metadata.json`: typed metadata, approach records, reviewed references and example/code/trace paths.
- `site/content/leetcode/problems/<number>/solutions.py` (or `.sql`/`.sh`): reviewed implementations; separate focused modules when the size cap requires it; never import original sample-print scripts.
- `site/content/leetcode/problems/<number>/examples.json`: named curated input/output cases and known boundaries. Trace files under `traces/<approach-id>/<example-id>.json` are deterministic committed authoring outputs validated against implementation hashes, not mutable site build output.
- `site/content/leetcode/paths/all-problems.json`: editorial full-coverage DAG with 2000 distinct referenced targets, coherent stages and explicit prerequisite edges. Named 150/250/company subsets remain future curated content.
- Tests mirror source under `site/tests/content/leetcode/problems/<number>/test_problem_<number>_solutions.py`; every basename is unique across the test tree. SQL/shell cases run through the curriculum harness with domain adapters and mirrored TypeScript/Python tool tests; no database/network service outside isolated local fixtures.

Platform contracts: strict `CurriculumDefinition`, canonical `ProblemId`, `validateTrace`, implementation hashes, bounded `curriculum.py check --ids ...` and source-preserving snapshot from platform Tasks 1/3/4. Keep fields/signatures identical across the two plans; no ad hoc parallel metadata schema.

## Task C1: Reconcile originals and account for every target

**Files:** Manifest, source map, coverage report, all-problems path; platform schema test fixtures only if needed for real records. Create no fabricated 2000 lesson bodies.

**Interfaces:** Consumes original source hashes and platform Task 1 contracts. Produces 2000 stable identity records, exact source mapping and evidence-qualified metadata; unresolved data remains explicitly pending. Company evidence absence does not invent a company or prevent an otherwise complete lesson if unknown is shown honestly.

- [ ] Inventory current Python/native files and all duplicate variants, read actual content for identity reconciliation, preserve path/hash for every original. Use the earlier 360/250/240/79 filename counts only as a comparison, not as truth if the worktree changed.
- [ ] Add failing schema/inventory assertions: `set(numbers) == set(range(1, 2001))`, no duplicate IDs, official slug/title/source evidence agreement, source hashes unchanged, duplicate variants all accounted for and outside-range originals retained without counting toward coverage.
- [ ] Research official accessible problem identity/title/domain/difficulty/constraints with provenance; record unavailable fields as unknown/pending. No full copyrighted statement scraping or guessed company data. Reconcile real SQL/shell problems explicitly.
- [ ] Build an editorial full-target path grouped by prerequisites/patterns, then validate DAG/order/unique target coverage. If a topic is unknown, place it in a visible pending-classification stage, not a false technique. Pending targets never masquerade as lessons.
- [ ] Run strict schema/source mapping checks and scoped format/static gates. Independently inspect mismatch cases/evidence, machine-check all entries, commit `content: inventory LeetCode targets and preserve source variants`.

## Task C2: Prove the lesson standard on eight problems

**Files:** Exact problem folders for 1, 3, 20, 64, 98, 127, 146, 175; mirrored implementation tests; manifest/path/coverage updates. Prototype UI mockups may be updated in ignored brainstorming space only, never copied into product source.

**Interfaces:** Depends on C1 and platform Tasks 1–5; produces actual data fixtures for platform Tasks 6–12. Before UI implementation, revise the mockup to show official links, sourced/unknown companies, studied controls, tree and player controls; collect visual feedback in the existing brainstorming context without treating it as production acceptance.

- [ ] For each target, read every mapped original and authoritative question evidence. Write original statement, complete input/output/constraints/examples, recognition cues, derivation, useful approach progression, proof, complexity/mutation/stack assumptions and mistakes. Keep any unsupported information explicitly pending.
- [ ] Write failing tests BEFORE the new solution implementations, using the exact problem contract: #1 duplicate values/distinct indices; #3 repeated-character window shrink; #20 mismatched/unfinished stack; #64 single row/column, all zeros and input mutation distinction; #98 ancestor-boundary violations and duplicate keys; #127 unreachable/shortest-distance rules; #146 eviction order, overwrite and capacity; #175 absent addresses/NULL and multiple matches. Match official valid-input domains rather than inventing APIs.
- [ ] Run selected tests red for the intended absence/incorrect behavior, then implement meaningful distinct approaches. Tree #98 includes iterative/recursive strategies; #64 includes brute force, top-down matrix memoization, bottom-up table and rolling row, with an explicitly mutating in-place alternative if retained as a distinct teaching approach.
- [ ] Check code against independent exhaustive/differential small-input oracles and known cases. SQL semantics use the specified dialect or document a verified compatible local engine; a SQLite pass alone cannot prove a MySQL-specific feature.
- [ ] Instrument each tested approach and curate examples that show its essential transition, not just happy-path output. Verify implementation hash, result, every transition/invariant, code-line references and transcript. If a trace is oversized choose a smaller complete example; preserve failed evidence.
- [ ] Add source-checked official links and only evidenced companies. No fabricated badges to make the mockup look complete. Annotate known unverified original variants without silently replacing their archive bytes.
- [ ] Run `python3 -B scripts/curriculum.py check --ids 1,3,20,64,98,127,146,175`, strict metadata/trace checks and targeted real browser player/lesson cases. Run scoped format/lint/type checks on authored executable content via the real configured gate.
- [ ] Fresh independent algorithm/teaching/trace review checks all approaches and examples, not only text formatting. Resolve/review every finding, then promote each passing target to verified with source/evidence hashes and update coverage counters.
- [ ] Main commits reviewed coherent pilot groups and creates/attaches a feature PR. Platform pilot success is recorded as 8/2000, never complete curriculum. If one pilot needs substitution, record why and preserve coverage obligations for the original.

## Task C3: Complete the remaining library through explicit coverage waves

**Files:** Same per-problem pattern as C2 for each selected batch; only the corresponding manifest/source-map/path/coverage records. Software fixes are separate focused changes with a regression and review, never hidden among thousands of editorial lines.

**Batch registry:** Generate checked-in `site/content/leetcode/batches.json` from the 2000-ID manifest after the pilot. Define exactly 40 coverage waves, `wave-01` through `wave-40`, covering numeric intervals 1–50, 51–100, …, 1951–2000 respectively. Within a wave, prerequisite order may differ from numeric order; reviewed content is split into independently reviewable sub-batches of at most five problems. Pilot IDs are already verified, not re-authored or double-counted. Numerical waves are accountability units, not the user's learning order.

- [ ] Create a reproducible registry validator: all target IDs occur in exactly one wave; union is 1..2000; intervals match; verified pilot IDs remain covered; evidence records contain exact file hashes and no unresolved lesson is marked complete.
- [ ] Open a checklist for the current wave in the ignored execution ledger and `tasks/todo.md`; list its exact still-unverified IDs, evidence gaps and at-most-five-ID sub-batches before dispatch. Do not dispatch a generic “write the rest” agent or simultaneous writers of the shared manifest.
- [ ] For each sub-batch, follow C2's source research → failing behavioral tests → minimal implementations → independent oracle → prose/proof → instrumented curated traces → strict checks → independent review/fix loop. Every approach has its own visualization, including brute-force approaches on suitably small inputs. Native shell uses isolated fixture files; no host filesystem scripts or archive imports.
- [ ] Run `python3 -B scripts/curriculum.py check --ids <explicit-comma-separated-IDs>` and affected schema/path/browser checks. Track results by exact problem and approach, not an aggregate test count. Source-state revalidation catches accidental original edits.
- [ ] Commit each reviewed sub-batch, open/update focused feature PRs at coherent feature points and retain public status/coverage honesty. A wave completes only when all 50 targets are verified. Do not skip evidence-limited/paid targets silently; record the required legitimate input and continue independent targets while seeking it.
- [ ] After each wave, regenerate exact sorted coverage/provenance report and validate path membership/denominators. Review balance of explanations and real algorithm diversity; template headings alone are not evidence of deep teaching.
- [ ] Repeat the explicit sub-batch checklist for all 40 waves. Final curriculum completion requires `verifiedIds == [1, 2, ..., 2000]`, no unresolved blocking source/correctness/trace/review evidence and all original sources preserved. Do not claim this from a 2000-entry manifest alone.

## Final curriculum acceptance

- [ ] Freeze the final content hashes, source map, trace versions and review ledger; independently audit the complete coverage report, edge/native domains and representative intermediate-state correctness across algorithm families. Prior per-lesson reviews are required evidence, not replaced by sampling.
- [ ] Run all published curriculum implementations/traces in bounded batches, final path/route/source-preservation checks, then the single complete serialized repository gate for the release-candidate change. Preserve logs/timeouts; fix actual causes before claiming green.
- [ ] Report exact content coverage, code/trace/review results, company evidence gaps that are honestly unknown, actual CI status and unverified live deployment constraints. Main updates/attaches PRs; no merge or deployment.

## Self-review

This plan explicitly owns all 2000 content targets, not only the pilot. Identity/provenance/gaps belong to C1; deep per-approach teaching/tests/traces and pilot proof to C2; scalable exact coverage and completion to C3. Five Review Focus cases are covered by named checks. Software, private accounts, path rendering and deployment readiness remain in the companion platform plan rather than being duplicated here. User approved both implementation plans on 2026-10-25; execution uses the established subagent-driven method.
