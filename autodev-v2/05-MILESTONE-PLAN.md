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
