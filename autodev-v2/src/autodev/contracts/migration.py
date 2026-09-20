"""Preview-only migration helpers for legacy repository contracts."""

from __future__ import annotations

import hashlib
from typing import Any

from .models import MigrationPlan
from .validation import _load_yaml


_DRAFT_V2_CONSTANTS: tuple[tuple[str, Any], ...] = (
    ("PROJECT.schema_version", 2),
    ("PROJECT.setup_state", "draft"),
    ("PROJECT.execution.harness", "gajae"),
    ("PROJECT.execution.workflow", "approved_roadmap_only"),
    ("PROJECT.execution.base_policy", "dependencies_integrated"),
    ("PROJECT.execution.max_active_milestones", 1),
    ("PROJECT.execution.max_primary_actions_per_cycle", 1),
    ("PROJECT.verification.require_independent_review", True),
    ("EXECUTION.schema_version", 2),
)


def preview_v1_migration(source_bytes: bytes) -> MigrationPlan:
    """Produce a deterministic, non-applicable draft migration preview.

    No authoritative V1 schema exists, so this function inventories the source
    structure and records only known V2 constants. All legacy semantic values
    remain unresolved, and there is intentionally no apply/write behavior.
    """

    if not isinstance(source_bytes, bytes):
        raise TypeError("source_bytes must be bytes")

    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    legacy_fields = _legacy_field_inventory(source_bytes)
    unresolved = tuple(path for path, _ in legacy_fields if path != "$")
    return MigrationPlan(
        schema_version=1,
        source_sha256=source_sha256,
        legacy_fields=legacy_fields,
        unresolved_fields=unresolved,
        draft_target=_DRAFT_V2_CONSTANTS,
        applicable=False,
        writes_performed=False,
    )


def _legacy_field_inventory(source_bytes: bytes) -> tuple[tuple[str, str], ...]:
    data = _load_yaml(source_bytes)
    fields: list[tuple[str, str]] = []
    _walk_legacy(data, "$", fields)
    return tuple(fields)


def _walk_legacy(value: Any, path: str, fields: list[tuple[str, str]]) -> None:
    fields.append((path, _legacy_type(value)))
    if isinstance(value, dict):
        for key, child in value.items():
            key_part = str(key)
            _walk_legacy(child, f"{path}.{key_part}", fields)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_legacy(child, f"{path}[{index}]", fields)


def _legacy_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, dict):
        return "mapping"
    if isinstance(value, list):
        return "sequence"
    return type(value).__name__
