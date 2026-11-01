"""ISO claim-gate tests — eligibility and governance ceilings only.

Does not authorize production. PROVEN requires PASS/PASS/hex64/APPLICABLE.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.validate_iso_claim_status import validate

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "evidence" / "iso_claim_status.json"
SCHEMA = ROOT / "evidence" / "schemas" / "iso_claim_status.schema.json"


def _complete_green(s: dict, rung: int = 3) -> None:
    s["gate_status"] = "GREEN"
    s["claim_rung"] = rung
    s["scope"] = "defined test scope"
    s["clause_mapping_ref"] = "docs/iso/fake_mapping.md"
    s["evidence_hashes"] = ["a" * 64]
    s["test_results_ref"] = "reports/fake_tests.json"
    s["critical_gaps"] = []
    s["independent_review"] = {
        "reviewer": "Reviewer A",
        "date": "2026-01-01",
        "report_hash": "b" * 64,
        "outcome": "SUPPORTS_CLAIM",
        "scope": "defined test scope",
        "independence_attestation": True,
    }


@pytest.fixture
def register():
    return json.loads(REGISTER.read_text(encoding="utf-8"))


def test_baseline_register_passes():
    ok, errors = validate(REGISTER, SCHEMA)
    assert ok, errors


def test_green_without_review_rejected(tmp_path, register):
    s = register["standards"][0]
    _complete_green(s)
    s["independent_review"] = None
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("independent_review" in e for e in errors)


def test_green_with_critical_gaps_rejected(tmp_path, register):
    s = register["standards"][0]
    _complete_green(s)
    s["critical_gaps"] = ["still open"]
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("critical_gaps" in e for e in errors)


def test_rung4_without_certificate_rejected(tmp_path, register):
    s = register["standards"][0]
    _complete_green(s, rung=4)
    s["certificate"] = None
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("certificate" in e for e in errors)


def test_not_applicable_without_rationale_rejected(tmp_path, register):
    s = register["standards"][0]
    s["gate_status"] = "NOT_APPLICABLE"
    s["not_applicable_rationale"] = None
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("rationale" in e or "NOT_APPLICABLE" in e for e in errors)


def test_unknown_gate_status_rejected(tmp_path, register):
    register["standards"][0]["gate_status"] = "PURPLE"
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok


def test_new_standards_not_default_green(register):
    for s in register["standards"]:
        assert s["gate_status"] != "GREEN"
        assert s["claim_rung"] == 0


def _force_proven_requirement(register, **overrides):
    s = register["standards"][0]
    r = (s.get("requirements") or [{}])[0]
    if not s.get("requirements"):
        s["requirements"] = [r]
    base = {
        "requirement_id": r.get("requirement_id") or "REQ-TEST",
        "title": "synthetic",
        "applicability": "APPLICABLE",
        "claim_status": "PROVEN",
        "claim_source": "ENGINE",
        "swi_allocation": "M11",
        "implementation_ref": "swi_v2/example.py",
        "evidence_ref": "evidence/example.json",
        "evidence_hash": "a" * 64,
        "source_commit": "deadbeef" * 5,
        "test_procedure": "tests/test_example.py",
        "test_result": "PASS",
        "replay_status": "PASS",
        "reproducibility_status": "PASS",
        "environment": "ci",
        "critical_gaps": [],
    }
    base.update(overrides)
    s["requirements"][0] = base
    return register


def test_proven_rejects_partial_replay(tmp_path, register):
    _force_proven_requirement(register, replay_status="PARTIAL")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("replay_status" in e and "PROVEN" in e for e in errors)


def test_proven_rejects_partial_reproducibility(tmp_path, register):
    _force_proven_requirement(register, reproducibility_status="PARTIAL")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("reproducibility" in e and "PROVEN" in e for e in errors)


def test_proven_rejects_not_run_replay(tmp_path, register):
    _force_proven_requirement(register, replay_status="NOT_RUN")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok


def test_proven_rejects_failed_test(tmp_path, register):
    _force_proven_requirement(register, test_result="FAIL")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok


def test_proven_rejects_invalid_hash_chars(tmp_path, register):
    _force_proven_requirement(register, evidence_hash="g" * 64)
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("evidence_hash" in e for e in errors)


def test_proven_rejects_wrong_hash_length(tmp_path, register):
    _force_proven_requirement(register, evidence_hash="a" * 63)
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok


def test_proven_rejects_missing_evidence_ref(tmp_path, register):
    _force_proven_requirement(register, evidence_ref="")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok


def test_proven_rejects_missing_source_commit(tmp_path, register):
    _force_proven_requirement(register, source_commit="")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok


def test_proven_rejects_not_assessed_applicability(tmp_path, register):
    _force_proven_requirement(register, applicability="NOT_ASSESSED")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("APPLICABLE" in e or "applicability" in e for e in errors)


def test_proven_rejects_not_applicable_promotion(tmp_path, register):
    _force_proven_requirement(register, applicability="NOT_APPLICABLE", claim_status="PROVEN")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok


def test_proven_rejects_manual_promotion(tmp_path, register):
    _force_proven_requirement(register, claim_source="MANUAL")
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("ENGINE" in e or "manual" in e.lower() for e in errors)


def test_production_authorized_true_rejected(tmp_path, register):
    register["governance"]["PRODUCTION_AUTHORIZED"] = True
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("PRODUCTION_AUTHORIZED" in e for e in errors)


def test_valid_complete_evidence_eligible_structure(tmp_path, register):
    """Structure-only: complete PASS/PASS/hex may be PROVEN at requirement level.
    Does not claim the baseline is proven.
    """
    _force_proven_requirement(register)
    register["governance"]["PROVEN"] = False
    register["governance"]["PRODUCTION_AUTHORIZED"] = False
    register["governance"]["ISO_CONFORMITY"] = "NOT_ESTABLISHED"
    register["governance"]["CONFORMITY_CLAIM"] = "SEALED"
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    if not ok:
        assert not any("replay_status must be PASS" in e for e in errors)
        assert not any("evidence_hash must be exactly 64" in e for e in errors)
