# AutoDev

## Hermes Project Onboarding and Autonomous Supervision Platform

**Status:** Implementation specification
**Version:** 1.1
**Primary execution model:** `ralplan → ralph` per milestone
**Reference project:** Nous
**CLI name:** `autodev`

---

# 1. Product Objective

AutoDev standardizes the process of turning a software repository into an autonomously supervised Hermes + Gajae project.

The existing Nous pipeline proves the desired architecture:

```text
Human
  ↓
Approved requirements / roadmap
  ↓
Hermes project supervisor
  ↓
Gajae Coordinator
  ↓
Claude / Codex
  ↓
Isolated implementation work
  ↓
Verification
  ↓
Next approved milestone
```

The problem is that onboarding Nous required substantial manual setup:

* Hermes profile creation
* Hermes model configuration
* repository working-directory configuration
* Gajae Coordinator MCP setup
* repository root permissions
* supervisor skill installation
* cron configuration
* notification configuration
* project control-file setup
* roadmap interpretation
* verification of the complete Hermes → Gajae chain

That process must not be repeated manually for every project.

AutoDev will turn that setup into a reusable, safe, deterministic provisioning workflow.

The intended user experience is:

```bash
cd ~/Projects/example-project

autodev init .
autodev onboard .
autodev preflight .
autodev enable .
```

After this, the project has its own isolated Hermes supervisor capable of autonomously advancing an approved roadmap through Gajae.

---

# 2. Product Philosophy

AutoDev is **not another agent framework**.

Do not build:

* a custom agent runtime
* a custom daemon
* a custom task database
* a custom worktree manager
* a replacement for Hermes
* a replacement for Gajae
* a replacement for Git
* a web dashboard
* LangGraph workflows
* CrewAI workflows
* a custom planning system
* another autonomous product manager

Use existing systems for their intended purposes.

```text
Hermes
= persistent runtime / scheduler / supervisor

Gajae
= engineering execution harness

Claude / Codex
= coding workers

Git
= repository history

Repository roadmap
= project state / approved work

AutoDev
= repository alignment + configuration + provisioning + validation
```

The implementation should remain deliberately small.

---

# 3. Core Design Principle

Separate **supervision algorithm**, **project configuration**, **machine configuration**, and **runtime state**.

## Generic behavior

Stored in:

```text
roadmap-project-supervisor
```

The supervisor knows:

* how to inspect project state
* how to inspect Gajae
* how to choose approved work
* how to dispatch work
* how to verify completion
* how to handle repairable failures
* when to escalate
* what it is forbidden from doing

It does not know anything about Nous specifically.

## Project-specific configuration

Stored in:

```text
.agent/PROJECT.yaml
```

The project contract tells AutoDev and the supervisor:

* project identity
* authoritative requirements
* roadmap location
* plan locations
* verification expectations
* authority boundaries
* optional project-specific verification commands

## Machine-specific state

Stored outside repositories:

```text
~/.hermes/autodev/projects.yaml
```

This records:

* absolute repository path
* Hermes profile
* enabled/disabled state
* provisioning metadata

## Runtime execution state

Remains owned by:

```text
Gajae
+
repository
+
Hermes cron
```

Do not create another mutable execution-state database for V1.

---

# 4. Repository Alignment Model

A new concept is introduced:

```text
autodev init
```

`init` is responsible for bringing a repository into the **expected AutoDev project shape** before infrastructure is provisioned.

It answers:

> Is this repository structurally ready to be understood by AutoDev, and if not, can AutoDev safely configure the missing pieces?

`init` is repository-local.

It must not:

* create Hermes profiles
* modify Gajae configuration
* configure MCP
* create cron jobs
* enable autonomous execution
* mutate GitHub
* start coding sessions

Its job is only:

```text
inspect repository
→ discover existing project artifacts
→ preserve valid configuration
→ create missing AutoDev control files
→ configure deterministic values
→ request or expose unresolved decisions
→ validate resulting structure
```

---

# 5. Repository Control Plane

Every AutoDev-managed repository must have:

```text
.agent/
└── PROJECT.yaml
```

`PROJECT.yaml` is the only universally mandatory AutoDev-owned repository file in V1.

Other artifacts such as:

* requirements
* roadmap
* milestone plans
* acceptance criteria
* test specifications

may already exist elsewhere in the project.

AutoDev should point to existing authoritative artifacts rather than forcing duplicate AutoDev-specific copies.

For example, all of these may be valid:

```text
README.md
docs/PRD.md
docs/ROADMAP.md
.omx/ROADMAP.yaml
.omx/plans/
spec/
planning/
```

The repository does **not** have to reorganize itself around AutoDev.

AutoDev adapts its project contract to the repository where safe.

---

# 6. `autodev init` Philosophy

`init` must be friendly, conservative, and idempotent.

The principle is:

```text
discover first
→ preserve existing truth
→ configure deterministic values
→ ask only when necessary
→ never fabricate approval or product intent
```

## Existing valid file

If:

```text
.agent/PROJECT.yaml
```

already exists and validates:

```text
✓ preserve it
✓ inspect referenced sources
✓ report missing downstream requirements
✓ do not rewrite it unnecessarily
```

## Existing partially valid file

If deterministic repairs are possible without changing product meaning:

```text
✓ offer/apply surgical repairs
```

Examples:

* normalize project slug
* add missing `schema_version`
* add newly required safe default field
* fill project name from existing repository metadata if unambiguous

Do not silently alter:

* requirements authority
* roadmap authority
* autonomous permissions
* acceptance criteria policy
* merge authority
* product scope

## Invalid existing file

If repair would require guessing product or authority semantics:

```text
do not overwrite
```

Instead:

* identify the exact invalid field
* explain the expected form
* propose a corrected value when safe
* preserve the original file
* stop with `NEEDS_INPUT`

## Missing file

If `PROJECT.yaml` does not exist:

```text
create .agent/
create .agent/PROJECT.yaml
```

Populate only values AutoDev can determine safely.

---

# 7. `init` Discovery

Before creating configuration, inspect the repository for likely authoritative artifacts.

## Project identity

Possible evidence:

* Git repository directory name
* Git remote repository name
* package metadata
* `pyproject.toml`
* `package.json`
* README title

Choose automatically only when evidence is unambiguous.

---

## Requirements candidates

Search for likely artifacts such as:

```text
PRD.md
REQUIREMENTS.md
requirements.md
docs/PRD.md
docs/requirements.md
*_requirements*.md
product-spec*.md
specification*.md
```

Do not treat every README as an approved product specification automatically.

A README may be surfaced as a candidate.

---

## Roadmap candidates

Look for:

```text
ROADMAP.md
ROADMAP.yaml
ROADMAP.yml
.omx/ROADMAP.yaml
.omx/plans/
docs/ROADMAP.md
docs/roadmap.md
planning/
plans/
```

Do not infer approval purely from a filename.

`init` only discovers/configures possible locations.

Approval remains a preflight/supervisor concern.

---

## Verification candidates

Inspect common project files for test infrastructure:

```text
pyproject.toml
pytest.ini
package.json
Makefile
Cargo.toml
go.mod
Gemfile
```

AutoDev may suggest likely verification commands.

It must not silently add arbitrary shell commands to trusted autonomous execution configuration unless confidence is high and behavior is conventional.

---

# 8. Interactive and Non-Interactive Init

## Interactive mode

When running in an interactive terminal:

```bash
autodev init .
```

AutoDev may ask a small number of focused questions when multiple valid choices exist.

Example:

```text
AutoDev found two possible roadmap sources:

1. .omx/ROADMAP.yaml
2. docs/ROADMAP.md

Which should be authoritative?
> 1
```

Or:

```text
No approved requirements source was detected.

Would you like to:
1. select an existing file
2. create a placeholder path for later
3. leave requirements unconfigured

> 2
```

Avoid long configuration wizards.

Use detected defaults whenever safe.

---

## Non-interactive mode

Support:

```bash
autodev init . --yes
```

or equivalent non-interactive behavior.

When ambiguity exists:

```text
do not guess
```

Generate the safe configuration that can be determined and mark unresolved values clearly.

Result:

```text
NEEDS_INPUT
```

rather than pretending the project is ready.

---

## Dry-run

Support:

```bash
autodev init . --dry-run
```

Show:

* files detected
* files that would be created
* fields that would be populated
* unresolved questions
* resulting alignment state

Do not mutate the repository.

---

# 9. Init Result Model

`init` should end in one of:

```text
ALIGNED
NEEDS_INPUT
ERROR
```

## ALIGNED

The repository has a valid AutoDev project contract.

This does **not** mean it is ready for autonomous execution.

Example:

```text
PROJECT.yaml valid
but no approved roadmap exists
```

can still be:

```text
INIT: ALIGNED
PREFLIGHT: NOT_READY
```

This distinction is important.

---

## NEEDS_INPUT

Repository structure is partially configured, but user input is required to determine project semantics safely.

Examples:

* two competing roadmap sources
* no known requirements source
* existing invalid authority setting
* conflicting project identity

---

## ERROR

Initialization could not safely continue.

Examples:

* not a Git repository
* repository root inaccessible
* permission failure
* malformed file that cannot be parsed safely
* filesystem write failure

---

# 10. Init Expected UX

Example fresh project:

```text
$ autodev init .

AutoDev Project Initialization

Repository
✓ Git repository detected
✓ Root: /Users/example/Projects/marketmove
✓ Project name: MarketMove
✓ Project slug: marketmove

Existing project artifacts
✓ Requirements candidate: docs/PRD.md
✓ Roadmap candidate: .omx/ROADMAP.yaml
✓ Plans directory: .omx/plans
✓ Python test environment detected

AutoDev configuration
+ Creating .agent/
+ Creating .agent/PROJECT.yaml

Configured
✓ requirements → docs/PRD.md
✓ roadmap → .omx/ROADMAP.yaml
✓ plans → .omx/plans
✓ execution harness → gajae
✓ safe authority defaults

Not configured automatically
! Verification command requires confirmation

Result: NEEDS_INPUT

Next:
Review .agent/PROJECT.yaml and run:

    autodev init .
```

After confirmation:

```text
$ autodev init .

✓ PROJECT.yaml valid
✓ Requirements configured
✓ Roadmap configured
✓ Verification configured
✓ Authority policy valid

Result: ALIGNED

Next:

    autodev preflight .
```

---

# 11. Init Idempotency

Repeated execution must be safe:

```bash
autodev init .
autodev init .
autodev init .
```

must not:

* duplicate files
* reorder configuration unnecessarily
* replace user comments without reason
* reset user choices
* weaken authority policy
* overwrite existing paths
* generate duplicate roadmaps
* generate duplicate requirements files

If the repository is already aligned:

```text
✓ Project already aligned.
No changes required.
```

---

# 12. Primary Product Success Condition

AutoDev V1 is successful when a second properly structured project can be aligned and onboarded without manually editing Hermes or Gajae configuration.

The workflow must support:

```bash
autodev init /path/to/project
autodev onboard /path/to/project
autodev preflight /path/to/project
autodev enable /path/to/project
```

and result in:

```text
✓ valid project contract
✓ existing project artifacts reused
✓ dedicated Hermes profile
✓ generic supervisor installed
✓ working directory restricted to project
✓ Gajae Coordinator configured
✓ Gajae root restricted to project
✓ project registered
✓ roadmap discoverable
✓ execution/verification contract discoverable
✓ supervisor dry-run passes
✓ cron supervision enabled
```

The existing Nous project and second test project must both use the same generic supervisor implementation.

---

# 13. Global Definition of Done

AutoDev V1 is complete only when all of the following are true.

## Functional

The following work as documented:

```text
autodev init
autodev onboard
autodev preflight
autodev enable
autodev disable
autodev status
autodev list
```

## Repository alignment

A new repository can be brought into the expected AutoDev project structure without manually authoring boilerplate.

## Preservation

Existing valid project artifacts are reused.

AutoDev does not unnecessarily rewrite the repository.

## Reusability

No Nous-specific product logic exists in the generic supervisor.

Adding a project does not require copying and editing the supervisor skill.

## Isolation

Each project receives a dedicated Hermes profile.

Each Gajae configuration is restricted to that project's exact repository root.

## Safety

`init` does not provision infrastructure.

`onboard` does not enable unattended execution.

`enable` fails when preflight is not green.

The system fails closed when authority or project configuration is ambiguous.

## Idempotency

Repeated:

```bash
autodev init .
autodev onboard .
autodev enable .
```

must not produce duplicate state.

## Recovery

Partial provisioning failure must be detectable and safely retryable.

## Verification

Automated tests cover deterministic AutoDev logic.

Real integration smoke tests prove:

```text
AutoDev
→ Hermes
→ Gajae Coordinator
```

works.

## Reference compatibility

Nous can operate through the generic supervisor without losing the safety properties of its current dedicated supervisor.

---

# 14. V1 Non-Goals

Do not implement:

* web UI
* custom daemon
* custom runtime database
* autonomous product planning
* automatic merge
* multi-project Hermes super-profile
* secrets manager
* self-modifying supervisor
* support for arbitrary coding harnesses
* automatic rewriting of a project's requirements
* automatic generation of approved product decisions

A repository without sufficient approved work remains:

```text
NOT_READY
```

AutoDev must not fix that by inventing work.

---

# 15. Recommended Implementation Stack

Prefer:

```text
Python 3.11+
```

Keep dependencies minimal.

Suggested:

```text
PyYAML
jsonschema
pytest
```

Prefer Python standard library for:

* CLI parsing
* subprocess invocation
* filesystem operations
* path resolution
* JSON
* temporary files
* hashing
* locking
* atomic replacement

---

# 16. Repository Layout

Target:

```text
hermes-autodev/
│
├── README.md
├── pyproject.toml
│
├── autodev/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   │
│   ├── config/
│   │   ├── project.py
│   │   ├── registry.py
│   │   └── schema.py
│   │
│   ├── discovery/
│   │   ├── project_identity.py
│   │   ├── requirements.py
│   │   ├── roadmap.py
│   │   └── verification.py
│   │
│   ├── commands/
│   │   ├── init.py
│   │   ├── onboard.py
│   │   ├── preflight.py
│   │   ├── enable.py
│   │   ├── disable.py
│   │   ├── status.py
│   │   └── list_projects.py
│   │
│   ├── integrations/
│   │   ├── hermes.py
│   │   ├── gajae.py
│   │   └── git.py
│   │
│   ├── provisioning/
│   │   ├── hermes.py
│   │   ├── gajae.py
│   │   ├── supervisor.py
│   │   └── cron.py
│   │
│   ├── preflight/
│   │   ├── checks.py
│   │   ├── result.py
│   │   └── runner.py
│   │
│   └── util/
│       ├── command.py
│       ├── filesystem.py
│       ├── locking.py
│       └── output.py
│
├── supervisor/
│   └── roadmap-project-supervisor/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── references/
│           ├── project-contract.md
│           ├── roadmap-discovery.md
│           ├── gajae-coordinator.md
│           ├── authority-policy.md
│           └── report-contract.md
│
├── schemas/
│   └── project.schema.json
│
├── templates/
│   └── PROJECT.yaml
│
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

# 17. PROJECT.yaml Contract

Initial shape:

```yaml
schema_version: 1

project:
  slug: nous
  name: Nous

sources:
  requirements:
    - nous_requirements_and_user_flows.md

  roadmap:
    path: .omx/ROADMAP.yaml

  plans:
    - .omx/plans

execution:
  harness: gajae

verification:
  require_tests: true
  require_acceptance_criteria: true
  require_fresh_evidence: true
  commands: []

authority:
  implementation: autonomous
  repair: autonomous

  commit: autonomous
  push_branch: autonomous
  create_pr: autonomous

  merge: human
  modify_approved_plan: human
  modify_requirements: human

  weaken_acceptance_criteria: never
```

`PROJECT.yaml` remains portable.

Never store:

* credentials
* absolute machine paths
* Gajae session IDs
* current milestone state
* Hermes profile paths
* cron IDs
* machine usernames
* mutable execution state

inside it.

---

# 18. Machine Registry

Default:

```text
~/.hermes/autodev/projects.yaml
```

Example:

```yaml
schema_version: 1

projects:

  nous:
    repo: /Users/example/Projects/nous
    profile: nous-supervisor
    enabled: true

  marketmove:
    repo: /Users/example/Projects/marketmove
    profile: marketmove-supervisor
    enabled: false
```

---

# 19. CLI Contract

## Init

```bash
autodev init [PATH]
```

Responsibilities:

```text
resolve repo
→ inspect existing artifacts
→ inspect PROJECT.yaml
→ discover candidate requirements/roadmap/plans/tests
→ create missing AutoDev control plane
→ populate deterministic configuration
→ preserve existing user configuration
→ surface ambiguity
→ validate result
```

Must not provision infrastructure.

Options should include:

```text
--dry-run
--yes
--json
```

Do not add `--force` unless a later verified need exists.

---

## Onboard

```bash
autodev onboard [PATH]
```

Responsibilities:

```text
run/reconcile init
→ require valid project contract
→ register project
→ create Hermes profile
→ install supervisor
→ configure project cwd
→ configure Gajae Coordinator
→ configure exact allowed root
→ run smoke checks
→ run preflight
→ run supervisor dry-run when safe
```

It must not enable autonomous cron.

If initialization reaches:

```text
NEEDS_INPUT
```

onboarding stops before infrastructure mutation and tells the user to complete:

```bash
autodev init .
```

---

## Preflight

```bash
autodev preflight [PROJECT_OR_PATH]
```

Optional:

```bash
autodev preflight . --json
```

Read-only readiness evaluation.

---

## Enable

```bash
autodev enable [PROJECT_OR_PATH]
```

Flow:

```text
full preflight
→ require READY
→ verify dry-run
→ provision exactly one cron
→ mark enabled
```

---

## Disable

```bash
autodev disable [PROJECT_OR_PATH]
```

Stops autonomous wake/supervision but preserves project configuration.

---

## Status

```bash
autodev status [PROJECT_OR_PATH]
```

Returns:

```text
project
profile
repo
enabled
init/alignment state
preflight state
cron state
Gajae reachability
active execution summary
supervisor state
```

---

## List

```bash
autodev list
```

Example:

```text
PROJECT       PROFILE                 AUTONOMY    HEALTH
Nous          nous-supervisor         enabled     healthy
MarketMove    marketmove-supervisor   disabled    ready
ProjectX      projectx-supervisor     disabled    not-ready
```

---

# 20. Standard Ralph Session Contract

Every milestone below is a separate bounded execution.

```text
ralplan
→ inspect specification/current repository
→ produce implementation plan
→ consensus if required
→ ralph
→ implement current milestone only
→ test
→ repair
→ produce evidence
→ stop
```

Ralph must not automatically begin the next milestone.

Every milestone concludes with:

1. files changed
2. implementation summary
3. tests executed
4. results
5. acceptance criteria matrix
6. known limitations
7. confirmation future milestones were not implemented

---

# 21. Milestone Dependency Graph

```text
M0  Golden Baseline + Scaffold
 │
 ▼
M1  Project Contract + Schema
 │
 ▼
M2  Project Init / Repository Alignment
 │
 ▼
M3  Generic Supervisor
 │
 ▼
M4  Nous Compatibility / Parity
 │
 ▼
M5  Preflight Engine
 │
 ├─────────────┐
 ▼             ▼
M6 Hermes      M7 Gajae
Provisioning   Provisioning
 │             │
 └──────┬──────┘
        ▼
M8  Onboarding Orchestrator
        │
        ▼
M9  Enable / Disable / Cron
        │
        ▼
M10 Registry / Status UX
        │
        ▼
M11 Reliability + Security Hardening
        │
        ▼
M12 Second-Project Pilot
        │
        ▼
M13 Release / Documentation
```

---

# M0 - Golden Baseline and Repository Scaffold

## Objective

Create the AutoDev repository foundation and capture the existing working Nous pipeline as a safe golden reference.

## Required work

* create Python package
* create test structure
* make `python -m autodev --help` work
* capture non-secret Nous architecture
* capture representative supervisor states:

  * READY
  * EXECUTING
  * VERIFYING
  * HUMAN_BLOCKED
  * COMPLETE

## Out of scope

No Nous mutations.

No Hermes/Gajae provisioning.

No cron.

## Success criteria

* [ ] package is importable
* [ ] CLI help works
* [ ] tests run
* [ ] baseline contains no secrets
* [ ] live Nous remains untouched

---

# M1 - Project Contract and Schema

## Objective

Implement the versioned `PROJECT.yaml` contract and deterministic validation model.

## Required work

Create:

```text
schemas/project.schema.json
templates/PROJECT.yaml
```

Implement:

* YAML loading
* schema validation
* unsupported-version rejection
* repository-root resolution
* safe repository-relative path validation
* structured project model

## Tests

Cover:

* valid contract
* malformed YAML
* missing fields
* unsupported version
* invalid authority
* path traversal
* symlink escape
* unknown harness

## Success criteria

* [ ] valid contract loads deterministically
* [ ] invalid contracts fail closed
* [ ] errors identify exact fields
* [ ] repository-relative paths cannot escape root
* [ ] template validates against schema
* [ ] safe authority defaults exist

---

# M2 - Project Init and Repository Alignment

## Objective

Implement:

```bash
autodev init [PATH]
```

as the safe repository-alignment layer.

This milestone must not provision Hermes, Gajae, MCP, cron, or autonomous execution.

---

## Required Work

### 1. Git repository inspection

Resolve exact repository root.

Fail safely if target is not a Git repository.

---

### 2. Existing AutoDev configuration detection

Check:

```text
.agent/PROJECT.yaml
```

Classify:

```text
MISSING
VALID
REPAIRABLE
INVALID
```

---

### 3. Artifact discovery

Implement repository-local discovery for:

#### Requirements

Find likely:

```text
PRD
requirements
product specifications
```

#### Roadmap

Find likely:

```text
ROADMAP.*
.omx/ROADMAP.*
planning directories
```

#### Plans

Find likely planning directories such as:

```text
.omx/plans
plans
planning
specs
```

#### Verification

Inspect common build/test configuration.

Do not execute tests during discovery unless required by a future explicit mode.

---

### 4. Confidence model

Discovery should distinguish:

```text
EXACT
HIGH_CONFIDENCE
AMBIGUOUS
NONE
```

Do not automatically choose an `AMBIGUOUS` source.

---

### 5. Friendly interactive configuration

When TTY is available, ask only questions necessary to resolve ambiguity.

Example:

```text
Two roadmap candidates found:

1. .omx/ROADMAP.yaml
2. docs/ROADMAP.md

Select authoritative roadmap:
> 1
```

Use strong defaults where evidence is unambiguous.

---

### 6. Non-interactive behavior

Support:

```bash
autodev init . --yes
```

Do not guess ambiguous product semantics.

Create deterministic configuration and return:

```text
NEEDS_INPUT
```

for unresolved decisions.

---

### 7. Dry-run

Support:

```bash
autodev init . --dry-run
```

Display intended file/config changes without mutation.

---

### 8. JSON output

Support:

```bash
autodev init . --json
```

Return structured data containing:

```text
repository
detected_artifacts
existing_configuration
planned_changes
unresolved_questions
result
```

---

### 9. Missing PROJECT.yaml creation

If missing:

```text
mkdir .agent
create .agent/PROJECT.yaml
```

Populate:

* schema version
* project identity when unambiguous
* detected source paths when unambiguous
* `gajae` execution harness
* conservative authority defaults

Never fabricate:

* approved roadmap state
* product requirements
* acceptance criteria
* autonomous authority

---

### 10. Existing PROJECT.yaml preservation

If valid:

```text
do not rewrite unnecessarily
```

If deterministic additions are needed:

```text
make surgical changes only
```

Never reset user choices.

---

### 11. Invalid configuration handling

If correction changes product semantics or authority:

```text
do not overwrite
```

Return:

```text
NEEDS_INPUT
```

with exact remediation.

---

### 12. Atomic writes

PROJECT.yaml creation/modification must be atomic.

Avoid leaving partially written configuration after interruption.

---

### 13. Idempotency

Repeated init must converge:

```bash
autodev init .
autodev init .
```

Second execution should normally report:

```text
No changes required.
```

---

## Init Acceptance Scenarios

### Fresh repository with obvious structure

Given:

```text
docs/PRD.md
.omx/ROADMAP.yaml
.omx/plans/
pyproject.toml
```

When:

```bash
autodev init .
```

Then:

```text
.agent/PROJECT.yaml
```

is correctly generated.

Result:

```text
ALIGNED
```

if no meaningful ambiguity remains.

---

### Existing valid configuration

Given valid:

```text
.agent/PROJECT.yaml
```

When init runs:

```text
preserve configuration
validate sources
report current state
```

No unnecessary diff.

---

### Multiple roadmaps

Given:

```text
docs/ROADMAP.md
.omx/ROADMAP.yaml
```

with no clear authority:

Interactive init asks.

Non-interactive init returns:

```text
NEEDS_INPUT
```

No arbitrary choice.

---

### Missing roadmap

Given a valid project but no roadmap:

Init may still produce a valid PROJECT.yaml.

Result:

```text
ALIGNED
```

is allowed if the project contract itself is structurally valid.

Later:

```text
preflight → NOT_READY
```

This separation must be preserved.

---

### Existing malformed PROJECT.yaml

Do not overwrite blindly.

Return actionable error.

---

## Success Criteria

* [ ] `autodev init .` works on fresh Git repository
* [ ] valid existing configuration is preserved
* [ ] safe artifact discovery works
* [ ] ambiguous sources are never silently selected
* [ ] missing `.agent/PROJECT.yaml` is generated
* [ ] safe authority defaults are used
* [ ] interactive choices work
* [ ] non-interactive unresolved state returns NEEDS_INPUT
* [ ] dry-run performs zero writes
* [ ] JSON output is deterministic
* [ ] atomic writes are used
* [ ] repeated init is idempotent
* [ ] no Hermes/Gajae/cron mutation occurs

## Completion Gate

M2 passes only when AutoDev can safely align both:

1. a fresh repository
2. an already configured repository

without requiring infrastructure access.

---

# M3 - Generic Roadmap Project Supervisor

## Objective

Extract the reusable behavior of the existing Nous supervisor into:

```text
roadmap-project-supervisor
```

Remove project-specific assumptions.

## Required behavior

The supervisor must:

1. load project contract
2. resolve authority
3. discover roadmap/milestones
4. inspect existing Gajae work first
5. classify milestone
6. reconcile repo/Gajae evidence
7. choose at most one primary action
8. enforce authority
9. independently verify completion
10. report
11. stop

## Modes

```text
status
dry-run
supervise
```

Default:

```text
dry-run
```

## States

```text
NOT_READY
READY
EXECUTING
WAITING_FOR_ANSWER
VERIFYING
FAILED_REPAIRABLE
HUMAN_BLOCKED
COMPLETE
```

## Genericity

No hardcoded:

```text
Nous
M7D
M7E
specific Nous filenames
fixed .omx structure
```

except labeled examples.

## Success criteria

* [ ] project-neutral
* [ ] bounded cycle preserved
* [ ] existing-work-first preserved
* [ ] completion gate preserved
* [ ] authority boundaries preserved
* [ ] fail-closed behavior preserved
* [ ] dry-run default preserved

---

# M4 - Nous Compatibility and Behavioral Parity

## Objective

Use Nous as the reference oracle and prove that the generic supervisor reaches materially equivalent conclusions.

## Required comparison

Compare:

* current milestone
* milestone state
* active Gajae work
* verification requirement
* next allowed action
* human blocker status

Do not replace live cron yet.

## Success criteria

* [ ] Nous contract validates
* [ ] old/new supervisors agree materially
* [ ] no unexpected mutation
* [ ] safety behavior is equivalent or stricter
* [ ] discrepancies documented
* [ ] discovered regressions gain tests

---

# M5 - Preflight Engine

## Objective

Implement deterministic, read-only readiness evaluation.

## Checks

### Repository

* valid Git repository
* root accessible
* project contract valid

### Requirements

* configured source exists

### Roadmap

* configured source exists

### Executable work

* safe approved work can be identified

### Completion contract

* enough evidence exists to determine completion

### Hermes

* expected runtime available/configurable

### Gajae

* expected harness available/configurable

## Check statuses

```text
PASS
WARN
FAIL
SKIP
```

Overall:

```text
READY
NOT_READY
ERROR
```

## Success criteria

* [ ] deterministic result
* [ ] JSON output
* [ ] human-readable remediation
* [ ] read-only operation
* [ ] warnings do not automatically fail readiness
* [ ] required failures do

---

# M6 - Hermes Provisioning

## Objective

Implement idempotent dedicated Hermes profile provisioning.

## Required work

* detect Hermes
* determine version
* create `<slug>-supervisor`
* reconcile existing profile
* configure exact project cwd
* make generic supervisor available
* preserve credentials externally
* avoid unrelated profile mutation

Use supported Hermes CLI interfaces.

Inspect local help instead of guessing commands.

## Success criteria

* [ ] profile creation works
* [ ] reruns idempotent
* [ ] exact cwd configured
* [ ] generic supervisor available
* [ ] unrelated profiles untouched
* [ ] no credentials persisted by AutoDev

---

# M7 - Gajae Coordinator Provisioning

## Objective

Implement safe Gajae Coordinator provisioning for one exact repository root.

## Required work

* detect `gjc`
* detect current Coordinator capability
* associate Hermes profile
* configure exact allowed root
* configure minimum mutation classes
* run Coordinator smoke test
* inspect configuration afterward
* reconcile on rerun

Never broaden root to:

```text
~
~/Projects
/
```

## Success criteria

* [ ] exact project root
* [ ] Coordinator reachable
* [ ] smoke passes
* [ ] profile integration works
* [ ] no permission broadening
* [ ] reruns safe

---

# M8 - Onboarding Orchestrator

## Objective

Implement:

```bash
autodev onboard .
```

by composing existing verified components.

## Workflow

```text
run/reconcile init
        │
        ▼
require PROJECT.yaml validity
        │
        ▼
register project
        │
        ▼
provision Hermes
        │
        ▼
provision Gajae
        │
        ▼
smoke tests
        │
        ▼
preflight
        │
        ▼
supervisor dry-run when safe
        │
        ▼
report
```

## Important init integration

`onboard` must call the same initialization implementation as:

```bash
autodev init
```

Do not create a second configuration-generation code path.

If init returns:

```text
NEEDS_INPUT
```

stop before infrastructure mutation.

Tell user:

```bash
autodev init .
```

must be completed.

## Dry-run

```bash
autodev onboard . --dry-run
```

must preview:

* init changes
* registry changes
* Hermes changes
* Gajae changes

without mutation.

## Success criteria

* [ ] fresh aligned project onboarded
* [ ] existing project reconciled
* [ ] no duplicated configuration
* [ ] partial failures recoverable
* [ ] onboarding never creates cron
* [ ] init logic is reused
* [ ] preflight runs automatically
* [ ] readiness clearly reported

---

# M9 - Enable, Disable, and Cron

## Objective

Implement explicit autonomy control.

## Enable

```bash
autodev enable .
```

Flow:

```text
resolve
→ full preflight
→ require READY
→ supervisor dry-run
→ require safe result
→ create/reconcile exactly one cron
→ verify cron state
→ registry enabled=true
```

## Disable

```bash
autodev disable .
```

Must stop future autonomous wakes while preserving:

* project registration
* Hermes profile
* Gajae sessions
* branches
* worktrees
* roadmap state

## Cron requirement

Each invocation:

```text
exactly one bounded supervision cycle
```

No endless polling loops.

## Success criteria

* [ ] NOT_READY cannot enable
* [ ] READY can enable
* [ ] one cron only
* [ ] enable idempotent
* [ ] disable stops future wakes
* [ ] re-enable works

---

# M10 - Registry, Status, and Operator UX

## Objective

Implement multi-project visibility.

## Registry

Support:

```text
add
get
update
list
```

Use atomic writes.

Resolve by:

```text
slug
path
current directory
```

## Status

Combine:

```text
init alignment
registry
PROJECT.yaml
Hermes
cron
Gajae
preflight
```

## Health

At minimum:

```text
HEALTHY
READY_DISABLED
NOT_READY
DEGRADED
ERROR
```

Autonomy separately:

```text
ENABLED
DISABLED
```

## Success criteria

* [ ] multiple projects supported
* [ ] atomic registry
* [ ] path/slug resolution
* [ ] status read-only
* [ ] deterministic JSON
* [ ] alignment state visible

---

# M11 - Reliability and Security Hardening

## Objective

Threat-model and harden the complete system.

## Required threats

Analyze:

* cross-project mutation
* root broadening
* duplicate cron
* partial provisioning
* uncertain subprocess results
* malicious PROJECT.yaml
* path traversal
* symlink escape
* registry corruption
* concurrent init/onboard
* accidental secrets in logs
* init overwriting existing project authority
* ambiguous discovery selecting wrong artifact

## Required protections

* reconcile uncertain mutation before retry
* atomic writes
* per-project locks
* safe subprocess wrapper
* strict root equality
* redaction
* no permission broadening
* no unsafe init overwrite

## Success criteria

* [ ] duplicate cron prevented
* [ ] cross-project tests pass
* [ ] traversal prevented
* [ ] symlink escape prevented
* [ ] init ambiguity fails closed
* [ ] concurrent mutation handled
* [ ] partial failure recoverable
* [ ] secrets not persisted

---

# M12 - Second-Project Pilot

## Objective

Prove AutoDev with a real second repository.

## Procedure

Start with a project with no manually configured Hermes/Gajae pipeline.

Run:

```bash
autodev init .
```

Validate that project-specific files are aligned.

Then:

```bash
autodev onboard .
autodev preflight .
autodev enable .
```

Execute one bounded supervision cycle.

Then:

```bash
autodev disable .
```

## Manual work allowed

The human may provide real project decisions that cannot safely be inferred during `init`.

The human must not manually configure:

* Hermes profile
* Gajae MCP
* Gajae root
* supervisor copy
* cron

## Isolation test

Verify:

```text
Project A cannot mutate Project B
Project B cannot mutate Project A
```

## Nous regression

Re-run Nous status/preflight afterward.

## Success criteria

* [ ] init aligns second project
* [ ] no manual Hermes configuration
* [ ] no manual Gajae configuration
* [ ] same generic supervisor
* [ ] preflight READY
* [ ] enable works
* [ ] bounded supervision succeeds
* [ ] disable works
* [ ] isolation proven
* [ ] Nous remains healthy

---

# M13 - Documentation and V1 Release

## Objective

Finalize operator documentation and release verification.

## Documentation

Include:

### README

* what AutoDev is
* architecture
* prerequisites
* quick start
* safety model

### Init guide

Explain:

```bash
autodev init .
```

including:

* discovery
* generated files
* interactive choices
* ALIGNED
* NEEDS_INPUT
* ERROR

### New-project workflow

```bash
cd ~/Projects/foo

autodev init .
autodev preflight .
autodev onboard .
autodev enable .
```

### PROJECT.yaml reference

Document all fields.

### Troubleshooting

Cover:

* invalid PROJECT.yaml
* ambiguous roadmap
* missing roadmap
* Hermes unavailable
* Gajae unavailable
* wrong root
* smoke failure
* unhealthy cron

### Emergency stop

Make obvious:

```bash
autodev disable <project>
```

## Release verification

Run:

* unit tests
* integration tests
* init fixture tests
* schema tests
* Nous dry-run
* pilot-project dry-run
* CLI help checks
* clean installation test

## Success criteria

* [ ] clean install works
* [ ] init documented
* [ ] all CLI commands documented
* [ ] PROJECT.yaml documented
* [ ] safety boundaries documented
* [ ] complete test suite passes
* [ ] Nous reference passes
* [ ] second project passes

---

# 22. Standard Milestone Verification Report

Every Ralph milestone ends with:

```markdown
# Milestone Verification - Mx

## Result

PASS | FAIL | HUMAN_BLOCKED

## Implemented

- ...

## Files Changed

- ...

## Verification Performed

### Command

`pytest ...`

Result:

PASS

## Acceptance Criteria

| Criterion | Result | Evidence |
|---|---|---|
| AC1 | PASS | ... |
| AC2 | PASS | ... |

## Scope Review

Confirmed not implemented:

- future milestone X
- future milestone Y

## Known Limitations

- ...

## Blockers

None.

## Recommended Next Milestone

Mx+1
```

A milestone cannot complete while mandatory acceptance criteria remain unresolved.

---

# 23. Global Coding Rules

## Surgical changes

Do not rewrite working subsystems unnecessarily.

## Inspect before assuming

For Hermes and Gajae integration, inspect actual installed behavior.

## Preserve repository truth

During `init`, existing project artifacts win over generated AutoDev boilerplate.

## Never fabricate authority

AutoDev can create structure.

It cannot declare:

```text
this roadmap is approved
this requirement is authoritative
this milestone is accepted
```

without repository or human evidence.

## Prefer supported interfaces

Use:

```text
Hermes CLI
Gajae CLI
Coordinator MCP
```

instead of private configuration internals where supported public interfaces exist.

## Do not scrape terminals

Gajae durable Coordinator state is authoritative.

## Fail closed

Ambiguity affecting product behavior or permissions must stop mutation.

## No acceptance weakening

Never change acceptance criteria simply to make work pass.

## No future milestone leakage

Implement only the active milestone.

## Add regression tests

Discovered bugs should gain coverage where practical.

## Preserve user configuration

Do not replace human configuration with generated defaults merely because they differ.

## No destructive cleanup shortcuts

Do not delete:

* Hermes profiles
* Gajae sessions
* Git branches
* worktrees

as a provisioning shortcut.

---

# 24. Global Acceptance Scenarios

## Scenario A - Init fresh repository

Given:

```text
Git repository
existing requirements
existing roadmap
no .agent/PROJECT.yaml
```

When:

```bash
autodev init .
```

Then:

```text
PROJECT.yaml created
existing artifacts referenced
safe defaults configured
no infrastructure mutation
```

---

## Scenario B - Init existing repository

Given valid AutoDev configuration:

```bash
autodev init .
```

Then:

```text
No unnecessary changes.
Result: ALIGNED
```

---

## Scenario C - Ambiguous project

Given two plausible authoritative roadmaps:

Interactive init asks.

Non-interactive init returns:

```text
NEEDS_INPUT
```

It does not choose arbitrarily.

---

## Scenario D - Existing Nous

Generic AutoDev inspection reaches correct supervision state without corrupting the working pipeline.

---

## Scenario E - New compliant project

```bash
autodev init .
autodev onboard .
autodev preflight .
autodev enable .
```

produces:

```text
valid project contract
dedicated Hermes profile
restricted Gajae root
generic supervisor
READY preflight
one cron
```

---

## Scenario F - Incomplete project

A repository without an approved roadmap may be successfully initialized.

But:

```text
preflight = NOT_READY
enable = rejected
```

AutoDev must not invent missing work.

---

## Scenario G - Repeated operations

Repeated:

```bash
autodev init .
autodev onboard .
autodev enable .
```

must converge without duplicates.

---

## Scenario H - Partial provisioning

If Hermes succeeds and Gajae fails:

```bash
autodev onboard .
```

must reconcile Hermes and resume safely.

---

## Scenario I - Isolation

Project A and Project B remain root-isolated.

---

## Scenario J - Emergency stop

```bash
autodev disable project-a
```

stops future autonomous cycles without destroying resume state.

---

# 25. Final V1 UX

## First-time repository

```text
$ cd ~/Projects/new-project

$ autodev init .

AutoDev Project Initialization

Repository
✓ Git root detected
✓ Existing PRD detected
✓ Existing roadmap detected
✓ Existing plans detected

Configuration
+ Created .agent/PROJECT.yaml
✓ Safe authority defaults configured

Result: ALIGNED
```

Then:

```text
$ autodev onboard .

Project alignment
✓ ALIGNED

Hermes
✓ new-project-supervisor

Gajae
✓ Coordinator configured
✓ Root restricted
✓ Smoke passed

Preflight
✓ READY

Supervisor
✓ Dry-run safe

Autonomous execution: DISABLED

Run:

    autodev enable new-project
```

Then:

```text
$ autodev enable new-project

✓ Final preflight READY
✓ Supervisor dry-run safe
✓ Cron enabled

new-project is now under autonomous supervision.
```

---

# 26. Responsibility Model

```text
Human
    WHY + WHAT

AutoDev Init
    REPOSITORY SHAPE

AutoDev
    SETUP + SAFETY

Hermes
    WHEN

Gajae
    HOW

Claude / Codex
    CODE

Tests / Acceptance Criteria
    DONE?
```

---

# 27. Execution Order

Execute exactly in this order unless a discovered technical dependency requires a documented adjustment:

```text
M0   Baseline + scaffold

M1   Project contract + schema

M2   Init + repository alignment

M3   Generic supervisor

M4   Nous parity

M5   Preflight

M6   Hermes provisioning

M7   Gajae provisioning

M8   Onboarding

M9   Enable / disable / cron

M10  Registry / status

M11  Hardening

M12  Second-project pilot

M13  V1 release
```

The most important sequencing rule remains:

```text
repository alignment
→ correctness
→ validation
→ provisioning
→ autonomy
```

not:

```text
provision everything
→ guess missing configuration
→ discover safety problems later
```
