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
