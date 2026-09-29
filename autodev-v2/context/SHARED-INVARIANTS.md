# Shared AutoDev Context Invariants

This summary is navigation context only. Normative authority remains in the cited
AutoDev source files and selected milestone snapshot entries.

## Workflow Boundary

- One approved AD milestone is the execution unit for `ralplan -> ralph`.
  Source: `autodev-v2/05-MILESTONE-PLAN.md`, `## Shared session contract`.
- Planning, architecture review, critic review, execution, verification, and
  handoff must share the same generated context snapshot. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, `CTX-AC3`.
- AD context isolation is repository maintenance. It is not completion of any
  roadmap AD milestone. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, planning boundary.

## Context Loading

- Ordinary AD work must start from the selected milestone snapshot, not the
  complete specification, full milestone plan, README, `.omx/` history, or a
  repository-wide read. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, `CTX-AC1`, `CTX-AC4`,
  and `CTX-AC5`.
- `context-map.json` is the machine-readable source of routing truth for AD
  context. Each milestone entry is explicit and fail-closed. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, architecture and data flow.
- Missing milestones, missing selectors, duplicate selectors, missing required
  predecessor evidence, and oversized snapshots are blockers. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, RALPLAN-DR principles.

## Expansion

- Missing information may be added only as an exact heading expansion with a
  reason. There is no whole-file or directory expansion option. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, `CTX-AC8`.
- Expansion changes the snapshot digest. A changed digest means prior consensus is
  stale until Architect and Critic review repeat. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, `CTX-AC9`.

## Safety And Authority

- Roadmap work does not authorize live mutation, credential changes, account
  changes, merge, force-push, destructive cleanup, or external messaging unless a
  selected milestone explicitly requires and authorizes it. Source:
  `autodev-v2/05-MILESTONE-PLAN.md`, `## Shared session contract`.
- Generated configuration cannot grant product authority. Human/operator
  approval remains content-bound and scoped. Source:
  `AutoDev_v2_Complete_Specification.md`, `### 3.3 Git and approval ceilings`.
- Unsupported or uncertain safety-relevant states fail closed rather than being
  coerced into readiness. Source:
  `AutoDev_v2_Complete_Specification.md`, `## 5. State model and exit contracts`.

## Evidence

- Verification must record changed files, commands and exit codes, acceptance
  evidence, effect audit, known limits, and next-session handoff. Source:
  `autodev-v2/05-MILESTONE-PLAN.md`, `## Shared session contract`.
- Fault IDs are selected explicitly per milestone. Ordinary context must not load
  the entire F01-F70 matrix. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, `CTX-AC6`.
- Direct predecessor evidence is selected and bounded. Missing required evidence
  is a positive fail-closed signal, not permission to fabricate evidence. Source:
  `.omx/plans/autodev-context-isolation-retrofit.md`, `CTX-AC7`.
