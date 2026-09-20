"""Deterministic contract validation diagnostics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    line: int | None = None
    column: int | None = None


class ContractValidationError(ValueError):
    """One or more ordered contract validation failures."""

    def __init__(self, issues: list[ValidationIssue] | tuple[ValidationIssue, ...]):
        self.issues = tuple(issues)
        detail = "; ".join(
            f"{issue.path}: {issue.message}"
            + (
                f" (line {issue.line}, column {issue.column})"
                if issue.line is not None and issue.column is not None
                else ""
            )
            for issue in self.issues
        )
        super().__init__(detail or "contract validation failed")
