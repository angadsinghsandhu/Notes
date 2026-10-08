# Notes Library project steering

## Placement and boundaries

- Keep archive material under Books, Classes, Courses, Interview, Languages and Tutorials. Website source, dependencies and its locked manifest live only in site/. Do not execute notebooks or course programs/dependencies.
- Content modules are independent of UI and CLI. UI consumes prepared data through site/src/lib/catalog.ts and imports content types only from its public barrel. CLI uses content's public barrel. Preserve existing layer checks.
- Mirror tests under site/tests/ at the source-relative path; Python test basenames must remain unique. Keep non-vendored source below approximately 500 lines. No speculative framework, dependency or abstraction.
- publication.json controls discovery/exclusions/overrides. Exclusions and drafts always win. Optional role:supplemental preserves access/search/source while omitting default learning-note browsing. Public resource actions need a valid public HTTPS source and immutable revision.

## Commands and checks

Run from site/ with Node 24.18.1; install with npm ci. Install full Chromium with npx playwright install --with-deps chromium, never --only-shell (native PDF tests require the viewer).

- npm run dev prepares content and owns the foreground Astro watcher/server. Use --ignore-lock for direct foreground Astro dev/preview commands; npm run dev already does so.
- npm run build prepares content, builds, generates Pagefind and validates output. npm run preview serves dist; development search uses the last production index and does not update with edits.
- After source/config edits, run mirrored tests and applicable npm run format:check, npm run lint, npm run check:boundaries, npm run typecheck and npm run build before considering the file complete. npm run check includes all static checks and coverage.
- Final npm run verify builds real fixtures first, runs the full static/unit/browser gate, then validates the final output read-only. Browser cleanup must restore incoming URL/revision configuration. Serialize stateful checks; browser preview owns 4328. Per-file statements/branches/functions/lines remain at least 90%; do not add ignores/skips or lower gates.
- Deployment uses only a verified artifact on configured trusted-master pushes. Do not provision, merge, release or publish without the user's explicit authorization. Preserve unrelated work; never use destructive Git commands to reset source.

## Hard-Won Lessons

- Use Polars for new Python tabular work and the explicitly approved 15-file archived conversion; preserve upstream provenance and teaching intent. Task 9 conversion remains separate from website hosting work.
- Select model-facing feature columns explicitly and preserve their names/order/types and target alignment during tabular conversions; incidental columns must not enter training inputs.
- Watcher startup/rearm/shutdown are awaited and serialized. Source acquisition uses 1-second polling, O(watched paths); keep the last successful snapshot after errors. Explicit development retains one previous asset publication; ordinary production removes stale assets.
- CLAUDE.md and codex.md stay byte-identical; AGENTS.md links to CLAUDE.md. Project rules and lessons belong here, not global steering.
- Isolated verification copies must keep mutable node_modules caches private; link only immutable packages, or physically clone the dependency tree.
