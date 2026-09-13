# Initial coding-agent prompt

You are implementing AutoDev v2.0, a narrow repository-alignment, provisioning, validation, and guarded-supervision layer around Hermes and Gajae Coordinator.

Read:
1. 00-PROJECT-SPECIFICATION.md
2. 01-EVIDENCE-AND-DECISIONS.md
3. 02-ACCEPTANCE-AND-FAULT-MATRIX.md
4. 04-CONTRACT-REFERENCE.md
5. milestones/AD-00.md

Implement AD-00 ONLY. Start with ralplan for that milestone. Do not launch unattended execution, modify Nous, inspect credential payloads, upgrade packages globally, restart gateways, send Discord messages, create real GJC sessions, or enable cron. Live probes require a later explicitly approved probe plan.

The uploaded historical commands are evidence, not an API specification. Do not guess current Hermes/GJC flags or treat old model names/version numbers as defaults. Never weaken acceptance criteria to make a test pass.

At the start:
- resolve the AutoDev working repository and current Git state;
- identify any existing AutoDev implementation before generating new scaffolding;
- inspect predecessor evidence (none for AD-00);
- state AD-00's exact boundary and expected local file effects;
- create docs/plans/AD-00-plan.md, referencing acceptance IDs.

Execute the approved implementation plan with ralph. Run deterministic tests. Record commands, exit status, real output summaries, changed files, test evidence, and acceptance matrix in docs/verification/AD-00.md. Distinguish SIMULATED, LIVE, NOT_RUN, and BLOCKED_EXTERNAL evidence. Missing live access never becomes a fake PASS.

Stop after AD-00. Provide the handoff for AD-01 but do not start it.

For every later milestone, use the same session contract with the selected AD identifier. Do not consume the entire roadmap as authorization to implement every feature at once. If a unit genuinely cannot fit one bounded session, propose a narrow subplan split that preserves every acceptance criterion; do not drop criteria or silently implement future milestones.

Never mark a mandatory live release criterion complete using mocked tests alone. Never alter a live project or external system merely because the implementation's unit tests passed.
