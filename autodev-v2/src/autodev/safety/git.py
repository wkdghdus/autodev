"""Passive Git inspection adapter backed by the safe command runner."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .command import CommandResult, CommandSpec, run_command


class GitPolicyError(ValueError):
    """Raised before process creation for unsupported passive Git requests."""


@dataclass(frozen=True)
class GitRequest:
    operation: str
    args: tuple[str, ...] = ()
    timeout_seconds: float = 30.0


PASSIVE_ENV: tuple[tuple[str, str], ...] = (
    ("GIT_CONFIG_NOSYSTEM", "1"),
    ("GIT_CONFIG_GLOBAL", "/dev/null"),
    ("GIT_ATTR_NOSYSTEM", "1"),
    ("GIT_OPTIONAL_LOCKS", "0"),
    ("GIT_EXTERNAL_DIFF", ""),
    ("GIT_TERMINAL_PROMPT", "0"),
    ("GIT_PAGER", "cat"),
)

DISABLE_CONFIG: tuple[str, ...] = (
    "core.hooksPath=/dev/null",
    "core.fsmonitor=false",
    "core.attributesFile=/dev/null",
    "diff.external=",
    "diff.autodev.textconv=",
    "protocol.file.allow=never",
    "pager.status=false",
    "status.showUntrackedFiles=all",
    "filter.lfs.clean=",
    "filter.lfs.smudge=",
    "filter.lfs.process=",
    "filter.lfs.required=false",
)


def _base_argv(repo_root: str | Path) -> list[str]:
    argv = ["git"]
    for item in DISABLE_CONFIG:
        argv.extend(("-c", item))
    argv.extend(("-C", str(Path(repo_root).resolve(strict=True))))
    return argv


def _validate_rev_parse(args: tuple[str, ...]) -> tuple[str, ...]:
    allowed = {
        "--show-toplevel",
        "--git-common-dir",
        "--is-inside-work-tree",
        "--show-prefix",
        "--absolute-git-dir",
        "--git-dir",
    }
    if not args or any(arg not in allowed for arg in args):
        raise GitPolicyError("rev-parse supports only passive repository metadata flags")
    return args


def _validate_status(args: tuple[str, ...]) -> tuple[str, ...]:
    allowed = {"--porcelain=v2", "-z", "--branch", "--ignored=no", "--untracked-files=all"}
    normalized = args or ("--porcelain=v2", "-z")
    if "--porcelain=v2" not in normalized or any(arg not in allowed for arg in normalized):
        raise GitPolicyError("status supports only porcelain-v2 passive output flags")
    return normalized


def _validate_path_args(args: tuple[str, ...], operation: str) -> tuple[str, ...]:
    if not args:
        return args
    if "--" in args:
        marker = args.index("--")
        options = args[:marker]
        paths = args[marker + 1 :]
    else:
        options = ()
        paths = args
    allowed_options = {"-z", "--cached", "--others", "--ignored", "--exclude-standard"} if operation == "ls-files" else {"-z", "-q"}
    if any(option not in allowed_options for option in options):
        raise GitPolicyError(f"{operation} contains unsupported option")
    if any(
        path.startswith("-") or "\x00" in path or Path(path).is_absolute() or ".." in Path(path).parts for path in paths
    ):
        raise GitPolicyError(f"{operation} paths must be passive relative path arguments")
    return args


def passive_git(repo_root: str | Path, request: GitRequest) -> CommandResult:
    """Run one allowlisted passive Git inspection command."""

    operation = request.operation
    if operation == "rev-parse":
        args = _validate_rev_parse(request.args)
    elif operation == "status":
        args = _validate_status(request.args)
    elif operation in {"ls-files", "check-ignore"}:
        args = _validate_path_args(request.args, operation)
    else:
        raise GitPolicyError("unsupported passive Git operation")

    argv = tuple(_base_argv(repo_root) + [operation, *args])
    return run_command(
        CommandSpec(
            argv=argv,
            cwd=str(Path(repo_root).resolve(strict=True)),
            env=PASSIVE_ENV,
            timeout_seconds=request.timeout_seconds,
        )
    )
