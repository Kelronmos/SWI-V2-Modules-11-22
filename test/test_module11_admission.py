"""Module 11 foundation admission tests."""
from __future__ import annotations

import pytest

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.contracts import AdmittedInput
from swi_v2.kernel.errors import (
    FoundationAdmissionError,
    IntegrityVerificationError,
    InvalidFoundationEvidence,
    ModuleKernelError,
    UnsupportedFoundationVersion,
)
from swi_v2.module12 import process as module12_process


def _valid_fixture(**overrides):
    """TEST FIXTURE — not production V1 evidence."""
    base = {
        "payload": {"text": "hello", "pipeline": "fixture"},
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "test-fixture-001",
        "verification_status": "foundation_verified_test_fixture",
        "source_reference": "TEST FIXTURE / not production V1 output",
    }
    base.update(overrides)
    if "integrity_reference" not in base:
        base["integrity_reference"] = compute_integrity_reference(
            payload=base["payload"],
            foundation_version=base["foundation_version"],
            evidence_schema_version=base["evidence_schema_version"],
            evidence_id=base["evidence_id"],
            source_reference=base["source_reference"],
        )
    return base


def test_raw_string_rejected():
    with pytest.raises(FoundationAdmissionError):
        admit_foundation_input("raw string")


def test_raw_dict_without_evidence_rejected():
    with pytest.raises(InvalidFoundationEvidence):
        admit_foundation_input({"payload": "x", "verified": True})


def test_trust_by_flag_rejected():
    with pytest.raises(InvalidFoundationEvidence):
        admit_foundation_input({"verified": True})


def test_missing_evidence_fields_rejected():
    with pytest.raises(InvalidFoundationEvidence):
        admit_foundation_input({"payload": {}})


def test_unknown_foundation_version_rejected():
    data = _valid_fixture(foundation_version="9.9-unknown")
    with pytest.raises(UnsupportedFoundationVersion):
        admit_foundation_input(data)


def test_unknown_schema_rejected():
    data = _valid_fixture(evidence_schema_version="9.9-unknown")
    with pytest.raises(UnsupportedFoundationVersion):
        admit_foundation_input(data)


def test_invalid_integrity_reference_rejected():
    data = _valid_fixture(integrity_reference="0" * 64)
    with pytest.raises(IntegrityVerificationError):
        admit_foundation_input(data)


def test_invalid_verification_status_rejected():
    data = _valid_fixture(verification_status="looks_fine")
    with pytest.raises(InvalidFoundationEvidence):
        admit_foundation_input(data)


def test_valid_fixture_admitted():
    admitted = admit_foundation_input(_valid_fixture())
    assert isinstance(admitted, AdmittedInput)
    assert admitted.admitted_by == "module_11_foundation_admission"


def test_module_12_accepts_admitted_input():
    admitted = admit_foundation_input(_valid_fixture())
    out = module12_process(admitted)
    assert out["status"] == "accepted_placeholder"


def test_failed_admission_never_reaches_module_12():
    with pytest.raises(ModuleKernelError):
        module12_process("raw")


def test_v1_pipeline_status_accepted_with_valid_integrity():
    """Real V1 producer status is admissible when integrity matches."""
    data = _valid_fixture(verification_status="v1_trainer_pipeline_completed")
    data["integrity_reference"] = compute_integrity_reference(
        payload=data["payload"],
        foundation_version=data["foundation_version"],
        evidence_schema_version=data["evidence_schema_version"],
        evidence_id=data["evidence_id"],
        source_reference=data["source_reference"],
    )
    admitted = admit_foundation_input(data)
    assert isinstance(admitted, AdmittedInput)
