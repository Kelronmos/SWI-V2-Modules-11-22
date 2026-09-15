"""Foundation evidence structures for V2 admission.

STATUS of the cross-repo contract: PROPOSED / IMPLEMENTATION PENDING on V1.

V1 (SWI-V1-Module-1-10) currently provides local pipeline results, tests, and
seal documentation. It does NOT yet emit a versioned, exportable foundation
evidence object for cross-repository consumption. Fields below are therefore
a PROPOSED interface that V2 can verify deterministically against fixtures
until V1 releases a real evidence producer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


SUPPORTED_FOUNDATION_VERSIONS = frozenset({"1.0-proposed"})
SUPPORTED_EVIDENCE_SCHEMA_VERSIONS = frozenset({"1.0-proposed"})


@dataclass(frozen=True)
class FoundationEvidenceEnvelope:
    """Proposed V1→V2 evidence envelope (TEST FIXTURE / PROPOSED contract)."""

    payload: Any
    foundation_version: str
    evidence_schema_version: str
    evidence_id: str
    integrity_reference: str
    verification_status: str
    source_reference: str


@dataclass(frozen=True)
class AdmittedInput:
    """Distinct type produced only by successful Module 11 admission."""

    payload: Any
    foundation_version: str
    evidence_schema_version: str
    evidence_id: str
    integrity_reference: str
    source_reference: str
    admitted_by: str = "module_11_foundation_admission"


def envelope_from_mapping(data: Mapping[str, Any]) -> FoundationEvidenceEnvelope:
    return FoundationEvidenceEnvelope(
        payload=data["payload"],
        foundation_version=str(data["foundation_version"]),
        evidence_schema_version=str(data["evidence_schema_version"]),
        evidence_id=str(data["evidence_id"]),
        integrity_reference=str(data["integrity_reference"]),
        verification_status=str(data["verification_status"]),
        source_reference=str(data["source_reference"]),
    )
