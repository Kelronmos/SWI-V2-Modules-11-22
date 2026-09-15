"""Module 11 foundation admission (deterministic, fail-closed)."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Union

from .contracts import (
    AdmittedInput,
    FoundationEvidenceEnvelope,
    SUPPORTED_EVIDENCE_SCHEMA_VERSIONS,
    SUPPORTED_FOUNDATION_VERSIONS,
    envelope_from_mapping,
)
from .errors import (
    FoundationAdmissionError,
    IntegrityVerificationError,
    InvalidFoundationEvidence,
    UnsupportedFoundationVersion,
)


def compute_integrity_reference(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> str:
    """Deterministic integrity reference for the proposed contract."""
    material = {
        "payload": payload,
        "foundation_version": foundation_version,
        "evidence_schema_version": evidence_schema_version,
        "evidence_id": evidence_id,
        "source_reference": source_reference,
    }
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def admit_foundation_input(
    candidate: Union[FoundationEvidenceEnvelope, Mapping[str, Any], Any],
) -> AdmittedInput:
    """Admit only candidates that satisfy the V1 foundation contract."""
    if isinstance(candidate, FoundationEvidenceEnvelope):
        envelope = candidate
    elif isinstance(candidate, Mapping):
        required = {
            "payload",
            "foundation_version",
            "evidence_schema_version",
            "evidence_id",
            "integrity_reference",
            "verification_status",
            "source_reference",
        }
        missing = required - set(candidate.keys())
        if missing:
            raise InvalidFoundationEvidence(
                f"missing required evidence fields: {sorted(missing)}"
            )
        try:
            envelope = envelope_from_mapping(candidate)
        except Exception as exc:
            raise InvalidFoundationEvidence(f"malformed envelope: {exc}") from exc
    else:
        raise FoundationAdmissionError(
            f"raw input rejected: expected evidence envelope, got {type(candidate).__name__}"
        )

    if envelope.foundation_version not in SUPPORTED_FOUNDATION_VERSIONS:
        raise UnsupportedFoundationVersion(
            f"unsupported foundation_version: {envelope.foundation_version!r}"
        )
    if envelope.evidence_schema_version not in SUPPORTED_EVIDENCE_SCHEMA_VERSIONS:
        raise UnsupportedFoundationVersion(
            f"unsupported evidence_schema_version: {envelope.evidence_schema_version!r}"
        )

    # Fixture status (unit tests) or real V1 Trainer export status.
    _accepted_status = frozenset({
        "foundation_verified_test_fixture",
        "v1_trainer_pipeline_completed",
    })
    if envelope.verification_status not in _accepted_status:
        raise InvalidFoundationEvidence(
            f"verification_status not acceptable for current V2 build: "
            f"{envelope.verification_status!r}"
        )

    expected = compute_integrity_reference(
        payload=envelope.payload,
        foundation_version=envelope.foundation_version,
        evidence_schema_version=envelope.evidence_schema_version,
        evidence_id=envelope.evidence_id,
        source_reference=envelope.source_reference,
    )
    if envelope.integrity_reference != expected:
        raise IntegrityVerificationError(
            "integrity_reference does not match computed foundation evidence digest"
        )

    return AdmittedInput(
        payload=envelope.payload,
        foundation_version=envelope.foundation_version,
        evidence_schema_version=envelope.evidence_schema_version,
        evidence_id=envelope.evidence_id,
        integrity_reference=envelope.integrity_reference,
        source_reference=envelope.source_reference,
        admitted_by="module_11_foundation_admission",
    )
