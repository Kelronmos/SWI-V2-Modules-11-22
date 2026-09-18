"""Module 11 foundation admission (deterministic, fail-closed).

Admits schema + integrity + allowed verification_status.
Does NOT establish factual truth, sender authentication, or action safety.

fixture status = TEST-ONLY
v1_trainer_pipeline_completed = V1 producer status string (still needs integrity match;
origin authenticity requires future CRTG signatures — NOT implemented here).
"""
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
    UnexpectedFieldError,
    UnsupportedFoundationVersion,
)

STATUS_TEST_FIXTURE = "foundation_verified_test_fixture"
STATUS_V1_PIPELINE = "v1_trainer_pipeline_completed"
_ACCEPTED_STATUS = frozenset({STATUS_TEST_FIXTURE, STATUS_V1_PIPELINE})


def compute_integrity_reference(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> str:
    """Same covered fields as V1 (excludes created_at metadata).

    Delegates to swi_v2.kernel.canonical (Lane B canonicalization_v0).
    """
    from .canonical import compute_integrity_reference as _canonical_integrity

    return _canonical_integrity(
        payload,
        foundation_version,
        evidence_schema_version,
        evidence_id,
        source_reference,
    )


def admit_foundation_input(
    candidate: Union[FoundationEvidenceEnvelope, Mapping[str, Any], Any],
) -> AdmittedInput:
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
        known_optional = {"created_at"}
        extra = set(candidate.keys()) - required - known_optional
        if extra:
            raise UnexpectedFieldError(
                f"evidence envelope contains fields outside the declared contract: "
                f"{sorted(extra)}"
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

    if envelope.verification_status not in _ACCEPTED_STATUS:
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
