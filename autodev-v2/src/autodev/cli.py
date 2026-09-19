"""Fail-closed AD-00 command line interface."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence

from . import __version__
from .evidence import EvidenceClass, Result

FUTURE_COMMANDS: tuple[str, ...] = (
    "init",
    "approve",
    "doctor",
    "preflight",
    "onboard",
    "validate",
    "enable",
    "disable",
    "cycle",
    "repair",
    "recover",
    "status",
    "list",
)

UNSUPPORTED_EXIT_CODE = 7


def unsupported_command_response(command: str) -> dict[str, object]:
    """Return the deterministic AD-00 placeholder response."""

    return {
        "schema_version": 1,
        "command": command,
        "outcome": Result.UNSUPPORTED.value,
        "implemented": False,
        "evidence_class": EvidenceClass.NOT_RUN.value,
        "live_verified": False,
    }


def _write_json(payload: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")


def _help_text() -> str:
    commands = "\n".join(f"  {command}" for command in FUTURE_COMMANDS)
    return (
        "usage: autodev [--help] [--version] <command>\n\n"
        "AutoDev V2 AD-00 scaffold. Future milestone commands are present only\n"
        "as fail-closed placeholders and perform no live checks or mutations.\n\n"
        "global options:\n"
        "  --help     show this help message and exit\n"
        "  --version  show package version and exit\n\n"
        "placeholder commands:\n"
        f"{commands}\n"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the AD-00 CLI."""

    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args == ["--help"] or args == ["-h"]:
        sys.stdout.write(_help_text())
        return 0

    if args == ["--version"]:
        sys.stdout.write(f"{__version__}\n")
        return 0

    command = args[0]
    if command in FUTURE_COMMANDS:
        _write_json(unsupported_command_response(command))
        return UNSUPPORTED_EXIT_CODE

    _write_json(
        {
            "schema_version": 1,
            "command": command,
            "outcome": Result.UNSUPPORTED.value,
            "implemented": False,
            "evidence_class": EvidenceClass.NOT_RUN.value,
            "live_verified": False,
        }
    )
    return UNSUPPORTED_EXIT_CODE
