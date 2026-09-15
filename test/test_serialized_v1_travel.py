"""Cross-repo style travel: JSON dict shaped like V1 export → M11 (no V1 import)."""
from __future__ import annotations

import json

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
from swi_v2.kernel.enforcement import require_admitted
from swi_v2.module12 import process as module12_process


def _v1_shaped_payload():
    """Matches V1 export_foundation_evidence payload keys (bounded public contract)."""
    return {
        "allowed": True,
        "reason": None,
        "security": {
            "risk_score": 0.0,
            "triggered": [],
            "block_threshold": 0.5,
            "blocked": False,
        },
        "sync": {"gap_seconds": 0.0, "stale": False, "out_of_order": False},
        "redaction": {
            "redacted_text": "travel-test [EMAIL]",
            "match_categories": ["EMAIL"],
        },
        "drift": {"similarity": 0.0, "drifted": True},
    }


def _serialized_v1_envelope(**overrides):
    """Simulate bytes crossing the repo boundary (JSON), then parse to dict."""
    base = {
        "payload": _v1_shaped_payload(),
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "v1-travel-sample-001",
        "verification_status": "v1_trainer_pipeline_completed",
        "source_reference": "Kelronmos/SWI-V1-Module-1-10:Trainer.process",
        "created_at": 1726400000.0,
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
    # Round-trip through JSON as the transfer medium
    return json.loads(json.dumps(base, sort_keys=True, default=str))


def test_serialized_v1_shaped_envelope_admitted():
    data = _serialized_v1_envelope()
    admitted = admit_foundation_input(data)
    assert isinstance(admitted, AdmittedInput)
    assert admitted.evidence_id == "v1-travel-sample-001"
    require_admitted(admitted)
    out = module12_process(admitted)
    assert out["status"] == "accepted_placeholder"


def test_created_at_optional_for_integrity():
    data = _serialized_v1_envelope()
    data["created_at"] = 9999999999.0
    # digest does not include created_at
    admitted = admit_foundation_input(data)
    assert isinstance(admitted, AdmittedInput)


def test_corrupted_payload_rejected():
    data = _serialized_v1_envelope()
    data["payload"] = dict(data["payload"])
    data["payload"]["allowed"] = False
    with pytest.raises(IntegrityVerificationError):
        admit_foundation_input(data)


def test_changed_integrity_hash_rejected():
    data = _serialized_v1_envelope(integrity_reference="0" * 64)
    with pytest.raises(IntegrityVerificationError):
        admit_foundation_input(data)


def test_missing_field_rejected():
    data = _serialized_v1_envelope()
    del data["source_reference"]
    with pytest.raises(InvalidFoundationEvidence):
        admit_foundation_input(data)


def test_unsupported_schema_rejected():
    data = _serialized_v1_envelope(evidence_schema_version="9.9")
    data["integrity_reference"] = compute_integrity_reference(
        data["payload"],
        data["foundation_version"],
        data["evidence_schema_version"],
        data["evidence_id"],
        data["source_reference"],
    )
    with pytest.raises(UnsupportedFoundationVersion):
        admit_foundation_input(data)


def test_invalid_status_rejected():
    data = _serialized_v1_envelope(verification_status="looks_authenticated")
    data["integrity_reference"] = compute_integrity_reference(
        data["payload"],
        data["foundation_version"],
        data["evidence_schema_version"],
        data["evidence_id"],
        data["source_reference"],
    )
    with pytest.raises(InvalidFoundationEvidence):
        admit_foundation_input(data)


def test_raw_pipeline_result_dict_rejected():
    """V1 internal-shaped object without evidence envelope fields must not admit."""
    with pytest.raises(InvalidFoundationEvidence):
        admit_foundation_input(
            {
                "allowed": True,
                "reason": None,
                "security": {},
                "sync": {},
                "redaction": {},
                "drift": {},
            }
        )


def test_rejection_never_reaches_module12():
    with pytest.raises(ModuleKernelError):
        module12_process("raw-string")
    with pytest.raises((InvalidFoundationEvidence, FoundationAdmissionError, IntegrityVerificationError)):
        bad = _serialized_v1_envelope(integrity_reference="ab" * 32)
        admit_foundation_input(bad)
