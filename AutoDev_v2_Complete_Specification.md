# AutoDev v2.0 - Complete Specification and Agent Handoff

This single-file edition combines the normative specification, evidence decisions, contract reference, 24 milestone handoffs, 70 fault scenarios, startup prompt, and source list. In-package relative references refer to the companion ZIP. No implementation or live certification is claimed.

# AutoDev v2.0
## Failure-aware project onboarding and bounded autonomous delivery

**Status:** Revised implementation specification and coding-agent handoff. Not an installed implementation; no live environment is certified by this document.
**Supersedes:** AutoDev v1.1 and its milestone numbering. Use AD-00 through AD-23 below; do not mix these identifiers with the old M0-M13 sequence.
**Reference system:** The user's Nous deployment, operated through Hermes and the Gajae Coordinator (GJC).
**Execution unit:** One approved AD milestone per `ralplan -> ralph` session. Stop at the boundary.
**Primary target:** The existing single-host macOS deployment. Other process managers or installation distributions are supported only after their adapters pass the same contracts.

## 0. How to use this package

Read this specification, `01-EVIDENCE-AND-DECISIONS.md`, and `02-ACCEPTANCE-AND-FAULT-MATRIX.md` first. Then read only the selected milestone file and its prerequisites. Begin with AD-00. Use `03-CODING-AGENT-START.md` as the initial coding-agent prompt.

This is a requirements package, not a request to install, upgrade, inspect credentials on, or mutate the user's machine from this conversation. Every proposed `autodev` command below is an interface to implement, not a command assumed to exist today. Native Hermes/GJC commands in the uploaded incident reports are historical observations, not timeless API contracts.

### Source labels

- **[S1]** Uploaded *Lessons Learned from Nous Autonomous Supervisor Setup*, `Pasted markdown(2).md`.
- **[S2]** Uploaded *Hermes + Gajae Automated Onboarding: Lessons from Nous*, `Pasted markdown (2).md`.
- **[S3]** Uploaded *Lessons Learned From Nous Autonomous Onboarding*, `Pasted markdown (3).md`.
- **[W1-W7]** Primary-source documentation listed in `reference/SOURCES.md`.
- **Design requirement** means a new decision in this specification, not a claim that an uploaded source or an installed tool already implements it.

The attached reports establish observed failures, not the current state of the live laptop. Preserve that distinction in every implementation report.

## 1. Product objective and release boundary

AutoDev should turn an arbitrary, explicitly authorized repository into a configured and demonstrably safe-to-operate Hermes/GJC deployment without repeating Nous's troubleshooting process. Installation alone is not the product outcome. The outcome is a known project, an explicit authority contract, working execution paths, recoverable operation, and evidence for each admission gate.

The reference interaction is:

```text
autodev init .
autodev doctor .
autodev onboard . --dry-run
autodev onboard .
autodev validate . --plan
autodev validate . --apply-plan <approved-plan-id>
autodev preflight . --scope enable
autodev enable .
```

`init` may be friendly and interactive. All unattended commands are noninteractive and fail closed on unresolved choices. A user may request a single guided experience later, but the same underlying stages and authorization boundaries must remain separately observable.

### Keep the system small

Reuse Hermes for scheduling/messaging, GJC for sessions/turns/worktrees, Git for source history, and provider-supported account interfaces for authentication and quota observations. Do not add a custom daemon, web dashboard, product planner, worktree manager, general workflow engine, or new credential vault.

A small deterministic guard, adapter layer, local operation journal, and evidence receipts ARE in scope. They are necessary to prevent duplicate or unauthorized side effects across crashes. They must not become a second source of truth for GJC execution or product progress.

### What V2 does not promise

No claim of universal foolproof operation, global exactly-once execution, guaranteed provider pricing, complete account-usage visibility, or security isolation from a mere working-directory setting is permitted. The supported promise is narrower: observed gates, bounded actions, safe treatment of uncertainty, measurable permission boundaries, and non-destructive recovery within a tested deployment.

## 2. Decisions that replace ambiguous V1 behavior

| Decision | Required behavior |
|---|---|
| Initialization versus infrastructure | `init` only aligns repository files. Profiles, MCP, provider calls, messages, broker sessions, and cron are later stages. |
| Dynamic discovery versus explicit roadmap | Discover arbitrary layouts, but compile a reviewed machine-readable execution index. Do not require `.omx/ROADMAP.yaml`; do require explicit approved task/dependency references before dispatch. |
| Readiness | Track repository alignment, deployment configuration, validation, admission, execution, and delivery separately. A valid YAML file does not mean READY. |
| Passive versus live checks | `doctor`/`preflight` inspect local state and existing receipts without model calls, code execution, messages, credential refresh, or disposable sessions. `validate` explicitly owns active probes. |
| Credentials versus billing | OAuth is an authentication fact, not proof of included-subscription billing. Resolve effective routes and account billing controls separately. |
| Provider selection | Pin all effective inference routes, including cron, roles, auxiliary tasks, and eligible credential-pool/fallback paths. Unresolved routing blocks strict admission. |
| Runtime versions | Detect actual distribution and capabilities. Do not assume every GJC installation needs Bun or copy an old version minimum into every environment. |
| Worktree roots | Authorize the repository identity and its GJC-registered managed worktrees, not an entire parent directory. `cwd` is not a sandbox. |
| Skills | One versioned source, profile-local verified installations. Do not rely on a global install or an unpinned mutable shared symlink. |
| Approval | Approval is a recorded human/operator decision bound to artifact content. Discovery and model confidence cannot grant approval. |
| Completion versus integration | Verified implementation, published branch/PR, and merged integration are distinct. Default successor dispatch requires dependencies on the approved base revision. |
| Disable versus cancel | Disable stops admission and future wakes; it does not falsely claim already-running workers have stopped. |
| Runtime truth | Query/reconcile GJC authority, not one stale list endpoint or a prior assistant reply. |
| Safety timing | Locks, ownership, operation records, redaction, and root checks are foundations, not a late hardening milestone. |

These are deliberate resolutions of tensions among [S1-S3] and the prior plan; the original reports remain intact in the user's source files.

## 3. Responsibility and trust boundaries

```text
Human/operator: product authority, account choice, deployment approval
AutoDev init: repository inspection and reviewed alignment
AutoDev guard: admission checks, operation identity, scope and recovery
Hermes: bounded supervisory reasoning, native scheduling and delivery
GJC Coordinator: durable coding delegation and lifecycle
Coding workers: implementation within authorized scope
Verifier: independent evidence and acceptance assessment
```

### 3.1 Scope enforcement is not just a prompt

The supervisor skill expresses policy. Deterministic code must enforce preconditions before side effects. Prefer existing native enforcement hooks. If native capabilities cannot enforce a required mutation check, implement a narrow local adapter around the existing Coordinator operations; do not invent another executor.

Every unattended mutation must pass the same guard: project identity, enabled epoch, approved plan hash, active-work reconciliation, root membership, idempotency identity, resource admission, and operation-specific authority. A guard that the same agent can trivially bypass by directly invoking raw mutating GJC tools, editing its own control files, or running an unrestricted terminal is not an enforced boundary.

Record assurance explicitly:

- `POLICY_ONLY`: instructions and detection exist, but unrestricted same-user tools can bypass them. Eligible for read-only/manual use, not strict unattended certification.
- `ENFORCED`: supported tool/OS/credential boundaries prevent the tested bypasses, and negative tests supply evidence.

Do not claim sandboxing because two Hermes profiles exist. A strict deployment must prove allowed filesystem roots, control-file protection, permitted network/credential paths, and protected Git operations using its actual execution backend. Read-only runtime/tool directories and trusted state directories are explicit additional capabilities; they are not permission to mutate the rest of the user's home directory.

### 3.2 Untrusted project content

Repository documents, dependency scripts, hooks, `.env` files, and model output are data until an authorized action makes them executable. `init` never sources shell files, installs dependencies, invokes package scripts, imports project modules, executes Git hooks, or sends repo text to a model.

A verification command is executable code, not a harmless configuration value. Commands must be reviewed, represented as executable plus argument array and explicit cwd/environment, and executed in the approved boundary. Avoid `shell=True`; a required shell script must itself be a reviewed, content-bound executable artifact.

### 3.3 Git and approval ceilings

Default proposal: isolated branch/worktree and local commit may be granted during guided setup; push and PR creation require an explicit choice; merge, force-push, protected-ref updates, credential changes, and destructive external operations remain denied to autonomous workers.

A generated file cannot silently grant implementation authority. The effective permission is the intersection of repository policy, operator-approved deployment grant, native tool permissions, and the OS/credential boundary. Editing repository YAML cannot broaden that grant.

## 4. Ownership, persistence, and identity

### 4.1 Portable repository contract

`.agent/PROJECT.yaml` is the default AutoDev entrypoint. It contains a stable `project_id`, human-friendly slug, source/discovery rules, execution-index location, verification specification, and requested policy. It contains no account secrets, absolute host paths, cron IDs, current sessions, or current worker status.

`schema_version: 2` replaces V1's incomplete implicit schema. `setup_state: draft` allows null or empty unresolved fields so `init` can write an honest draft; `setup_state: configured` requires structural completeness. Neither value grants execution approval.

Repository alignment results:

- `ALIGNED`: contract is structurally configured. It may have an empty execution index and therefore no dispatchable work.
- `NEEDS_INPUT`: draft or conflict remains, including unresolved authoritative source selection.
- `ERROR`: parse, filesystem, safety, or unsupported-schema failure.

### 4.2 Execution index, without a forced folder layout

Use an existing validated machine-readable index where an adapter supports its semantics. Otherwise propose `.agent/EXECUTION.yaml`. A different repository-relative path is valid when declared in PROJECT.yaml. This index references existing requirements, PRDs, execution maps, plans, tests, exclusions, and dependency relationships; it must not duplicate their prose.

Expose approval through `autodev approve <project> --milestone <id> --plan`, followed by an explicit operator `--apply-plan <plan-id>`. Show scope, exclusions, dependency base, criteria hashes, and granted operation classes before approval. This surface must be unavailable to unattended workers.

Each milestone record requires: unique ID, title, dependencies, plan/acceptance source references and digests, approval state/evidence, implementation scope, verification IDs, approved base policy, and lifecycle evidence references. Status labels imported from prose are observations, not completion proof.

Draft import produces `approval: proposed`, never `approved`. An approval receipt references the selected milestone, exact authority artifacts and content hashes, approving operator action, and applicable boundaries. Historical evidence may justify an imported completion record after explicit review; filename order or previous partial implementation alone does not approve future work.

Track completion changes through append-only evidence pointers or narrowly scoped status updates. Never rewrite accepted scope, dependency order, or criteria as a side effect of marking completion.

### 4.3 Host-owned installation binding

Default data root: `~/.hermes/autodev/`, configurable through one explicit AutoDev setting. It contains:

```text
projects.yaml
installations/<installation_id>/installation.yaml
installations/<installation_id>/grants/
installations/<installation_id>/receipts/
installations/<installation_id>/operations/
installations/<installation_id>/recovery/
locks/
```

The binding records canonical repository path and Git common-directory identity, profile identity, runtime distribution and capability fingerprint, selected providers/models, redacted account references, explicit environment paths, delivery target reference, cron ownership/ID, grant revision, and deployment epoch.

Project ID, installation ID, and operation ID are distinct. Slugs are labels, not uniqueness/security keys. A clone sharing project_id is not automatically the same installation. V2 certifies one active deployment owner per project; multi-host failover requires an external coordination design and is not implemented by pretending a local lock is distributed.

### 4.4 Small journal, not a replacement task database

Durably record each logical mutation BEFORE dispatch: operation ID, canonical-arguments hash, idempotency key, project/milestone/grant hashes, owner epoch, state, and returned native IDs. States include `PREPARED`, `SENT`, `ACKNOWLEDGED`, `UNCERTAIN`, and reconciled terminal outcome.

Reuse native authoritative records whenever they provide the required guarantees. AutoDev's records link intent to native records; they do not override GJC state. Use atomic replacement, locking, restrictive permissions, bounded retention, and durable writes for the pre-send record. Do not hash or copy token values into receipts.

## 5. State model and exit contracts

Do not compress unrelated states into a single READY flag.

| Dimension | Representative states |
|---|---|
| Repository | DRAFT / ALIGNED / INVALID |
| Deployment | ABSENT / CONFIGURED / PARTIAL / DRIFTED |
| Validation | NOT_RUN / PASSED / FAILED / STALE / BLOCKED_EXTERNAL |
| Admission | ALLOW / DENY / UNKNOWN |
| Schedule | ABSENT / PAUSED / ENABLED / UNKNOWN |
| Execution | IDLE / EXECUTING / WAITING_FOR_ANSWER / VERIFYING / FAILED_REPAIRABLE / UNCERTAIN / HUMAN_BLOCKED / VERIFIED_UNMERGED / INTEGRATED |
| Resource | AVAILABLE / BLOCKED_QUOTA / UNKNOWN |
| Delivery | NOT_TESTED / DELIVERED / FAILED / UNKNOWN |

`READY_FOR_ENABLE` is a computed predicate: structural alignment + supported configured deployment + current required validation receipts + operator grant + enforcement assurance + tested delivery + no unresolved ownership or drift conflict. It does not imply new product work is ready right now. An approved but exhausted roadmap is a safe IDLE condition.

`READY_TO_DISPATCH` additionally requires exactly one eligible approved milestone, satisfied dependencies/base policy, no active or uncertain matching work, and current resource admission. When no new work is eligible, report the precise reason rather than fabricating another milestone.

Proposed stable exit codes: 0 = requested operation completed or PASS; 2 = required input/NOT_READY; 3 = safety denial/conflict; 4 = dependency/probe failure; 5 = uncertainty/reconciliation required; 6 = quota denial; 7 = unsupported capability. `status --json` returns 0 when it successfully reports an unhealthy state; `preflight` returns nonzero when its requested gate is not met. JSON always includes schema version, operation, outcome, checks, warnings, planned/applied changes, and next safe action. Human prompts go to stderr and are disabled for machine-readable/non-TTY usage.

## 6. Command contracts

| Command | Default scope and allowed effects |
|---|---|
| `init [path]` | Inspect repo; preview/confirm local configuration writes. No profile, provider, broker, message, or cron activity. |
| `approve [project] --milestone <id> --plan` | Preview content-bound milestone approval; `--apply-plan <id>` requires an explicit operator action and cannot run from unattended workers. |
| `doctor [project]` | Passive diagnosis of declared/observable state and receipts, with typed remediation. No repair or live probes. |
| `preflight [project] --scope repo|enable|dispatch` | Pure gate evaluation from current local evidence. Missing live evidence returns NOT_RUN/STALE, never synthetic PASS. |
| `onboard [path] --dry-run` | Complete deterministic change plan, including reused init results. Zero writes. |
| `onboard [path]` | Apply reviewed owned configuration; verify readback; no inference, coding session, test message, or active schedule by default. |
| `validate [project] --plan` | Enumerate active probes, token-using routes, filesystem footprints, required permissions, cleanup, and timeout bounds. |
| `validate [project] --apply-plan <id>` | Run only the explicitly authorized active probes; write receipts. Does not enable recurring work. |
| `enable [project]` | Recheck current admission and canary receipts; enable exactly one owned schedule under the active deployment epoch. |
| `disable [project]` | Close admission first; stop future wakes; preserve active work and report it. No implicit worker termination. |
| `cycle [project]` | Internal guarded one-cycle entrypoint; inspect, choose at most one primary action, record, report, exit. |
| `repair [project] --plan` | Read-only remediation proposal. `--apply-plan <id>` permits only explicitly reviewed, scoped changes. |
| `recover [project] --plan` | Preserve and reconcile uncertain/stranded work. No deletion, reset, overwrite, or new dispatch from diagnosis alone. |
| `status`, `list` | Read-only multidimensional state and native identifiers, with JSON support. |

`--yes` suppresses low-risk scaffolding prompts only. It never means approve a roadmap, spend money, remove a deny-list entry, adopt an existing profile, restart a shared gateway, delete credentials, or enable autonomy. Do not add an escape hatch named `--force` to bypass a mandatory gate.

## 7. Init: friendly, reversible repository alignment

### Required algorithm

1. Resolve a real Git root and Git common directory with trusted, noninteractive read commands. Detect bare/shallow/detached/unborn repositories and report supported behavior explicitly. An unborn repo may be aligned but cannot pass worktree validation without an approved initial commit; init must not commit for the user.
2. Inventory existing PROJECT.yaml, AGENT.md, AGENTS.md, CLAUDE.md, `.hermes.md`, requirements, execution maps, plans, acceptance matrices, tests, and toolchain manifests. Do not treat similarly named context files as interchangeable or rename them automatically. [S3 sections 1, 2, 17]
3. Search within declared roots with size/count/depth limits. Exclude `.git`, dependencies, caches, generated build output, existing worktrees, and symlink escapes. Do not follow cross-repo links by default.
4. Preserve valid explicit references. Candidate scores explain discovery confidence only; they are not approval. Present ambiguous candidates with reason and source excerpts, not a silent winner.
5. Propose a portable contract and, when absent, an execution-index draft. Reuse existing artifacts at their existing paths. With no requirements/authority source selected, retain a draft and return NEEDS_INPUT. With selected sources but no approved work yet, ALIGNED + NOT_READY_TO_DISPATCH is correct.
6. Detect the actual GJC worktree strategy if already known. For an in-repo managed bucket, check Git ignore semantics and whether files are already tracked. Offer an exact anchored ignore entry only when appropriate, then verify it. Do not always append `/.worktrees`; external buckets differ. Do not remove tracked worktree files automatically. [S2 section 4]
7. Preview exact changes. Preserve comments/order for existing YAML with round-trip editing or a targeted patch; a wholesale parse/dump is not a surgical edit. A minimal additional YAML dependency is justified for this requirement.
8. Before applying, recheck file identity/hash under a repo lock. Use atomic replacement and a recovery record. A changed file invalidates the plan; do not overwrite it using an old preview.
9. Return applied changes, unresolved choices, structural result, and the next command. Repeating init against unchanged inputs must be byte-for-byte no-op.

### Hostile and unusual paths

Test spaces, Unicode, long names, macOS case collisions, symlinks, submodules, linked worktrees, same-slug repos, and two copies of the same project. V2 may explicitly reject unsupported cases, but must not misidentify their roots. Missing or malformed source files never cause automatic plan fabrication.

## 8. Compatibility, runtimes, and profile installation

### 8.1 Capability manifest before configuration

For the actual installed Hermes/GJC distribution, capture supported native operations, argument schemas, protocol/tool metadata, installation paths, versions/generations, and relevant runtime requirements. Bind adapters to this manifest. Unrecognized safety semantics return UNSUPPORTED rather than trying near-matching flags.

The uploaded Bun/GJC version mismatch is a required regression fixture [S2], not a universal deployment requirement. The public GJC README also documents standalone binaries that do not require Bun [W4]. Detect how the executable was installed before enforcing a Bun constraint. Never auto-upgrade shared installations during onboarding.

A proposed upgrade is a separate human-approved change: inventory active work, verify compatibility first, pin prior known-good identity, apply through supported mechanisms, inspect actual executables afterward, restart only affected processes with authorization, then invalidate dependent receipts. Installer success text is not version evidence.

### 8.2 Distinct execution environments

Probe and fingerprint these separately when used:

- operator CLI;
- Hermes interactive profile;
- Hermes terminal execution environment;
- MCP subprocess environment;
- GJC broker/worker environment;
- persistent gateway environment;
- actual scheduled worker environment.

A green shell probe cannot satisfy gateway or cron gates. [S2; S3 sections 3, 5, 18]

Store explicit interpreter/executable choices and profile-scoped initialization. Do not edit `.zshrc` or global PATH as an automatic fix. Environment receipts contain relevant executable realpaths/versions and an allowlisted environment fingerprint, not a full environment dump. Secret-valued variables are represented only as presence/source metadata. Runtime-specific filesystem path mapping must be verified when a sandbox/container is involved.

### 8.3 Hermes profile and skill

One dedicated profile per project. Inspect ownership before adopting an existing profile. Preserve unrelated tools and disabled lists. Install the generic skill from one versioned source into the correct profile; verify content hash, entrypoint, enabled/available state, and actual injection in a fresh session. A global skill file is not evidence that the project profile has it. [S1 sections 4, 6; S3 section 6]

Changes to loaded configuration may require a fresh process. A canary uses a new profile session after configuration; an old process reporting a former tool list is not a passing test.

### 8.4 GJC MCP

For the supported adapter, configure the outer MCP executable with a verified absolute path and a deterministic MCP PATH. Preserve the native managed-session selector semantics; in the observed setup `GJC_COORDINATOR_MCP_SESSION_COMMAND = "gjc --worktree"` was not an arbitrary shell command to rewrite. [S2 sections 2, 7]

Check definition, enabled state, startup, discovery, policy filtering, active-model visibility, real read invocation, broker lifecycle, and workflow independently. Match required capability semantics/schema, not a hardcoded tool count.

If `mcp-gjc_coordinator` is disabled, report it precisely. A repair plan may remove only that entry after approval; do not assume every denial is accidental. Preserve Tool Search settings unless the supported version's tested contract requires otherwise. Never disable Tool Search as a generic fix. [S2 sections 8-10]

## 9. Authentication, billing routes, and resource admission

### 9.1 Separate the facts

A route record must distinguish:

```text
provider + endpoint + model + role
credential mechanism + redacted account identity + source
eligible credential-pool members and rotations
fallback/auxiliary routing
subscription entitlement / metered path / unknown
account overage or paid-credit capability / unknown
validation evidence + observation time + expiry
```

`credential_type: oauth` must never auto-populate `billing_mode: subscription_only`. The uploaded reports describe OAuth audits; the stronger billing claim requires independent evidence. Public account documentation describes usage credits beyond plan limits [W6, W7]. This specification does not certify any current account's overage setting.

### 9.2 Audit scope and secret handling

Inspect only authorized known sources: current process configuration, selected profile configuration, relevant project overrides, selected service environment, native credential metadata, and known provider/model override files. Report coverage and inaccessible sources. Do not recursively scrape the user's whole home or dump environment values.

Prefer native redacted credential inspection. A read-only GJC database adapter is permitted only for a recognized schema, explicitly selected metadata columns, and no sensitive payload column. Do not run `SELECT *`, log raw databases, copy credential stores, or mutate credentials to make a check pass. Unsupported schema or unavailable metadata means UNKNOWN.

Merely finding an unrelated API key elsewhere on the machine is not proof that this deployment will bill it; conversely, not finding a key in the shell is not proof of safety. The question is whether the effective autonomous route can reach it. Exact coverage and enforceable route restrictions are mandatory. [S1 sections 7-14]

### 9.3 Effective-route closure

Resolve supervisor, cron, GJC default/planner/architect/critic/executor/reviewer roles, and any auxiliary model-using services. Check custom base URLs, provider overrides, account rotation, and fallback settings. One successful model call does not validate all routes. [S2 section 5]

Hermes documentation distinguishes same-provider credential pools, primary fallback, and independent auxiliary routing [W2, W3]. Therefore an empty cross-provider fallback list alone is not a sufficient audit. Disable unused auxiliary paths or bind them to approved routes; never quietly leave `auto` unresolved.

Strict subscription-only requested policy: deny metered routes, unknown entitlement, unapproved paid-credit/overage use, unapproved account rotation, and ambiguous fallback. Unknown coverage fails admission. Operator acknowledgement of uncertainty may permit manual diagnostics, but it cannot be labeled verified zero-cost autonomy.

### 9.4 Resource gate

Return `ALLOW`, `DENY`, or `UNKNOWN` for a specific proposed operation, not one global guess. Account quota observations include provider/account identity, unit, window, reset timestamp, observed time, and freshness. Use only supported account telemetry; do not guess reset from elapsed wall-clock time.

The uploaded 20%/85% thresholds and 3h/4h cadences are examples, not universally correct defaults. Ask the operator to select a policy. A proposed conservative polling default may be four hours, but never overwrite an existing cadence. Strict unknown quota denies new expensive work when required telemetry is unavailable; report the capability gap rather than scrape credentials or invent an API.

Resource limits apply before the supervisor model call as well as before expensive GJC dispatch. When supervisor inference is denied, use deterministic diagnostics/status delivery rather than spawning another model to explain the denial. Local checks are allowed only if genuinely local and authorized; a test that calls paid APIs is not exempt.

Share local admissions/reservations by account across projects so two projects cannot independently consume the same observed allowance. This reduces races, not a guarantee against simultaneous external account use. Quota telemetry is not a reservation service. Hard monetary guarantees require provider-enforced account controls and a restricted route boundary.

Bound retry counts, repair attempts per failure signature across cycles, role fan-out, requests/output where supported, and worker lifecycle budgets. A supervisor timeout alone does not limit a GJC worker that continues afterward. If a required worker limit is unenforceable, report it and deny the corresponding strict mode.

## 10. Reconciliation and duplicate prevention

### 10.1 Observe several sources

Reconcile coordination status, relevant active turns, durable turn records, live SDK activity, structured questions, event progression, and session listings. Record provenance, timestamps, broker generation, and confidence. Do not treat `list_sessions` as the sole truth. [S3 sections 8-10]

`unavailable`, a timeout, or missing final text is observation uncertainty, not proof a worker failed. Advancing live event sequence is evidence of activity, but does not itself prove product correctness or authorization. When authoritative sources disagree, block a new mutation and keep read-only reconciliation available.

### 10.2 One logical mutation, one durable identity

Acquire the project mutation lock, refresh state, recheck the enabled epoch, and write PREPARED intent before contacting GJC. Idempotency identity includes installation, milestone, plan digest, operation kind, and a persisted unique logical-operation ID. Do not derive a new identity from the current time on every retry.

If the response is lost, mark UNCERTAIN and reconcile. Retry the identical canonical request with the identical key only where the native contract supports it. A changed payload under the same key is an error. A repair is a new logical operation, but a missing acknowledgement is not a reason to label the original dispatch a repair.

Allow at most one active implementation lane per project and one primary dispatch/repair per cycle in V2. Parallel GJC subagents, if authorized, remain inside that one lane and count toward the worker budget. Unknown existing work also reserves the lane until reconciled.

### 10.3 Concurrency and ownership

Single-host local locking covers manual and scheduled invocation of AutoDev. Native coordinator idempotency covers supported network retry uncertainty. A deployment epoch fences old cron workers after disable/configuration change. Recheck it at the mutation boundary, not only at cycle start.

An in-flight native request may already have been accepted before disable. Preserve and reconcile it. Do not claim it never happened. A stale lock is not stolen merely because a timestamp is old; verify owner/process identity and native active work. PID reuse and restart generation are test cases.

### 10.4 Cycle contract

```text
cheap deterministic admission -> acquire/reconcile ownership
-> fresh repo/GJC observations -> choose one primary action
-> guarded bounded read/answer/verify/dispatch/repair/escalate
-> durable receipt -> delivery status -> exit
```

Dispatch asynchronously using the supported native equivalent of non-waiting delegation. Record IDs, then stop. No indefinite polling, no agent-created schedules, and no uncontrolled retry loop across future wakes.

## 11. Verification, authority freshness, and dependency bases

### 11.1 Classify failures before repairing code

Confirm interpreter/executable identity in the environment that actually performs verification. The uploaded Ruby 2.6 versus 3.4 incident is an environment regression fixture, not a reason to lower language requirements or rewrite tests. [S3 sections 3, 5]

Results distinguish ENVIRONMENT_FAILURE, VERIFICATION_FAILURE, ACCEPTANCE_GAP, POLICY_VIOLATION, and UNKNOWN. An environment failure should propose environment remediation and leave product criteria untouched.

### 11.2 Evidence applicability

A verification receipt binds the implementation revision and dirty-tree snapshot, approved artifact hashes, verification commands, source/test/config/dependency/toolchain inputs, and environment fingerprint. Different HEAD alone does not require a full rerun if a conservatively complete applicability check proves relevant inputs unchanged. [S3 section 4]

The relevant input set includes test files, fixtures, lockfiles, build/CI scripts, generated-code inputs, runtime versions, verification commands, and policy/acceptance artifacts, not only `lib/` and `scripts/`. Deleted/renamed files and untracked changes count. Unknown dependency coverage invalidates the receipt. No worker may redefine the relevance set after tests fail.

### 11.3 Completion and integration

Require no still-active matching turn, scope/exclusion compliance, current test results, independent acceptance assessment, approved-artifact integrity, and no unresolved blocker. Executor prose is only a claim to investigate. [S1 section 21; S3 sections 3, 13-15]

Classify completed code as `VERIFIED_UNMERGED` until the approved integration policy is satisfied. Default successor dispatch uses the protected/default target base only after required predecessor commits are actually present. Do not launch the next milestone from `main` when its predecessor exists only in another worktree. Stacked branches/dependency integration are a separate future policy, not an implicit merge loophole.

Acceptance files can be protected read-only where supported; otherwise compare approved content hashes and reject unauthorized changes. Hash detection is not preventive filesystem enforcement, and the report must not conflate them. Ordinary implementation tests may be added/fixed, but changing the locked acceptance contract requires human review.

## 12. Layered active validation and admission receipts

### 12.1 Live probes are explicitly authorized

`validate --plan` lists token-using routes, per-route probe budgets, session/worktree artifacts, messages/targets, exact allowlisted modifications, and cleanup plan. A planning-only workflow can still consume quota and create native session/plan artifacts; call it non-product-mutating, not side-effect-free.

All probes use unique IDs, bounded waits, and a probe registry. No new permanent permission is granted to run a test. Use an isolated pilot deployment for destructive negative tests. When the real project's broker lifecycle must be checked, explicitly authorize an empty diagnostic worktree and verify no product-file changes. Source execution smoke happens only in a defined disposable managed worktree with an exact harmless diagnostic-file allowlist.

The minimal inference probe uses an exact nonce-bearing response such as `GJC_OK:<probe-id>` and prohibits tool calls. A mismatched response is a probe-contract failure, not automatically an authentication failure. Capture the selected route and actual tool trace, not just final prose.

### 12.2 Gate sequence

| Gate | Required proof | Must not be confused with |
|---|---|---|
| G00 | Valid repo identity, contract, index/authority references, worktree hygiene | Approved executable work |
| G01 | Supported actual runtime/distribution and adapter semantics | Installer log success |
| G02 | Effective provider/auth/billing route coverage and resource gate | `env` contains no API key |
| G03 | Authorized minimal inference on each distinct used route, no tools | TUI starts |
| G04 | Direct planning workflow completes with correct route/profile | Basic inference succeeds |
| G05 | MCP configured/enabled/process/discovery pass | Model can call discovered tools |
| G06 | Fresh Hermes session actually invokes a read-only Coordinator tool; trace proves it | LLM says it can see tools |
| G07 | Native broker creates a managed worktree/session with correct identity | Direct GJC TUI works |
| G08 | Hermes -> GJC -> planning workflow returns plan and native IDs | Coordinator transport smoke |
| G09 | One authorized bounded diagnostic execution, allowed diff only | Planning-only success |
| G10 | Independent second wake reconciles the same live/uncertain operation; no duplicate | One happy-path dispatch |
| G11 | Terminal verification, immutable criteria, dependency/base handling pass | Executor says done |
| G12 | Actual gateway and scheduled-worker environment probes, pinned route, skill/context, and delivery | Interactive CLI or Discord alone |
| G13 | Admission/disable/restart/uncertainty negative tests pass on supported deployment | Scheduler lock exists |

Passive failures prevent dependent probes. Independent safe checks may continue to produce a useful report; never spend tokens testing a downstream layer whose prerequisite is already unsafe.

### 12.3 Receipt requirements

Every receipt contains gate ID, project/installation IDs, invocation source, probe nonce, timestamps, software/capability fingerprint, config/policy/skill/authority hashes, relevant repo revision, redacted effective model/account route, native correlation IDs, exact observations, effect summary, result, expiry, and invalidation dependencies.

Use `SIMULATED`, `LIVE`, and `NOT_RUN` evidence classes. Unit tests never satisfy a LIVE gate. A static grep of SKILL.md cannot prove a model obeys it. An LLM-written "PASS" without tool trace cannot satisfy G06. A message accepted by a platform is not evidence a human read it.

Receipt expiry is risk-specific and operator-visible. Provider quota expires much sooner than a static schema check. Any relevant config, account route, executable generation, skill, service identity, worktree strategy, or approved-plan change invalidates dependent receipts. OAuth token refresh alone need not invalidate stable account identity, but account/routing changes do. Upgrade invalidation is conservative.

## 13. Gateway, cron, observability, and host lifecycle

### 13.1 Separate installation and activation

Do not overwrite or restart a shared gateway automatically. Identify which profile/service owns which scheduler and what loaded configuration generation is active. Configure a paused/unscheduled canary using supported native semantics, verify readback, and only then authorize a single runtime validation invocation.

The scheduled-worker entrypoint is a separate deployment target. Test its actual cwd, toolchain, profile/skill hash, model route, GJC access, guard epoch, and notification target. Discord entry through the gateway is useful evidence but does not alone prove cron's environment. [S3 sections 18, 22]

Current Hermes docs describe per-job pins and snapshot/cron-default resolution [W1]. Implement the installed-version behavior through an adapter and verify the effective job route; do not require a historical `model_drift_guard` flag without capability evidence. Enforce explicit approved model/provider/endpoint and deny drift at execution time.

### 13.2 Cheap wakes and bounded native scheduling

Use Hermes's supported no-agent/script or equivalent pre-dispatch mechanism where available so a blocked/unchanged wake need not instantiate an LLM. Do not create a new scheduler daemon. If the installed runtime cannot enforce pre-inference gating, strict admission must say so instead of falsely claiming it.

Disable recursive agent scheduling at the actual tool boundary. Limit native schedule concurrency and AutoDev project concurrency separately. Coalesce missed occurrences after sleep/restart into one reconciliation; do not replay every missed expensive wake. Explicitly distinguish scheduled occurrence identity from a manual run.

### 13.3 Delivery is its own outcome

Use an explicit profile-bound destination, not an ambiguous origin. Protect private repo content; default report includes milestone/action/state, sanitized errors, session/turn IDs, verification summary, and exact human decision needed. Do not post credentials, prompts containing secrets, full environment, or unrestricted logs.

Record execution result independently from delivery result. A Discord timeout must retry/report delivery only; it must never trigger another coding dispatch. Platform acknowledgement/message ID is the delivery proof; uncertainty stays UNKNOWN. Deduplicate notification retries where supported. Notification failure pauses new unattended dispatch under the default policy while allowing deterministic reconciliation and preservation.

Prefer a concise result per cycle with repeated identical errors coalesced, plus important transitions and decisions. Reuse native output/history/outbox facilities where they satisfy this requirement. No separate messaging daemon.

### 13.4 Host availability

Declare local/server/container topology and required uptime. A local sleeping or offline host cannot run its own watchdog. Report last heartbeat and stale runtime state when next observable; do not promise an offline alert without separately provisioned external monitoring. Never automatically change power settings or install persistent sleep prevention.

## 14. Disable, repair, restart, and recovery

### 14.1 Disable order

Persist disabled admission and increment the deployment epoch first. Then pause the exact AutoDev-owned schedule by native ID. Inspect actual schedule state and active/uncertain work. Return `DISABLED` with active work clearly reported, or `ADMISSION_CLOSED_SCHEDULE_UNCERTAIN` when pause cannot be confirmed. The guard must still refuse old scheduled mutation attempts.

A separate explicit cancellation plan may request supported GJC cancellation. Do not kill a broker, reset a worktree, or terminate unrelated sessions as an emergency shortcut. The meaning of disable is no new work, not guaranteed instantaneous cessation of accepted work.

### 14.2 Typed repair

`repair --plan` includes diagnosis evidence, exact owned fields/files to change, expected hashes, impact, required authorization, rollback, and verification gate. Safe supported repairs may include an approved anchored ignore entry, a profile PATH change, reinstallation of the pinned skill, or removal of one explicitly approved disabled-toolset entry.

Credential changes, provider/account substitutions, package upgrades, shared-service restarts, scope expansion, and destructive Git operations require distinct human authorization. Failure repetition triggers a persistent circuit breaker keyed by normalized cause; a new cron cycle does not reset its attempt count.

### 14.3 Non-destructive execution recovery

Recovery begins with root/branch/worktree/session/turn/broker identity, full Git status including untracked/binary files, and evidence of liveness. Never conclude an old worktree is expendable because no commit exists. Do not assume a recovery commit exists.

For a stranded but valuable implementation, propose: preserve original unchanged; inventory and verify a private backup or patch plus untracked/binary data; create a fresh GJC-managed worktree only after original execution is conclusively inactive or explicitly cancelled; transfer only approved implementation changes; verify the transferred diff and base; rebind evidence to new native IDs; run verification again. Keep rollback/preservation evidence. Unknown original liveness blocks automatic duplicate recovery.

Do not use a stranded implementation worktree as the Coordinator root just to bypass lifecycle checks. GJC remains the owner of managed-worktree creation. This recovery design is an added safeguard; the three uploaded files do not establish a completed end-to-end test of it.

### 14.4 Restart reconciliation

Use native broker generation/process identity to assess stale state. An unsupported `broker.shutdown` request is an unsupported diagnostic route, not proof the broker is old. [S2] After restart: inspect outstanding operations and active GJC work, reconcile delivery separately, invalidate process-dependent receipts, and resume observation before permitting dispatch.

## 15. Release evidence and non-negotiable invariants

A release must provide unit/contract tests, negative/fault tests, actual fresh-session integration traces, a Nous read-only parity report, and a second-project pilot. Manual/live unavailable tests must be labeled BLOCKED_EXTERNAL, never silently skipped into PASS.

The following invariants are mandatory:

1. No ambiguous artifact discovery grants product authority.
2. No old context, list endpoint, or transport error alone authorizes a new execution.
3. No enabled job exists before authorized canary proof and current admission.
4. No direct mutating route bypasses the guard in a certified deployment.
5. No unknown effective billing route passes strict subscription-only admission.
6. No missing/unknown quota is replaced with an elapsed-time guess.
7. No worker modifies approved scope/criteria to manufacture success.
8. No child milestone starts from a base missing required predecessor changes.
9. No notification retry becomes an implementation retry.
10. No recover/disable path destroys uncommitted work implicitly.
11. No claimed sandbox is based only on cwd/profile naming.
12. No fake or mocked integration result is represented as a live result.
13. No existing user profile/config is adopted or overwritten without review.
14. No global/shared setting is changed as a convenient project-local repair.
15. No unknown native interface is guessed into a mutating call.

The fault matrix and milestone acceptance criteria operationalize these invariants. A technically blocked mandatory gate is an honest release blocker, not permission to weaken it.

## 16. Implementation roadmap

The 24 bounded work units are defined in `05-MILESTONE-PLAN.md` and separately in `milestones/AD-00.md` through `AD-23.md`. They replace the earlier M0-M13 sequence. Read the source crosswalk before continuing an existing V1 implementation. The fault matrix contains 70 acceptance/failure-injection scenarios.


---

# Evidence map and design decisions

## What the uploaded failures establish

The reports describe a layered reliability problem: a successful check often exercised a different process, route, lifecycle, or authority layer from the failing one. V2 keeps those observed causes separate rather than using one generic "integration healthy" flag. Historical incidents remain historical; no current machine diagnosis is asserted here.

| Lesson | Uploaded basis | Reported bottleneck | V2 requirement | Milestones | Fault coverage |
|---|---|---|---|---|---|
| L01 | S1 section 1 | Hermes/GJC/worker responsibilities blurred | Keep runtime, lifecycle, implementation and guard roles separate. | AD-00/13 | F57 |
| L02 | S1 sections 2-3; S2 sections 8-10; S3 section 7 | MCP registered or connected but not callable | Separate enabled, discovery, filtering, fresh visibility and real invocation gates. | AD-08/09 | F12/F15 |
| L03 | S2 bottleneck table | Tool Search was suspected incorrectly | Preserve search behavior; never reset unrelated disabled toolsets. | AD-08/09 | F13 |
| L04 | S1 section 4; S3 section 6 | Skill file existed outside actual usable profile context | Versioned profile-local install and fresh injection proof. | AD-08/13 | F16 |
| L05 | S1 section 5; S3 sections 1-2 | Explicit state needed but layout varied | Dynamic discovery -> reviewed source-bound machine index, any supported path. | AD-03/04 | F04/F66 |
| L06 | S1 section 6 | Existing repositories/profiles could be overwritten | Inspect, own, preview, reconcile; preserve comments and human decisions. | AD-02/03/16 | F06/F07/F62 |
| L07 | S1 sections 7-9 | Clean shell did not cover durable credentials | Scoped metadata/coverage audit, no payload reads or SELECT *. | AD-06 | F19 |
| L08 | S1 section 8 | Provider label did not reveal authentication type | Separate mechanism, effective route, entitlement and overage evidence. | AD-06 | F22 |
| L09 | S1 section 10 | models.yml could override the expected route | Audit profile/model/endpoint overrides across every used role. | AD-06 | F20 |
| L10 | S1 section 11; S3 section 5 | Service environment differed from shell | Probe actual distinct execution surfaces; do not trust shell alone. | AD-08/17/18 | F41/F50 |
| L11 | S1 sections 12-13 | Cron inherited/drifted from expected model | Verify actual installed resolution and pin each job route; invalidate on drift. | AD-18 | F23 |
| L12 | S1 section 14 | Fallback could escape subscription boundary | Audit reachable pools and auxiliaries as well as cross-provider fallback. | AD-06/07 | F21 |
| L13 | S1 sections 15-17; S3 section 12 | Frequent/endless/recursive scheduled agents wasted usage | Bound cycles; cheap pre-inference gate; deny recursive scheduling. | AD-07/13/18 | F39/F53/F68 |
| L14 | S1 section 18; S3 section 8 | Fresh wakes could duplicate milestone work | Single guarded lane, native reconciliation and second-wake test. | AD-11/12 | F30/F35 |
| L15 | S1 section 19; S3 section 23 | Cron still depended on awake local compute | Declare topology; report stale heartbeat; coalesce missed wakes. | AD-17/18 | F54 |
| L16 | S1 sections 20-21; S3 sections 13-15 | Engineering autonomy risked product/criteria/Git authority | Human content-bound approval; protected grant; verified branch != merged base. | AD-04/12/14 | F44/F45/F57 |
| L17 | S2 sections 2-3 | GJC update and Bun dependency failed mid-upgrade | Detect distribution/dependency first; inspect actual version after approved change. | AD-05 | F10/F11 |
| L18 | S2 section 7 | MCP PATH and lifecycle selector were conflated | Absolute outer executable; deterministic MCP PATH; preserve typed selector. | AD-05/09 | F14 |
| L19 | S2 sections 5-6 | Transport smoke hid invalid Bedrock model credentials | Separate route inference from workflow and end-to-end probes. | AD-06/15 | F17/F18 |
| L20 | S2 sections 4, 11-12 | spawn_failed hid worktree_bucket_not_ignored | Preflight actual bucket and run supported low-level lifecycle diagnosis. | AD-03/10 | F09/F27/F28 |
| L21 | S2 sections 13-14 | Unsupported broker.shutdown was mistaken for stale runtime | Use native identity/generation evidence; do not kill guessed processes. | AD-05/19 | F29/F38 |
| L22 | S3 sections 3, 5 | Ruby environment caused apparent verification failure | Validate verifier runtime before attributing failure to implementation. | AD-08/14/17 | F41 |
| L23 | S3 section 4 | Different HEAD did not necessarily stale source verification | Complete relevant-input applicability check, not SHA inequality alone. | AD-14 | F42/F43 |
| L24 | S3 section 9 | list_sessions missed the active coordination state | Multi-source provenance and conflict-aware reconciliation. | AD-11 | F30/F32 |
| L25 | S3 sections 10-11 | Unavailable response coexisted with live progressing execution | Uncertainty reserves lane; durable operation key before dispatch. | AD-11/12 | F31/F33/F34 |
| L26 | S3 section 12 | Waiting synchronously could occupy the supervisor indefinitely | Non-waiting native delegation and bounded observation budget. | AD-13 | F39 |
| L27 | S3 sections 19-21 | Quota guesses/retries wasted limited worker allowance | Supported fresh telemetry; UNKNOWN denies expensive work; local status may continue. | AD-07 | F24/F26/F68 |
| L28 | S3 section 17 | AGENT.md not necessarily auto-injected as project context | Detect and explicitly declare context; no silent rename. | AD-03/13 | F46 |
| L29 | S3 section 18 | Chat/Discord success did not prove cron deployment path | Actual scheduled-worker canary with per-surface fingerprint. | AD-17/18 | F50 |
| L30 | S3 section 22 | Invisible cron work was difficult to trust | Explicit delivery proof and separate delivery/execution status. | AD-17/19 | F55/F56 |
| L31 | S3 section 24 | Previous agent text could become stale truth | Fresh repo/native observations; historical messages are evidence only. | AD-11/14 | F30/F42 |
| L32 | S3 section 16; S2 sections 12, 15-17 | Skipping staged validation hid downstream faults | Authorized gate ladder, one execution, second wake, terminal proof before enable. | AD-15/18/22 | F48/F49/F65 |

## Conflicts resolved explicitly

### D1. Dynamic roadmap discovery versus mandatory explicit state

[S1 section 5] asks for an explicit manifest; [S3 section 1] rejects a single hardcoded roadmap location. V2 accepts arbitrary source layouts and requires a reviewed execution index that references them. This retains both safety objectives instead of silently choosing one report over the other.

### D2. Init as full onboarding versus repo-only init

The incident reports sometimes call the entire infrastructure flow "init". V1.1 separated init from onboard. V2 retains that useful command boundary and adds validate for experiments. The combined guided workflow may present all stages, but init alone never creates sessions, spends model usage, or enables schedules.

### D3. OAuth versus subscription-only billing

[S1] documents OAuth and API-key absence checks. V2 preserves them but does not accept OAuth as sufficient billing proof. Account credit/overage controls and all reachable model routes need separate evidence. This is a strengthened design requirement, supported by the primary-source account documentation [W6, W7], not a claim that the uploaded audit proved zero cost.

### D4. Historical flags/versions versus portable capability checks

Values such as GJC 0.16.6, Bun 1.4.0, a fixed tool count, named model releases, and a historical model_drift_guard flag are fixtures. V2 discovers installed distribution/protocol semantics. Public documentation also changes; adapter proof on the real target remains authoritative.

### D5. Read-only versus plan-only

A planning turn can consume quota and create native state even when no product files change. Passive doctor/preflight do not run it. An explicit validation plan authorizes those costs and artifacts.

### D6. No custom database versus durable idempotency

V1 discouraged a new task database. V2 keeps that non-goal but requires a minimal intent journal and evidence store where native records alone cannot bind pre-send intent to recovered IDs. It is not another task scheduler or execution authority.

### D7. Exact repo root versus managed sibling worktrees

A hard string equality to one repo path can reject legitimate GJC worktrees; a broad parent allowlist grants too much. V2 validates registered managed-worktree membership in the intended project, plus minimal explicit runtime capabilities.

### D8. Profiles/cwd versus enforceable isolation

Profile separation is useful configuration hygiene, not a filesystem security boundary. V2 makes this limitation visible and requires actual negative tests for strict unattended certification. [W8]

### D9. Verify-complete versus safe next milestone

The earlier loop could move from verified code in one worktree to a successor based on main without the predecessor changes. V2 adds VERIFIED_UNMERGED/INTEGRATED and defaults to dependency-integrated base selection. This is a new design safeguard.

### D10. Disable versus stop everything

V2 closes new-work admission before pausing native schedules and separately reports already accepted work. Killing broker processes is not the default stop action. This is a new race/recovery safeguard.

### D11. Skill reuse versus live-file drift

Use one source artifact with versioned profile-local installations, not an unpinned shared mutable skill file. Changing the source does not silently change every enabled deployment.

### D12. Prompt guardrails versus guaranteed enforcement

Critical admission and mutation rules live in deterministic code and tested permission boundaries. A prompt-only deployment is explicitly POLICY_ONLY. V2 cannot honestly promise strict isolation or spending guarantees when a raw terminal/API route bypasses the checks.

## Additional safeguards proposed, not claimed as past incidents

Account-scoped local reservations; disable epochs; compare-before-write change plans; conservative receipt invalidation; delivery-only retries; dirty/binary/untracked recovery preservation; protected control-file enforcement; refusal to infer approval from model confidence; bounded missed-occurrence handling; source-anchored dependency bases; and simulated-versus-live evidence classes are new requirements.

## Crosswalk from V1.1

| Old milestone | V2 replacement |
|---|---|
| M0 Baseline | AD-00 |
| M1 Contract | AD-01, AD-02, AD-04 |
| M2 Init | AD-03, AD-04 |
| M3 Generic supervisor | AD-11, AD-12, AD-13 |
| M4 Nous parity | AD-21 |
| M5 Preflight | AD-05, AD-06, AD-07, AD-15 |
| M6 Hermes provisioning | AD-08, AD-17 |
| M7 Gajae provisioning | AD-09, AD-10 |
| M8 Onboarding | AD-16 |
| M9 Enable/disable/cron | AD-18, AD-19 |
| M10 Registry/status | AD-02 foundations; AD-15/16/17 reporting |
| M11 Hardening | Early AD-02/06/07/12 foundations plus AD-20 audit |
| M12 Second project | AD-22 |
| M13 Release | AD-23 |

Nous parity now follows a complete safety/integration implementation rather than blocking initial development on a half-built generic skill. Live Nous mutation is still not authorized by the parity milestone.


---

# Contract reference: normative implementation targets

These are AutoDev-owned schemas to implement, not native Hermes/GJC configuration files. Version every schema independently. Validate unknown fields, duplicate YAML keys, unsafe tags, oversized inputs, and unsupported major versions. Do not auto-coerce booleans, permissions, paths, or approval states.

## A. PROJECT.yaml

| Field | Type / allowed values | Rules |
|---|---|---|
| schema_version | integer, 2 | Unknown major version is unsupported; migration is previewed and approved. |
| setup_state | draft / configured | Draft may contain null unresolved selections; configured requires structurally complete selections. |
| project.id | UUID string | Stable logical identity. Mint only when missing, once, during an approved init write. |
| project.slug | lowercase slug | Display/CLI alias only. Validate collisions independently. |
| project.name | nonempty string | Preserve existing choice. |
| sources.requirements | list of relative files | Can be empty in draft only. Selection does not itself prove approval. |
| sources.context | list of relative files | Explicit context loading, including AGENT.md where the integration does not auto-load it. |
| sources.discovery.roots | list of relative directories | Bounded within repo; excludes worktrees, .git, dependencies and generated output. |
| sources.execution_index | relative file | Existing supported machine-readable index or default .agent/EXECUTION.yaml. |
| execution.harness | gajae | Other values are unsupported in V2. |
| execution.workflow | approved_roadmap_only | No opportunistic product creation. |
| execution.base_policy | dependencies_integrated | Stacked-base execution not enabled in V2. |
| execution.target_ref | ref string or null in draft | Selected during setup; never assume master/main. |
| execution.max_active_milestones | integer, 1 | Single lane per project. |
| execution.max_primary_actions_per_cycle | integer, 1 | Does not forbid bounded reads needed to reconcile that action. |
| verification.commands | list of command objects | id, argv, cwd, input_paths, network policy, timeout, approval binding. No arbitrary shell string. |
| verification.acceptance_sources | relative references | Sources and exact sections/IDs where possible. Locked digest on approval. |
| verification.require_independent_review | true | Executor self-report insufficient. |
| authority.requested | named permission map | denied / human / autonomous. Request is intersected with operator grant; never self-authorizing. |

Paths are relative to the resolved Git repository and may contain spaces/Unicode. Absolute host paths, credential values, runtime session IDs, and schedule IDs are prohibited here. Empty execution index is structurally valid but supplies no work to dispatch.

## B. EXECUTION.yaml

| Field | Meaning |
|---|---|
| schema_version | 2 |
| project_id | Must match PROJECT.yaml |
| milestones[].id | Unique stable work identifier |
| title | Human title |
| depends_on | Existing milestone IDs; acyclic graph |
| authority_refs | Source path + section/reference + digest; do not fabricate digest placeholders as accepted values |
| acceptance_refs | Source-bound explicit acceptance criteria |
| scope | Allowed product paths, exclusions, and prohibited operations |
| verification_ids | IDs resolving to approved verification command/assessment definitions |
| approval.state | proposed / approved / revoked |
| approval.receipt_ref | Human approval record; required when approved |
| base_policy | Inherit dependencies_integrated unless an approved future version adds another policy |
| evidence_refs | Evidence receipts, never unverified claims converted into COMPLETE |

Invalid dependency IDs, cycles, revoked approval, missing scope/verification, conflicting authority, or changed content digests block selection. Approval of one milestone never implicitly approves later ones.

Sources may be moved without changing product semantics, but resolving a moved reference must preserve identity/digest and go through a reviewed metadata update. A filename heuristic cannot silently relink it to different content.

## C. installation.yaml (host-owned)

Record schema_version, installation_id, project_id, repo_realpath, git_common_dir_realpath, profile identity, service identity, root-binding policy, runtime capability manifest reference, exact selected model routes, redacted auth/account references, resource policy, deployment grant reference, versioned skill hash, delivery target reference, cron ID/ownership, desired_enabled, and deployment_epoch.

Protect it from the supervised worker. If that is not possible in a backend, report POLICY_ONLY assurance. It is not a secrets vault. A credential reference is an opaque handle, not an encrypted copy of a token.

## D. Operation journal record

Required: schema_version, operation_id, installation_id, milestone_id if relevant, operation_kind, plan_digest, grant_digest, canonical_arguments_digest, idempotency_key, created_at, owner_identity, deployment_epoch, operation_state, native_ids, reconciliation_evidence_refs, and terminal result when known.

Canonical request bodies may be persisted only after redaction and exclusion of secret material. Never include a credential in a JSON command argument that will be printed. The safe request identity includes configuration/account reference identity, not token contents.

PREPARED must be durable before send. A fresh process must recover the same idempotency key and canonical arguments. An operation with uncertain outcome consumes its lane until resolved; clearing a cache cannot release it.

## E. Validation receipt

Required: gate_id, evidence_class (SIMULATED/LIVE), probe_id, installation/project IDs, invocation_source, observed_at, expires_at, capability fingerprint, relevant config/skill/grant/authority hashes, repo revision and dirty-input fingerprint, redacted route identity, native trace references, allowed/observed effects, cleanup state, result, invalidation keys.

Results: PASS / FAIL / UNKNOWN / NOT_RUN / BLOCKED_EXTERNAL. A receipt without a native trace cannot prove an actual tool call. A receipt from a different profile/process generation cannot prove a new runtime session is configured.

## F. Mutation grant

A grant binds operator identity/action, installation ID, exact operation classes, repository and managed-worktree membership rule, protected files/refs, allowed provider/account routes, approved product artifact hashes, spending/resource constraints, expiry/revocation epoch, and enforcement backend.

The worker cannot edit its own grant. A stale plan or changed installation invalidates it. Approval UI must show the meaningful impact, not just ask a vague 'Continue?'.

## G. Repair/validation/recovery change plan

Use one plan format: plan ID, kind, target installation/project, expected preconditions/hashes, ordered operations, effects, required permissions, model/network usage, irreversible risks, rollback or preservation steps, verification gates, expiry, and approving operator receipt.

Apply must recheck the previewed preconditions under a lock. A materially changed file/config/native resource invalidates the plan. Do not silently widen an already-approved plan to repair an additional failure.

## H. Compatibility manifest

Record installation distribution, executable realpath/version, optional interpreter requirement, API/protocol generation, supported read/mutation/probe operations, discovered argument schemas, capability hashes, restart/new-session requirements, known error mappings, and supported enforcement mechanisms.

No generic 'latest compatible' claim. An adapter is verified only for its observed contract. Unknown fields in safety-relevant native output result in UNKNOWN/UNSUPPORTED until handled explicitly.

## I. Resource admission result

Required: proposed operation class, effective route/account reference, telemetry source, unit, usage window, reset timestamp if supplied, observed_at, TTL, requested headroom/reservation policy, ALLOW/DENY/UNKNOWN, reason code, next observation time, enforcement limitations.

No provider-neutral percentage inference. No universal five-hour window assumption. Monitoring/verification exceptions apply only to operations that do not themselves consume the blocked resource.

## J. Retention and crash consistency

Prune only terminal native-linked records older than the configured retention horizon; never prune active/uncertain operations, needed approval receipts, or unresolved recovery backups. Retention must not make a previously used native idempotency key eligible for silent reuse.

Use repo locks for repo writes, installation locks for configuration and cycle admission, and account-scoped local locks for resource reservations. Lock ordering must be globally specified and tested to avoid deadlock. Default order: account admission lock -> installation lock -> repo write lock, with short critical sections; long inference is never performed while holding multiple locks.

If dispatch journaling and account reservation cannot be committed atomically across local stores, represent pending states explicitly and reconcile after crash. Do not claim a filesystem rename makes a multi-system transaction atomic.


---

# Milestone execution plan

## Shared session contract

Each AD identifier is one bounded `ralplan -> ralph` work unit. The work list is implementation scope; acceptance criteria are the completion contract. A model's estimated session duration is not a reason to omit tests. Split a genuinely oversized unit into reviewed subplans without changing its criteria.

Before coding, inspect the current repo, predecessor evidence, relevant sources, and any existing implementation. Create `docs/plans/AD-XX-plan.md`. After coding, write `docs/verification/AD-XX.md` containing changed files, commands and exit codes, acceptance matrix with evidence links, effect audit, known limits, and next-session handoff. Do not mark future milestones implemented merely because interfaces were stubbed; unsupported stubs must fail closed.

Automated tests should map to the F01-F70 fault IDs. Suggested paths below are organizational guidance, not permission for large unrelated refactors. The Python package may use `src/autodev/`, `tests/unit/`, `tests/contracts/`, `tests/integration/`, and `tests/faults/`. The expected commands after packaging foundations are `python -m autodev --help` and `python -m pytest`; record the actual environment used.

Evidence states for the milestone: `CODE_VERIFIED`, `LIVE_VALIDATION_BLOCKED`, `ACCEPTED`, or `FAILED`. A code milestone may complete its specified mock/contract tests before active validation exists, but that never certifies a deployment. A milestone whose own criteria require a live result remains blocked until that result exists. Do not claim the complete product is accepted with mandatory live gates outstanding.

Unless a milestone explicitly requires an approved live operation, its tests run in temporary repositories and synthetic configuration, not the live Nous environment. No merge, forced cleanup, global upgrade, credential mutation, or unapproved external message is authorized by this roadmap.

## AD-00 - Baseline, scope lock, and evidence inventory

**Depends on:** none. **Purpose:** protect the working system before generalization.

### Work
- Scaffold the package/CLI/test runner and document V2 scope and non-goals.
- Import the three source reports as referenced evidence records; preserve hashes/titles and distinguish observations from proposed requirements.
- Capture a sanitized baseline inventory using provided files first. A live read-only export requires an explicit approved scope; never dump credential files.
- Represent READY, active, uncertain, verifying, human-blocked, and completed examples as synthetic fixtures when no real trace exists. Label them synthetic.
- Add an environment manifest template and a no-live-mutation test harness.

### Success criteria
- **AD-00-AC1:** package imports, CLI help exits successfully, and the initial test suite passes.
- **AC2:** each input has a traceable identity and no fabricated live result.
- **AC3:** baseline report identifies every unknown needed for later compatibility probing.
- **AC4:** a file/process effect audit shows no modification to Nous, Hermes, GJC, cron, or account state.
- **AC5:** future milestone commands are either absent or explicit non-passing placeholders.

**Tests/evidence:** package smoke, source-hash test, secret canary redaction, effect audit; F63 principles.
**Deliverables:** package scaffold, baseline report, fixture manifest, scope/decision log.
**Stop/rollback:** stop after documentation and scaffold; remove only newly owned scaffold files if rejected.

## AD-01 - Schemas, identities, authority, and orthogonal states

**Depends on:** AD-00. **Purpose:** make ambiguous states representable without unsafe defaults.

### Work
- Implement versioned models for PROJECT, execution index, installation binding, grants, receipts, operations, and command results using the contract reference.
- Distinguish draft structural configuration, configured deployment, certification, admission, execution, quota, and delivery states.
- Implement stable project/installation identity and slug collision checks.
- Define human approval bound to content and permission intersection; generated configuration cannot grant authority.
- Provide draft/configured fixtures and a preview-only migration interface from V1.

### Success criteria
- **AD-01-AC1:** draft with explicit unknowns loads, but cannot be admitted for execution.
- **AC2:** invalid/duplicate YAML keys, unsafe tags, unknown schema versions, malformed permissions, and root escapes fail with field-specific errors.
- **AC3:** ALIGNED, READY_FOR_ENABLE, and READY_TO_DISPATCH have different tested predicates.
- **AC4:** cloned project identity is not silently adopted as the same machine installation.
- **AC5:** no approval or credential values are inferred from a provider name or a filename.

**Tests/evidence:** F02, F03, F08, F66; schema fixtures and permission-intersection truth table.
**Deliverables:** schemas/models, version migration plan model, identity and state tests.
**Stop/rollback:** no real repo/config conversion; migrations remain planned until init applies them.

## AD-02 - Safe storage, command execution, locks, and journals

**Depends on:** AD-01. **Purpose:** build safety primitives before provisioning.

### Work
- Implement atomic file replacement, expected-content checks, restrictive permissions, ownership metadata, and recoverable write records.
- Implement installation/repo/account locks with a documented lock order and short critical sections.
- Build a typed subprocess runner with explicit argv/cwd/environment, timeouts, bounded output, redaction, and no arbitrary shell interpolation.
- Add operation records written durably before native mutation and safely loaded after interruption.
- Add passive Git inspection that disables optional mutation/external helper paths relevant to the supported version.

### Success criteria
- **AD-02-AC1:** interrupted write preserves a parseable old or new file and exposes recovery status.
- **AC2:** concurrent writers cannot lose another project record or overwrite a changed preview.
- **AC3:** stale PID/lock evidence is not enough to steal ownership.
- **AC4:** command logs and exception paths do not expose seeded secret canaries.
- **AC5:** canonical operation request changes cannot reuse the same identity silently.

**Tests/evidence:** F07, F34, F36, F38, F69, F70, including injected disk failure and process death.
**Deliverables:** storage, locking, command, Git-read, journal modules and fault tests.
**Stop/rollback:** temporary fixtures only; do not touch real credential or broker databases.

## AD-03 - Friendly init and conservative artifact discovery

**Depends on:** AD-01, AD-02. **Purpose:** align repos without infrastructure effects.

### Work
- Implement bounded discovery of context, requirements, execution maps, plans, acceptance sources, and test/toolchain metadata.
- Preserve explicit existing references, comments, formatting, and user choices. Resolve ambiguity interactively or return NEEDS_INPUT.
- Generate draft PROJECT and execution-index files only after a preview; `--yes` never approves product authority.
- Detect managed worktree strategy and offer a minimal verified ignore change where needed; tracked worktree content is a blocker, not an auto-delete target.
- Implement `--dry-run`, deterministic JSON, byte-stable reruns, and context-file recognition diagnostics.

### Success criteria
- **AD-03-AC1:** empty/incomplete repo produces honest draft state, not invented PRD/milestones.
- **AC2:** existing valid configuration is byte-identical after a no-op rerun.
- **AC3:** two equally plausible roadmaps require a choice; non-TTY mode does not guess.
- **AC4:** init executes no project hooks/scripts, model calls, MCP sessions, or profile configuration.
- **AC5:** unusual paths and Git states are handled safely or explicitly rejected.

**Tests/evidence:** F01, F04-F06, F09, F46, F67; before/after file hashes and effect audit.
**Deliverables:** init/discovery modules, round-trip write support, CLI, fixture suite.
**Stop/rollback:** only reviewed repository alignment files may change; use recorded original bytes to roll back owned edits.

## AD-04 - Execution-index compiler and approval binding

**Depends on:** AD-03. **Purpose:** combine flexible layouts with deterministic task selection.

### Work
- Import candidate milestones/dependencies from explicitly selected artifacts into a proposed machine index without copying product prose.
- Validate dependency graph, source digests, acceptance references, target base, and verification IDs.
- Implement `autodev approve --milestone <id> --plan/--apply-plan` with operator review, approval receipt generation and revocation semantics; do not infer approval from folder names or earlier milestones.
- Make changed/missing source content invalidate affected approval.
- Define the dependency-integrated policy and VERIFIED_UNMERGED versus INTEGRATED states.

### Success criteria
- **AD-04-AC1:** nested or unconventional plan layouts work without `.omx/ROADMAP.yaml` being mandatory.
- **AC2:** files under a 'draft' directory are assessed from selected authority content, not blanket rejected or approved.
- **AC3:** imports remain proposed until explicit content-bound approval.
- **AC4:** cycle, missing dependency, revoked approval, or digest drift blocks readiness.
- **AC5:** predecessor code absent from the selected base blocks the successor.

**Tests/evidence:** F04, F44, F45, F66; graph and approval mutation tests.
**Deliverables:** execution-index adapter/compiler, approval model integration, explain-selection output.
**Stop/rollback:** never edit original plans/criteria to make the index validate; retain import proposals separately.

## AD-05 - Native capability and runtime compatibility adapters

**Depends on:** AD-02. **Purpose:** replace guessed commands with observed contracts.

### Work
- Build adapters that detect actual Hermes/GJC installation distribution, executable paths, version/protocol generation, and available native operations.
- Check Bun only for distributions that need it; read supported-version requirements rather than freeze historical numbers.
- Distinguish outer MCP executable from managed-session lifecycle selector.
- Implement sanitized compatibility snapshots, explicit UNSUPPORTED outcomes, and invalidation on executable/generation change.
- Add a preview-only shared-runtime upgrade plan; no automatic upgrade or restart.

### Success criteria
- **AD-05-AC1:** both Bun-backed and standalone-binary fixtures are classified correctly.
- **AC2:** incompatible runtime fails before any configuration mutation.
- **AC3:** unknown safety-relevant native API cannot fall through to guessed flags.
- **AC4:** unsupported shutdown operation is not diagnosed as stale broker.
- **AC5:** post-upgrade executable inspection, not installer text, determines the installed state.

**Tests/evidence:** F10, F11, F14, F29; sanitized native-help/output contract fixtures. Authorized local capability inspection may establish a supported target; no sessions or model calls.
**Deliverables:** native capability manifest, adapter interfaces, compatibility report.
**Stop/rollback:** runtime unchanged; unsupported target remains blocked.

## AD-06 - Credential metadata and effective billing-route audit

**Depends on:** AD-01, AD-02, AD-05. **Purpose:** prove routing coverage without exposing secrets.

### Work
- Resolve all configured inference roles: supervisor, cron, GJC workflow roles, reviewer, auxiliary tasks, pool rotation and fallback endpoints.
- Inspect only authorized known metadata sources; support native redacted inspection first and versioned read-only DB metadata second.
- Detect model overrides and custom endpoints; distinguish auth mechanism, route selection, entitlement evidence, and account overage state.
- Produce a coverage report with PASS/DENY/UNKNOWN and remediation, not raw token dumps.
- Implement strict policy evaluation without deleting credentials or switching accounts/providers automatically.

### Success criteria
- **AD-06-AC1:** a hidden eligible API credential/override produces denial or explicit uncertainty even with a clean shell.
- **AC2:** OAuth alone cannot yield verified subscription-only billing.
- **AC3:** all eligible pool/fallback/auxiliary paths are resolved or blocked.
- **AC4:** unknown database schema and inaccessible service settings are UNKNOWN, not silently safe.
- **AC5:** no test secret appears in output, journal, error, or support report.

**Tests/evidence:** F17, F19-F22; synthetic stores only until a scoped read is separately authorized.
**Deliverables:** auth metadata adapters, route graph, billing policy report, coverage matrix.
**Stop/rollback:** audit only; no login, token refresh, database writes, or account-setting changes.

## AD-07 - Resource admission and shared-account budgets

**Depends on:** AD-06. **Purpose:** block expensive work before it starts.

### Work
- Implement supported telemetry adapters and ALLOW/DENY/UNKNOWN results with observed time, reset/window/unit, and TTL.
- Apply gates to supervisor inference, worker delegation, role fan-out, and external-cost verification independently.
- Add local account-scoped reservations and release/reconciliation of uncertain admissions.
- Persist retry/circuit-breaker state across cron cycles and distinguish quota exhaustion from transient transport failure.
- Enforce configured budgets using supported native limits; declare unenforceable limits explicitly.

### Success criteria
- **AD-07-AC1:** unknown/stale required usage blocks expensive work without another LLM call.
- **AC2:** two projects cannot both consume one local admission reservation.
- **AC3:** monitoring continues deterministically where it does not consume the blocked resource.
- **AC4:** time elapsed never substitutes for authoritative reset evidence.
- **AC5:** quota failure never enables a paid fallback or a new credential automatically.

**Tests/evidence:** F18, F24-F26, F68; fake clock, simulated shared accounts and boundary values.
**Deliverables:** resource guard, account locking integration, circuit breaker, admission explain output.
**Stop/rollback:** no purchases, no hardcoded 20%/85% global thresholds, no unsupported quota scraping.

## AD-08 - Hermes profile, skill installation, and deterministic environments

**Depends on:** AD-03, AD-05, AD-06. **Purpose:** configure owned profiles without global drift.

### Work
- Implement profile creation and explicit adoption of compatible existing profiles using ownership markers.
- Install one pinned generic-skill artifact per profile with content hash and enabled/readiness checks; use a policy stub until AD-13 is ready, never claim supervision certification.
- Configure explicit cwd and profile-scoped interpreter/PATH initialization without editing global shell files.
- Inspect disabled toolsets and Tool Search state; propose surgical repairs rather than overwrite the whole list.
- Record loaded-versus-on-disk generation and fresh-session requirements.

### Success criteria
- **AD-08-AC1:** rerun preserves unrelated profile settings and produces no duplicate profile.
- **AC2:** another project's same-slug profile cannot be adopted silently.
- **AC3:** a global-only or old-hash skill does not pass profile availability checks.
- **AC4:** explicit shell configuration has a reversible, owned diff.
- **AC5:** config changes cannot be certified using an already-running stale process.

**Tests/evidence:** F12, F13, F16, F41, F62; mocked CLI and temporary profile homes. Live profile mutation requires an approved apply plan.
**Deliverables:** profile/skill/environment provisioners and safe adoption plan.
**Stop/rollback:** no gateway restart, token copying, model probe, or cron creation.

## AD-09 - MCP configuration and actual-tool-access probe

**Depends on:** AD-05, AD-08. **Purpose:** distinguish transport from callable capability.

### Work
- Provision the supported GJC MCP definition with exact executable, environment, selector semantics and minimal permission surface.
- Implement separate results for configured/enabled/started/discovered/filtered/visible/callable stages.
- Design a fresh-Hermes-session probe requiring one actual read-only Coordinator invocation and native tool trace.
- Preserve unrelated disabled entries and Tool Search behavior; a repair removing a denial requires reviewed authority.
- Match capability schemas/semantics instead of asserting a fixed tool count.

### Success criteria
- **AD-09-AC1:** green MCP discovery with blocked model access is a failed callable gate.
- **AC2:** an LLM saying 'tools available' without a real call cannot pass.
- **AC3:** terminal PATH and MCP PATH are independently diagnosed.
- **AC4:** the lifecycle selector is not rewritten into an arbitrary absolute shell command.
- **AC5:** discovery/probe implementations never create a coding turn implicitly.

**Tests/evidence:** F12-F15; trace fixtures. Actual token-using fresh-session proof is performed under AD-15/17 authorization, not hidden in onboard.
**Deliverables:** MCP provisioner, stage diagnostics, active-read probe definition.
**Stop/rollback:** restore only AutoDev-owned changed MCP fields on failed apply; preserve external entries.

## AD-10 - Managed-worktree and broker lifecycle probes

**Depends on:** AD-05, AD-09. **Purpose:** surface lifecycle errors below sanitized Coordinator failures.

### Work
- Implement repo/bucket writability and ignore prerequisites without manual worktree creation.
- Add a supported low-level lifecycle probe with unique operation ID, native idempotency, exact root identity, and explicit probe effects.
- Map sanitized spawn errors to safe lower-level diagnosis, including bucket-not-ignored and worktree-in-use.
- Record broker identity/generation, original repo, managed worktree, session, and cleanup ownership.
- Add guarded cleanup planning: only proven disposable, inactive, unchanged probe resources are eligible.

### Success criteria
- **AD-10-AC1:** direct TUI success cannot satisfy lifecycle readiness.
- **AC2:** ignored-bucket prerequisite fails before creation and reports a concrete cause.
- **AC3:** successful managed worktree maps back to the intended project identity.
- **AC4:** generic spawn failure does not produce repeated new sessions.
- **AC5:** cleanup preserves unknown/untracked/user-owned work and reports CLEANUP_PENDING.

**Tests/evidence:** F09, F27, F28, F58; contract tests plus an explicitly authorized live disposable lifecycle probe when validation runs.
**Deliverables:** lifecycle diagnostic adapter and probe/cleanup contracts.
**Stop/rollback:** GJC owns lifecycle; no custom worktree manager, global broker kill, or broad allowlist.

## AD-11 - Multi-source execution reconciliation

**Depends on:** AD-04, AD-05, AD-10. **Purpose:** determine reality before another mutation.

### Work
- Normalize coordination status, active/durable turns, live SDK status, event sequence, questions, and listings with timestamps/provenance.
- Implement conflict/uncertainty handling and exact milestone/operation correlation.
- Treat active/uncertain work as occupying the single execution lane.
- Distinguish environmental/provider/transport/workflow/implementation errors without claiming a root cause not in evidence.
- Build replay fixtures for the uploaded stale-list and unavailable-but-streaming incidents.

### Success criteria
- **AD-11-AC1:** stale empty/session listing does not override authoritative active-turn evidence.
- **AC2:** advancing live activity prevents classification as conclusively failed based only on an observation error.
- **AC3:** irreconcilable sources yield UNCERTAIN and prohibit dispatch.
- **AC4:** a prior supervisor message is never canonical execution state.
- **AC5:** stale broker/process metadata does not justify stealing ownership without native reconciliation.

**Tests/evidence:** F30-F32, F38 with fake clocks, broker generations, reordered observations, and event sequences.
**Deliverables:** normalized observation model, reconciler, explain-state report.
**Stop/rollback:** read-only module; no repair or dispatch yet.

## AD-12 - Guarded dispatch, idempotency, and fencing

**Depends on:** AD-02, AD-07, AD-11. **Purpose:** enforce mutation admission outside model prose.

### Work
- Implement one guarded path for allowed Coordinator mutations, using native checks where supported and a narrow adapter where required.
- Enforce project/root/grant/plan/resource/active-work predicates immediately before send.
- Durably persist operation identity and canonical request before dispatch; reconcile uncertain acknowledgement with the same identity.
- Fence disabled/stale epochs and serialize manual/scheduled calls through the same boundary.
- Detect and block raw-tool/terminal bypass in the supported enforcement backend; otherwise expose POLICY_ONLY and deny strict certification.

### Success criteria
- **AD-12-AC1:** crash-after-send retry does not create a second logical execution.
- **AC2:** changed arguments with the same key are rejected.
- **AC3:** concurrent triggers produce at most one admitted primary operation.
- **AC4:** an old epoch cannot start new mutation after disable admission closes.
- **AC5:** required bypass tests fail safely or the deployment cannot be certified ENFORCED.

**Tests/evidence:** F33-F37, F57; kill the guard at each journal/send/ack boundary in fixtures.
**Deliverables:** admission/mutation guard, narrow native bridge, race tests, assurance report.
**Stop/rollback:** no production dispatch; accepted in-flight operations are reconciled, not blindly cancelled.

## AD-13 - Generic supervisor and bounded cycle

**Depends on:** AD-04, AD-11, AD-12. **Purpose:** generalize policy without giving it uncontrolled authority.

### Work
- Implement the project-neutral supervisor skill and status/dry-run/supervise modes.
- Implement guarded cycle orchestration with bounded read budgets and one primary action.
- Route implementation-local questions to evidence-backed answers and protected choices to human blocks.
- Dispatch asynchronously, record IDs, and exit; persist repeated failure signatures across cycles.
- Load declared context explicitly and prevent agent scheduling through native permissions, not text alone.

### Success criteria
- **AD-13-AC1:** no Nous filenames/milestone logic exists outside labeled fixtures/examples.
- **AC2:** default mode is dry-run and cannot mutate native execution.
- **AC3:** active work is monitored/reconciled, not duplicated.
- **AC4:** configured cycle timeout ends supervision without discarding durable worker identity.
- **AC5:** same failure across fresh cycles reaches the persistent retry limit rather than looping forever.

**Tests/evidence:** F39, F40, F46, F53 plus reconciler/guard tests; static skill validation is necessary but not live behavioral proof.
**Deliverables:** versioned generic skill, cycle command, bounded report contract.
**Stop/rollback:** no self-modification or future milestone execution; keep old Nous skill intact.

## AD-14 - Independent verification and revision applicability

**Depends on:** AD-04, AD-11, AD-13. **Purpose:** make completion reproducible.

### Work
- Resolve approved command/acceptance inputs and validate the actual execution toolchain before judging code.
- Execute authorized checks in the implementation worktree and collect exit codes/artifact hashes.
- Implement conservative applicability analysis covering source/tests/fixtures/lockfiles/build scripts/config/runtime/authority and dirty files.
- Detect approved-plan/criteria drift and classify verified-unmerged versus integrated state.
- Require independence from executor self-report and explicit evidence per acceptance criterion.

### Success criteria
- **AD-14-AC1:** Ruby/runtime mismatch is ENVIRONMENT_FAILURE, not automatic code repair.
- **AC2:** documentation-only change can reuse evidence only when its complete dependency set is proven unaffected.
- **AC3:** lockfile/test/command/toolchain change invalidates related evidence.
- **AC4:** edits weakening the locked contract cannot produce accepted completion.
- **AC5:** unmerged predecessor blocks default successor base selection.

**Tests/evidence:** F41-F45; controlled revisions, renamed/deleted/untracked files, failing checks, and unchanged source hashes.
**Deliverables:** verifier, applicability engine, criterion matrix/report generator.
**Stop/rollback:** no rewrite of tests/specification to manufacture PASS; no implicit merge.

## AD-15 - Doctor, active validation ladder, and admission receipts

**Depends on:** AD-06-AD-14. **Purpose:** implement the boundary between inspection and experiments.

### Work
- Implement passive doctor/preflight and active validate-plan/apply commands using G00-G13 gate definitions.
- Add actual minimal-model, direct-workflow, MCP-read, managed-lifecycle, end-to-end plan, diagnostic-execution, second-wake, and terminal-check probes.
- Make probe effects, tokens, routes, timeouts, allowlisted diffs, native IDs, and cleanup explicit.
- Persist versioned receipts with fingerprints/TTL/invalidation and evidence class.
- Build enable/dispatch predicates; unperformed gateway/cron gates remain NOT_RUN until AD-17/18.

### Success criteria
- **AD-15-AC1:** passive commands trigger zero model calls, messages, source execution, or native session creation.
- **AC2:** applying a validation plan runs only approved probe effects and bounds.
- **AC3:** a model/default route passes only its own distinct route gate, not every role.
- **AC4:** simulated, stale, different-profile, or untraced results cannot satisfy a required live gate.
- **AC5:** failure at a prerequisite suppresses dependent paid/mutating probes and supplies layered remediation.

**Tests/evidence:** F47-F49, F65 plus all gate-specific faults. Obtain actual authorized LIVE G03-G11 evidence in an isolated pilot; otherwise label that validation blocked.
**Deliverables:** doctor/preflight/validate commands, receipts, probe plan UI, readiness report.
**Stop/rollback:** no recurring autonomy. Preserve failed-probe artifacts when cleanup ownership/liveness is uncertain.

## AD-16 - Idempotent onboarding and reviewed remediation

**Depends on:** AD-03, AD-08-AD-10, AD-15. **Purpose:** compose setup without hidden execution.

### Work
- Implement onboard using the same init/discovery code path; unresolved init stops before infrastructure mutation.
- Assemble an ordered change plan with field ownership, expected hashes, impact, verification, and rollback.
- Apply only approved profile/MCP/skill/environment/registry changes and verify native readback.
- Implement recoverable partial provisioning and per-field repair plans.
- Implement `status` and `list` over the registry/health model, resolving project slug/path/current directory and reporting alignment, configuration, validation, admission and known native state without live probes.
- Preserve active schedules and live Nous configuration; no model probes or live sessions hidden in onboard.

### Success criteria
- **AD-16-AC1:** repeated onboard converges without duplicate profile/MCP/registry state.
- **AC2:** partial Hermes success followed by GJC failure can be reconciled safely on rerun.
- **AC3:** a changed previewed file/resource stops apply rather than overwriting it.
- **AC4:** unrelated/global configuration is byte/semantically unchanged as appropriate.
- **AC5:** result distinguishes CONFIGURED from VALIDATED/READY_FOR_ENABLE and recommends the authorized next step.
- **AC6:** `status`/`list` support stable JSON, multiple projects, path/slug lookup, and explicit UNKNOWN native state without mutating or spawning a probe.

**Tests/evidence:** F05-F07, F62; injected native command failures at each provisioning stage.
**Deliverables:** onboard orchestrator, ownership reconciliation, repair-plan apply path.
**Stop/rollback:** rollback touches only owned changed fields, never destroys user profiles/worktrees or reverses accepted native work blindly.

## AD-17 - Actual gateway environment and delivery proof

**Depends on:** AD-08, AD-15, AD-16. **Purpose:** verify the resident runtime, not just CLI behavior.

### Work
- Identify the actual profile/service owner and loaded generation without modifying shared services automatically.
- Add approved gateway probes for cwd, interpreter/executables, declared context, skill hash, and actual GJC read access.
- Bind an explicit notification destination, send a bounded approved test, and record acknowledgement/correlation.
- Separate execution and delivery outcomes and implement native-backed delivery-only retries where supported.
- Report local host sleep/offline limitations and stale heartbeat without claiming an offline local alert.

### Success criteria
- **AD-17-AC1:** wrong gateway Ruby/PATH is caught even when interactive shell passes.
- **AC2:** a gateway result is traceable to the intended profile/process generation.
- **AC3:** wrong/unavailable Discord destination does not pass delivery readiness.
- **AC4:** message retry cannot initiate another coding dispatch.
- **AC5:** logs/messages redact secret canaries and avoid full environment export.

**Tests/evidence:** F41, F55, F56, F63 plus authorized live gateway/test-message receipts. Cron-specific environment remains unproven until AD-18.
**Deliverables:** runtime adapter, delivery health/reporting, gateway validation receipts.
**Stop/rollback:** no shared-service restart or chat-wide configuration changes without separate approval.

## AD-18 - Paused canary, guarded cron, and explicit enablement

**Depends on:** AD-07, AD-12, AD-15, AD-17. **Purpose:** certify and enable the actual scheduled path.

### Work
- Create/reconcile a natively paused or otherwise provably unscheduled AutoDev-owned canary; do not create-active-then-pause.
- Pin effective model/provider/endpoint, workdir, skill, guard entrypoint, recursion/concurrency behavior using the installed capability adapter.
- Run one approved scheduled-worker canary with no product dispatch, verify actual environment/route/delivery, and persist a receipt.
- Implement final fresh preflight + operator grant + exact schedule-ID activation; never match ambiguous names.
- Implement cheap pre-inference gating and bounded missed-occurrence coalescing using native scheduling facilities.

### Success criteria
- **AD-18-AC1:** no recurring occurrence can fire before explicit activation.
- **AC2:** global model/config drift cannot silently change the effective approved job route.
- **AC3:** repeated enable retains exactly one owned schedule; unknown/duplicate ownership blocks.
- **AC4:** scheduled invocation proves its own cwd/toolchain/skill/guard/delivery, independent of interactive tests.
- **AC5:** blocked wake performs no LLM call; agent cannot create recursive schedules through permitted surfaces.

**Tests/evidence:** F23, F50-F54, F68; authorized LIVE G12 canary plus native contract tests.
**Deliverables:** cron adapter, paused-canary validation, enable command, schedule ownership evidence.
**Stop/rollback:** on failure leave admission closed and schedule paused; never substitute an active schedule for missing paused semantics.

## AD-19 - Disable, restart reconciliation, and safe recovery

**Depends on:** AD-11, AD-12, AD-16, AD-18. **Purpose:** preserve work when operation is interrupted.

### Work
- Implement disable with admission closure/epoch fencing first, exact schedule pause second, and truthful active-work reporting.
- Implement restart reconciliation for outstanding journal operations and new native generations.
- Implement read-only recovery plans that inventory uncommitted, binary, untracked, and native-state evidence.
- Support an approved preserve-and-transfer path to a fresh GJC-owned worktree only after original execution is known inactive.
- Separate worker cancellation, notification retry, configuration repair, and implementation recovery.

### Success criteria
- **AD-19-AC1:** stale scheduled workers cannot initiate a new operation after admission closes.
- **AC2:** failed pause is reported as schedule uncertainty, not falsely as everything stopped.
- **AC3:** active work is not killed or deleted by disable.
- **AC4:** recovery preserves original dirty/untracked/binary data and never assumes a commit exists.
- **AC5:** unknown liveness forbids automatic duplicate recovery; old/new IDs and transferred diff are auditable.

**Tests/evidence:** F37, F55, F59-F61; restart and preservation drills in disposable repositories.
**Deliverables:** disable/recover/repair integration, preservation receipts, rollback/restore checks.
**Stop/rollback:** never reset/delete the original implementation as cleanup; retain recovery backups until separately authorized retention.

## AD-20 - Adversarial acceptance and enforcement audit

**Depends on:** AD-00-AD-19. **Purpose:** verify the safety claims independently of happy paths.

### Work
- Execute the full F01-F70 matrix, including process death, uncertainty, environment drift, disabled tools, hidden routes and wrong bases.
- Test bypass attempts through raw MCP, terminal, control-file edits, outside-root writes, protected Git actions and credential routes in the selected backend.
- Run manual/scheduled overlap and shared-account concurrency drills.
- Verify every failure maps to a layer, next safe action, retained evidence, and bounded retry policy.
- Record assurance limitations and any unsupported gates as release blockers.

### Success criteria
- **AD-20-AC1:** every fault ID has an automated result or explicitly justified LIVE/BLOCKED_EXTERNAL result.
- **AC2:** no injected failure causes duplicate logical implementation or unapproved permission broadening.
- **AC3:** no secret canary leaks and no dirty work is lost.
- **AC4:** certified isolation is supported by actual negative tests, not cwd naming.
- **AC5:** all required live G13 results pass before strict unattended release.

**Tests/evidence:** full F01-F70; independent test execution and signed-off verification matrix.
**Deliverables:** adversarial report, safety regression tests, release-blocker list.
**Stop/rollback:** do not weaken limits or label failures acceptable to reach a green dashboard.

## AD-21 - Nous shadow parity and controlled migration plan

**Depends on:** AD-20. **Purpose:** prove compatibility without disrupting the golden deployment.

### Work
- Build a reviewed Nous project binding using dynamically selected authority artifacts and current evidence.
- Compare old and generic supervisors on the same read-only snapshot: milestone, active/uncertain work, allowed action, verifier applicability, quota and human blocks.
- Keep existing live schedule and worker ownership intact during comparison; never create a second mutating supervisor.
- Produce a migration plan that drains/reconciles old ownership, preserves records, validates the new binding, and enables at most one owner after explicit approval.
- Recheck Nous after pilot provisioning to catch shared global drift.

### Success criteria
- **AD-21-AC1:** material decisions agree or every difference is justified against the approved evidence hierarchy.
- **AC2:** old production configuration remains unchanged during shadow validation.
- **AC3:** existing GJC IDs are reconciled rather than replaced unnecessarily.
- **AC4:** migration rollback restores known owned settings without duplicate active schedules.
- **AC5:** a required live snapshot unavailable to the coding agent is BLOCKED_EXTERNAL, not invented parity.

**Tests/evidence:** F30, F41, F44, F64 and a real read-only parity report under approved access.
**Deliverables:** Nous binding proposal, comparison report, staged migration/rollback plan.
**Stop/rollback:** executing migration is a separate operator decision; this milestone does not grant blanket permission to change Nous.

## AD-22 - Independent second-project pilot

**Depends on:** AD-20, AD-21. **Purpose:** prove reuse instead of a Nous-only refactor.

### Work
- Use an operator-approved disposable but real Git project with no manually configured Hermes/GJC pipeline.
- First test incomplete requirements/index: init aligns draft safely and enable remains rejected.
- Provide a genuinely approved tiny milestone and verify init, onboard, validate, preflight, and explicit enable without hand-editing runtime configuration.
- Complete one bounded action, perform independent second-wake and terminal verification, observe delivery, and disable.
- Prove project isolation and no changes to Nous/shared global settings.

### Success criteria
- **AD-22-AC1:** the identical generic supervisor artifact is used unchanged.
- **AC2:** no manual Hermes/MCP/cron editing is needed; any workaround becomes a bug/regression test.
- **AC3:** live execution has native IDs, one logical operation, allowed diff, independent verification, and delivery evidence.
- **AC4:** incomplete project and cross-project negative scenarios fail safely.
- **AC5:** disable preserves usable project state and Nous remains healthy.

**Tests/evidence:** F05, F48, F57, F58, F65 plus end-to-end live operator runbook.
**Deliverables:** second-project pilot report, receipts, reproduction instructions, discovered regression tests.
**Stop/rollback:** no auto-generated product approval; no use of a sensitive production project as a test fixture.

## AD-23 - Release, operator runbooks, and evidence freeze

**Depends on:** AD-22. **Purpose:** ship a usable, honestly bounded tool.

### Work
- Finalize install/package tests, CLI help/JSON compatibility, schemas, command reference, and supported-platform matrix.
- Document init versus onboard versus validate versus enable; add a short happy-path guide and actionable failure examples.
- Document billing assurance limits, profile versus sandbox isolation, quota unknowns, disable versus cancel, recovery, and host uptime.
- Freeze versioned supervisor/adapters and publish a migration/rollback procedure for future upgrades.
- Audit all advertised features against actual tests and live receipts; remove inaccurate claims rather than hiding blockers.

### Success criteria
- **AD-23-AC1:** clean local installation and every CLI help/JSON contract test pass.
- **AC2:** a reader can onboard a new supported project from the runbook without undocumented edits.
- **AC3:** all mandatory release/live criteria have traceable evidence; unsupported targets are clearly marked.
- **AC4:** no secrets, private raw configuration, or unfinished required TODO is in the release artifact.
- **AC5:** final release report states supported guarantees and limitations without claiming universal foolproof or exactly-once behavior.

**Tests/evidence:** full regression suite, build/install test, document/example validation, Nous and second-project evidence audit.
**Deliverables:** distributable package, documentation, release notes, checksums, V2 verification report.
**Stop/rollback:** release only the tested version; do not add new features during final packaging.


---

# Acceptance and fault-injection matrix

This is a normative test backlog, not a report of tests already executed. Every case needs an evidence link in the implementation. Existing incident-derived tests and additional design tests are both included; source mapping is in 01-EVIDENCE-AND-DECISIONS.md.

## Evidence requirements

For each case record fixture/setup, exact invocation, injected failure point, observed exit/result, attempted/accepted mutation counts, file hashes before/after, native IDs where relevant, secret-canary result, and retained recovery evidence. Use a deterministic fake clock for expiry/retry tests. Clearly label SIMULATED versus LIVE.

Unit/contract tests run without production credentials. Negative OS/network/credential tests use an authorized isolated deployment. A skipped mandatory live test is BLOCKED_EXTERNAL, not PASS.

| ID | Injected condition / scenario | Required outcome | Primary owner |
|---|---|---|---|
| F01 | Non-Git, bare, unborn or unsupported worktree input | Align only where safe; no automatic initial commit or fake worktree readiness. | AD-03 |
| F02 | Malformed YAML, duplicate keys, unsafe tags or invalid permission enum | Reject with field-specific error; preserve original bytes and deny mutation. | AD-01 |
| F03 | Traversal, symlink escape or case-colliding root | Reject escaped/ambiguous identity before reading or writing target content. | AD-01 |
| F04 | Two roadmaps or conflicting authority artifacts | Prompt in interactive mode; NEEDS_INPUT without guessing otherwise. | AD-03/04 |
| F05 | Fresh repo without PROJECT/index/approved plan | Generate only reviewed drafts; no product approval or enablement. | AD-03/16 |
| F06 | Repeat init/onboard on already-correct user config | No duplicate artifacts/profiles; valid existing bytes/comments preserved. | AD-03/16 |
| F07 | File/native resource changes between preview and apply | Expected-hash check rejects stale plan; no overwrite. | AD-02/16 |
| F08 | Unknown schema or major native contract version | Return UNSUPPORTED, never coerce into a known mutating schema. | AD-01/05 |
| F09 | Unignored in-repo bucket or already tracked worktree content | Block lifecycle; propose exact ignore repair; never delete tracked work. | AD-03/10 |
| F10 | Old Bun for Bun-backed GJC; standalone binary without Bun | First case blocked from runtime metadata; second not falsely rejected. | AD-05 |
| F11 | Installer says success but executable/generation is inconsistent | Inspect actual binaries; mark partial/drifted; invalidate receipts. | AD-05 |
| F12 | MCP defined/enabled but denied by agent toolset policy | Callable gate fails; repair only exact approved denial entry. | AD-08/09 |
| F13 | Other disabled toolsets exist; Tool Search is auto | Preserve unrelated denials/search behavior; no blanket reset. | AD-08/09 |
| F14 | Interactive PATH succeeds but MCP PATH fails; selector rewritten | Diagnose subprocess environment; preserve managed selector semantics. | AD-05/09 |
| F15 | Positive tool discovery count or claimed visibility without invocation | Require real fresh-session tool trace; no simulated callable PASS. | AD-09 |
| F16 | Skill global-only, disabled, stale hash or old loaded session | Profile skill/injection gate fails until correct fresh session proof. | AD-08 |
| F17 | Default inference succeeds but planning/critic route has invalid auth | Fail affected route/workflow gate; no automatic provider substitution. | AD-06/15 |
| F18 | Quota exhaustion, provider 403, or unavailable route at dispatch | Classify responsible layer; no paid fallback, uncontrolled retries or new work. | AD-07 |
| F19 | Clean shell but eligible hidden stored API credential | Coverage/route audit denies or reports UNKNOWN; never prints payload. | AD-06 |
| F20 | models.yml, custom endpoint or model-profile override changes route | Resolve effective route or deny; no trust in the visible default alone. | AD-06 |
| F21 | Empty fallback list but metered pool member or auxiliary auto route | Route-closure gate fails unless all reachable paths are approved. | AD-06 |
| F22 | OAuth present but entitlement/overage behavior unknown or paid | Do not certify subscription-only; require route/account control evidence. | AD-06 |
| F23 | Global model changes; old job snapshot/cron default differs | Use actual installed resolution; pin and enforce expected effective route. | AD-18 |
| F24 | Unknown/stale quota, clock change, or guessed reset timestamp | DENY/UNKNOWN for required expensive admission; no elapsed-time guess. | AD-07 |
| F25 | Two projects simultaneously use one account allowance snapshot | Serialize local admissions/reservations; document external-usage limits. | AD-07 |
| F26 | Verification labeled local calls a paid remote API | Require network/resource authorization; no monitoring exemption. | AD-07/14 |
| F27 | Coordinator returns only spawn_failed | One supported lower-level diagnosis; no repeated new-session retries. | AD-10 |
| F28 | Direct GJC TUI/inference works but broker session creation fails | Keep lifecycle gate failed and retain typed root cause. | AD-10 |
| F29 | broker.shutdown is unsupported through attempted CLI route | Report unsupported diagnostic, not stale broker; never kill guessed PID. | AD-05 |
| F30 | list_sessions stale/empty while coordination status has active turn | Reconcile actual active work; new dispatch count stays zero. | AD-11 |
| F31 | unavailable/terminal_uncertain with live advancing SDK events | Treat as observation uncertainty/activity, not conclusive failure. | AD-11 |
| F32 | Native sources conflict without conclusive liveness | UNCERTAIN consumes lane; inspection allowed, new mutation denied. | AD-11 |
| F33 | Request accepted but acknowledgement lost | Recover same operation/key; at most one logical execution in native records. | AD-12 |
| F34 | Same idempotency key reused with different canonical payload | Reject locally and preserve original request identity. | AD-02/12 |
| F35 | Manual and cron triggers overlap | Single project mutation admission; exactly one primary action proceeds. | AD-12 |
| F36 | Crash before journal, after PREPARED, after send, or before ack save | Recover intent/native IDs conservatively; never invent a fresh retry identity. | AD-02/12 |
| F37 | Old cycle resumes after disable increments epoch | Mutation denied at boundary; already accepted work remains visible. | AD-12/19 |
| F38 | PID reused or lock appears old while worker is active | No blind ownership theft; reconcile generation/process/native evidence. | AD-02/11 |
| F39 | Long-running worker exceeds supervisor wait budget | Supervisor exits boundedly with native IDs; worker state not forgotten. | AD-13 |
| F40 | Same repair failure recurs across fresh cron sessions | Persistent attempt budget/circuit breaker blocks infinite repair loop. | AD-13 |
| F41 | CLI uses correct Ruby; gateway/worker resolves old interpreter | ENVIRONMENT_FAILURE with exact runtime evidence; do not weaken tests. | AD-08/14/17 |
| F42 | Verified SHA differs only in irrelevant documentation | Reuse only after complete relevance/inputs check; record applicability evidence. | AD-14 |
| F43 | Lockfile, test, fixture, build config, toolchain or untracked input changes | Invalidate dependent verification receipt and rerun required checks. | AD-14 |
| F44 | Worker edits acceptance/plan/test contract to pass | Detect approved-hash violation; refuse completion and escalate. | AD-04/14 |
| F45 | Predecessor verified only on unmerged branch, successor starts on main | Block successor until approved dependency/base policy is satisfied. | AD-04/14 |
| F46 | Repo has AGENT.md but runtime auto-loads other names | Load declared context explicitly; do not rename or assume ingestion. | AD-03/13 |
| F47 | Passive preflight secretly launches model/script/session/message | Effect audit fails; move operation to explicit active validate tier. | AD-15 |
| F48 | Plan-only/diagnostic probe touches product files or leaves uncertain worker | Fail scope check; preserve evidence; cleanup only owned inactive resources. | AD-15 |
| F49 | Receipt mocked, expired, wrong profile, wrong version or untraced | Cannot satisfy live admission; show precise invalidation reason. | AD-15 |
| F50 | Chat/gateway works but actual cron cwd/profile/PATH is wrong | Scheduled-worker gate fails independently of interactive evidence. | AD-17/18 |
| F51 | Active schedule would be created before it can be paused | Reject unsafe creation path; use natively unscheduled/paused canary only. | AD-18 |
| F52 | Duplicate job names, unknown ownership or uncertain enable response | Resolve exact owned IDs; block/reconcile instead of create another job. | AD-18 |
| F53 | Scheduled agent attempts to schedule again through tools/terminal | Enforced boundary denies recursion or deployment cannot be certified. | AD-13/18 |
| F54 | Host sleeps/offline; many occurrences missed on restart | One bounded reconciliation, no catch-up storm or false offline-alert claim. | AD-18 |
| F55 | Coding succeeds but Discord response/send acknowledgement fails | Retry delivery only; native implementation count must not increase. | AD-17/19 |
| F56 | Secrets in provider error, environment, prompt or support output | Redaction/effect tests fail before report is stored or delivered. | AD-02/17 |
| F57 | Agent writes outside root, edits guard/grant, or calls raw mutation bypass | Block under enforced backend; otherwise POLICY_ONLY and no strict enable. | AD-12/20 |
| F58 | Sibling/nested managed worktree, another repo or broad parent allowlist | Validate registered membership; allow only authorized project/worktree identity. | AD-10/22 |
| F59 | Recovery target has no commit plus binary/untracked implementation | Preserve original and all approved data; verify backup/transfer completeness. | AD-19 |
| F60 | Proposed recovery duplicates an old session with unknown/live execution | Block recovery dispatch until liveness/cancellation is resolved. | AD-19 |
| F61 | disable closes admission but schedule pause fails; worker already running | Report schedule uncertainty and active work truthfully; do not kill/delete. | AD-19 |
| F62 | Existing profile belongs to another repo or lacks AutoDev ownership | Require reviewed adoption or choose distinct identity; no overwrite. | AD-08/16 |
| F63 | External access/service/API capability unavailable | BLOCKED_EXTERNAL/UNSUPPORTED with remediation; never fabricated live PASS. | AD-00/17/21 |
| F64 | Onboarding second project changes shared runtime or Nous settings | Regression fails; restore only owned changes and require separate approval. | AD-21/22 |
| F65 | Happy-path approved small milestone from fresh profile | One native execution, allowed diff, fresh independent verification and delivery proof. | AD-15/22 |
| F66 | Draft-named folder, filename-ordered plans, dependency cycle or approval drift | Evaluate content/explicit authority; reject invalid graph or unapproved work. | AD-01/04 |
| F67 | Repo metadata tries to source shell files or run package hooks during init | No project code runs; suggestions stay data pending explicit approval. | AD-03 |
| F68 | Supervisor quota blocked but scheduler starts LLM to check quota anyway | Fail pre-inference gate; deterministic report without model call. | AD-07/18 |
| F69 | Disk-full/interrupted registry update or corrupt journal record | Preserve recoverable state; no lost projects or unsafe operation admission. | AD-02 |
| F70 | Passive Git command invokes configured external diff/filter/fsmonitor helper | Trusted read adapter prevents side effects or refuses unsupported mode. | AD-02 |

## End-to-end release scenarios

**R1 - Existing Nous, shadow only:** compare old and generic decisions against the same current evidence without creating a second mutating owner.

**R2 - Fresh incomplete project:** init creates only safe drafts; onboard stops on unresolved semantic input; validate/enable cannot invent approval.

**R3 - Fresh approved project:** init -> onboard -> authorized validate -> fresh preflight -> enable -> one bounded execution -> independent duplicate check -> terminal verification -> delivery -> disable. No manual runtime-file editing is allowed as an undocumented workaround.

**R4 - Lost acknowledgement and restart:** interrupt after native accept, restart AutoDev, and prove one logical implementation remains through native IDs and operation identity.

**R5 - Policy/config drift:** change model route, skill version, approval hash, or executable generation; affected receipts invalidate and next mutation is refused until recertified.

**R6 - Dirty-work recovery:** preserve a stranded uncommitted implementation including binary/untracked files, prove original inactive, create a fresh native worktree, transfer approved changes, and independently verify.

**R7 - Failure to notify:** finish code, fail delivery, and prove retry changes only notification state.

**R8 - Permission boundary:** attempt cross-project mutation, self-grant edit, raw Coordinator bypass, protected Git operation and unapproved provider route; certify only boundaries actually enforced.

**R9 - No provider telemetry:** strict admission stays UNKNOWN/DENIED, deterministic status still works, no hidden token-using diagnostic runs.

**R10 - Disable race:** close admission while a cycle is paused before send; prove stale epoch cannot dispatch. Separately demonstrate truthful reporting for a request accepted before disable.

## Release decision

Release requires all mandatory implemented behavior and required live gates for the advertised target. Do not average failures into a percentage score. One unresolved critical invariant is enough to block strict unattended enablement. Publish CODE_VERIFIED separately from LIVE_CERTIFIED.


---

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


---

# Sources and limits

## Uploaded incident reports: primary basis

[S1] Lessons Learned from Nous Autonomous Supervisor Setup.
File: `Pasted markdown(2).md`.
SHA-256: `6ace331bbf3f2ee7af23b46f8cbd579290c434e0f3d913a0e0eccc2d035b928d`.

[S2] Hermes + Gajae Automated Onboarding: Lessons from Nous.
File: `Pasted markdown (2).md`.
SHA-256: `d0ea218d74b658f174bd8566c8bf017981b06d7df51a12df4ecb94e997bf052b`.

[S3] Lessons Learned From Nous Autonomous Onboarding.
File: `Pasted markdown (3).md` (begins with an introductory paragraph before the main heading).
SHA-256: `bdac1bb84c3de3f695462d371ee3509e9a98007f9091b2292ad6f83eb2dd43b5`.

These are the user's retrospective accounts. The package treats their incidents as reported observations, not independently reproduced current machine facts. Account IDs, host paths, model names, version numbers, and session IDs in those files are not universal defaults. Original files are not copied into this distributable package.

## External primary-source checks

Consulted while revising the specification on September 12, 2026 (America/Toronto). Documentation is mutable and does not supersede the installed-version compatibility probe.

[W1] Hermes, Scheduled Tasks (Cron).
`https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/`
Relevance: effective job model selection, cron workdir, native paused canaries, scheduling and execution/delivery separation. Use installed capability checks rather than freeze current docs into hardcoded flags.

[W2] Hermes, Credential Pools.
`https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools/`
Relevance: account/credential rotation is a separate route from cross-provider fallback.

[W3] Hermes, Fallback Providers.
`https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers/`
Relevance: primary and auxiliary provider resolution must be audited separately.

[W4] Gajae Code, public repository README.
`https://github.com/Yeachan-Heo/gajae-code`
Relevance: installation distribution matters; standalone binary instructions do not require Bun. This is not a claim about the user's installed distribution.

[W5] Gajae Code, Coordinator MCP bridge.
`https://github.com/Yeachan-Heo/gajae-code/blob/main/docs/hermes-mcp-bridge.md`
Relevance: native Coordinator, setup, managed worktree selector, and durable turns. The historical incident's SDK behavior must be checked against the installed API.

[W6] Claude Help Center, Manage usage credits for paid Claude plans.
`https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans`
Relevance: authentication and subscription membership alone do not prove that usage beyond included limits cannot be charged.

[W7] OpenAI Help Center, Using Credits for Flexible Usage in ChatGPT (Personal plans).
`https://help.openai.com/en/articles/12642688`
Relevance: the account's credit/usage controls need separate inspection from its OAuth credential mechanism. This package does not determine the user's plan-specific billing settings.

[W8] Hermes, Configuration.
`https://hermes-agent.nousresearch.com/docs/user-guide/configuration/`
Relevance: local tools execute with user filesystem access; a cwd/profile is not a sandbox.

## What was not verified

No command was run on the user's laptop. No provider account or credential store was inspected. No live Hermes/GJC integration, broker recovery, cron run, gateway restart, or Discord delivery was performed. No feature in the specification should be reported implemented merely because its source material describes it.
