# LeetCode 1–2000 interactive learning library

Status: design proposal; requires user approval before implementation planning.
Date: 2026-10-24 (America/Los_Angeles).

## Intent and agreed scope

Extend the existing Notes Astro site into a complete, public, self-contained study library for LeetCode frontend problem numbers 1 through 2000, inclusive. The user wants deep teaching, not brief revision notes: the question, meaningful solution approaches ordered from brute force toward more efficient techniques, detailed comments, and a visualization for every distinct approach.

Every lesson links to its official LeetCode question and shows sourced company associations where evidence exists. Reusable learning-path trees recommend an order and later support sets such as LeetCode 150, a specified 250 set, and Uber/Meta preparation. The same lesson can appear in multiple paths. Private progress syncs across phone and computer for the owner's account only. Completed means studied the lesson, not accepted a submission.

The user chose to extend this site, keep all hosted infrastructure on Cloudflare, and initially use only curated animation examples. The design must allow custom inputs later without implementing an input editor now.

## Existing system and preservation

- Astro static output, TypeScript content preparation, sanitized source readers, Pagefind, source-folder navigation and PDF.js already exist. Preserve their safety and publishing contracts.
- Initial filename inventory: 360 Python files, 250 distinct numbered problems, 240 within 1–2000; 79 numbers have duplicate files. This is a filename inventory, not proof of correct identity, correctness or lesson completeness.
- Existing code is shown as an archive resource, not a structured lesson. For example #64 contains an in-place solution, comments and a sample call but no complete lesson.
- Physical source archive paths, existing resource URLs, persistent document UIDs, downloads and original bytes remain intact. Consolidation maps variants to one new canonical lesson; it does not delete or silently rewrite originals.
- A separate organization refactor is partially uncommitted on codex/notes-organization-reader. Preserve it. Implementation must reconcile its reviewed public catalog, membership/path interfaces and route claims before integrating; never assume unreviewed partial files are a stable release.
- Do not execute existing archived scripts on import. Extract/review selected algorithms into a dedicated, isolated curriculum test harness.

## Goals, non-goals and anti-goals

Goals: all 2000 identities accounted for; deep verified lessons; transparent content status; executable, checked approaches and traces; accessible reading and playback; truthful progress; useful curated paths; ordinary Git-based editing; local operation and Cloudflare deployment readiness.

Not in this release: arbitrary user-code execution, browser Python interpreters, custom input UI, public signup, social features, submission scraping, automatic LeetCode-account sync, AI chat, gamification, payments, exhaustive enumeration of every syntactic solution, or automatic company-frequency rankings.

Failures even if the UI works: claiming 2000 finished lessons when most are placeholders; generic filler repeated across questions; invented companies/constraints/proofs; animations contradicting executable solutions; inaccessible animation-only teaching; exposing owner progress; breaking original routes; weakening the existing verification gates.

## Approaches considered and selected

1. Extend Astro with structured lesson content and small interactive visualization components. Reuse readers, themes, routes, deployment and content preparation; add a Cloudflare Worker and D1 for progress. Selected by the user. Most integration effort, least duplicated product surface.
2. Separate learning application. Independent curriculum UI and release cycle, but duplicated navigation, search, styling and publishing; rejected in favor of extending the site.

For hosted progress, Cloudflare Pages + Supabase was suggested as the lower-custom-auth option; the user chose all Cloudflare instead. Use Pages for public static content, Workers for authenticated API and D1 for private progress. Cloudflare Access email one-time PIN is the proposed owner authentication choice, not an explicitly selected identity provider. The owner can approve it with this document.

This is a curriculum project plus supporting software, delivered through a representative pilot then reviewed batches. A pilot is a quality gate, not a replacement for the full 2000-problem goal. No promise that automatic generation alone produces verified teaching.

## Lesson identity and authoring

One immutable identity `leetcode:<frontend-number>` per problem. Do not confuse frontend numbers with internal LeetCode IDs. A checked-in manifest must enumerate exactly 1–2000 without gaps or duplicates, record official slug/URL, title, difficulty, domain, topics, source evidence and readiness. Problems outside that range remain accessible in the archive and are not counted toward the target.

Canonical proposed routes: `/practice/leetcode/`, `/practice/leetcode/<number>/`, `/practice/paths/`, `/practice/paths/<id>/`. Numeric lesson routes survive title changes. Claim routes in the existing publication collision validator; make source resource pages link to the corresponding lesson. Never replace the source page with a silent redirect.

Store curriculum material under `site/content/leetcode/`: versioned manifest and per-problem directories with strict metadata, Markdown lesson prose, Python/native-language implementations, curated examples, expected results and trace definitions. Exact subdivisions/schema names are builder decisions. Reuse the current Markdown/sanitization/highlighting pipeline; no arbitrary executable MDX in prose. Build artifacts and absolute local paths are not committed as content.

Each lesson contains:

1. Number/title, difficulty, topics, official question link, evidenced companies and content review status.
2. Original, self-contained statement, input/output contract, checked constraints, explained examples and relevant follow-ups. No bulk copied proprietary editorials or paid metadata; links and source records retain provenance. Unknown or restricted information remains visibly pending rather than fabricated. Authoring uses legitimately accessible sources or materials the user can supply.
3. Prerequisites, recognition cues, reasoning that derives the state/invariant, and a progression of distinct approaches.
4. For every approach: when to use it, steps, correctness argument, annotated executable code, exact time/auxiliary-space analysis, recursion/mutation assumptions, walkthrough visualization and pitfalls.
5. Comparison table: partial tradeoffs, not an unsupported universal ranking. Ties, memory-versus-time and mutation-versus-preservation are explained.
6. Tests, boundary cases, common wrong ideas, related problems and learning-path placement.

Python is the default algorithm language. Proposed coverage rule for non-algorithm questions within 1–2000: SQL questions include tested SQL; shell questions include tested shell, rather than pretending a Python analog satisfies the original question. An optional Python analogy must be explicitly labeled. This is an assistant proposal requiring user approval with the design.

“All solution types” means pedagogically distinct, justified approaches. Do not pad lessons with cosmetic rewrites. Include iterative and recursive tree approaches where meaningful and a top-down matrix formulation for applicable two-dimensional DP. Do not publish a deliberately wrong approach as a valid solution; use labeled counterexamples instead.

## Companies and question provenance

Store company associations as evidence-bearing records: company ID/name, source URL or user-supplied source reference, source type, observation date and any documented reporting period. Display “reported by source,” not certainty that a company will ask it. Do not invent frequency/counts, treat old reports as current, or use path inclusion as proof of a company report. Show “No verified company information recorded” when absent.

Company-preparation paths can be author-curated recommendations independent of reported company associations. Label this distinction. Do not scrape paywalled lists or publish unsupported premium claims. Restricted statements do not justify defeating access controls. Record unavailable evidence and request authorized input if needed; a pending record is not a complete lesson.

## Visualization architecture and behavior

Each approach has at least one curated example with deterministic playback, tied to its exact implementation version. Prefer several small examples covering the approach's important behavior. Exponential approaches use genuinely small complete inputs; if a demonstration truncates, label truncation and never imply the truncated result is the solution.

Architecture: curated input → approach-specific instrumented execution → normalized bounded trace → reusable visual renderer + textual step explanation. Share primitives for arrays/pointers, grids/tables, trees/graphs, stacks/queues/heaps and recursion/call trees. Do not build a universal algorithm simulator or a separate renderer for every problem.

Each frame records stable step ID, code-line reference, human explanation, relevant state and highlights; all data is serializable and validated. Frames or deterministic events can be generated during preparation in a bounded test environment. Never execute submitted code or imported archive modules in the browser. Python output/trace fixtures must be checked against the tested implementation; a hand-authored TypeScript animation is not accepted as equivalent merely because the final answer matches.

Controls: play/pause, forward/back one step, reset, speed and curated-example selection. Pause when changing approach/example, leaving the visible player or hiding the document; clean up timers. No autoplay by default. Support keyboard and touch, reduced motion, color-independent state labels and a complete static transcript. Live-region announcements are user-controlled or limited to manual steps, not a stream at playback speed. Use HTML/SVG first; canvas only with an equivalent semantic view.

Initial guardrail proposal: maximum 2000 trace frames and 1 MiB uncompressed trace per example, enforced with useful diagnostics. Split or replace an oversized example; never silently truncate. Load only the current lesson's selected visualization on demand, preferably on explicit activation; text remains readable before loading. No full-corpus traces in the initial bundle.

Keep input schema validation, execution/trace generation and rendering separate. This enables a future bounded, validated custom-input feature without adding arbitrary execution capability or generic plugin machinery today.

## Library, lesson and path UI

Keep existing themes and source navigation. Provide number/title search, topic/pattern, difficulty and company filters, clear empty states and URL-addressable filter state. Reuse Pagefind for lesson text rather than downloading all lesson bodies. Exclude listing pages from duplicate full-text results; add canonical lesson scope/metadata without removing source-search access.

Lesson layout: readable long-form content, section navigation, official link/company evidence near the title, comparison table, per-approach visualization next to the corresponding explanation/code, source links and private “Mark studied” control. On narrow screens use a compact section menu, stacked panels and contained horizontal scrolling for code/tables. Do not compress a wide flowchart into unreadable text.

Learning paths are a versioned directed acyclic graph, presented as an expandable tree/forest plus accessible ordered outline. Nodes represent stages/groups and references to canonical problems; prerequisite edges are explicit. A problem may appear under multiple branches and paths. Validate IDs/references, detect cycles, check ordering and provide deterministic next recommendations. Prerequisites advise; they do not lock lessons.

Start with a clearly named editorial route covering all 2000 identities, divided into coherent topic stages. Planned lessons can appear visibly pending; next-ready recommendations skip unavailable lessons. Exactly one manifest identity per number; path appearances never inflate counts. The UI distinguishes unique target coverage from ready, verified lessons.

Support future named subsets without implementing their editorial lists now. “LeetCode 150” and “250” are ambiguous titles until an exact source/membership is chosen: do not silently equate them with NeetCode 150 or invent an official 250. Uber/Meta paths likewise need explicit editorial membership and dated evidence where company claims are made. Launching these named subsets is deferred; the shared path capability is in scope.

Path counters count distinct problem IDs and the owner's studied state once. Show studied/available lessons and unavailable targets separately. Full target completion requires all required lessons, not only the currently published pilot. Switching paths never resets progress.

## Progress and synchronization

Required state is `not-started` or `studied`, reversible by the owner, keyed by canonical problem ID. Record server timestamps and the lesson revision studied; a later lesson update shows “updated since studied” without silently clearing completion. No inferred completion from scroll, video playback or elapsed time. Extra learning/review states, personal notes and accepted-submission tracking were suggested but not requested; defer them.

Anonymous visitors read all lessons. Only the configured owner signs in and reads/writes progress. No signup, browser-accessible D1 credentials or personal progress in static HTML/Pagefind/build logs. Owner identity/allowed email is runtime configuration, never public metadata.

Prefer a Worker mounted on `/api/progress/*` and `/account/*` on the same custom site hostname, protected by an Access application scoped only to those paths. Access email OTP allow policy restricts the exact owner email; requiring OTP alone must not allow all emails. The Worker independently verifies the Access JWT signature, issuer, intended audience, expiry and permitted owner identity using supported maintained tooling; reject direct-origin/header-spoof attempts. Disable or equivalently protect alternate workers.dev/preview ingress. A custom Cloudflare-controlled hostname and owner email are deployment prerequisites to supply later, not values to invent or provision now. Localhost/pages.dev do not prove the production Access topology.

Explicit sign-in opens protected `/account/` using a safe relative return route. Once authenticated, same-origin credentialed API calls read/write progress. Handle expired Access redirects/HTML as sign-in-needed, never parse them as successful JSON. Preserve the lesson and pending action through sign-in; require user confirmation to apply any pending change afterward. If the final deployment cannot use this same-origin topology, resolve the design before substituting cross-origin cookies/CORS.

Worker API exposes authenticated bootstrap/read and bounded per-problem writes. Unknown IDs, invalid types, excess bodies, unsupported methods and unapproved origins fail. Use prepared SQL bindings, exact Origin/CSRF protections for mutations, JSON responses, no-store private caching and no permissive CORS. D1 row includes owner key, problem ID, studied boolean, studied revision/time, updated time and monotonically increasing version; a unique owner/problem key prevents duplicates.

Conflict policy: compare-and-swap with expected version. Two devices editing the same problem yield a visible conflict and fresh server state; no silent last-writer overwrite or client-clock ordering. Retry with the same state is safe/idempotent. Different problems sync independently. Refetch on sign-in, focus and successful writes. Cloudflare/D1 read consistency must be proven in implementation rather than assumed; use supported primary/session behavior as necessary. Do not claim immediate realtime updates between idle devices.

Offline: public lessons remain readable if already loaded; marking studied reports unsaved while offline. Initial release has no persistent offline write queue. No false green “synced” badge. Failed/conflicted writes retain the user's intent in the live view and offer retry. Sign-out clears in-memory owner state and uses Access logout; no personal state in service-worker/public caches.

Export owner's progress as versioned JSON through the authenticated API for portability/recovery. Initial release need not support bulk import. Keep migrations versioned, test rollback/recovery procedures against local data, and document backup/export before remote schema changes.

## Editorial rollout and verification

Inventory every existing file by actual problem identity, provenance, variant and quality; filename collisions/misnumbering need reconciliation before reuse. Deduplicate teaching at the new canonical lesson level while preserving all originals.

Pilot proposal: #1, #3, #20, #64, #98, #127, #146 and #175. These exercise arrays/hash maps, sliding window, stack, multiple DP formulations, trees, graph search, mutable data structures and SQL. Include real recursion and a memory tradeoff; shell joins the first expansion batch. Pilot final selection is a builder call if actual input evidence requires substitutions.

Workflow per lesson: source validation → original draft → executable approach tests → trace/implementation parity → independent teaching/correctness review → publish as verified. Track `planned`, `draft`, `verified`, with precise outstanding reasons. Publicly readable drafts are prominently marked and do not count as complete; invalid content never publishes. All required per-approach code, proof, tests and visualization must pass before verified status. Unbounded naive approaches get small-input tests and explicit complexity warnings.

Use known examples, boundary cases, deterministic exhaustive/differential checks on small domains, reference oracles where justified and mutation/structure tests. Verify constraints/assumptions, numerical overflow distinctions where relevant, SQL NULL/duplicates/order semantics, and shell input handling. Do not represent local checks as official LeetCode accepted submissions.

Content authoring and trace generation are offline editorial actions committed to the repo, not live LLM calls or cloud jobs. New tests execute only reviewed bounded curriculum implementations in a local harness with timeout/resource limits, no network and temporary data; never run entire archived course code.

After pilot validation, expand by coherent, reviewable topic batches toward complete 1–2000 coverage. Every batch updates a reproducible coverage report with exact ready/pending IDs and evidence. No fixed delivery date or inference that 2000 deep lessons can be completed by scaffolding 2000 pages. Full completion means every target meets the same content/code/trace/review standard, including evidence-limited targets resolved legitimately.

Software acceptance includes preserved source hashes/routes/anchors and PDF rendering; lesson/path/schema/collision validation; no duplicate canonical indexing; responsive keyboard/no-JS reading; reduced motion; deterministic playback/backtracking; stale/expired authentication; forged identity; wrong owner; CSRF; cross-device races; D1 local migrations and private-cache exclusion. Test public reading with the API unavailable.

Use targeted tests/static checks while editing. Preserve all existing coverage floors and boundaries; extend them to Worker code and content validation rather than bypassing them. Run the complete serialized repository gate once after the change and final-review fixes, immediately before final PR readiness; repeat only when material overlap/fixes invalidate evidence. Editorial batch checks must be incremental by affected lessons so checking the library stays practical at 2000.

## Hosting, local operation and delivery boundaries

Retain existing Cloudflare Pages Direct Upload/GitHub Actions verified artifact flow for static output. Worker/D1 schema and Access configuration are separate reviewed deliverables; a successful static deploy does not imply private sync works. Cloudflare-only hosting does not promise all usage fits a free allowance; check current quotas and actual artifact/trace sizes before deployment, without automatically choosing paid capacity.

Local site continues to start with the existing workflow; a separate Wrangler local Worker + local D1 and restricted development-only identity fixture enable integration tests. The fixture must be impossible to enable on a production host; unknown/missing production auth configuration fails closed. Static preview works without credentials, showing sync unavailable. Never use remote D1 as a local test database.

Deploy instructions must inventory actual domain/account, allowlisted email, Access team/audience, Worker route and database binding without putting secrets in Git or public artifacts. Owner supplies these at deployment time. Establish access restrictions before enabling writes. Actual provisioning, remote migrations, deployment or merges remain separately authorized actions.

Implementation plan follows approval. It must explicitly resolve the currently unfinished organization refactor dependency, preserve all uncommitted work, use focused commits and feature PRs, and distinguish curriculum progress from platform completion. The browser mockup under `.superpowers/brainstorm/3771-1792887339/` is throwaway design material, not production code or proof of correctness. Update it to show companies, official link, path tree, progress and playback before implementing UI.

## Builder decisions and approval points

Already selected by user: extend the site; Cloudflare-only infrastructure; 1–2000 complete deep lessons; all distinct approaches visualized; curated inputs initially; future custom-input compatibility; single-owner synchronized studied progress; official links/company information; reusable learning-path trees.

Assistant proposals for approval: Access email OTP, binary studied progress, same-origin custom-domain auth topology, immutable numeric routes, staged verified publishing, evidence-only company tags, native SQL/shell where required, named subset membership deferred, explicit offline unsaved behavior and optimistic concurrency conflicts. Exact module boundaries, trace compression, small renderer choices and batching mechanics remain builder decisions under these contracts.

## Primary references checked

- [Cloudflare Access OTP](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/) and [Access policies](https://developers.cloudflare.com/cloudflare-one/access-controls/policies/): email-code login and restrictive allow policy.
- [Access JWT validation](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/): validate identity at the application boundary.
- [D1 bindings](https://developers.cloudflare.com/d1/worker-api/), [local development](https://developers.cloudflare.com/d1/best-practices/local-development/) and [migrations](https://developers.cloudflare.com/d1/reference/migrations/): Worker database integration and local verification.
- [LeetCode #175](https://leetcode.com/problems/combine-two-tables/description/): illustrates that the first 2000 include SQL questions, not exclusively Python algorithm exercises.

References establish capability and scope; no deployment, free-tier capacity, company list or full content verification has been performed during design.
