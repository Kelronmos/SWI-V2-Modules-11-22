"""ISO claim-gate tests — claim wording control, not authorization."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.validate_iso_claim_status import validate

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "evidence" / "iso_claim_status.json"
SCHEMA = ROOT / "evidence" / "schemas" / "iso_claim_status.schema.json"


@pytest.fixture
def register():
    return json.loads(REGISTER.read_text(encoding="utf-8"))


def test_baseline_register_passes():
    ok, errors = validate(REGISTER, SCHEMA)
    assert ok, errors


def test_green_without_review_rejected(tmp_path, register):
    s = register["standards"][0]
    s["gate_status"] = "GREEN"
    s["claim_rung"] = 2
    s["scope"] = "test scope"
    s["clause_mapping_ref"] = "docs/fake_mapping.md"
    s["evidence_hashes"] = ["a" * 64]
    s["test_results_ref"] = "reports/fake.json"
    s["independent_review"] = None
    s["critical_gaps"] = []
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("independent_review" in e for e in errors)


def test_green_with_critical_gaps_rejected(tmp_path, register):
    s = register["standards"][0]
    s["gate_status"] = "GREEN"
    s["claim_rung"] = 2
    s["scope"] = "scope"
    s["clause_mapping_ref"] = "map"
    s["evidence_hashes"] = ["b" * 64]
    s["test_results_ref"] = "tests"
    s["independent_review"] = {"reviewer": "A", "date": "2026-01-01", "report_hash": "c" * 64}
    s["critical_gaps"] = ["still open"]
    p = tmp_path / "r.json"
    p.write_text(json.dumps(register))
    ok, errors = validate(p, SCHEMA)
    assert not ok
    assert any("critical_gaps" in e for e in errors)


def test_rung4_without_certificate_rejected(tmp_path, register):
    s = register["standards"][0]
    s["gate_status"] = "GREEN"
    s["claim_rung"] = 4
    s["scope"] = "scope"
    s["clause_mapping_ref"] = "map"
    s["evidence_hashes"] = ["d" * 64]
    s["test_results_ref"] = "tests"
    s["independent_review"] = {"reviewer": "A", "date": "2026-01-01", "report_hash": "e" * 64}
    s["critical_gaps"] = []
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
    assert any("not_applicable_rationale" in e for e in errors)


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


def test_governance_defaults_forbid_production(register):
    assert register["governance"]["PRODUCTION_AUTHORIZED"] is False
    assert register["governance"]["ISO_CONFORMITY"] == "NOT_ESTABLISHED"
