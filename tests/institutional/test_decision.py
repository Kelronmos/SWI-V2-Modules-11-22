"""Institutional decision + adversarial tests."""
from swi_v2.institutional.decision import evaluate_access, case_transition_allowed
from swi_v2.institutional.models import AccessRequest, AuthorityRecord
from swi_v2.institutional.demo import synthetic_authorities, run_synthetic_demo


def _auth(**kw):
    base = dict(
        authority_id="A1", actor_id="TEACHER-001", role="teacher",
        subject_scope=["STUDENT-001"], resource_scope=["student_case_status"],
        action_scope=["view"], jurisdiction="example", authority_source="t",
        valid_from="2026-01-01", valid_until="2027-01-01", status="VALID",
        human_authority_required=False, evidence_required=True,
    )
    base.update(kw)
    return AuthorityRecord(**base)


def test_no_authority_blocked():
    req = AccessRequest("R1", "STRANGER", "STUDENT-001", "student_case_status", "view", "x", "example")
    r = evaluate_access(req, [_auth()], evidence=[])
    assert r["decision"] == "BLOCKED"
    assert r["s9_proven"] is False


def test_expired_authority():
    req = AccessRequest("R1", "TEACHER-001", "STUDENT-001", "student_case_status", "view", "x", "example", authority_ref="A1")
    r = evaluate_access(req, [_auth(status="EXPIRED")], evidence=[{"relevance": "PASS", "freshness": "PASS", "scope": "PASS", "provenance": "PASS", "integrity": "PASS"}])
    assert r["decision"] == "EXPIRED"


def test_cross_student_blocked():
    req = AccessRequest("R1", "TEACHER-001", "STUDENT-002", "student_case_status", "view", "x", "example")
    r = evaluate_access(req, [_auth()], evidence=[])
    assert r["decision"] == "BLOCKED"


def test_private_history_withheld():
    a = _auth(resource_scope=["student_case_status"])
    req = AccessRequest("R1", "TEACHER-001", "STUDENT-001", "student_private_history", "view", "x", "example", authority_ref="A1")
    r = evaluate_access(req, [a], evidence=[{"relevance": "PASS", "freshness": "PASS", "scope": "PASS", "provenance": "PASS", "integrity": "PASS"}],
                        law=["c"], governance=["c"], security=["c"], human=["c"], constraints=["c"])
    assert r["decision"] == "WITHHELD"


def test_evidence_required_empty_blocked():
    req = AccessRequest("R1", "TEACHER-001", "STUDENT-001", "student_case_status", "view", "x", "example", authority_ref="A1")
    r = evaluate_access(req, [_auth(evidence_required=True)], evidence=[])
    assert r["decision"] == "BLOCKED"
    assert r["e_exists"] is False


def test_inadequate_evidence_blocked():
    req = AccessRequest("R1", "TEACHER-001", "STUDENT-001", "student_case_status", "view", "x", "example", authority_ref="A1")
    r = evaluate_access(req, [_auth()], evidence=[{"relevance": "FAIL", "freshness": "PASS", "scope": "PASS", "provenance": "PASS", "integrity": "PASS"}],
                        law=["c"], governance=["c"], security=["c"], human=["c"], constraints=["c"])
    assert r["decision"] == "BLOCKED"
    assert r["e_exists"] is True
    assert r["e_adequate"] is False


def test_human_required_awaiting():
    a = _auth(human_authority_required=True, evidence_required=True)
    req = AccessRequest("R1", "TEACHER-001", "STUDENT-001", "student_case_status", "view", "x", "example", authority_ref="A1")
    r = evaluate_access(req, [a], evidence=[{"relevance": "PASS", "freshness": "PASS", "scope": "PASS", "provenance": "PASS", "integrity": "PASS"}],
                        law=["c"], governance=["c"], security=["c"], human=[], constraints=["c"])
    assert r["decision"] == "AWAITING"


def test_invalid_case_transitions():
    assert case_transition_allowed("BLOCKED", "ALLOWED") is False
    assert case_transition_allowed("ESCALATED", "APPROVED") is False
    assert case_transition_allowed("WITHHELD", "DISCLOSED") is False


def test_role_is_not_authority():
    req = AccessRequest("R1", "TEACHER-999", "STUDENT-001", "student_case_status", "view", "x", "example")
    r = evaluate_access(req, synthetic_authorities(), evidence=[])
    assert r["decision"] == "BLOCKED"


def test_demo_never_claims_s9_proven():
    out = run_synthetic_demo(source_commit="aa62042888886f5252e2b80e7aec8dce49e4bab3")
    assert out["s9_proven"] is False
    assert out["production_authorized"] is False
    assert out["scoreboard"]["BLOCKED"] >= 1
