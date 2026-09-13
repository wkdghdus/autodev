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
