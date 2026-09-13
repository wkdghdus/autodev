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
