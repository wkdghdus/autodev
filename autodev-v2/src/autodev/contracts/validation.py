"""Strict YAML ingestion and schema validation without discovery or writes."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable
from uuid import UUID

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.error import MarkedYAMLError
from ruamel.yaml.tokens import AliasToken, AnchorToken, TagToken

from .errors import ContractValidationError, ValidationIssue
from .models import (
    ApprovalState,
    AuthorityConfig,
    ContentReference,
    DiscoveryConfig,
    ExecutionConfig,
    ExecutionIndex,
    Milestone,
    MilestoneApproval,
    MilestoneScope,
    Permission,
    ProjectConfig,
    ProjectIdentity,
    SetupState,
    SourcesConfig,
    VerificationCommand,
    VerificationConfig,
)

MAX_DOCUMENT_BYTES = 1024 * 1024
_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")


def _mark(obj: Any, key: Any | None = None) -> tuple[int | None, int | None]:
    try:
        point = obj.lc.key(key) if key is not None else (obj.lc.line, obj.lc.col)
        return point[0] + 1, point[1] + 1
    except (AttributeError, KeyError, TypeError):
        return None, None


class _Issues:
    def __init__(self) -> None:
        self.items: list[ValidationIssue] = []

    def add(self, code: str, path: str, message: str, obj: Any = None, key: Any = None) -> None:
        line, column = _mark(obj, key)
        self.items.append(ValidationIssue(code, path, message, line, column))

    def require_keys(self, value: Any, path: str, allowed: set[str], required: set[str]) -> bool:
        if not isinstance(value, dict):
            self.add("TYPE", path, "must be a mapping", value)
            return False
        for key in value:
            if key not in allowed:
                self.add("UNKNOWN_FIELD", f"{path}.{key}", "unknown field", value, key)
        for key in sorted(required):
            if key not in value:
                self.add("REQUIRED", f"{path}.{key}", "required field is missing", value)
        return True


def _decode(source: bytes | str) -> str:
    if isinstance(source, bytes):
        if len(source) > MAX_DOCUMENT_BYTES:
            raise ContractValidationError([ValidationIssue("INPUT_TOO_LARGE", "$", "input exceeds 1 MiB")])
        try:
            return source.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ContractValidationError(
                [ValidationIssue("INVALID_UTF8", "$", "input must be UTF-8", exc.start + 1, 1)]
            ) from exc
    if not isinstance(source, str):
        raise TypeError("source must be bytes or str")
    if len(source.encode("utf-8")) > MAX_DOCUMENT_BYTES:
        raise ContractValidationError([ValidationIssue("INPUT_TOO_LARGE", "$", "input exceeds 1 MiB")])
    return source


def _load_yaml(source: bytes | str) -> CommentedMap:
    text = _decode(source)
    yaml = YAML(typ="rt", pure=True)
    yaml.version = (1, 2)
    yaml.allow_duplicate_keys = False
    try:
        for token in yaml.scan(text):
            if isinstance(token, (AliasToken, AnchorToken, TagToken)):
                mark = token.start_mark
                kind = type(token).__name__.removesuffix("Token").lower()
                raise ContractValidationError(
                    [ValidationIssue("UNSAFE_YAML", "$", f"YAML {kind}s are not allowed", mark.line + 1, mark.column + 1)]
                )
        documents = list(yaml.load_all(text))
    except ContractValidationError:
        raise
    except MarkedYAMLError as exc:
        mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
        code = "DUPLICATE_KEY" if "duplicate key" in str(exc).lower() else "MALFORMED_YAML"
        raise ContractValidationError(
            [
                ValidationIssue(
                    code,
                    "$",
                    str(getattr(exc, "problem", None) or "malformed YAML"),
                    mark.line + 1 if mark else None,
                    mark.column + 1 if mark else None,
                )
            ]
        ) from exc
    if len(documents) != 1:
        line, column = _mark(documents[1] if len(documents) > 1 else None)
        raise ContractValidationError(
            [ValidationIssue("MULTIPLE_DOCUMENTS", "$", "exactly one YAML document is required", line, column)]
        )
    data = documents[0]
    if not isinstance(data, CommentedMap):
        raise ContractValidationError([ValidationIssue("TYPE", "$", "document root must be a mapping", 1, 1)])
    issues = _Issues()
    _check_yaml_tree(data, "$", issues)
    if issues.items:
        raise ContractValidationError(issues.items)
    return data


def _check_yaml_tree(value: Any, path: str, issues: _Issues) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                issues.add("NON_STRING_KEY", path, "mapping keys must be strings", value, key)
                continue
            child_path = f"{path}.{key}"
            if key == "<<":
                issues.add("MERGE_KEY", child_path, "YAML merge keys are not allowed", value, key)
            _check_yaml_tree(child, child_path, issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _check_yaml_tree(child, f"{path}[{index}]", issues)


def _scalar(
    mapping: dict[str, Any], key: str, path: str, expected: type, issues: _Issues, *, nullable: bool = False
) -> Any:
    value = mapping.get(key)
    if value is None and nullable:
        return None
    if type(value) is not expected:
        issues.add("TYPE", f"{path}.{key}", f"must be {expected.__name__}", mapping, key)
        return None
    return value


def _nonempty_string(mapping: dict[str, Any], key: str, path: str, issues: _Issues) -> str | None:
    value = _scalar(mapping, key, path, str, issues)
    if value is not None and not value.strip():
        issues.add("EMPTY", f"{path}.{key}", "must be nonempty", mapping, key)
        return None
    return value


def _uuid(value: Any, path: str, obj: Any, key: str, issues: _Issues, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if type(value) is not str:
        issues.add("TYPE", path, "must be a UUID string", obj, key)
        return None
    try:
        parsed = UUID(value)
    except ValueError:
        issues.add("INVALID_UUID", path, "must be a valid UUID", obj, key)
        return None
    if str(parsed) != value:
        issues.add("INVALID_UUID", path, "UUID must use canonical lowercase form", obj, key)
        return None
    return value


def _portable_path(
    value: Any,
    path: str,
    root: Path,
    obj: Any,
    key: Any,
    issues: _Issues,
    *,
    nullable: bool = False,
) -> str | None:
    if value is None and nullable:
        return None
    if type(value) is not str or not value:
        issues.add("TYPE", path, "must be a nonempty relative path string", obj, key)
        return None
    if "\x00" in value:
        issues.add("INVALID_PATH", path, "path contains NUL", obj, key)
        return None
    candidate = Path(value)
    if candidate.is_absolute() or any(part == ".." for part in candidate.parts):
        issues.add("ROOT_ESCAPE", path, "path must remain relative to the repository root", obj, key)
        return None
    resolved_root = root.resolve()
    try:
        (resolved_root / candidate).resolve().relative_to(resolved_root)
    except ValueError:
        issues.add("ROOT_ESCAPE", path, "path resolves outside the repository root", obj, key)
        return None
    return value


def _path_list(value: Any, path: str, root: Path, issues: _Issues) -> tuple[str, ...]:
    if not isinstance(value, list):
        issues.add("TYPE", path, "must be a list", value)
        return ()
    result: list[str] = []
    seen: dict[str, str] = {}
    for index, item in enumerate(value):
        valid = _portable_path(item, f"{path}[{index}]", root, value, index, issues)
        if valid is None:
            continue
        folded = valid.casefold()
        if folded in seen and seen[folded] != valid:
            issues.add("CASE_COLLISION", f"{path}[{index}]", f"path case-collides with {seen[folded]!r}", value, index)
        else:
            seen[folded] = valid
        result.append(valid)
    return tuple(result)


def load_project_yaml(source: bytes | str, repository_root: str | Path) -> ProjectConfig:
    """Load PROJECT YAML from explicit content under an explicit repository root."""

    root = Path(repository_root)
    data = _load_yaml(source)
    issues = _Issues()
    top = {"schema_version", "setup_state", "project", "sources", "execution", "verification", "authority"}
    issues.require_keys(data, "$", top, top)
    version = _scalar(data, "schema_version", "$", int, issues)
    if version is not None and version != 2:
        issues.add("UNSUPPORTED_VERSION", "$.schema_version", "supported PROJECT schema version is 2", data, "schema_version")
    setup_raw = _scalar(data, "setup_state", "$", str, issues)
    try:
        setup = SetupState(setup_raw)
    except (ValueError, TypeError):
        issues.add("INVALID_ENUM", "$.setup_state", "must be draft or configured", data, "setup_state")
        setup = SetupState.DRAFT
    draft = setup is SetupState.DRAFT

    project = data.get("project")
    issues.require_keys(project, "$.project", {"id", "slug", "name"}, {"id", "slug", "name"})
    if not isinstance(project, dict):
        project = {}
    project_id = _uuid(project.get("id"), "$.project.id", project, "id", issues, nullable=draft)
    slug = _scalar(project, "slug", "$.project", str, issues, nullable=draft)
    if slug is not None and not _SLUG.fullmatch(slug):
        issues.add("INVALID_SLUG", "$.project.slug", "must be a lowercase hyphenated slug", project, "slug")
    name = _scalar(project, "name", "$.project", str, issues, nullable=draft)
    if name is not None and not name.strip():
        issues.add("EMPTY", "$.project.name", "must be nonempty", project, "name")

    sources = data.get("sources")
    issues.require_keys(sources, "$.sources", {"requirements", "context", "discovery", "execution_index"}, {"requirements", "context", "discovery", "execution_index"})
    if not isinstance(sources, dict):
        sources = {}
    requirements = _path_list(sources.get("requirements"), "$.sources.requirements", root, issues)
    context = _path_list(sources.get("context"), "$.sources.context", root, issues)
    if not draft and not requirements:
        issues.add("REQUIRED", "$.sources.requirements", "configured projects require at least one requirements source", sources, "requirements")
    discovery = sources.get("discovery")
    issues.require_keys(discovery, "$.sources.discovery", {"roots"}, {"roots"})
    if not isinstance(discovery, dict):
        discovery = {}
    roots = _path_list(discovery.get("roots"), "$.sources.discovery.roots", root, issues)
    if not draft and not roots:
        issues.add("REQUIRED", "$.sources.discovery.roots", "at least one discovery root is required", discovery, "roots")
    execution_index = _portable_path(
        sources.get("execution_index"),
        "$.sources.execution_index",
        root,
        sources,
        "execution_index",
        issues,
        nullable=draft,
    )

    execution = data.get("execution")
    execution_keys = {"harness", "workflow", "base_policy", "target_ref", "max_active_milestones", "max_primary_actions_per_cycle"}
    issues.require_keys(execution, "$.execution", execution_keys, execution_keys)
    if not isinstance(execution, dict):
        execution = {}
    harness = _scalar(execution, "harness", "$.execution", str, issues, nullable=draft)
    workflow = _scalar(execution, "workflow", "$.execution", str, issues, nullable=draft)
    base_policy = _scalar(execution, "base_policy", "$.execution", str, issues, nullable=draft)
    target_ref = _scalar(execution, "target_ref", "$.execution", str, issues, nullable=draft)
    max_active = _scalar(execution, "max_active_milestones", "$.execution", int, issues, nullable=draft)
    max_actions = _scalar(execution, "max_primary_actions_per_cycle", "$.execution", int, issues, nullable=draft)
    for key, actual, expected in (
        ("harness", harness, "gajae"), ("workflow", workflow, "approved_roadmap_only"),
        ("base_policy", base_policy, "dependencies_integrated"), ("max_active_milestones", max_active, 1),
        ("max_primary_actions_per_cycle", max_actions, 1),
    ):
        if actual is not None and actual != expected:
            issues.add("UNSUPPORTED_VALUE", f"$.execution.{key}", f"must be {expected!r}", execution, key)
    if target_ref is not None and not target_ref.strip():
        issues.add("EMPTY", "$.execution.target_ref", "must be nonempty", execution, "target_ref")

    verification = data.get("verification")
    verification_keys = {"commands", "acceptance_sources", "require_independent_review"}
    issues.require_keys(verification, "$.verification", verification_keys, verification_keys)
    if not isinstance(verification, dict):
        verification = {}
    commands = _verification_commands(verification.get("commands"), root, issues)
    acceptance_sources = _path_list(verification.get("acceptance_sources"), "$.verification.acceptance_sources", root, issues)
    independent = _scalar(verification, "require_independent_review", "$.verification", bool, issues, nullable=draft)
    if independent is not None and independent is not True:
        issues.add("UNSUPPORTED_VALUE", "$.verification.require_independent_review", "must be true", verification, "require_independent_review")
    if not draft and (not commands or not acceptance_sources):
        issues.add("REQUIRED", "$.verification", "configured projects require commands and acceptance sources", verification)

    authority = data.get("authority")
    issues.require_keys(authority, "$.authority", {"requested"}, {"requested"})
    if not isinstance(authority, dict):
        authority = {}
    requested = authority.get("requested")
    if not isinstance(requested, dict):
        issues.add("TYPE", "$.authority.requested", "must be a permission mapping", requested)
        requested = {}
    permissions: list[tuple[str, Permission]] = []
    for key, raw in requested.items():
        if not key:
            issues.add("EMPTY", "$.authority.requested", "permission names must be nonempty", requested, key)
            continue
        if type(raw) is not str or raw not in {"denied", "human", "autonomous"}:
            issues.add("INVALID_PERMISSION", f"$.authority.requested.{key}", "must be denied, human, or autonomous", requested, key)
            continue
        permissions.append((key, Permission.from_value(raw)))
    if not draft and not permissions:
        issues.add("REQUIRED", "$.authority.requested", "configured projects require explicit permission requests", requested)

    if issues.items:
        raise ContractValidationError(issues.items)
    return ProjectConfig(
        2, setup, ProjectIdentity(project_id, slug, name),
        SourcesConfig(requirements, context, DiscoveryConfig(roots), execution_index),
        ExecutionConfig(harness, workflow, base_policy, target_ref, max_active, max_actions),
        VerificationConfig(commands, acceptance_sources, independent), AuthorityConfig(tuple(permissions)),
    )


def _verification_commands(value: Any, root: Path, issues: _Issues) -> tuple[VerificationCommand, ...]:
    if not isinstance(value, list):
        issues.add("TYPE", "$.verification.commands", "must be a list", value)
        return ()
    result: list[VerificationCommand] = []
    seen: set[str] = set()
    allowed = {"id", "argv", "cwd", "input_paths", "network_policy", "timeout_seconds", "approval_binding"}
    for index, item in enumerate(value):
        path = f"$.verification.commands[{index}]"
        issues.require_keys(item, path, allowed, allowed)
        if not isinstance(item, dict):
            continue
        command_id = _nonempty_string(item, "id", path, issues)
        argv = item.get("argv")
        if not isinstance(argv, list) or not argv or any(type(arg) is not str or not arg for arg in argv):
            issues.add("INVALID_ARGV", f"{path}.argv", "must be a nonempty list of nonempty strings", item, "argv")
            argv = []
        cwd = _portable_path(item.get("cwd"), f"{path}.cwd", root, item, "cwd", issues)
        inputs = _path_list(item.get("input_paths"), f"{path}.input_paths", root, issues)
        network = _nonempty_string(item, "network_policy", path, issues)
        timeout = _scalar(item, "timeout_seconds", path, int, issues)
        binding = _nonempty_string(item, "approval_binding", path, issues)
        if timeout is not None and timeout <= 0:
            issues.add("RANGE", f"{path}.timeout_seconds", "must be positive", item, "timeout_seconds")
        if command_id in seen:
            issues.add("DUPLICATE_ID", f"{path}.id", "verification command ID must be unique", item, "id")
        elif command_id:
            seen.add(command_id)
        if all(x is not None for x in (command_id, cwd, network, timeout, binding)) and argv:
            result.append(VerificationCommand(command_id, tuple(argv), cwd, inputs, network, timeout, binding))
    return tuple(result)


def load_execution_yaml(
    source: bytes | str,
    repository_root: str | Path,
    *,
    project: ProjectConfig | None = None,
    verification_ids: Iterable[str] | None = None,
) -> ExecutionIndex:
    """Load EXECUTION YAML and optionally bind it to a PROJECT contract."""

    root = Path(repository_root)
    data = _load_yaml(source)
    issues = _Issues()
    allowed = {"schema_version", "project_id", "milestones"}
    issues.require_keys(data, "$", allowed, allowed)
    version = _scalar(data, "schema_version", "$", int, issues)
    if version is not None and version != 2:
        issues.add("UNSUPPORTED_VERSION", "$.schema_version", "supported EXECUTION schema version is 2", data, "schema_version")
    project_id = _uuid(data.get("project_id"), "$.project_id", data, "project_id", issues)
    if project is not None and project.project.id != project_id:
        issues.add("PROJECT_ID_MISMATCH", "$.project_id", "must match PROJECT project.id", data, "project_id")
    known_verification = set(verification_ids or ())
    if project is not None:
        known_verification.update(command.id for command in project.verification.commands)
    raw_milestones = data.get("milestones")
    if not isinstance(raw_milestones, list):
        issues.add("TYPE", "$.milestones", "must be a list", raw_milestones)
        raw_milestones = []
    milestones: list[Milestone] = []
    ids: set[str] = set()
    dependency_rows: list[tuple[str, tuple[str, ...], Any]] = []
    milestone_keys = {"id", "title", "depends_on", "authority_refs", "acceptance_refs", "scope", "verification_ids", "approval", "base_policy", "evidence_refs"}
    for index, item in enumerate(raw_milestones):
        path = f"$.milestones[{index}]"
        issues.require_keys(item, path, milestone_keys, milestone_keys)
        if not isinstance(item, dict):
            continue
        milestone_id = _nonempty_string(item, "id", path, issues)
        title = _nonempty_string(item, "title", path, issues)
        if not milestone_id or (milestone_id in ids):
            if milestone_id in ids:
                issues.add("DUPLICATE_ID", f"{path}.id", "milestone ID must be unique", item, "id")
        else:
            ids.add(milestone_id)
        depends = _string_list(item.get("depends_on"), f"{path}.depends_on", issues)
        authority_refs = _content_refs(item.get("authority_refs"), f"{path}.authority_refs", root, issues)
        acceptance_refs = _content_refs(item.get("acceptance_refs"), f"{path}.acceptance_refs", root, issues)
        scope = _scope(item.get("scope"), f"{path}.scope", root, issues)
        milestone_verification = _string_list(item.get("verification_ids"), f"{path}.verification_ids", issues)
        if not milestone_verification:
            issues.add("REQUIRED", f"{path}.verification_ids", "at least one verification ID is required", item, "verification_ids")
        for verification_id in milestone_verification:
            if known_verification and verification_id not in known_verification:
                issues.add("UNKNOWN_REFERENCE", f"{path}.verification_ids", f"unknown verification ID {verification_id!r}", item, "verification_ids")
        approval = _approval(item.get("approval"), f"{path}.approval", root, issues)
        base_policy = _scalar(item, "base_policy", path, str, issues)
        if base_policy is not None and base_policy != "dependencies_integrated":
            issues.add("UNSUPPORTED_VALUE", f"{path}.base_policy", "must be 'dependencies_integrated'", item, "base_policy")
        evidence_refs = _path_list(item.get("evidence_refs"), f"{path}.evidence_refs", root, issues)
        if milestone_id:
            dependency_rows.append((milestone_id, depends, item))
        if all(x is not None for x in (milestone_id, title, scope, approval, base_policy)):
            milestones.append(Milestone(milestone_id, title, depends, authority_refs, acceptance_refs, scope, milestone_verification, approval, base_policy, evidence_refs))
    for milestone_id, depends, item in dependency_rows:
        for dependency in depends:
            if dependency not in ids:
                issues.add("MISSING_DEPENDENCY", f"$.milestones[{milestone_id}].depends_on", f"unknown milestone {dependency!r}", item, "depends_on")
    _check_cycles(dependency_rows, issues)
    if issues.items:
        raise ContractValidationError(issues.items)
    return ExecutionIndex(2, project_id, tuple(milestones))


def _string_list(value: Any, path: str, issues: _Issues) -> tuple[str, ...]:
    if not isinstance(value, list) or any(type(item) is not str or not item for item in value):
        issues.add("TYPE", path, "must be a list of nonempty strings", value)
        return ()
    return tuple(value)


def _content_refs(value: Any, path: str, root: Path, issues: _Issues) -> tuple[ContentReference, ...]:
    if not isinstance(value, list) or not value:
        issues.add("REQUIRED", path, "at least one content reference is required", value)
        return ()
    result: list[ContentReference] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        allowed = {"path", "reference", "digest"}
        issues.require_keys(item, item_path, allowed, allowed)
        if not isinstance(item, dict):
            continue
        source_path = _portable_path(item.get("path"), f"{item_path}.path", root, item, "path", issues)
        reference = _nonempty_string(item, "reference", item_path, issues)
        digest = _scalar(item, "digest", item_path, str, issues)
        if digest is not None and not _DIGEST.fullmatch(digest):
            issues.add("INVALID_DIGEST", f"{item_path}.digest", "must be a lowercase SHA-256 digest", item, "digest")
        if source_path and reference and digest and _DIGEST.fullmatch(digest):
            result.append(ContentReference(source_path, reference, digest))
    return tuple(result)


def _scope(value: Any, path: str, root: Path, issues: _Issues) -> MilestoneScope | None:
    allowed = {"allowed_paths", "exclusions", "prohibited_operations"}
    if not issues.require_keys(value, path, allowed, allowed):
        return None
    allowed_paths = _path_list(value.get("allowed_paths"), f"{path}.allowed_paths", root, issues)
    exclusions = _path_list(value.get("exclusions"), f"{path}.exclusions", root, issues)
    prohibited = _string_list(value.get("prohibited_operations"), f"{path}.prohibited_operations", issues)
    if not allowed_paths:
        issues.add("REQUIRED", f"{path}.allowed_paths", "scope must include allowed product paths", value, "allowed_paths")
    return MilestoneScope(allowed_paths, exclusions, prohibited)


def _approval(value: Any, path: str, root: Path, issues: _Issues) -> MilestoneApproval | None:
    allowed = {"state", "receipt_ref"}
    if not issues.require_keys(value, path, allowed, {"state", "receipt_ref"}):
        return None
    raw = _scalar(value, "state", path, str, issues)
    try:
        state = ApprovalState(raw)
    except (ValueError, TypeError):
        issues.add("INVALID_ENUM", f"{path}.state", "must be proposed, approved, or revoked", value, "state")
        return None
    receipt = value.get("receipt_ref")
    if receipt is not None:
        receipt = _portable_path(receipt, f"{path}.receipt_ref", root, value, "receipt_ref", issues)
    if state is ApprovalState.APPROVED and not receipt:
        issues.add("RECEIPT_REQUIRED", f"{path}.receipt_ref", "approved milestones require a receipt reference", value, "receipt_ref")
    if state is ApprovalState.REVOKED:
        issues.add("APPROVAL_REVOKED", f"{path}.state", "revoked milestones are not selectable", value, "state")
    return MilestoneApproval(state, receipt)


def _check_cycles(rows: list[tuple[str, tuple[str, ...], Any]], issues: _Issues) -> None:
    graph: dict[str, tuple[str, ...]] = {}
    for milestone_id, dependencies, _ in rows:
        graph.setdefault(milestone_id, dependencies)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            issues.add("DEPENDENCY_CYCLE", "$.milestones", f"dependency cycle includes {node!r}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, ()):
            if dependency in graph:
                visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def validate_mapping_record(
    mapping: dict[str, Any], *, record_name: str, allowed_fields: set[str], required_fields: set[str], schema_version: int = 1
) -> dict[str, Any]:
    """Validate a host-owned mapping's version and closed field set without coercion."""

    issues = _Issues()
    issues.require_keys(mapping, "$", allowed_fields | {"schema_version"}, required_fields | {"schema_version"})
    version = mapping.get("schema_version")
    if type(version) is not int:
        issues.add("TYPE", "$.schema_version", "must be int", mapping, "schema_version")
    elif version != schema_version:
        issues.add("UNSUPPORTED_VERSION", "$.schema_version", f"supported {record_name} schema version is {schema_version}", mapping, "schema_version")
    if issues.items:
        raise ContractValidationError(issues.items)
    return dict(mapping)
