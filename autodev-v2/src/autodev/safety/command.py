"""Bounded subprocess execution with explicit inputs and redacted outputs."""

from __future__ import annotations

import os
import signal
import subprocess
from dataclasses import dataclass
from pathlib import Path

from autodev.redaction import redact_text

from .locks import held_lock_count


class CommandError(RuntimeError):
    """Base class for command runner failures."""


class CommandPolicyError(CommandError):
    """Raised before process creation when a command violates safety policy."""


class CommandExecutionError(CommandError):
    """Raised for process creation failures after redacting diagnostics."""


@dataclass(frozen=True)
class CommandSpec:
    argv: tuple[str, ...]
    cwd: str
    env: tuple[tuple[str, str], ...] = ()
    timeout_seconds: float = 30.0
    max_output_bytes: int = 64 * 1024


@dataclass(frozen=True)
class CommandResult:
    argv: tuple[str, ...]
    cwd: str
    env_keys: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool
    stdout_truncated: bool
    stderr_truncated: bool


def _bounded_decode(data: bytes, limit: int) -> tuple[str, bool]:
    truncated = len(data) > limit
    visible = data[:limit]
    return redact_text(visible.decode("utf-8", errors="replace")), truncated


def run_command(spec: CommandSpec) -> CommandResult:
    """Run a command with shell=False, fresh process group, timeout, and redaction."""

    if isinstance(spec.argv, str) or not isinstance(spec.argv, tuple):
        raise CommandPolicyError("argv must be an explicit tuple of command arguments")
    if not spec.argv or any(type(arg) is not str or not arg or "\x00" in arg for arg in spec.argv):
        raise CommandPolicyError("argv must contain nonempty strings")
    if held_lock_count() > 1:
        raise CommandPolicyError("command execution is denied while multiple ordered locks are held")
    cwd = Path(spec.cwd).resolve(strict=True)
    if not cwd.is_dir():
        raise CommandPolicyError("cwd must be an existing directory")
    if spec.timeout_seconds <= 0:
        raise CommandPolicyError("timeout_seconds must be positive")
    if spec.max_output_bytes < 0:
        raise CommandPolicyError("max_output_bytes must be nonnegative")

    env = {key: value for key, value in spec.env}
    if len(env) != len(spec.env) or any(not key or "=" in key or "\x00" in key for key in env):
        raise CommandPolicyError("environment entries must have unique nonempty keys")

    try:
        process = subprocess.Popen(
            spec.argv,
            cwd=str(cwd),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            start_new_session=True,
        )
    except OSError as exc:
        raise CommandExecutionError(redact_text(str(exc))) from exc

    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=spec.timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(process.pid, signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=2)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = process.communicate()

    stdout_text, stdout_truncated = _bounded_decode(stdout, spec.max_output_bytes)
    stderr_text, stderr_truncated = _bounded_decode(stderr, spec.max_output_bytes)
    return CommandResult(
        argv=tuple(redact_text(arg) for arg in spec.argv),
        cwd=str(cwd),
        env_keys=tuple(sorted(env)),
        returncode=process.returncode,
        stdout=stdout_text,
        stderr=stderr_text,
        timed_out=timed_out,
        stdout_truncated=stdout_truncated,
        stderr_truncated=stderr_truncated,
    )
