"""Ordered non-blocking POSIX locks for local AutoDev safety boundaries."""

from __future__ import annotations

import errno
import json
import os
import socket
import threading
import time
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from pathlib import Path
from types import TracebackType


class LockScope(IntEnum):
    """Lock acquisition order from broadest account scope to repository scope."""

    ACCOUNT = 10
    INSTALLATION = 20
    REPOSITORY = 30


class LockStatus(StrEnum):
    ACQUIRED = "ACQUIRED"
    BUSY = "BUSY"
    UNSUPPORTED = "UNSUPPORTED"
    ORDER_VIOLATION = "ORDER_VIOLATION"


class LockError(RuntimeError):
    """Base class for lock failures."""


class LockOrderError(LockError):
    """Raised when a caller attempts to acquire locks out of order."""


class LockBusyError(LockError):
    """Raised when a non-blocking kernel lock is already held elsewhere."""


class LockUnsupportedError(LockError):
    """Raised when POSIX flock is unavailable."""


@dataclass(frozen=True)
class LockSpec:
    """Explicit local lock location and ordered scope."""

    root: str
    scope: LockScope
    name: str


@dataclass(frozen=True)
class LockMetadata:
    """Diagnostic metadata only; never used as authority to steal a lock."""

    pid: int
    host: str
    acquired_monotonic: float
    acquired_wall_time: float


@dataclass(frozen=True)
class LockAcquireResult:
    status: LockStatus
    path: str
    metadata: LockMetadata | None = None
    message: str | None = None


_THREAD_STATE = threading.local()


def _held_stack() -> list[LockScope]:
    stack = getattr(_THREAD_STATE, "stack", None)
    if stack is None:
        stack = []
        _THREAD_STATE.stack = stack
    return stack


def held_lock_count() -> int:
    """Return the number of locks held by this thread."""

    return len(_held_stack())


def _lock_filename(scope: LockScope, name: str) -> str:
    if not name or name in {".", ".."} or "/" in name or "\x00" in name:
        raise ValueError("lock name must be a nonempty path segment")
    return f"{scope.name.lower()}-{name}.lock"


class OrderedLock:
    """Context-manager wrapper around a single non-blocking kernel flock."""

    def __init__(self, spec: LockSpec):
        self.spec = spec
        root = Path(spec.root)
        self.path = root / _lock_filename(spec.scope, spec.name)
        self._fd: int | None = None
        self._metadata: LockMetadata | None = None

    @property
    def metadata(self) -> LockMetadata | None:
        return self._metadata

    def try_acquire(self) -> LockAcquireResult:
        try:
            import fcntl
        except ImportError:
            return LockAcquireResult(LockStatus.UNSUPPORTED, str(self.path), message="POSIX flock is unavailable")

        stack = _held_stack()
        if stack and self.spec.scope < stack[-1]:
            return LockAcquireResult(
                LockStatus.ORDER_VIOLATION,
                str(self.path),
                message="locks must be acquired in account -> installation -> repository order",
            )

        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            os.close(fd)
            if exc.errno in (errno.EACCES, errno.EAGAIN):
                return LockAcquireResult(LockStatus.BUSY, str(self.path), message="lock is held")
            raise

        metadata = LockMetadata(
            pid=os.getpid(),
            host=socket.gethostname(),
            acquired_monotonic=time.monotonic(),
            acquired_wall_time=time.time(),
        )
        os.ftruncate(fd, 0)
        os.write(fd, json.dumps(metadata.__dict__, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        os.fsync(fd)
        self._fd = fd
        self._metadata = metadata
        stack.append(self.spec.scope)
        return LockAcquireResult(LockStatus.ACQUIRED, str(self.path), metadata=metadata)

    def acquire(self) -> "OrderedLock":
        result = self.try_acquire()
        if result.status is LockStatus.ACQUIRED:
            return self
        if result.status is LockStatus.BUSY:
            raise LockBusyError(result.message or "lock is held")
        if result.status is LockStatus.UNSUPPORTED:
            raise LockUnsupportedError(result.message or "POSIX flock is unavailable")
        raise LockOrderError(result.message or "lock order violation")

    def release(self) -> None:
        if self._fd is None:
            return
        try:
            import fcntl

            fcntl.flock(self._fd, fcntl.LOCK_UN)
        finally:
            os.close(self._fd)
            self._fd = None
            stack = _held_stack()
            if stack:
                stack.pop()

    def __enter__(self) -> "OrderedLock":
        return self.acquire()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.release()


def acquire_lock(spec: LockSpec) -> OrderedLock:
    """Acquire a single ordered lock or raise a typed failure."""

    return OrderedLock(spec).acquire()
