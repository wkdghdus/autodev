# Initial coding-agent prompt

You are implementing AutoDev v2.0, a narrow repository-alignment, provisioning, validation, and guarded-supervision layer around Hermes and Gajae Coordinator.

Enter `autodev-v2/` and follow its `AGENTS.md` as the canonical coding-agent bootstrap. Select **AD-00 only** for this initial session. From that directory, run `python scripts/build_context.py AD-00`, read the generated bounded snapshot, and start `ralplan` with that same snapshot for Planner, Architect, and Critic. Bind the approved `docs/plans/AD-00-plan.md` to it using the exact fields `Context snapshot`, `Context SHA-256`, and `Context map SHA-256`. Verify those bindings before `ralph`. Do not begin if the context builder fails closed.

Resolve the working repository and Git state, identify any existing AutoDev implementation before scaffolding, confirm AD-00 has no predecessor evidence, and state its exact boundary and expected local effects. Reference its acceptance IDs in the plan. Execute the approved plan with `ralph`, run deterministic tests, and record commands, exit status, real output summaries, changed files, effects, and acceptance evidence in `docs/verification/AD-00.md`. Distinguish `SIMULATED`, `LIVE`, `NOT_RUN`, and `BLOCKED_EXTERNAL`; missing live access never becomes a fake PASS.

Stop after AD-00 and hand off AD-01 without starting it. For later milestones, select one AD identifier and repeat the same snapshot-bound session contract. If a unit cannot fit one bounded session, propose narrow reviewed subplans that preserve every criterion.

Do not launch unattended execution, modify Nous, inspect credential payloads, upgrade packages globally, restart gateways, send Discord messages, create real GJC sessions, or enable cron. Live probes require a later explicitly approved probe plan. Uploaded historical commands are evidence, not current Hermes/GJC API contracts; do not guess flags, model names, or version defaults. Never weaken acceptance criteria, count mocks as mandatory live proof, or alter a live project merely because unit tests passed.
