"""Small local instrumentation helpers for AD-00 no-live-effect checks."""

from __future__ import annotations

import builtins
import os
from collections.abc import Callable, Iterable
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from unittest import mock


@dataclass(frozen=True)
class EffectEvent:
    """A denied live-effect attempt recorded by the AD-00 harness."""

    kind: str
    target: str


@dataclass
class EffectAudit:
    """Records attempted live effects inside an instrumented local scope."""

    events: list[EffectEvent] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not self.events

    def record(self, kind: str, target: object) -> None:
        self.events.append(EffectEvent(kind=kind, target=str(target)))

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "clean": self.clean,
            "event_count": len(self.events),
            "events": [event.__dict__ for event in self.events],
        }


def _blocked_call(audit: EffectAudit, kind: str) -> Callable[..., Any]:
    def blocked(*args: Any, **_kwargs: Any) -> Any:
        target = args[0] if args else kind
        audit.record(kind, target)
        raise RuntimeError(f"AD-00 live effect blocked: {kind}")

    return blocked


def _audited_open(audit: EffectAudit, original_open: Callable[..., Any]) -> Callable[..., Any]:
    def opened(file: object, mode: str = "r", *args: Any, **kwargs: Any) -> Any:
        if any(flag in mode for flag in ("w", "a", "x", "+")):
            audit.record("open.write", file)
            raise RuntimeError("AD-00 live effect blocked: open.write")
        return original_open(file, mode, *args, **kwargs)

    return opened


@contextmanager
def instrument_live_effects() -> Iterable[EffectAudit]:
    """Patch common live-effect APIs and yield the captured audit.

    This is a unit-test harness, not an operating-system sandbox. It proves
    that exercised code paths did not call these standard-library APIs.
    """

    audit = EffectAudit()
    original_open = builtins.open
    patchers = [
        mock.patch("builtins.open", side_effect=_audited_open(audit, original_open)),
        mock.patch("os.remove", side_effect=_blocked_call(audit, "os.remove")),
        mock.patch("os.unlink", side_effect=_blocked_call(audit, "os.unlink")),
        mock.patch("os.rename", side_effect=_blocked_call(audit, "os.rename")),
        mock.patch("os.replace", side_effect=_blocked_call(audit, "os.replace")),
        mock.patch("os.makedirs", side_effect=_blocked_call(audit, "os.makedirs")),
        mock.patch("os.mkdir", side_effect=_blocked_call(audit, "os.mkdir")),
        mock.patch("urllib.request.urlopen", side_effect=_blocked_call(audit, "urllib.request.urlopen")),
        mock.patch("subprocess.Popen", side_effect=_blocked_call(audit, "subprocess.Popen")),
        mock.patch("socket.create_connection", side_effect=_blocked_call(audit, "socket.create_connection")),
        mock.patch("socket.socket.connect", side_effect=_blocked_call(audit, "socket.socket.connect")),
        mock.patch("pathlib.Path.write_text", side_effect=_blocked_call(audit, "pathlib.Path.write_text")),
        mock.patch("pathlib.Path.write_bytes", side_effect=_blocked_call(audit, "pathlib.Path.write_bytes")),
        mock.patch.object(Path, "unlink", side_effect=_blocked_call(audit, "pathlib.Path.unlink")),
        mock.patch.object(Path, "rename", side_effect=_blocked_call(audit, "pathlib.Path.rename")),
        mock.patch.object(Path, "replace", side_effect=_blocked_call(audit, "pathlib.Path.replace")),
    ]
    # Keep static analysis honest: os is imported because these patch targets are
    # part of the AD-00 effect boundary.
    _ = os
    for patcher in patchers:
        patcher.start()
    try:
        yield audit
    finally:
        for patcher in reversed(patchers):
            patcher.stop()
