"""Pure contract logic for permissions, readiness, and installation identity."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .models import (
    AdmissionState,
    DeliveryState,
    DeploymentState,
    EnforcementAssurance,
    ExecutionState,
    InstallationBinding,
    Permission,
    ReadinessInputs,
    ReadinessResult,
    RepositoryState,
    ResourceState,
    ValidationState,
)


class InstallationIdentityOutcome(str, Enum):
    EXISTING_BINDING_MATCH = "EXISTING_BINDING_MATCH"
    SLUG_COLLISION = "SLUG_COLLISION"
    INSTALLATION_CONFLICT = "INSTALLATION_CONFLICT"
    NEW_INSTALLATION_REQUIRED = "NEW_INSTALLATION_REQUIRED"


@dataclass(frozen=True)
class InstallationIdentityResult:
    outcome: InstallationIdentityOutcome
    binding: InstallationBinding | None = None
    conflicts: tuple[InstallationBinding, ...] = ()
    reasons: tuple[str, ...] = ()


def _permission(value: Permission | str | None) -> Permission:
    if value is None:
        return Permission.DENIED
    if isinstance(value, Permission):
        return value
    if isinstance(value, str):
        try:
            return Permission.from_value(value)
        except KeyError as exc:
            raise ValueError(f"unsupported permission {value!r}") from exc
    raise TypeError("permission boundary must be Permission, str, or None")


def effective_permission(
    requested: Permission | str | None,
    operator_grant: Permission | str | None,
    native_limit: Permission | str | None,
    enforcement_limit: Permission | str | None,
) -> Permission:
    """Return the most restrictive permission across all required ceilings."""

    return min(
        _permission(requested),
        _permission(operator_grant),
        _permission(native_limit),
        _permission(enforcement_limit),
    )


def evaluate_readiness(inputs: ReadinessInputs) -> ReadinessResult:
    """Evaluate orthogonal readiness predicates without mutating state."""

    reasons: list[str] = []

    aligned = inputs.repository is RepositoryState.ALIGNED
    if not aligned:
        reasons.append("REPOSITORY_NOT_ALIGNED")

    enable_checks = (
        (inputs.deployment is DeploymentState.CONFIGURED, "DEPLOYMENT_NOT_CONFIGURED"),
        (inputs.validation is ValidationState.PASSED, "VALIDATION_NOT_PASSED"),
        (inputs.operator_grant_current, "OPERATOR_GRANT_MISSING"),
        (inputs.grant_content_bound, "GRANT_NOT_CONTENT_BOUND"),
        (inputs.enforcement is EnforcementAssurance.ENFORCED, "ENFORCEMENT_NOT_ASSURED"),
        (inputs.delivery is DeliveryState.DELIVERED, "DELIVERY_NOT_TESTED"),
        (not inputs.ownership_conflict, "OWNERSHIP_CONFLICT"),
        (not inputs.drift_conflict, "DRIFT_CONFLICT"),
    )
    for passed, code in enable_checks:
        if not passed:
            reasons.append(code)

    ready_for_enable = aligned and all(passed for passed, _ in enable_checks)

    if inputs.eligible_approved_milestones == 0:
        reasons.append("NO_ELIGIBLE_APPROVED_MILESTONE")
        milestone_count_ok = False
    elif inputs.eligible_approved_milestones == 1:
        milestone_count_ok = True
    else:
        reasons.append("MULTIPLE_ELIGIBLE_APPROVED_MILESTONES")
        milestone_count_ok = False

    dispatch_checks = (
        (inputs.dependencies_satisfied, "DEPENDENCIES_UNSATISFIED"),
        (inputs.base_policy_satisfied, "BASE_POLICY_UNSATISFIED"),
        (inputs.execution is ExecutionState.IDLE, "EXECUTION_NOT_IDLE"),
        (inputs.admission is AdmissionState.ALLOW, "ADMISSION_NOT_ALLOW"),
        (inputs.resource is ResourceState.AVAILABLE, "RESOURCE_NOT_AVAILABLE"),
    )
    for passed, code in dispatch_checks:
        if not passed:
            reasons.append(code)

    ready_to_dispatch = (
        ready_for_enable
        and milestone_count_ok
        and all(passed for passed, _ in dispatch_checks)
    )
    return ReadinessResult(aligned, ready_for_enable, ready_to_dispatch, tuple(reasons))


def check_installation_identity(
    *,
    project_id: str,
    repo_realpath: str,
    git_common_dir_realpath: str,
    existing_bindings: Iterable[InstallationBinding],
    project_slug: str | None = None,
    installation_id: str | None = None,
) -> InstallationIdentityResult:
    """Compare a proposed installation identity against known host bindings.

    AD-01 only classifies identity state. It never mints a new installation ID
    and never adopts a clone or mismatched Git common directory as equivalent.
    """

    bindings = tuple(existing_bindings)
    slug_conflicts = tuple(
        binding
        for binding in bindings
        if project_slug
        and binding.project_slug == project_slug
        and binding.project_id != project_id
    )
    if slug_conflicts:
        return InstallationIdentityResult(
            InstallationIdentityOutcome.SLUG_COLLISION,
            conflicts=slug_conflicts,
            reasons=("SLUG_USED_BY_DIFFERENT_PROJECT",),
        )

    installation_conflicts = tuple(
        binding
        for binding in bindings
        if installation_id
        and binding.installation_id == installation_id
        and (
            binding.project_id != project_id
            or binding.repo_realpath != repo_realpath
            or binding.git_common_dir_realpath != git_common_dir_realpath
        )
    )
    if installation_conflicts:
        return InstallationIdentityResult(
            InstallationIdentityOutcome.INSTALLATION_CONFLICT,
            conflicts=installation_conflicts,
            reasons=("INSTALLATION_ID_REUSED_WITH_DIFFERENT_IDENTITY",),
        )

    exact_matches = tuple(
        binding
        for binding in bindings
        if binding.project_id == project_id
        and binding.repo_realpath == repo_realpath
        and binding.git_common_dir_realpath == git_common_dir_realpath
        and (installation_id is None or binding.installation_id == installation_id)
    )
    if exact_matches:
        return InstallationIdentityResult(
            InstallationIdentityOutcome.EXISTING_BINDING_MATCH,
            binding=exact_matches[0],
        )

    root_identity_conflicts = tuple(
        binding
        for binding in bindings
        if installation_id is not None
        and binding.project_id == project_id
        and binding.repo_realpath == repo_realpath
        and binding.git_common_dir_realpath == git_common_dir_realpath
        and binding.installation_id != installation_id
    )
    if root_identity_conflicts:
        return InstallationIdentityResult(
            InstallationIdentityOutcome.INSTALLATION_CONFLICT,
            conflicts=root_identity_conflicts,
            reasons=("ROOT_ALREADY_BOUND_TO_DIFFERENT_INSTALLATION",),
        )

    git_conflicts = tuple(
        binding
        for binding in bindings
        if binding.project_id == project_id
        and binding.repo_realpath == repo_realpath
        and binding.git_common_dir_realpath != git_common_dir_realpath
    )
    if git_conflicts:
        return InstallationIdentityResult(
            InstallationIdentityOutcome.INSTALLATION_CONFLICT,
            conflicts=git_conflicts,
            reasons=("GIT_COMMON_DIR_MISMATCH",),
        )

    project_clones = tuple(
        binding
        for binding in bindings
        if binding.project_id == project_id
        and (
            binding.repo_realpath != repo_realpath
            or binding.git_common_dir_realpath != git_common_dir_realpath
        )
    )
    if project_clones:
        return InstallationIdentityResult(
            InstallationIdentityOutcome.NEW_INSTALLATION_REQUIRED,
            conflicts=project_clones,
            reasons=("PROJECT_ID_ALREADY_BOUND_TO_OTHER_ROOT",),
        )

    return InstallationIdentityResult(
        InstallationIdentityOutcome.NEW_INSTALLATION_REQUIRED,
        reasons=("NO_EXISTING_BINDING",),
    )
