"""S9 evaluator — negative matrix and pure evaluation."""
from __future__ import annotations

import pytest

from swi_v2.s9.evaluator import evaluate_s9


def _base(**kw):
    a = {
        "action_id": "A-001",
        "claim_id": "CLAIM-S9-001",
        "constraints": ["c1"],
        "law": ["c1"],
        "governance": ["c1"],
        "security": ["c1"],
        "human": ["c1"],
        "evidence": [
            {
                "evidence_id": "E-001",
                "exists": True,
                "relevance": "PASS",
                "freshness": "PASS",
                "scope": "PASS",
                "provenance": "PASS",
                "integrity": "PASS",
            }
        ],
        "dependencies": [],
        "authority": {"required": False, "present": False},
    }
    a.update(kw)
    return a


def test_s9_001_complete_valid_case_satisfied_case_only():
    r = evaluate_s9(_base())
    assert r.documented_equation_result == "SATISFIED"
    assert r.evidence_adequacy_result == "SATISFIED"
    assert r.system_result == "SATISFIED"
    assert r.promotion_eligible is False


def test_s9_002_no_evidence_blocked():
    r = evaluate_s9(_base(evidence=[]))
    assert r.documented_equation_result == "BLOCKED"
    assert r.system_result == "BLOCKED"


def test_s9_003_missing_law_blocked():
    r = evaluate_s9(_base(law=[]))
    assert r.law == "MISSING"
    assert r.system_result == "BLOCKED"


def test_s9_004_missing_governance_blocked():
    r = evaluate_s9(_base(governance=[]))
    assert r.governance == "MISSING"
    assert r.system_result == "BLOCKED"


def test_s9_005_missing_security_blocked():
    r = evaluate_s9(_base(security=[]))
    assert r.security == "MISSING"
    assert r.system_result == "BLOCKED"


def test_s9_006_missing_human_blocked():
    r = evaluate_s9(_base(human=[]))
    assert r.human == "MISSING"
    assert r.system_result == "BLOCKED"


def test_s9_007_constraint_mismatch_blocked():
    r = evaluate_s9(_base(constraints=["c1", "c2"], law=["c1"], governance=["c1"], security=["c1"], human=["c1"]))
    assert r.constraint_coverage is False
    assert r.system_result == "BLOCKED"


def test_s9_008_irrelevant_evidence_blocked():
    r = evaluate_s9(
        _base(
            evidence=[{
                "evidence_id": "E-bad", "exists": True,
                "relevance": "FAIL", "freshness": "PASS", "scope": "PASS",
                "provenance": "PASS", "integrity": "PASS",
            }]
        )
    )
    assert r.evidence_exists is True
    assert r.evidence_adequacy_result == "BLOCKED"
    assert r.system_result == "BLOCKED"


def test_s9_009_stale_evidence_blocked():
    r = evaluate_s9(
        _base(
            evidence=[{
                "evidence_id": "E-stale", "exists": True,
                "relevance": "PASS", "freshness": "FAIL", "scope": "PASS",
                "provenance": "PASS", "integrity": "PASS",
            }]
        )
    )
    assert r.system_result == "BLOCKED"


def test_s9_010_wrong_scope_blocked():
    r = evaluate_s9(
        _base(
            evidence=[{
                "evidence_id": "E-scope", "exists": True,
                "relevance": "PASS", "freshness": "PASS", "scope": "FAIL",
                "provenance": "PASS", "integrity": "PASS",
            }]
        )
    )
    assert r.system_result == "BLOCKED"


def test_s9_011_invalid_provenance_blocked():
    r = evaluate_s9(
        _base(
            evidence=[{
                "evidence_id": "E-prov", "exists": True,
                "relevance": "PASS", "freshness": "PASS", "scope": "PASS",
                "provenance": "FAIL", "integrity": "PASS",
            }]
        )
    )
    assert r.system_result == "BLOCKED"


def test_s9_013_unknown_unresolved():
    r = evaluate_s9(_base(unknown_conditions=["U1"]))
    assert r.system_result == "UNRESOLVED"


def test_s9_018_signature_not_authority():
    r = evaluate_s9(_base(authority={"required": True, "present": False, "signature": "deadbeef"}))
    assert r.system_result == "BLOCKED"


def test_s9_019_test_pass_not_authorization():
    r = evaluate_s9(_base(human=[], authority={"required": True, "present": False}))
    assert r.promotion_eligible is False
    assert r.system_result == "BLOCKED"


def test_never_infer_missing_h_as_satisfied():
    r2 = evaluate_s9({**_base(), "human": []})
    assert r2.human == "MISSING"
