# AutoDev Context Isolation Retrofit

## Status

Repository maintenance task to complete **before continuing AD-03**.

This task is **not a new AD milestone** and must not mark AD-03 or any other roadmap milestone complete.

Use the existing `ralplan → ralph` workflow for implementation. The purpose of this task is to reduce the context fed into that workflow, not to replace or weaken it.

---

# 1. Objective

Refactor AutoDev's agent-facing documentation and startup flow so that an implementation session loads only the context required for the selected `AD-XX` milestone.

The target execution model is:

```text
selected AD milestone
        ↓
deterministic bounded context snapshot
        ↓
ralplan
  Planner
    ↓
  Architect
    ↓
  Critic
        ↓
approved plan
        ↓
ralph
        ↓
implementation + verification
```

Planner, Architect, Critic, and Ralph must operate from the **same digest-bound milestone context snapshot** instead of independently rediscovering the full repository documentation.

The existing quality gates remain unchanged.

---

# 2. Problem Being Fixed

The repository currently encourages coding agents to read broad project documentation before every milestone.

Examples include:

- `03-CODING-AGENT-START.md` requiring full reads of the main specification, evidence document, complete fault matrix, and contract reference.
- milestone files instructing agents to read `05-MILESTONE-PLAN.md` and the normative project specification.
- `README.md` presenting a read-everything startup sequence.
- `AutoDev_v2_Complete_Specification.md` duplicating most of the split specification.
- Ralplan subagents potentially inheriting this already-large context.

This causes the same roadmap-wide information to be repeatedly present in Planner, Architect, Critic, and Ralph contexts.

The fix must address **retrieval and context composition only**.

---

# 3. Non-Goals

Do not:

- remove or bypass `ralplan`;
- remove or bypass `ralph`;
- weaken Planner → Architect → Critic review;
- weaken milestone acceptance criteria;
- alter the AD-00 through AD-23 roadmap;
- redesign AutoDev runtime behavior;
- rewrite normative requirements for brevity;
- delete the complete specification;
- replace normative documents with generated summaries;
- modify tests or criteria merely to satisfy context-size limits;
- automatically truncate context when it exceeds the limit;
- silently fall back to reading the entire specification when context metadata is missing.

Context uncertainty must fail closed.

---

# 4. Target Architecture

Introduce three layers.

```text
AGENTS.md
   ↓
small permanent bootstrap instructions

context/context-map.json
   ↓
machine-readable routing for AD-XX

scripts/build_context.py
   ↓
extract exact required material

.omx/context/AD-XX-<digest>.md
   ↓
canonical context passed through ralplan → ralph
```

Normative documents remain authoritative.

The context system only decides **which parts are presented to the agent**.

---

# 5. Files to Add

Create:

```text
AGENTS.md

autodev-v2/AGENTS.md

autodev-v2/context/
    README.md
    SHARED-INVARIANTS.md
    context-map.json

autodev-v2/scripts/
    build_context.py

autodev-v2/tests/
    test_context_routing.py
```

Do not introduce a new runtime dependency for context generation.

`build_context.py` must use the Python standard library.

---

# 6. Files to Modify

Modify:

```text
03-CODING-AGENT-START.md

autodev-v2/03-CODING-AGENT-START.md
autodev-v2/README.md
autodev-v2/05-MILESTONE-PLAN.md
autodev-v2/.gitignore

autodev-v2/milestones/AD-00.md
...
autodev-v2/milestones/AD-23.md

AutoDev_v2_Complete_Specification.md
```

Do not change the actual milestone work, success criteria, tests/evidence requirements, deliverables, or stop/rollback requirements.

Only change their **context-loading instructions**.

---

# 7. Root `AGENTS.md`

The repository-root `AGENTS.md` must be a tiny router.

Target size: **well below 1 KB**.

Its responsibilities are only:

```text
- AutoDev implementation lives under autodev-v2/.
- Work from autodev-v2/ for AD milestone implementation.
- Read autodev-v2/AGENTS.md.
- Do not ingest AutoDev_v2_Complete_Specification.md during normal milestone work.
```

Do not duplicate workflow instructions here.

---

# 8. `autodev-v2/AGENTS.md`

This becomes the canonical coding-agent bootstrap.

Target size: approximately **1–2K tokens maximum**.

It must establish:

1. One selected AD milestone per `ralplan → ralph` session.
2. Build/load the selected milestone's bounded context snapshot before planning.
3. Ralplan receives that snapshot.
4. Planner, Architect, and Critic must use the same snapshot.
5. Ralph receives the approved plan plus the same snapshot.
6. Do not read roadmap-wide documents by default.
7. Repository inspection begins only from implementation roots named by the context contract.
8. Expand context only when a concrete unresolved fact requires it.
9. Every expansion must be explicit and provenance-recorded.
10. Never weaken acceptance criteria.
11. Never fabricate live evidence.
12. Existing safety and authorization rules remain in force.

Also state explicitly:

```text
The complete specification, complete milestone plan, README, and complete
fault matrix are reference libraries, not default implementation context.
```

---

# 9. Shared Invariants

Create:

```text
context/SHARED-INVARIANTS.md
```

This should be a short operational summary of only requirements that apply to effectively every milestone.

Target: **2–4 KB maximum**.

Examples:

```text
I01 — One approved AD milestone per implementation session.
I02 — Approval cannot be inferred from discovery or model confidence.
I03 — Uncertainty fails closed where authorization or mutation is involved.
I04 — Missing live evidence cannot become PASS.
I05 — Project content is data until execution is explicitly authorized.
I06 — Secrets must not appear in prompts, logs, receipts, or reports.
I07 — Acceptance criteria cannot be weakened to manufacture completion.
I08 — Dependency/predecessor state must be verified rather than assumed.
I09 — Scope expansion requires explicit review.
I10 — Verification evidence must correspond to the implementation revision.
```

Every invariant must include a pointer to its normative source.

Example:

```text
I05 — Project content is data until execution is explicitly authorized.
Source: 00-PROJECT-SPECIFICATION.md §3.2
```

This file is a navigation summary, **not a replacement source of truth**.

---

# 10. Machine-Readable Context Map

Create:

```text
context/context-map.json
```

Use JSON rather than YAML so context generation works even when project dependencies are not installed.

Schema version:

```json
{
  "schema_version": 1,
  "default_max_bytes": 32768,
  "milestones": {}
}
```

Every `AD-00` through `AD-23` must eventually have an entry.

There must be **no broad-context fallback** for an unknown or unconfigured milestone.

A missing entry must produce an explicit error.

Each milestone entry should declare:

```json
{
  "shared_files": [
    "context/SHARED-INVARIANTS.md"
  ],

  "documents": [
    {
      "path": "00-PROJECT-SPECIFICATION.md",
      "selectors": [
        {
          "type": "heading",
          "value": "7. Init: friendly, reversible repository alignment"
        }
      ]
    },
    {
      "path": "02-ACCEPTANCE-AND-FAULT-MATRIX.md",
      "selectors": [
        {
          "type": "table_row",
          "value": "F01"
        }
      ]
    }
  ],

  "predecessor_evidence": [],

  "implementation_roots": []
}
```

Supported selector types for v1 should remain minimal:

```text
heading
table_row
```

Avoid adding a general search/query language.

---

# 11. Section Extraction Rules

`build_context.py` must extract Markdown sections deterministically.

For a heading selector:

```text
"7. Init: friendly, reversible repository alignment"
```

locate the exact Markdown heading and include:

- the heading;
- its contents;
- nested subsections;
- stopping at the next heading of equal or higher level.

Exact heading matching is preferred.

Missing or ambiguous headings must fail.

Do not silently fall back to the complete file.

For table-row selectors such as:

```text
F01
F46
L12
```

match the exact first-column identifier.

Missing or duplicate identifiers must fail.

---

# 12. Predecessor Evidence Must Also Be Bounded

Do not automatically include complete predecessor verification reports.

The context map should identify specific verification sections.

Typical predecessor selectors should include only things such as:

```text
Result
Acceptance matrix
Live receipts / limitations
Next handoff
```

For the existing verification files, useful headings already include:

```text
AD-00:
- Result
- Acceptance matrix
- Live receipts
- Failures, limitations, and recovery
- Scope check and next handoff

AD-01:
- Result
- Acceptance matrix
- Live receipts and limitations
- Rollback and next handoff
```

Use direct predecessor evidence, not the complete history of all previous milestones.

If a required predecessor verification file does not exist, fail explicitly.

For example, an AD-03 context build must not pretend AD-02 evidence exists if `docs/verification/AD-02.md` is absent.

Do not compensate by scanning the repository for clues.

---

# 13. `build_context.py`

Implement:

```bash
python scripts/build_context.py AD-03
```

The command should:

1. Resolve repository root.
2. Load `context/context-map.json`.
3. Validate schema version.
4. Resolve the requested milestone.
5. Read `context/SHARED-INVARIANTS.md`.
6. Read the selected `milestones/AD-XX.md`.
7. Extract only configured document sections/rows.
8. Extract configured predecessor evidence.
9. Include implementation roots as navigation hints only.
10. Generate source digests.
11. Construct deterministic Markdown.
12. calculate the final snapshot SHA-256.
13. enforce the byte budget.
14. write:

```text
.omx/context/AD-XX-<digest-prefix>.md
```

Do not put timestamps in the generated content.

The same repository state + context map must produce byte-identical output.

---

# 14. Generated Snapshot Format

Use approximately:

```text
# AutoDev Milestone Context

Milestone: AD-03
Schema: 1
Context map digest: ...
Snapshot digest: ...

## Context Contract

Implementation roots:
- src/autodev/cli.py
- src/autodev/contracts/
- src/autodev/safety/
- tests/

## Shared Invariants

...

## Milestone

[contents of milestones/AD-03.md]

## Normative Context

### Source
00-PROJECT-SPECIFICATION.md
Selector: §7 ...
Source digest: ...

[extracted section]

...

## Applicable Fault Scenarios

F01 ...
F04 ...
...

## Predecessor Evidence

...

## Provenance

- path
- selector
- SHA-256
```

Do not copy unrelated document prose.

---

# 15. Context Budget

Default hard limit:

```text
32 KiB
```

Target:

```text
16–24 KiB
```

If generated context exceeds the limit:

```text
FAIL
```

Do not:

```text
truncate
summarize automatically
drop sources automatically
increase the limit automatically
```

The context contract must instead be refined deliberately.

---

# 16. Controlled Context Expansion

Agents must still be able to investigate genuinely missing information.

Support explicit bounded expansion.

Recommended interface:

```bash
python scripts/build_context.py AD-03 \
  --extra-heading "00-PROJECT-SPECIFICATION.md::4.2 Execution index, without a forced folder layout" \
  --reason "Required to resolve AD-03 authority-source ambiguity"
```

Requirements:

- `--reason` is mandatory whenever an extra selector is supplied.
- extra context must use an exact selector;
- no `--extra-whole-file` option;
- expansion produces a different snapshot digest;
- expansion metadata appears in the generated snapshot;
- size limit still applies.

If context expansion occurs **after Ralplan consensus approval**, the previous plan must be considered stale for execution.

The expanded snapshot must go back through the required Architect/Critic review before Ralph continues.

This preserves the quality guarantees of the existing workflow.

---

# 17. AD-03 Context Contract

AD-03 should be the first end-to-end test.

Its baseline context should include:

### Shared

```text
context/SHARED-INVARIANTS.md
milestones/AD-03.md
```

### Project Specification

Select only the relevant sections around:

```text
§3.2 Untrusted project content
§3.3 Git and approval ceilings
§4.1 Portable repository contract
§6 Command contracts
§7 Init: friendly, reversible repository alignment
```

Include the nested `Required algorithm` and `Hostile and unusual paths` content through normal heading extraction.

### Contract Reference

Select:

```text
A. PROJECT.yaml
```

Add another contract section only if AD-03 actually needs it.

### Fault Matrix

Exact rows:

```text
F01
F04
F05
F06
F09
F46
F67
```

These IDs already come from AD-03's milestone contract.

### Predecessors

Direct predecessors:

```text
AD-01
AD-02
```

Include only their bounded verification summary sections.

### Initial implementation roots

```text
src/autodev/cli.py
src/autodev/contracts/
src/autodev/safety/
tests/
templates/
```

Implementation roots are places to begin repository inspection.

Their contents are **not automatically injected into the context snapshot**.

---

# 18. Ralplan Integration Contract

Before invoking Ralplan:

```bash
python scripts/build_context.py AD-XX
```

The workflow invocation must identify the resulting snapshot as canonical milestone context.

Conceptually:

```text
Implement AD-XX only.

Canonical repository context:
.omx/context/AD-XX-<digest>.md

Use this snapshot as the shared repository context for Planner,
Architect, and Critic.

Do not independently ingest roadmap-wide documentation.

If required information is absent, perform explicit bounded context
expansion rather than broad repository-document ingestion.
```

Do not alter Ralplan's Planner → Architect → Critic sequence.

---

# 19. Plan Artifact Binding

Every generated:

```text
docs/plans/AD-XX-plan.md
```

must record:

```text
Context snapshot: .omx/context/AD-XX-<digest>.md
Context SHA-256: ...
Context map SHA-256: ...
```

The reviewed plan is therefore explicitly tied to the knowledge set that produced it.

If the snapshot changes, the plan's context binding becomes stale.

---

# 20. Ralph Integration Contract

Ralph receives:

```text
1. approved docs/plans/AD-XX-plan.md
2. exact context snapshot used by Ralplan
3. current Git state
4. implementation files selected by the approved plan
5. test/verification output generated during work
```

Ralph must not begin by rereading:

```text
00-PROJECT-SPECIFICATION.md
01-EVIDENCE-AND-DECISIONS.md
02-ACCEPTANCE-AND-FAULT-MATRIX.md
04-CONTRACT-REFERENCE.md
05-MILESTONE-PLAN.md
AutoDev_v2_Complete_Specification.md
```

unless an exact bounded expansion is required.

---

# 21. Fix `03-CODING-AGENT-START.md`

Both copies currently contain a broad mandatory reading list.

Replace that behavior.

The new startup contract should be approximately:

```text
Work from autodev-v2/.

Read AGENTS.md.

Select exactly one AD milestone.

Build its canonical bounded context snapshot using:
python scripts/build_context.py AD-XX

Run ralplan using that snapshot.

After consensus approval, run ralph using the approved plan and the
same context snapshot.

Do not ingest roadmap-wide documents unless an explicit bounded
context expansion is required.
```

Avoid maintaining two independent copies of detailed startup instructions.

Prefer making the root startup document a pointer into the canonical `autodev-v2/` bootstrap.

---

# 22. Fix Milestone Footers

All milestone files currently contain wording equivalent to:

```text
read the shared session contract in 05-MILESTONE-PLAN.md
and the normative project specification
```

Remove this requirement from all AD-00 through AD-23 files.

Replace it with:

```text
Before execution, load this milestone through the repository context
contract and its generated bounded context snapshot.

The complete roadmap and specification are reference libraries, not
default session context.
```

Do not change anything else in the milestone definitions.

---

# 23. Fix `05-MILESTONE-PLAN.md`

Preserve the statement that each AD milestone is one:

```text
ralplan → ralph
```

work unit.

Change the broad instruction:

```text
inspect the current repo, predecessor evidence, relevant sources...
```

to something equivalent to:

```text
Resolve normative sources and predecessor evidence through the selected
milestone's context contract.

Begin implementation inspection from the declared implementation roots.

Expand outside the bounded context only when a concrete unresolved
planning or verification question requires it.
```

`05-MILESTONE-PLAN.md` itself must no longer be mandatory per-session context.

---

# 24. Quarantine the Combined Specification

Keep:

```text
AutoDev_v2_Complete_Specification.md
```

but add an obvious top-level notice:

```text
AGENT CONTEXT POLICY

This is a combined archival/reference edition and intentionally
duplicates the split normative sources.

Do not load this file during ordinary AD milestone planning or
implementation.

Use it only for explicit cross-roadmap audits, release-wide consistency
checks, or direct human requests for the combined specification.
```

Do not modify the actual specification content.

---

# 25. README Split

Update `autodev-v2/README.md` to distinguish:

```text
Human documentation path
```

from:

```text
Coding-agent entrypoint
```

The coding-agent sequence should be:

```text
1. Read AGENTS.md.
2. Identify AD-XX.
3. Build its bounded context snapshot.
4. Run ralplan against the snapshot.
5. Run ralph against the approved plan + same snapshot.
```

Do not tell coding agents to follow the human read-everything sequence.

---

# 26. `.omx/` Hygiene

Update:

```text
autodev-v2/.gitignore
```

to include:

```gitignore
.omx/
__pycache__/
*.py[cod]
```

Generated context snapshots and workflow state are orchestration artifacts, not product documentation.

---

# 27. Backfill All Context Contracts

After AD-03 works end-to-end, populate `context-map.json` for:

```text
AD-00 through AD-23
```

Use this rule:

```text
milestone
+ shared invariants
+ exact relevant specification sections
+ exact applicable Fxx rows
+ relevant contract sections
+ bounded direct-predecessor evidence
+ implementation-root hints
```

Do not copy the entire contents of `05-MILESTONE-PLAN.md` into the map.

Do not select the complete specification.

Do not select all F01-F70 unless the milestone explicitly requires the entire matrix, such as the adversarial audit milestone.

AD-20 is expected to legitimately have a much larger context than AD-03.

Context budgets may be explicitly overridden per milestone only where the milestone itself inherently requires broad evidence.

Any override must be visible in `context-map.json`.

---

# 28. Tests

Implement `tests/test_context_routing.py`.

At minimum verify:

### Map integrity

- schema version is supported;
- AD-00 through AD-23 all exist;
- milestone files exist;
- referenced source files exist;
- headings exist exactly once;
- table-row IDs exist exactly once;
- predecessor references correspond to declared dependencies.

### Context boundaries

- normal milestone entries do not include `AutoDev_v2_Complete_Specification.md`;
- `05-MILESTONE-PLAN.md` is not injected as default context;
- README is not injected as default context;
- `.omx/` is never recursively inspected;
- context generation does not implicitly include directories.

### Determinism

Two runs against unchanged inputs produce identical bytes and identical digest.

### Budget

Every ordinary milestone context fits its declared limit.

Failure occurs instead of silent truncation.

### Failure behavior

Unknown milestone fails.

Missing section fails.

Ambiguous section fails.

Missing Fxx row fails.

Missing required predecessor verification fails.

Oversized context fails.

### Expansion behavior

Expansion without `--reason` fails.

Exact heading expansion succeeds.

Expansion changes the snapshot digest.

Expansion remains subject to the size limit.

---

# 29. Verification Commands

Run from:

```text
autodev-v2/
```

At minimum:

```bash
python scripts/build_context.py AD-00
python scripts/build_context.py AD-01

python -m unittest tests.test_context_routing -v

python -m unittest discover -s tests -p 'test_*.py'

python -m compileall -q src scripts tests

git diff --check
git status --short
```

Attempt:

```bash
python scripts/build_context.py AD-03
```

If AD-03 requires predecessor evidence that does not yet exist, the expected behavior is an explicit bounded failure identifying the missing predecessor.

That counts as evidence that the context router fails closed.

Do **not** fabricate the missing verification document merely to make the context builder succeed.

---

# 30. Pilot Verification

Before declaring the retrofit complete, perform one actual Ralplan planning pass using the new context system.

Preferred target:

```text
AD-03
```

Verify manually that:

- the initial agent context contains the bootstrap, not the complete specification;
- the generated snapshot is within the expected size;
- Planner uses the snapshot;
- Architect receives the same snapshot;
- Critic receives the same snapshot;
- no participant independently reads the complete specification;
- no participant automatically reads `05-MILESTONE-PLAN.md`;
- only selected Fxx rows are present;
- bounded source expansion still works when deliberately tested.

Do not start AD-03 implementation as part of this maintenance task unless separately authorized after the context retrofit is accepted.

---

# 31. Acceptance Criteria

The context isolation retrofit is complete when all of the following are true:

**CTX-AC1 — Bootstrap isolation**

A coding agent can identify and prepare an AD milestone without loading any roadmap-wide document.

**CTX-AC2 — Deterministic routing**

`build_context.py AD-XX` produces a deterministic digest-bound context snapshot from explicitly declared sources.

**CTX-AC3 — Shared consensus context**

Planner, Architect, Critic, and Ralph are instructed to use the same canonical snapshot.

**CTX-AC4 — No duplicate specification ingestion**

`AutoDev_v2_Complete_Specification.md` is never part of ordinary milestone context.

**CTX-AC5 — No roadmap-wide default**

`05-MILESTONE-PLAN.md` is not default session context.

**CTX-AC6 — Fault selection**

Ordinary milestones include only explicitly selected fault rows rather than F01-F70.

**CTX-AC7 — Bounded predecessor evidence**

Only direct, selected predecessor evidence is included.

**CTX-AC8 — Controlled expansion**

Missing information can be added through explicit bounded expansion with provenance and reason.

**CTX-AC9 — Consensus invalidation**

Changing the context snapshot after consensus invalidates the previous execution handoff until the required review is repeated.

**CTX-AC10 — Size enforcement**

Normal snapshots remain within the configured byte limit and oversized snapshots fail rather than silently truncating.

**CTX-AC11 — Complete roadmap coverage**

AD-00 through AD-23 have explicit context-map entries before the retrofit is considered fully complete.

**CTX-AC12 — Workflow preservation**

The existing `ralplan → ralph`, acceptance, testing, verification, authorization, and safety requirements remain unchanged.

---

# 32. Implementation Order

Execute in this order:

```text
1. Add root AGENTS.md.
2. Add autodev-v2/AGENTS.md.
3. Add SHARED-INVARIANTS.md.
4. Define context-map.json schema.
5. Implement build_context.py.
6. Implement AD-03 context mapping first.
7. Add context-routing tests.
8. Replace broad startup instructions.
9. Replace all milestone broad-read footers.
10. Update 05-MILESTONE-PLAN.md session wording.
11. Update README agent entrypoint.
12. Mark combined specification reference-only.
13. Ignore .omx/.
14. Verify deterministic AD-03 routing behavior.
15. Backfill AD-00 through AD-23 context maps.
16. Run complete regression suite.
17. Run one bounded Ralplan pilot.
18. Stop and report results.
```

Do not mix unrelated AutoDev feature implementation into this change.

---

# 33. Expected Result

After this retrofit, a normal future AD session should begin approximately like:

```text
User / supervisor:
Implement AD-07.

Agent:
read AGENTS.md

→ python scripts/build_context.py AD-07

Generated:
.omx/context/AD-07-a42d91c83e11.md
~20 KiB

→ ralplan using that snapshot

Planner
    ↓
Architect
    ↓
Critic

→ docs/plans/AD-07-plan.md
   bound to context digest

→ ralph
   approved plan
   + same context snapshot
   + selected implementation files
```

The workflow retains consensus planning and persistent verified execution while eliminating repeated ingestion of the complete AutoDev knowledge base.