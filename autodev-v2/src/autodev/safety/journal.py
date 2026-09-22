"""Durable idempotent operation journals backed by strict canonical JSON."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .storage import atomic_write_bytes, file_sha256, inspect_recovery, resolve_target, RecoveryStatus


class JournalError(RuntimeError):
    """Base class for journal failures."""


class ChangedOperationError(JournalError):
    """Raised when an idempotency key is reused with different logical fields."""


class JournalRecoveryError(JournalError):
    """Raised when corrupt or ambiguous recovery evidence blocks admission."""


class JournalTransitionError(JournalError):
    """Raised when a compare-and-set state transition fails."""


class OperationState(StrEnum):
    PREPARED = "PREPARED"
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    UNCERTAIN = "UNCERTAIN"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


TERMINAL_STATES = frozenset({OperationState.SUCCEEDED, OperationState.FAILED})


@dataclass(frozen=True)
class OperationRecord:
    operation_id: str
    idempotency_key: str
    operation: str
    arguments_sha256: str
    state: OperationState
    prepared_wall_time: float
    updated_wall_time: float


@dataclass(frozen=True)
class TombstoneRecord:
    operation_id: str
    idempotency_key: str
    operation: str
    arguments_sha256: str
    terminal_state: OperationState
    pruned_wall_time: float


def canonical_json_bytes(value: Any) -> bytes:
    """Encode strict canonical JSON for logical journal fields."""

    _validate_json_value(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _validate_json_value(value: Any) -> None:
    if value is None or type(value) in {str, int, bool}:
        return
    if type(value) is float:
        if value != value or value in {float("inf"), float("-inf")}:
            raise TypeError("JSON floats must be finite")
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_value(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if type(key) is not str:
                raise TypeError("JSON object keys must be strings")
            _validate_json_value(item)
        return
    raise TypeError(f"value of type {type(value).__name__} is not JSON")


def _operation_identity(idempotency_key: str, operation: str, arguments: Any) -> tuple[str, str]:
    canonical_arguments = canonical_json_bytes(arguments)
    arguments_digest = hashlib.sha256(canonical_arguments).hexdigest()
    identity_payload = canonical_json_bytes(
        {
            "arguments_sha256": arguments_digest,
            "idempotency_key": idempotency_key,
            "operation": operation,
        }
    )
    return hashlib.sha256(identity_payload).hexdigest(), arguments_digest


class JournalStore:
    """Single-file durable operation journal below an explicit root."""

    def __init__(self, root: str | Path, target: str | Path):
        self.root = str(root)
        self.target = str(target)

    def _load(self) -> dict[str, Any]:
        recovery = inspect_recovery(self.root, self.target)
        if recovery.status in {RecoveryStatus.CONFLICT, RecoveryStatus.CORRUPT}:
            raise JournalRecoveryError(recovery.message or "journal recovery is ambiguous")
        try:
            path = resolve_target(self.root, self.target, for_write=True)
        except FileNotFoundError:
            return {"schema_version": 1, "operations": {}, "keys": {}, "tombstones": {}}
        if not path.exists():
            return {"schema_version": 1, "operations": {}, "keys": {}, "tombstones": {}}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise JournalRecoveryError("journal is not parseable canonical JSON") from exc
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise JournalRecoveryError("journal schema is unsupported")
        data.setdefault("operations", {})
        data.setdefault("keys", {})
        data.setdefault("tombstones", {})
        return data

    def _save(self, data: dict[str, Any], expected_sha256: str | None) -> None:
        payload = canonical_json_bytes(data)
        atomic_write_bytes(self.root, self.target, payload, expected_sha256=expected_sha256)

    def prepare(self, idempotency_key: str, operation: str, arguments: Any) -> OperationRecord:
        if not idempotency_key or not operation:
            raise ValueError("idempotency_key and operation must be nonempty")
        operation_id, arguments_digest = _operation_identity(idempotency_key, operation, arguments)
        data = self._load()
        current_digest = file_sha256(resolve_target(self.root, self.target, for_write=True))
        existing_id = data["keys"].get(idempotency_key)
        if existing_id is not None:
            raw = data["operations"].get(existing_id) or data["tombstones"].get(existing_id)
            if not raw:
                raise JournalRecoveryError("journal key index references a missing operation")
            if (
                raw.get("operation_id") != operation_id
                or raw.get("operation") != operation
                or raw.get("arguments_sha256") != arguments_digest
            ):
                raise ChangedOperationError("idempotency key already belongs to different canonical arguments")
            return _record_from_dict(raw)

        now = time.time()
        record = OperationRecord(
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            operation=operation,
            arguments_sha256=arguments_digest,
            state=OperationState.PREPARED,
            prepared_wall_time=now,
            updated_wall_time=now,
        )
        data["operations"][operation_id] = _record_to_dict(record)
        data["keys"][idempotency_key] = operation_id
        self._save(data, current_digest)
        return record

    def transition(
        self,
        operation_id: str,
        *,
        expected: OperationState,
        new_state: OperationState,
    ) -> OperationRecord:
        data = self._load()
        current_digest = file_sha256(resolve_target(self.root, self.target, for_write=True))
        raw = data["operations"].get(operation_id)
        if raw is None:
            raise JournalTransitionError("operation is not active")
        record = _record_from_dict(raw)
        if record.state is not expected:
            raise JournalTransitionError("operation state compare-and-set failed")
        updated = OperationRecord(
            operation_id=record.operation_id,
            idempotency_key=record.idempotency_key,
            operation=record.operation,
            arguments_sha256=record.arguments_sha256,
            state=new_state,
            prepared_wall_time=record.prepared_wall_time,
            updated_wall_time=time.time(),
        )
        data["operations"][operation_id] = _record_to_dict(updated)
        self._save(data, current_digest)
        return updated

    def prune_terminal(self, operation_id: str) -> TombstoneRecord:
        data = self._load()
        current_digest = file_sha256(resolve_target(self.root, self.target, for_write=True))
        raw = data["operations"].get(operation_id)
        if raw is None:
            existing = data["tombstones"].get(operation_id)
            if existing is None:
                raise JournalTransitionError("operation is not active")
            return _tombstone_from_dict(existing)
        record = _record_from_dict(raw)
        if record.state not in TERMINAL_STATES:
            raise JournalTransitionError("only terminal records are eligible for pruning")
        tombstone = TombstoneRecord(
            operation_id=record.operation_id,
            idempotency_key=record.idempotency_key,
            operation=record.operation,
            arguments_sha256=record.arguments_sha256,
            terminal_state=record.state,
            pruned_wall_time=time.time(),
        )
        del data["operations"][operation_id]
        data["tombstones"][operation_id] = _tombstone_to_dict(tombstone)
        self._save(data, current_digest)
        return tombstone


def _record_to_dict(record: OperationRecord) -> dict[str, Any]:
    return {
        "operation_id": record.operation_id,
        "idempotency_key": record.idempotency_key,
        "operation": record.operation,
        "arguments_sha256": record.arguments_sha256,
        "state": record.state.value,
        "prepared_wall_time": record.prepared_wall_time,
        "updated_wall_time": record.updated_wall_time,
    }


def _record_from_dict(raw: dict[str, Any]) -> OperationRecord:
    return OperationRecord(
        operation_id=str(raw["operation_id"]),
        idempotency_key=str(raw["idempotency_key"]),
        operation=str(raw["operation"]),
        arguments_sha256=str(raw["arguments_sha256"]),
        state=OperationState(str(raw["state"])),
        prepared_wall_time=float(raw["prepared_wall_time"]),
        updated_wall_time=float(raw["updated_wall_time"]),
    )


def _tombstone_to_dict(record: TombstoneRecord) -> dict[str, Any]:
    return {
        "operation_id": record.operation_id,
        "idempotency_key": record.idempotency_key,
        "operation": record.operation,
        "arguments_sha256": record.arguments_sha256,
        "terminal_state": record.terminal_state.value,
        "pruned_wall_time": record.pruned_wall_time,
    }


def _tombstone_from_dict(raw: dict[str, Any]) -> TombstoneRecord:
    return TombstoneRecord(
        operation_id=str(raw["operation_id"]),
        idempotency_key=str(raw["idempotency_key"]),
        operation=str(raw["operation"]),
        arguments_sha256=str(raw["arguments_sha256"]),
        terminal_state=OperationState(str(raw["terminal_state"])),
        pruned_wall_time=float(raw["pruned_wall_time"]),
    )
