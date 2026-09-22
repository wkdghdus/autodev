"""Atomic byte storage under explicit roots with content-free recovery records."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .locks import LockScope, LockSpec, OrderedLock


class StorageError(RuntimeError):
    """Base class for atomic storage failures."""


class UnsafePathError(StorageError):
    """Raised when a relative target escapes or traverses the explicit root."""


class ExpectedDigestMismatch(StorageError):
    """Raised when the on-disk file changed since preview."""


class AmbiguousRecoveryError(StorageError):
    """Raised when recovery evidence is corrupt or cannot be finalized safely."""


class RecoveryStatus(StrEnum):
    NONE = "NONE"
    OLD_PRESENT = "OLD_PRESENT"
    NEW_PRESENT = "NEW_PRESENT"
    CONFLICT = "CONFLICT"
    CORRUPT = "CORRUPT"


@dataclass(frozen=True)
class AtomicWriteResult:
    target: str
    old_sha256: str | None
    new_sha256: str
    recovery_path: str
    bytes_written: int


@dataclass(frozen=True)
class RecoveryRecord:
    schema_version: int
    target: str
    old_sha256: str | None
    new_sha256: str
    temp_name: str
    mode: int
    uid: int | None
    gid: int | None
    prepared_wall_time: float


@dataclass(frozen=True)
class RecoveryInspection:
    status: RecoveryStatus
    target: str
    recovery_path: str
    current_sha256: str | None
    record: RecoveryRecord | None = None
    message: str | None = None


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: str | Path) -> str | None:
    target = Path(path)
    if not target.exists():
        return None
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_relative(target: str | Path) -> Path:
    rel = Path(target)
    if rel.is_absolute() or not rel.parts or any(part in {"..", ""} for part in rel.parts):
        raise UnsafePathError("target must be a nonempty relative path inside the explicit root")
    if "\x00" in str(target):
        raise UnsafePathError("target contains NUL")
    return rel


def resolve_target(root: str | Path, target: str | Path, *, for_write: bool = False) -> Path:
    root_path = Path(root).resolve(strict=True)
    rel = _validate_relative(target)
    candidate = root_path / rel
    parent = candidate.parent
    if for_write:
        existing_parent = parent
        missing: list[Path] = []
        while not existing_parent.exists():
            missing.append(existing_parent)
            existing_parent = existing_parent.parent
        if existing_parent.is_symlink():
            raise UnsafePathError("target parent is a symlink")
        existing_parent.resolve(strict=True).relative_to(root_path)
        for ancestor in parent.parents:
            if ancestor == root_path.parent:
                break
            if ancestor.exists() and ancestor.is_symlink():
                raise UnsafePathError("target parent contains a symlink")
        if candidate.exists() and candidate.is_symlink():
            raise UnsafePathError("target is a symlink")
        return candidate
    resolved = candidate.resolve(strict=True)
    resolved.relative_to(root_path)
    if any((root_path / Path(*rel.parts[:index])).is_symlink() for index in range(1, len(rel.parts) + 1)):
        raise UnsafePathError("target contains a symlink")
    return resolved


def recovery_path_for(root: str | Path, target: str | Path) -> Path:
    path = resolve_target(root, target, for_write=True)
    return path.with_name(f".{path.name}.autodev-recovery.json")


def _fsync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb", closefd=True) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        _fsync_directory(path.parent)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def _record_from_dict(value: dict[str, Any]) -> RecoveryRecord:
    return RecoveryRecord(
        schema_version=int(value["schema_version"]),
        target=str(value["target"]),
        old_sha256=value["old_sha256"] if value["old_sha256"] is None else str(value["old_sha256"]),
        new_sha256=str(value["new_sha256"]),
        temp_name=str(value["temp_name"]),
        mode=int(value["mode"]),
        uid=value["uid"] if value["uid"] is None else int(value["uid"]),
        gid=value["gid"] if value["gid"] is None else int(value["gid"]),
        prepared_wall_time=float(value["prepared_wall_time"]),
    )


def inspect_recovery(root: str | Path, target: str | Path) -> RecoveryInspection:
    path = resolve_target(root, target, for_write=True)
    recovery_path = recovery_path_for(root, target)
    current = file_sha256(path)
    if not recovery_path.exists():
        return RecoveryInspection(RecoveryStatus.NONE, str(path), str(recovery_path), current)
    try:
        raw = json.loads(recovery_path.read_text(encoding="utf-8"))
        record = _record_from_dict(raw)
        if record.schema_version != 1 or record.target != str(_validate_relative(target)):
            raise ValueError("record does not match target")
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        return RecoveryInspection(RecoveryStatus.CORRUPT, str(path), str(recovery_path), current, message=str(exc))
    if current == record.old_sha256:
        status = RecoveryStatus.OLD_PRESENT
    elif current == record.new_sha256:
        status = RecoveryStatus.NEW_PRESENT
    else:
        status = RecoveryStatus.CONFLICT
    return RecoveryInspection(status, str(path), str(recovery_path), current, record=record)


def finalize_recovery(root: str | Path, target: str | Path) -> RecoveryInspection:
    inspection = inspect_recovery(root, target)
    if inspection.status in {RecoveryStatus.CONFLICT, RecoveryStatus.CORRUPT}:
        raise AmbiguousRecoveryError(inspection.message or "ambiguous recovery state blocks mutation")
    if inspection.status is not RecoveryStatus.NONE:
        Path(inspection.recovery_path).unlink(missing_ok=True)
        _fsync_directory(Path(inspection.recovery_path).parent)
    return inspection


def atomic_write_bytes(
    root: str | Path,
    target: str | Path,
    data: bytes,
    *,
    expected_sha256: str | None,
) -> AtomicWriteResult:
    """Replace a relative target atomically after an expected-digest check."""

    rel = _validate_relative(target)
    lock_name = sha256_bytes(str(rel).encode("utf-8"))
    with OrderedLock(LockSpec(str(Path(root).resolve(strict=True) / ".autodev-locks"), LockScope.REPOSITORY, lock_name)):
        return _atomic_write_bytes_unlocked(root, target, data, expected_sha256=expected_sha256)


def _atomic_write_bytes_unlocked(
    root: str | Path,
    target: str | Path,
    data: bytes,
    *,
    expected_sha256: str | None,
) -> AtomicWriteResult:
    inspection = inspect_recovery(root, target)
    if inspection.status in {RecoveryStatus.CONFLICT, RecoveryStatus.CORRUPT}:
        raise AmbiguousRecoveryError(inspection.message or "ambiguous recovery state blocks mutation")

    path = resolve_target(root, target, for_write=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        raise UnsafePathError("target is a symlink")
    old_digest = file_sha256(path)
    if old_digest != expected_sha256:
        raise ExpectedDigestMismatch("current file digest does not match expected preview digest")

    new_digest = sha256_bytes(data)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    recovery_path = recovery_path_for(root, target)
    stat_result = path.stat() if path.exists() else None
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb", closefd=True) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        record = RecoveryRecord(
            schema_version=1,
            target=str(_validate_relative(target)),
            old_sha256=old_digest,
            new_sha256=new_digest,
            temp_name=Path(temp_name).name,
            mode=stat.S_IMODE(stat_result.st_mode) if stat_result else 0o600,
            uid=stat_result.st_uid if stat_result else None,
            gid=stat_result.st_gid if stat_result else None,
            prepared_wall_time=time.time(),
        )
        _write_json_atomic(recovery_path, record.__dict__)
        os.replace(temp_name, path)
        os.chmod(path, 0o600)
        _fsync_directory(path.parent)
        return AtomicWriteResult(str(path), old_digest, new_digest, str(recovery_path), len(data))
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
