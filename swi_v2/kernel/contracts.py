"""Foundation evidence structures for V2 admission.

STATUS of the cross-repo contract: V1 now provides a versioned/exportable
foundation evidence producer (swi_core/foundation_evidence.py).

V1 emits a FoundationEvidenceEnvelope-compatible object with:
  payload, foundation_version, evidence_schema_version, evidence_id,
  integrity_reference, verification_status, source_reference, created_at

The integrity digest covers the defined fields while excluding created_at
(metadata). The current foundation/schema version remains 1.0-proposed.

This contract establishes deterministic schema and integrity handling.
It does NOT establish sender authentication, factual truth, action safety,
CRTG signatures, or Foundation Seal 5.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


SUPPORTED_FOUNDATION_VERSIONS = frozenset({"1.0-proposed"})
SUPPORTED_EVIDENCE_SCHEMA_VERSIONS = frozenset({"1.0-proposed"})


@dataclass(frozen=True)
class FoundationEvidenceEnvelope:
    """V1→V2 evidence envelope (schema + integrity contract)."""

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
