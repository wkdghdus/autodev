#!/usr/bin/env python3
"""Build deterministic, bounded AD milestone context snapshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


MILESTONE_RE = re.compile(r"^AD-\d{2}$")
HEADING_RE = re.compile(r"^(#{1,6})\s+")
EXPECTED_MILESTONES = [f"AD-{index:02d}" for index in range(24)]
FAULT_ID_RE = re.compile(r"^F\d{2}$")
FAULT_RANGE_RE = re.compile(r"^F\d{2}-F\d{2}$")
FORBIDDEN_DEFAULT_PATHS = {
    "AutoDev_v2_Complete_Specification.md",
    "05-MILESTONE-PLAN.md",
    "README.md",
    ".omx",
}


class ContextError(RuntimeError):
    """Fail-closed context construction error."""


@dataclass(frozen=True)
class SourcePart:
    label: str
    path: str
    selector: dict[str, str]
    content: str
    source_sha256: str
    selected_sha256: str
    reason: str | None = None
    predecessor: str | None = None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_context_map(root: Path | None = None) -> dict[str, Any]:
    root = root or repo_root()
    path = root / "context" / "context-map.json"
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ContextError(f"context map missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContextError(f"context map is invalid JSON: {path}: {exc}") from exc
    validate_context_map(data)
    return data


def validate_context_map(data: dict[str, Any]) -> None:
    if data.get("schema_version") != 1:
        raise ContextError("context map schema_version must be 1")
    if not isinstance(data.get("default_byte_budget"), int) or data["default_byte_budget"] <= 0:
        raise ContextError("context map default_byte_budget must be a positive integer")
    milestones = data.get("milestones")
    if not isinstance(milestones, dict):
        raise ContextError("context map milestones must be an object")
    keys = sorted(milestones)
    if keys != EXPECTED_MILESTONES:
        raise ContextError(f"context map must contain exactly AD-00..AD-23, got {keys}")
    for section_name in ("shared_documents",):
        docs = data.get(section_name, [])
        if not isinstance(docs, list):
            raise ContextError(f"{section_name} must be a list")
        for item in docs:
            validate_document_entry(item, f"{section_name} entry")
            assert_not_forbidden_default_path(item["path"])
    fault_matrix = data.get("fault_matrix")
    if not isinstance(fault_matrix, dict):
        raise ContextError("context map fault_matrix must be an object")
    validate_document_entry(fault_matrix, "fault_matrix")
    assert_not_forbidden_default_path(fault_matrix["path"])
    for milestone, entry in milestones.items():
        if not isinstance(entry, dict):
            raise ContextError(f"{milestone} map entry must be an object")
        for key in ("title", "documents", "fault_ids", "predecessor_evidence", "implementation_roots"):
            if key not in entry:
                raise ContextError(f"{milestone} missing required key {key}")
        if not isinstance(entry["documents"], list) or not entry["documents"]:
            raise ContextError(f"{milestone} documents must be a non-empty list")
        for doc in entry["documents"]:
            validate_document_entry(doc, f"{milestone} document")
            assert_not_forbidden_default_path(doc["path"])
        if not isinstance(entry["fault_ids"], list) or not entry["fault_ids"]:
            raise ContextError(f"{milestone} fault_ids must be a non-empty list")
        for fault_id in entry["fault_ids"]:
            if not isinstance(fault_id, str) or not fault_id:
                raise ContextError(f"{milestone} fault_ids must contain strings")
            if (
                not FAULT_ID_RE.fullmatch(fault_id)
                and not FAULT_RANGE_RE.fullmatch(fault_id)
                and fault_id != "full regression suite"
            ):
                raise ContextError(f"{milestone} has invalid fault selector {fault_id}")
        if not isinstance(entry["predecessor_evidence"], list):
            raise ContextError(f"{milestone} predecessor_evidence must be a list")
        for evidence in entry["predecessor_evidence"]:
            validate_document_entry(evidence, f"{milestone} predecessor evidence")
            predecessor = evidence.get("milestone")
            if not isinstance(predecessor, str) or not MILESTONE_RE.fullmatch(predecessor):
                raise ContextError(f"{milestone} predecessor evidence has invalid milestone")
        if not isinstance(entry["implementation_roots"], list):
            raise ContextError(f"{milestone} implementation_roots must be a list")


def validate_document_entry(item: Any, label: str) -> None:
    if not isinstance(item, dict):
        raise ContextError(f"{label} must be an object")
    if not isinstance(item.get("path"), str) or not item["path"]:
        raise ContextError(f"{label} missing path")
    selector = item.get("selector")
    if not isinstance(selector, dict):
        raise ContextError(f"{label} missing selector")
    if selector.get("type") not in {"heading", "table_row"}:
        raise ContextError(f"{label} selector type must be heading or table_row")
    if not isinstance(selector.get("value"), str) or not selector["value"]:
        raise ContextError(f"{label} selector missing value")


def assert_not_forbidden_default_path(path: str) -> None:
    first = path.split("/", 1)[0]
    if path in FORBIDDEN_DEFAULT_PATHS or first in FORBIDDEN_DEFAULT_PATHS:
        raise ContextError(f"default context cannot include forbidden broad path: {path}")


def safe_source_path(root: Path, relative_path: str) -> Path:
    if Path(relative_path).is_absolute():
        raise ContextError(f"source path must be repository-relative: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ContextError(f"source path escapes repository root: {relative_path}") from exc
    return resolved


def read_source(root: Path, relative_path: str) -> tuple[str, str]:
    path = safe_source_path(root, relative_path)
    try:
        data = path.read_bytes()
    except FileNotFoundError as exc:
        raise ContextError(f"required source missing: {relative_path}") from exc
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContextError(f"required source is not UTF-8 text: {relative_path}") from exc
    return text, sha256_bytes(data)


def extract_heading(markdown: str, heading: str, source_label: str) -> str:
    lines = markdown.splitlines(keepends=True)
    matches = [index for index, line in enumerate(lines) if line.rstrip("\n") == heading]
    if not matches:
        raise ContextError(f"missing heading selector in {source_label}: {heading}")
    if len(matches) > 1:
        raise ContextError(f"duplicate heading selector in {source_label}: {heading}")
    start = matches[0]
    marker = HEADING_RE.match(lines[start])
    if not marker:
        raise ContextError(f"selector is not a markdown heading in {source_label}: {heading}")
    level = len(marker.group(1))
    end = len(lines)
    for index in range(start + 1, len(lines)):
        candidate = HEADING_RE.match(lines[index])
        if candidate and len(candidate.group(1)) <= level:
            end = index
            break
    return "".join(lines[start:end]).rstrip() + "\n"


def extract_table_row(markdown: str, row_id: str, source_label: str) -> str:
    rows: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and cells[0] == row_id:
            rows.append(line.rstrip() + "\n")
    if not rows:
        raise ContextError(f"missing table_row selector in {source_label}: {row_id}")
    if len(rows) > 1:
        raise ContextError(f"duplicate table_row selector in {source_label}: {row_id}")
    return rows[0]


def apply_selector(markdown: str, selector: dict[str, str], source_label: str) -> str:
    selector_type = selector["type"]
    value = selector["value"]
    if selector_type == "heading":
        return extract_heading(markdown, value, source_label)
    if selector_type == "table_row":
        return extract_table_row(markdown, value, source_label)
    raise ContextError(f"unsupported selector type in {source_label}: {selector_type}")


def collect_part(
    root: Path,
    item: dict[str, Any],
    label: str,
    *,
    reason: str | None = None,
    predecessor: str | None = None,
) -> SourcePart:
    relative_path = item["path"]
    markdown, source_digest = read_source(root, relative_path)
    selected = apply_selector(markdown, item["selector"], relative_path)
    return SourcePart(
        label=label,
        path=relative_path,
        selector=dict(item["selector"]),
        content=selected,
        source_sha256=source_digest,
        selected_sha256=sha256_text(selected),
        reason=reason,
        predecessor=predecessor,
    )


def collect_fault_parts(root: Path, fault_matrix: dict[str, Any], fault_ids: list[str]) -> list[SourcePart]:
    parts: list[SourcePart] = []
    for fault_id in expand_fault_ids(fault_ids):
        item = {
            "path": fault_matrix["path"],
            "selector": {"type": "table_row", "value": fault_id},
        }
        parts.append(collect_part(root, item, "fault"))
    return parts


def expand_fault_ids(fault_ids: list[str]) -> list[str]:
    expanded: list[str] = []
    for fault_id in fault_ids:
        if FAULT_ID_RE.fullmatch(fault_id):
            expanded.append(fault_id)
            continue
        if FAULT_RANGE_RE.fullmatch(fault_id):
            start, end = fault_id.split("-", 1)
            start_number = int(start[1:])
            end_number = int(end[1:])
            if start_number > end_number:
                raise ContextError(f"invalid descending fault range {fault_id}")
            expanded.extend(f"F{number:02d}" for number in range(start_number, end_number + 1))
    return expanded


def parse_extra_heading(value: str) -> dict[str, Any]:
    if "::" not in value:
        raise ContextError("--extra-heading must use PATH::HEADING")
    path, heading = value.split("::", 1)
    if not path or not heading:
        raise ContextError("--extra-heading must include both path and heading")
    return {"path": path, "selector": {"type": "heading", "value": heading}}


def context_map_digest(root: Path) -> str:
    path = root / "context" / "context-map.json"
    return sha256_bytes(path.read_bytes())


def build_snapshot(
    milestone: str,
    *,
    root: Path | None = None,
    extra_headings: Iterable[str] = (),
    reason: str | None = None,
    write: bool = True,
    output_dir: Path | None = None,
) -> tuple[str, str, Path | None]:
    root = root or repo_root()
    if not MILESTONE_RE.fullmatch(milestone):
        raise ContextError(f"unknown milestone format: {milestone}")
    data = load_context_map(root)
    milestones = data["milestones"]
    if milestone not in milestones:
        raise ContextError(f"unknown milestone: {milestone}")
    extras = list(extra_headings)
    if extras and not reason:
        raise ContextError("--reason is required when --extra-heading is used")

    entry = milestones[milestone]
    parts: list[SourcePart] = []
    for item in data.get("shared_documents", []):
        parts.append(collect_part(root, item, "shared"))
    for item in entry["documents"]:
        parts.append(collect_part(root, item, "milestone"))
    parts.extend(collect_fault_parts(root, data["fault_matrix"], entry["fault_ids"]))
    for item in entry["predecessor_evidence"]:
        parts.append(
            collect_part(
                root,
                item,
                "predecessor",
                predecessor=item["milestone"],
            )
        )
    for raw_extra in extras:
        item = parse_extra_heading(raw_extra)
        parts.append(collect_part(root, item, "expansion", reason=reason))

    budget = int(entry.get("byte_budget", data["default_byte_budget"]))
    map_digest = context_map_digest(root)
    body_without_digest = render_snapshot(
        milestone=milestone,
        title=entry["title"],
        schema_version=data["schema_version"],
        map_digest=map_digest,
        snapshot_digest="PENDING",
        byte_budget=budget,
        fault_ids=entry["fault_ids"],
        implementation_roots=entry["implementation_roots"],
        parts=parts,
    )
    snapshot_digest = sha256_text(body_without_digest.replace("Context SHA-256: PENDING", "Context SHA-256:"))
    body = render_snapshot(
        milestone=milestone,
        title=entry["title"],
        schema_version=data["schema_version"],
        map_digest=map_digest,
        snapshot_digest=snapshot_digest,
        byte_budget=budget,
        fault_ids=entry["fault_ids"],
        implementation_roots=entry["implementation_roots"],
        parts=parts,
    )
    size = len(body.encode("utf-8"))
    if size > budget:
        raise ContextError(
            f"{milestone} context snapshot exceeds byte budget: {size} > {budget}; no snapshot written"
        )
    path: Path | None = None
    if write:
        out_dir = output_dir or (root / ".omx" / "context")
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{milestone}-{snapshot_digest[:12]}.md"
        path.write_text(body, encoding="utf-8")
    return body, snapshot_digest, path


def render_snapshot(
    *,
    milestone: str,
    title: str,
    schema_version: int,
    map_digest: str,
    snapshot_digest: str,
    byte_budget: int,
    fault_ids: list[str],
    implementation_roots: list[str],
    parts: list[SourcePart],
) -> str:
    lines: list[str] = [
        f"# Context Snapshot: {milestone} - {title}",
        "",
        f"Milestone: {milestone}",
        f"Schema version: {schema_version}",
        f"Context SHA-256: {snapshot_digest}",
        f"Context map SHA-256: {map_digest}",
        f"Byte budget: {byte_budget}",
        "",
        "## Workflow Binding",
        "",
        "Planner, Architect, Critic, approved plan binding, and Ralph must use this exact snapshot.",
        "Any expansion changes the digest and requires Architect/Critic review before Ralph handoff.",
        "",
        "## Selected Fault IDs",
        "",
        ", ".join(fault_ids),
        "",
        "## Implementation Roots",
        "",
    ]
    lines.extend(f"- `{root}`" for root in implementation_roots)
    lines.extend(["", "## Provenance", ""])
    for index, part in enumerate(parts, start=1):
        selector = json.dumps(part.selector, sort_keys=True, separators=(",", ":"))
        extra = f"; reason={part.reason}" if part.reason else ""
        predecessor = f"; predecessor={part.predecessor}" if part.predecessor else ""
        lines.append(
            f"{index}. {part.label}: `{part.path}` selector `{selector}` "
            f"source_sha256={part.source_sha256} selected_sha256={part.selected_sha256}"
            f"{predecessor}{extra}"
        )
    lines.extend(["", "## Included Sources", ""])
    for part in parts:
        selector_title = part.selector["value"]
        lines.extend(
            [
                f"### {part.label}: {part.path} :: {selector_title}",
                "",
                part.content.rstrip(),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("milestone", help="AD-XX milestone to build")
    parser.add_argument(
        "--extra-heading",
        action="append",
        default=[],
        help="Add PATH::HEADING expansion",
    )
    parser.add_argument("--reason", help="Required reason for extra heading expansion")
    parser.add_argument("--output-dir", help="Override snapshot output directory")
    args = parser.parse_args(argv)
    try:
        _, digest, path = build_snapshot(
            args.milestone,
            extra_headings=args.extra_heading,
            reason=args.reason,
            output_dir=Path(args.output_dir) if args.output_dir else None,
        )
    except ContextError as exc:
        print(f"build_context failed: {exc}", file=sys.stderr)
        return 2
    print(f"Context snapshot: {path}")
    print(f"Context SHA-256: {digest}")
    print(f"Context map SHA-256: {context_map_digest(repo_root())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
