"""Deterministic redaction helpers for AD-00 evidence handling."""

from __future__ import annotations

import re
from collections.abc import Mapping

SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b[A-Za-z0-9_]*SECRET_CANARY[A-Za-z0-9_]*\b", re.IGNORECASE),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*([^\s,;]+)"),
    re.compile(r"\b(sk-[A-Za-z0-9_-]{8,})\b"),
    re.compile(r"\b(xox[baprs]-[A-Za-z0-9-]{8,})\b"),
)


def redact_text(value: str) -> str:
    """Redact common credential-shaped values without changing other text."""

    redacted = value
    for pattern in SECRET_PATTERNS:
        if pattern.groups >= 2:
            redacted = pattern.sub(lambda match: f"{match.group(1)}=<REDACTED>", redacted)
        else:
            redacted = pattern.sub("<REDACTED>", redacted)
    return redacted


def redact_mapping(values: Mapping[str, object]) -> dict[str, object]:
    """Redact string values and secret-looking keys in a shallow mapping."""

    output: dict[str, object] = {}
    for key, value in values.items():
        if re.search(r"(?i)(api[_-]?key|token|secret|password)", key):
            output[key] = "<REDACTED>"
        elif isinstance(value, str):
            output[key] = redact_text(value)
        else:
            output[key] = value
    return output
