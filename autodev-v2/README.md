# AutoDev v2.0 implementation handoff

An upgraded specification based on three Nous bottleneck reports. This package contains requirements, work units, test cases and safe configuration examples, not an implementation or installed Hermes skill.

## Human reference documents

The source library remains available for human review: `00-PROJECT-SPECIFICATION.md` defines architecture and guardrails; `01-EVIDENCE-AND-DECISIONS.md` records incident traceability and decisions; `02-ACCEPTANCE-AND-FAULT-MATRIX.md` records 70 failure/acceptance scenarios; `04-CONTRACT-REFERENCE.md` defines contracts; and `05-MILESTONE-PLAN.md` describes the full roadmap. Individual handoffs are in `milestones/`.

## Coding-agent entrypoint

Follow `AGENTS.md` in this directory. Select one `AD-XX` milestone, run `python scripts/build_context.py AD-XX`, and use its generated bounded snapshot through `ralplan` and `ralph`. The snapshot resolves the selected normative sections, fault rows, contracts, and direct predecessor evidence with provenance. The full roadmap and combined specification are reference documents, not default coding-agent context. `03-CODING-AGENT-START.md` is the initial AD-00 prompt.

## Delivery scope

24 bounded milestone handoffs, 70 fault/acceptance scenarios, source mapping, contract definitions, and draft templates. No live environment was probed or changed while preparing this package. No milestone implementation is claimed complete.

## Milestones

| ID | Bounded work unit |
|---|---|
| AD-00 | Baseline, scope lock, and evidence inventory |
| AD-01 | Schemas, identities, authority, and orthogonal states |
| AD-02 | Safe storage, command execution, locks, and journals |
| AD-03 | Friendly init and conservative artifact discovery |
| AD-04 | Execution-index compiler and approval binding |
| AD-05 | Native capability and runtime compatibility adapters |
| AD-06 | Credential metadata and effective billing-route audit |
| AD-07 | Resource admission and shared-account budgets |
| AD-08 | Hermes profile, skill installation, and deterministic environments |
| AD-09 | MCP configuration and actual-tool-access probe |
| AD-10 | Managed-worktree and broker lifecycle probes |
| AD-11 | Multi-source execution reconciliation |
| AD-12 | Guarded dispatch, idempotency, and fencing |
| AD-13 | Generic supervisor and bounded cycle |
| AD-14 | Independent verification and revision applicability |
| AD-15 | Doctor, active validation ladder, and admission receipts |
| AD-16 | Idempotent onboarding and reviewed remediation |
| AD-17 | Actual gateway environment and delivery proof |
| AD-18 | Paused canary, guarded cron, and explicit enablement |
| AD-19 | Disable, restart reconciliation, and safe recovery |
| AD-20 | Adversarial acceptance and enforcement audit |
| AD-21 | Nous shadow parity and controlled migration plan |
| AD-22 | Independent second-project pilot |
| AD-23 | Release, operator runbooks, and evidence freeze |

## Template caution

Templates are proposed AutoDev schemas, not ready-to-write native Hermes/GJC configuration. They deliberately contain unresolved/draft values and cannot authorize unattended work. The coding agent must implement validation and reviewed migration before applying them.
