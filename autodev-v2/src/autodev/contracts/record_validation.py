"""Closed, non-coercing validators for host-owned version-1 records."""

from __future__ import annotations

import re
from typing import Any

from .errors import ContractValidationError, ValidationIssue
from .models import (
    ApprovalReceipt,
    CommandResult,
    InstallationBinding,
    MutationGrant,
    OperationRecord,
    OperationState,
    ValidationReceipt,
)

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _closed(
    mapping: Any, name: str, required: set[str], optional: set[str] | None = None
) -> dict[str, Any]:
    if not isinstance(mapping, dict):
        raise ContractValidationError([ValidationIssue("TYPE", "$", f"{name} must be a mapping")])
    optional = optional or set()
    issues: list[ValidationIssue] = []
    for key in mapping:
        if type(key) is not str:
            issues.append(ValidationIssue("NON_STRING_KEY", "$", "mapping keys must be strings"))
        elif key not in required | optional | {"schema_version"}:
            issues.append(ValidationIssue("UNKNOWN_FIELD", f"$.{key}", "unknown field"))
    for key in sorted(required | {"schema_version"}):
        if key not in mapping:
            issues.append(ValidationIssue("REQUIRED", f"$.{key}", "required field is missing"))
    version = mapping.get("schema_version")
    if type(version) is not int:
        issues.append(ValidationIssue("TYPE", "$.schema_version", "must be int"))
    elif version != 1:
        issues.append(ValidationIssue("UNSUPPORTED_VERSION", "$.schema_version", f"supported {name} schema version is 1"))
    if issues:
        raise ContractValidationError(issues)
    return mapping


def _typed(mapping: dict[str, Any], specs: dict[str, type | tuple[type, ...]], nullable: set[str] = set()) -> None:
    issues: list[ValidationIssue] = []
    for key, expected in specs.items():
        value = mapping.get(key)
        if value is None and key in nullable:
            continue
        expected_types = expected if isinstance(expected, tuple) else (expected,)
        if not any(type(value) is item for item in expected_types):
            label = " or ".join(item.__name__ for item in expected_types)
            issues.append(ValidationIssue("TYPE", f"$.{key}", f"must be {label}"))
        elif isinstance(value, str) and not value:
            issues.append(ValidationIssue("EMPTY", f"$.{key}", "must be nonempty"))
    if issues:
        raise ContractValidationError(issues)


def _strings(value: Any, path: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or any(type(item) is not str or not item for item in value):
        raise ContractValidationError([ValidationIssue("TYPE", path, "must be a list of nonempty strings")])
    return tuple(value)


def _string_map(value: Any, path: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, dict) or any(type(k) is not str or type(v) is not str for k, v in value.items()):
        raise ContractValidationError([ValidationIssue("TYPE", path, "must be a string-to-string mapping")])
    return tuple(value.items())


def _digests(value: Any, path: str, *, require_nonempty: bool = False) -> tuple[str, ...]:
    digests = _strings(value, path)
    if require_nonempty and not digests:
        raise ContractValidationError([ValidationIssue("REQUIRED", path, "at least one digest is required")])
    invalid = [index for index, digest in enumerate(digests) if not _SHA256.fullmatch(digest)]
    if invalid:
        raise ContractValidationError(
            [ValidationIssue("INVALID_DIGEST", f"{path}[{index}]", "must be a lowercase SHA-256 digest") for index in invalid]
        )
    return digests


def validate_installation_binding(mapping: dict[str, Any]) -> InstallationBinding:
    fields = {
        "installation_id", "project_id", "repo_realpath", "git_common_dir_realpath", "profile_identity",
        "service_identity", "root_binding_policy", "runtime_capability_manifest_ref", "model_routes",
        "auth_account_refs", "resource_policy", "deployment_grant_ref", "skill_hash", "delivery_target_ref",
        "cron_id", "cron_ownership", "desired_enabled", "deployment_epoch",
    }
    data = _closed(mapping, "installation binding", fields, {"project_slug"})
    string_fields = fields - {"model_routes", "auth_account_refs", "desired_enabled", "deployment_epoch", "cron_id", "cron_ownership"}
    _typed(data, {**{key: str for key in string_fields}, "desired_enabled": bool, "deployment_epoch": int, "cron_id": str, "cron_ownership": str}, {"cron_id", "cron_ownership"})
    slug = data.get("project_slug")
    if slug is not None and (type(slug) is not str or not slug):
        raise ContractValidationError([ValidationIssue("TYPE", "$.project_slug", "must be a nonempty string or null")])
    return InstallationBinding(
        1, data["installation_id"], data["project_id"], data["repo_realpath"], data["git_common_dir_realpath"],
        data["profile_identity"], data["service_identity"], data["root_binding_policy"],
        data["runtime_capability_manifest_ref"], _string_map(data["model_routes"], "$.model_routes"),
        _strings(data["auth_account_refs"], "$.auth_account_refs"), data["resource_policy"],
        data["deployment_grant_ref"], data["skill_hash"], data["delivery_target_ref"], data["cron_id"],
        data["cron_ownership"], data["desired_enabled"], data["deployment_epoch"], slug,
    )


def validate_mutation_grant(mapping: dict[str, Any]) -> MutationGrant:
    fields = {
        "grant_id", "operator_identity", "operator_action", "installation_id", "operation_classes",
        "repository_membership_rule", "managed_worktree_membership_rule", "protected_files", "protected_refs",
        "allowed_routes", "artifact_hashes", "resource_constraints", "expires_at", "revocation_epoch",
        "enforcement_backend", "content_digest",
    }
    data = _closed(mapping, "mutation grant", fields)
    list_fields = {"operation_classes", "protected_files", "protected_refs", "allowed_routes", "artifact_hashes"}
    _typed(data, {**{key: str for key in fields - list_fields - {"resource_constraints", "revocation_epoch"}}, "revocation_epoch": int})
    if not _SHA256.fullmatch(data["content_digest"]):
        raise ContractValidationError(
            [ValidationIssue("INVALID_DIGEST", "$.content_digest", "must be a lowercase SHA-256 digest")]
        )
    return MutationGrant(
        1, data["grant_id"], data["operator_identity"], data["operator_action"], data["installation_id"],
        _strings(data["operation_classes"], "$.operation_classes"), data["repository_membership_rule"],
        data["managed_worktree_membership_rule"], _strings(data["protected_files"], "$.protected_files"),
        _strings(data["protected_refs"], "$.protected_refs"), _strings(data["allowed_routes"], "$.allowed_routes"),
        _digests(data["artifact_hashes"], "$.artifact_hashes"), _string_map(data["resource_constraints"], "$.resource_constraints"),
        data["expires_at"], data["revocation_epoch"], data["enforcement_backend"], data["content_digest"],
    )


def validate_approval_receipt(mapping: dict[str, Any]) -> ApprovalReceipt:
    fields = {"receipt_id", "operator_identity", "operator_action", "project_id", "installation_id", "artifact_digests", "operation_classes", "scope", "expires_at", "revocation_epoch"}
    data = _closed(mapping, "approval receipt", fields)
    _typed(data, {**{key: str for key in fields - {"artifact_digests", "operation_classes", "scope", "revocation_epoch"}}, "revocation_epoch": int})
    operation_classes = _strings(data["operation_classes"], "$.operation_classes")
    scope = _strings(data["scope"], "$.scope")
    issues: list[ValidationIssue] = []
    if not operation_classes:
        issues.append(ValidationIssue("REQUIRED", "$.operation_classes", "at least one operation class is required"))
    if not scope:
        issues.append(ValidationIssue("REQUIRED", "$.scope", "at least one scope entry is required"))
    if issues:
        raise ContractValidationError(issues)
    return ApprovalReceipt(1, data["receipt_id"], data["operator_identity"], data["operator_action"], data["project_id"], data["installation_id"], _digests(data["artifact_digests"], "$.artifact_digests", require_nonempty=True), operation_classes, scope, data["expires_at"], data["revocation_epoch"])


def validate_validation_receipt(mapping: dict[str, Any]) -> ValidationReceipt:
    lists = {"bound_hashes", "native_trace_refs", "allowed_effects", "observed_effects", "invalidation_keys"}
    fields = {"gate_id", "evidence_class", "probe_id", "installation_id", "project_id", "invocation_source", "observed_at", "expires_at", "capability_fingerprint", "repo_revision", "dirty_input_fingerprint", "route_identity", "cleanup_state", "result"} | lists
    data = _closed(mapping, "validation receipt", fields)
    _typed(data, {key: str for key in fields - lists})
    issues: list[ValidationIssue] = []
    if data["evidence_class"] not in {"SIMULATED", "LIVE"}:
        issues.append(ValidationIssue("INVALID_ENUM", "$.evidence_class", "must be SIMULATED or LIVE"))
    if data["result"] not in {"PASS", "FAIL", "UNKNOWN", "NOT_RUN", "BLOCKED_EXTERNAL"}:
        issues.append(ValidationIssue("INVALID_ENUM", "$.result", "unknown validation result"))
    native_trace_refs = _strings(data["native_trace_refs"], "$.native_trace_refs")
    if data["evidence_class"] == "LIVE" and data["result"] == "PASS" and not native_trace_refs:
        issues.append(
            ValidationIssue("NATIVE_TRACE_REQUIRED", "$.native_trace_refs", "LIVE PASS requires native trace evidence")
        )
    if issues:
        raise ContractValidationError(issues)
    return ValidationReceipt(1, data["gate_id"], data["evidence_class"], data["probe_id"], data["installation_id"], data["project_id"], data["invocation_source"], data["observed_at"], data["expires_at"], data["capability_fingerprint"], _digests(data["bound_hashes"], "$.bound_hashes"), data["repo_revision"], data["dirty_input_fingerprint"], data["route_identity"], native_trace_refs, _strings(data["allowed_effects"], "$.allowed_effects"), _strings(data["observed_effects"], "$.observed_effects"), data["cleanup_state"], data["result"], _strings(data["invalidation_keys"], "$.invalidation_keys"))


def validate_operation_record(mapping: dict[str, Any]) -> OperationRecord:
    lists = {"native_ids", "reconciliation_evidence_refs"}
    fields = {"operation_id", "installation_id", "milestone_id", "operation_kind", "plan_digest", "grant_digest", "canonical_arguments_digest", "idempotency_key", "created_at", "owner_identity", "deployment_epoch", "operation_state", "terminal_result"} | lists
    data = _closed(mapping, "operation record", fields)
    string_fields = fields - lists - {"deployment_epoch", "milestone_id", "terminal_result"}
    _typed(data, {**{key: str for key in string_fields}, "deployment_epoch": int, "milestone_id": str, "terminal_result": str}, {"milestone_id", "terminal_result"})
    try:
        state = OperationState(data["operation_state"])
    except ValueError as exc:
        raise ContractValidationError([ValidationIssue("INVALID_ENUM", "$.operation_state", "unknown operation state")]) from exc
    return OperationRecord(1, data["operation_id"], data["installation_id"], data["milestone_id"], data["operation_kind"], data["plan_digest"], data["grant_digest"], data["canonical_arguments_digest"], data["idempotency_key"], data["created_at"], data["owner_identity"], data["deployment_epoch"], state, _strings(data["native_ids"], "$.native_ids"), _strings(data["reconciliation_evidence_refs"], "$.reconciliation_evidence_refs"), data["terminal_result"])


def validate_command_result(mapping: dict[str, Any]) -> CommandResult:
    required = {"operation", "outcome", "checks", "warnings", "planned_changes", "applied_changes", "next_safe_action"}
    data = _closed(mapping, "command result", required)
    _typed(data, {"operation": str, "outcome": str, "next_safe_action": str}, {"next_safe_action"})
    return CommandResult(1, data["operation"], data["outcome"], _strings(data["checks"], "$.checks"), _strings(data["warnings"], "$.warnings"), _strings(data["planned_changes"], "$.planned_changes"), _strings(data["applied_changes"], "$.applied_changes"), data["next_safe_action"])
