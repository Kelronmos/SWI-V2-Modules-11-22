"""Strict-schema rejection and opt-in ReplayGuard.

Documents previously unguarded behavior: unexpected extra fields were
silently admitted; the same evidence_id could be admitted repeatedly.
"""
from __future__ import annotations

import pytest

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.errors import ReplayError, UnexpectedFieldError
from swi_v2.kernel.replay_guard import ReplayGuard


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


def test_valid_envelope_still_admits():
    admitted = admit_foundation_input(_valid_fixture())
    assert admitted.evidence_id == "test-fixture-001"


def test_created_at_optional_still_admits():
    admitted = admit_foundation_input(_valid_fixture(created_at=1726400000.0))
    assert admitted.evidence_id == "test-fixture-001"


def test_unexpected_extra_field_rejected():
    envelope = _valid_fixture()
    envelope["unexpected_extra_field"] = "should not be admitted"
    with pytest.raises(UnexpectedFieldError):
        admit_foundation_input(envelope)


def test_multiple_unexpected_fields_all_named_in_error():
    envelope = _valid_fixture()
    envelope["extra_one"] = 1
    envelope["extra_two"] = 2
    with pytest.raises(UnexpectedFieldError) as exc_info:
        admit_foundation_input(envelope)
    assert "extra_one" in str(exc_info.value)
    assert "extra_two" in str(exc_info.value)


def test_replay_guard_admits_first_presentation():
    guard = ReplayGuard()
    admitted = guard.admit(_valid_fixture())
    assert admitted.evidence_id == "test-fixture-001"


def test_replay_guard_rejects_second_presentation_of_same_evidence_id():
    guard = ReplayGuard()
    guard.admit(_valid_fixture())
    with pytest.raises(ReplayError):
        guard.admit(_valid_fixture())


def test_replay_guard_allows_distinct_evidence_ids():
    guard = ReplayGuard()
    guard.admit(_valid_fixture(evidence_id="id-one"))
    admitted_two = guard.admit(_valid_fixture(evidence_id="id-two"))
    assert admitted_two.evidence_id == "id-two"


def test_replay_guard_does_not_record_a_rejected_candidate():
    guard = ReplayGuard()
    tampered = _valid_fixture()
    tampered["payload"] = {"text": "tampered", "pipeline": "fixture"}
    with pytest.raises(Exception):
        guard.admit(tampered)
    admitted = guard.admit(_valid_fixture())
    assert admitted.evidence_id == "test-fixture-001"


def test_replay_guard_reset_clears_seen_state():
    guard = ReplayGuard()
    guard.admit(_valid_fixture())
    guard.reset()
    admitted = guard.admit(_valid_fixture())
    assert admitted.evidence_id == "test-fixture-001"
