"""Observation / Claim separation — OC-001..OC-008.

OBSERVATION ≠ CLAIM ≠ PROOF ≠ AUTHORIZATION
PRODUCTION_AUTHORIZED = NO
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_v2.reports.test_report import (
    ClaimRecord,
    ObservationRecord,
    TestReportBuilder,
    write_reports,
)


@pytest.fixture
def builder(tmp_path):
    return TestReportBuilder(report_type="observation_claim", root=ROOT)


def test_oc001_claim_references_nonexistent_observation(builder):
    builder.add_observation(
        ObservationRecord(observation_id="O-1", observation_type="result", description="ok")
    )
    c = builder.add_claim(
        ClaimRecord(
            claim_id="C-1",
            claim_text="uses missing obs",
            supporting_observation_ids=["O-1", "O-MISSING"],
            verification_status="VERIFIED",
        )
    )
    assert c.verification_status == "REJECTED"
    assert any("missing_observations" in x for x in c.limitations)


def test_oc002_claim_without_required_evidence_not_verified(builder):
    c = builder.add_claim(
        ClaimRecord(
            claim_id="C-2",
            claim_text="no observations",
            supporting_observation_ids=[],
            verification_status="VERIFIED",
        )
    )
    assert c.verification_status == "REJECTED"
    assert c.verification_status != "VERIFIED"


def test_oc003_passing_test_not_universal_proof(builder):
    builder.add_observation(
        ObservationRecord(
            observation_id="O-pass",
            observation_type="test_result",
            description="one test passed",
            observed_status="PASS",
        )
    )
    c = builder.add_claim(
        ClaimRecord(
            claim_id="C-univ",
            claim_text="system is universally correct",
            category="universal_proof",
            supporting_observation_ids=["O-pass"],
            verification_status="UNVERIFIED",
        )
    )
    builder.promote_claim("C-univ", "VERIFIED", required_observation_ids=["O-pass"])
    assert c.verification_status == "REJECTED"
    assert any("universal_proof" in u for u in c.unproven)


def test_oc004_contradictory_observations_preserved(builder):
    builder.add_observation(
        ObservationRecord(observation_id="O-a", observation_type="sensor", description="value=1")
    )
    builder.add_observation(
        ObservationRecord(observation_id="O-b", observation_type="sensor", description="value=2")
    )
    ids = builder.observation_ids()
    assert "O-a" in ids and "O-b" in ids
    assert len(builder.observations) == 2


def test_oc005_report_serialization_round_trip(builder, tmp_path):
    builder.add_observation(
        ObservationRecord(observation_id="O-rt", observation_type="t", description="d")
    )
    builder.add_claim(
        ClaimRecord(
            claim_id="C-rt",
            claim_text="linked",
            supporting_observation_ids=["O-rt"],
            verification_status="UNVERIFIED",
        )
    )
    paths = write_reports(builder, tmp_path / "reports")
    data = json.loads(paths["json"].read_text())
    assert len(data["observations"]) == 1
    assert data["observations"][0]["observation_id"] == "O-rt"
    assert data["claims"][0]["supporting_observation_ids"] == ["O-rt"]
    assert data["governance"]["production_authorized"] == "NO"


def test_oc006_incomplete_observation_remains_explicit(builder):
    o = ObservationRecord(
        observation_id="O-inc",
        observation_type="partial",
        description="incomplete extract",
        incomplete=True,
        uncertain=True,
    )
    builder.add_observation(o)
    assert builder.observations[0].incomplete is True
    assert builder.observations[0].uncertain is True


def test_oc007_claim_status_promotion_requires_conditions(builder):
    builder.add_observation(
        ObservationRecord(observation_id="O-p", observation_type="t", description="x")
    )
    builder.add_claim(
        ClaimRecord(
            claim_id="C-p",
            claim_text="maybe",
            supporting_observation_ids=["O-p"],
            verification_status="UNVERIFIED",
        )
    )
    builder.promote_claim("C-p", "VERIFIED", required_observation_ids=["O-ABSENT"])
    assert builder.claims[0].verification_status == "REJECTED"


def test_oc008_observation_cannot_grant_authority(builder):
    builder.add_observation(
        ObservationRecord(
            observation_id="O-auth",
            observation_type="observer_output",
            description="observer says authorized",
        )
    )
    c = builder.add_claim(
        ClaimRecord(
            claim_id="C-auth",
            claim_text="system is production authorized",
            category="production_authorization",
            supporting_observation_ids=["O-auth"],
            verification_status="UNVERIFIED",
        )
    )
    builder.promote_claim("C-auth", "VERIFIED", required_observation_ids=["O-auth"])
    assert c.verification_status == "REJECTED"
    assert any("authority" in u.lower() or "production" in u.lower() or "promote" in u for u in c.unproven)
