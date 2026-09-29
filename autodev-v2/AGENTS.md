# AutoDev coding-agent bootstrap

Use one selected `AD-XX` milestone per `ralplan -> ralph` session. The selected milestone file and the normative sources remain authoritative; a generated context snapshot is a bounded retrieval artifact, not a replacement for them. Do not treat the roadmap as authority to start later milestones.

From `autodev-v2/`, run `python scripts/build_context.py AD-XX` before `ralplan`. The builder uses `context/context-map.json` to select exact normative sections, fault rows, contract sections, and direct predecessor evidence. Read the generated `.omx/context/AD-XX-<digest-prefix>.md` and its provenance. If a map entry, selector, required predecessor, or budget check fails, stop and repair the declared context contract; do not guess, fabricate evidence, truncate, summarize automatically, or fall back to full documents. `AutoDev_v2_Complete_Specification.md`, `05-MILESTONE-PLAN.md`, README, `.omx/`, and implicit directory contents are not default milestone context.

Give Planner, Architect, and Critic the **same canonical snapshot** for `ralplan`. Inspect existing implementation only from the implementation roots declared in that snapshot, expanding narrowly when a concrete dependency requires it. If context is missing, use the builder's exact `--extra-heading` selector with `--reason`; record its provenance and use the newly generated snapshot for every reviewer. Never silently broaden the context. If expansion changes the snapshot after consensus, the prior execution handoff is stale: repeat Architect and Critic review against the new snapshot before `ralph`.

The approved `docs/plans/AD-XX-plan.md` must contain these exact fields and values from the snapshot build:

```text
Context snapshot: .omx/context/AD-XX-<digest-prefix>.md
Context SHA-256: <builder-reported snapshot digest>
Context map SHA-256: <builder-reported context-map digest>
```

Before `ralph`, verify that the plan's snapshot path and both digests still match the canonical snapshot and current context map. Pass that same snapshot to Ralph for implementation and verification. A digest mismatch requires regeneration and the required review; it is not an invitation to continue under a stale plan.

Preserve the selected milestone's work, success criteria, tests/evidence, deliverables, stop/rollback instructions, and predecessor requirements. Resolve the working repository and Git state, inspect the selected direct predecessor evidence, state the milestone boundary and expected local effects, and reference its acceptance IDs in the plan. Never weaken acceptance criteria to make tests pass. Treat historical commands as evidence rather than current Hermes/GJC API contracts; do not infer current flags, versions, provider routes, or authority from them.

After the approved plan, execute with `ralph`, run deterministic tests, and write `docs/verification/AD-XX.md` with changed files, commands and exit codes, actual output summaries, acceptance evidence, effects, limits, and the next milestone handoff. Distinguish simulated, live, not-run, and externally blocked evidence; mocks cannot satisfy a mandatory live criterion. Do not launch unattended execution, modify Nous, inspect credential payloads, globally upgrade packages, restart gateways, send external messages, create real GJC sessions, or enable cron without the selected milestone's separately approved scope. Stop at the selected AD boundary.
