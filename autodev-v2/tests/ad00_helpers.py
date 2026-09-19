"""Shared helpers for AD-00 contract tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

PLACEHOLDER_COMMANDS = (
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

EXPECTED_SOURCES = {
    "S1": {
        "title": "Lessons Learned from Nous Autonomous Supervisor Setup",
        "filename": "Pasted markdown(2).md",
        "sha256": "6ace331bbf3f2ee7af23b46f8cbd579290c434e0f3d913a0e0eccc2d035b928d",
    },
    "S2": {
        "title": "Hermes + Gajae Automated Onboarding: Lessons from Nous",
        "filename": "Pasted markdown (2).md",
        "sha256": "d0ea218d74b658f174bd8566c8bf017981b06d7df51a12df4ecb94e997bf052b",
    },
    "S3": {
        "title": "Lessons Learned From Nous Autonomous Onboarding",
        "filename": "Pasted markdown (3).md",
        "sha256": "bdac1bb84c3de3f695462d371ee3509e9a98007f9091b2292ad6f83eb2dd43b5",
    },
}

UNKNOWN_CATEGORIES = (
    "hermes",
    "gjc",
    "runtime",
    "route",
    "account",
    "profile",
    "schedule",
    "message",
    "host",
    "process",
    "enforcement",
)

SYNTHETIC_STATES = (
    "ready",
    "active",
    "uncertain",
    "verifying",
    "human-blocked",
    "completed",
)


def ensure_src_on_path() -> None:
    src = str(SRC_ROOT)
    if src not in sys.path:
        sys.path.insert(0, src)


def run_autodev(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(SRC_ROOT) if not existing else f"{SRC_ROOT}{os.pathsep}{existing}"
    return subprocess.run(
        [sys.executable, "-m", "autodev", *args],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def decode_json_output(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    try:
        payload = json.loads(combined)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"expected deterministic JSON output, got: {combined!r}") from exc
    if not isinstance(payload, dict):
        raise AssertionError(f"expected JSON object, got {type(payload).__name__}")
    return payload


def json_files_under(*parts: str) -> list[Path]:
    root = PROJECT_ROOT.joinpath(*parts)
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.json") if path.is_file())


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for key, item in value.items():
            result.extend(flatten_strings(key))
            result.extend(flatten_strings(item))
        return result
    if isinstance(value, (list, tuple)):
        result = []
        for item in value:
            result.extend(flatten_strings(item))
        return result
    return [] if value is None else [str(value)]


def iter_records(value: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if isinstance(value, dict):
        records.append(value)
        for item in value.values():
            records.extend(iter_records(item))
    elif isinstance(value, list):
        for item in value:
            records.extend(iter_records(item))
    return records


def find_json_document_containing(root_parts: tuple[str, ...], *needles: str) -> tuple[Path, Any]:
    lowered_needles = tuple(needle.lower() for needle in needles)
    for path in json_files_under(*root_parts):
        data = load_json(path)
        haystack = "\n".join(flatten_strings(data)).lower()
        if all(needle in haystack for needle in lowered_needles):
            return path, data
    raise AssertionError(
        f"no JSON document under {'/'.join(root_parts)} contains all of: {', '.join(needles)}"
    )


def read_text_tree(*parts: str) -> str:
    root = PROJECT_ROOT.joinpath(*parts)
    if not root.exists():
        return ""
    chunks = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt", ".yaml", ".yml"}:
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)
