# AutoDev Context Contract

This directory owns the bounded context contract for AD milestone work. A selected
milestone is routed through `context-map.json` and rendered by
`scripts/build_context.py` before `ralplan` or `ralph` work begins.

The contract is intentionally narrow:

- one selected `AD-XX` milestone per session;
- explicit source files and exact selectors only;
- no whole-roadmap fallback;
- no automatic truncation or summarization;
- SHA-256 provenance for every included source and selected excerpt;
- byte-budget failure before any misleading snapshot is written;
- controlled expansion only through exact headings plus a written reason.

Generated snapshots are written to `.omx/context/AD-XX-<digest>.md` from the
`autodev-v2/` directory. Planner, Architect, Critic, approved plan binding, and
Ralph must all use that same snapshot path, snapshot digest, and context-map
digest. If the context is expanded after consensus, the changed digest invalidates
the previous handoff until review repeats.
