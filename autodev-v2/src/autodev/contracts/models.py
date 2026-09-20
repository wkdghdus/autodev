"""Immutable versioned models for AutoDev-owned contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any


class RepositoryState(str, Enum):
    DRAFT = "DRAFT"
    ALIGNED = "ALIGNED"
    INVALID = "INVALID"


class AlignmentOutcome(str, Enum):
    ALIGNED = "ALIGNED"
    NEEDS_INPUT = "NEEDS_INPUT"
    ERROR = "ERROR"


class DeploymentState(str, Enum):
    ABSENT = "ABSENT"
    CONFIGURED = "CONFIGURED"
    PARTIAL = "PARTIAL"
    DRIFTED = "DRIFTED"


class ValidationState(str, Enum):
    NOT_RUN = "NOT_RUN"
    PASSED = "PASSED"
    FAILED = "FAILED"
    STALE = "STALE"
    BLOCKED_EXTERNAL = "BLOCKED_EXTERNAL"


class AdmissionState(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    UNKNOWN = "UNKNOWN"


class ScheduleState(str, Enum):
    ABSENT = "ABSENT"
    PAUSED = "PAUSED"
    ENABLED = "ENABLED"
    UNKNOWN = "UNKNOWN"


class ExecutionState(str, Enum):
    IDLE = "IDLE"
    EXECUTING = "EXECUTING"
    WAITING_FOR_ANSWER = "WAITING_FOR_ANSWER"
    VERIFYING = "VERIFYING"
    FAILED_REPAIRABLE = "FAILED_REPAIRABLE"
    UNCERTAIN = "UNCERTAIN"
    HUMAN_BLOCKED = "HUMAN_BLOCKED"
    VERIFIED_UNMERGED = "VERIFIED_UNMERGED"
    INTEGRATED = "INTEGRATED"


class ResourceState(str, Enum):
    AVAILABLE = "AVAILABLE"
    BLOCKED_QUOTA = "BLOCKED_QUOTA"
    UNKNOWN = "UNKNOWN"


class DeliveryState(str, Enum):
    NOT_TESTED = "NOT_TESTED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class Permission(IntEnum):
    DENIED = 0
    HUMAN = 1
    AUTONOMOUS = 2

    @classmethod
    def from_value(cls, value: str | "Permission") -> "Permission":
        if isinstance(value, cls):
            return value
        return cls[value.upper()]

    def __str__(self) -> str:
        return self.name.lower()


class SetupState(str, Enum):
    DRAFT = "draft"
    CONFIGURED = "configured"


class ApprovalState(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REVOKED = "revoked"


class EnforcementAssurance(str, Enum):
    POLICY_ONLY = "POLICY_ONLY"
    ENFORCED = "ENFORCED"


class OperationState(str, Enum):
    PREPARED = "PREPARED"
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    UNCERTAIN = "UNCERTAIN"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ProjectIdentity:
    id: str | None
    slug: str | None
    name: str | None


@dataclass(frozen=True)
class DiscoveryConfig:
    roots: tuple[str, ...]


@dataclass(frozen=True)
class SourcesConfig:
    requirements: tuple[str, ...]
    context: tuple[str, ...]
    discovery: DiscoveryConfig
    execution_index: str | None


@dataclass(frozen=True)
class ExecutionConfig:
    harness: str | None
    workflow: str | None
    base_policy: str | None
    target_ref: str | None
    max_active_milestones: int | None
    max_primary_actions_per_cycle: int | None


@dataclass(frozen=True)
class VerificationCommand:
    id: str
    argv: tuple[str, ...]
    cwd: str
    input_paths: tuple[str, ...]
    network: str
    timeout_seconds: int
    approval_binding: str


@dataclass(frozen=True)
class VerificationConfig:
    commands: tuple[VerificationCommand, ...]
    acceptance_sources: tuple[str, ...]
    require_independent_review: bool | None


@dataclass(frozen=True)
class AuthorityConfig:
    requested: tuple[tuple[str, Permission], ...]

    def permission_for(self, operation: str) -> Permission | None:
        return dict(self.requested).get(operation)


@dataclass(frozen=True)
class ProjectConfig:
    schema_version: int
    setup_state: SetupState
    project: ProjectIdentity
    sources: SourcesConfig
    execution: ExecutionConfig
    verification: VerificationConfig
    authority: AuthorityConfig

    @property
    def repository_state(self) -> RepositoryState:
        return RepositoryState.DRAFT if self.setup_state is SetupState.DRAFT else RepositoryState.ALIGNED

    @property
    def alignment_outcome(self) -> AlignmentOutcome:
        return AlignmentOutcome.NEEDS_INPUT if self.setup_state is SetupState.DRAFT else AlignmentOutcome.ALIGNED


@dataclass(frozen=True)
class ContentReference:
    path: str
    reference: str
    digest: str


@dataclass(frozen=True)
class MilestoneScope:
    allowed_paths: tuple[str, ...]
    exclusions: tuple[str, ...]
    prohibited_operations: tuple[str, ...]


@dataclass(frozen=True)
class MilestoneApproval:
    state: ApprovalState
    receipt_ref: str | None


@dataclass(frozen=True)
class Milestone:
    id: str
    title: str
    depends_on: tuple[str, ...]
    authority_refs: tuple[ContentReference, ...]
    acceptance_refs: tuple[ContentReference, ...]
    scope: MilestoneScope
    verification_ids: tuple[str, ...]
    approval: MilestoneApproval
    base_policy: str
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionIndex:
    schema_version: int
    project_id: str | None
    milestones: tuple[Milestone, ...]


@dataclass(frozen=True)
class InstallationBinding:
    schema_version: int
    installation_id: str
    project_id: str
    repo_realpath: str
    git_common_dir_realpath: str
    profile_identity: str
    service_identity: str
    root_binding_policy: str
    runtime_capability_manifest_ref: str
    model_routes: tuple[tuple[str, str], ...]
    auth_account_refs: tuple[str, ...]
    resource_policy: str
    deployment_grant_ref: str
    skill_hash: str
    delivery_target_ref: str
    cron_id: str | None
    cron_ownership: str | None
    desired_enabled: bool
    deployment_epoch: int
    project_slug: str | None = None


@dataclass(frozen=True)
class MutationGrant:
    schema_version: int
    grant_id: str
    operator_identity: str
    operator_action: str
    installation_id: str
    operation_classes: tuple[str, ...]
    repository_membership_rule: str
    managed_worktree_membership_rule: str
    protected_files: tuple[str, ...]
    protected_refs: tuple[str, ...]
    allowed_routes: tuple[str, ...]
    artifact_hashes: tuple[str, ...]
    resource_constraints: tuple[tuple[str, str], ...]
    expires_at: str
    revocation_epoch: int
    enforcement_backend: str
    content_digest: str


@dataclass(frozen=True)
class ApprovalReceipt:
    schema_version: int
    receipt_id: str
    operator_identity: str
    operator_action: str
    project_id: str
    installation_id: str
    artifact_digests: tuple[str, ...]
    operation_classes: tuple[str, ...]
    scope: tuple[str, ...]
    expires_at: str
    revocation_epoch: int


@dataclass(frozen=True)
class ValidationReceipt:
    schema_version: int
    gate_id: str
    evidence_class: str
    probe_id: str
    installation_id: str
    project_id: str
    invocation_source: str
    observed_at: str
    expires_at: str
    capability_fingerprint: str
    bound_hashes: tuple[str, ...]
    repo_revision: str
    dirty_input_fingerprint: str
    route_identity: str
    native_trace_refs: tuple[str, ...]
    allowed_effects: tuple[str, ...]
    observed_effects: tuple[str, ...]
    cleanup_state: str
    result: str
    invalidation_keys: tuple[str, ...]


@dataclass(frozen=True)
class OperationRecord:
    schema_version: int
    operation_id: str
    installation_id: str
    milestone_id: str | None
    operation_kind: str
    plan_digest: str
    grant_digest: str
    canonical_arguments_digest: str
    idempotency_key: str
    created_at: str
    owner_identity: str
    deployment_epoch: int
    operation_state: OperationState
    native_ids: tuple[str, ...]
    reconciliation_evidence_refs: tuple[str, ...]
    terminal_result: str | None


@dataclass(frozen=True)
class CommandResult:
    schema_version: int
    operation: str
    outcome: str
    checks: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    planned_changes: tuple[str, ...] = ()
    applied_changes: tuple[str, ...] = ()
    next_safe_action: str | None = None


@dataclass(frozen=True)
class MigrationPlan:
    schema_version: int
    source_sha256: str
    legacy_fields: tuple[tuple[str, str], ...]
    unresolved_fields: tuple[str, ...]
    draft_target: tuple[tuple[str, Any], ...]
    applicable: bool = False
    writes_performed: bool = False


@dataclass(frozen=True)
class ReadinessInputs:
    repository: RepositoryState
    deployment: DeploymentState
    validation: ValidationState
    admission: AdmissionState
    schedule: ScheduleState
    execution: ExecutionState
    resource: ResourceState
    delivery: DeliveryState
    operator_grant_current: bool = False
    grant_content_bound: bool = False
    enforcement: EnforcementAssurance = EnforcementAssurance.POLICY_ONLY
    ownership_conflict: bool = False
    drift_conflict: bool = False
    eligible_approved_milestones: int = 0
    dependencies_satisfied: bool = False
    base_policy_satisfied: bool = False


@dataclass(frozen=True)
class ReadinessResult:
    aligned: bool
    ready_for_enable: bool
    ready_to_dispatch: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)
