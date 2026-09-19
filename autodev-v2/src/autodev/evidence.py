"""AD-00 evidence records and result classification."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class EvidenceClass(str, Enum):
    PROVIDED_FILE = "PROVIDED_FILE"
    SIMULATED = "SIMULATED"
    NOT_RUN = "NOT_RUN"
    BLOCKED_EXTERNAL = "BLOCKED_EXTERNAL"


class Result(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    NOT_RUN = "NOT_RUN"
    BLOCKED_EXTERNAL = "BLOCKED_EXTERNAL"
    UNSUPPORTED = "UNSUPPORTED"


@dataclass(frozen=True)
class SourceEvidence:
    id: str
    title: str
    filename: str
    sha256: str
    evidence_class: str = EvidenceClass.PROVIDED_FILE.value
    original_body_available: bool = False
    live_verified: bool = False
    note: str = "Identity-only source record; original upload body is not distributed."

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


SOURCE_EVIDENCE: tuple[SourceEvidence, ...] = (
    SourceEvidence(
        id="S1",
        title="Lessons Learned from Nous Autonomous Supervisor Setup",
        filename="Pasted markdown(2).md",
        sha256="6ace331bbf3f2ee7af23b46f8cbd579290c434e0f3d913a0e0eccc2d035b928d",
    ),
    SourceEvidence(
        id="S2",
        title="Hermes + Gajae Automated Onboarding: Lessons from Nous",
        filename="Pasted markdown (2).md",
        sha256="d0ea218d74b658f174bd8566c8bf017981b06d7df51a12df4ecb94e997bf052b",
    ),
    SourceEvidence(
        id="S3",
        title="Lessons Learned From Nous Autonomous Onboarding",
        filename="Pasted markdown (3).md",
        sha256="bdac1bb84c3de3f695462d371ee3509e9a98007f9091b2292ad6f83eb2dd43b5",
    ),
)


def source_inventory() -> list[dict[str, object]]:
    """Return identity-only records for the unavailable source uploads."""

    return [record.as_dict() for record in SOURCE_EVIDENCE]


def classify_unavailable_external_capability(capability: str) -> dict[str, object]:
    """Represent F63 without fabricating live success."""

    return {
        "schema_version": 1,
        "capability": capability,
        "result": Result.BLOCKED_EXTERNAL.value,
        "evidence_class": EvidenceClass.BLOCKED_EXTERNAL.value,
        "live_verified": False,
        "remediation": "Obtain separately authorized live access before probing.",
    }
