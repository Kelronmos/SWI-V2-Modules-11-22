"""Synthetic multi-level demonstration — NO REAL PERSON DATA."""
from __future__ import annotations

from typing import Any, Dict, List

from .decision import evaluate_access, case_transition_allowed
from .models import (
    AccessRequest,
    AuthorityRecord,
    Case,
    EscalationRecord,
    OrganizationNode,
    WithholdRecord,
)


def synthetic_org() -> List[OrganizationNode]:
    return [
        OrganizationNode("COUNTRY-001", "country", "example", None, ["policy_aggregate"], ["aggregate"], ["report"], [], ["STATE-001"]),
        OrganizationNode("STATE-001", "state", "example", "COUNTRY-001", ["policy"], ["aggregate"], ["report"], [], ["REGION-001"]),
        OrganizationNode("REGION-001", "region", "example", "STATE-001", ["jurisdiction_example"], ["aggregate"], ["review"], [], ["SCHOOL-001"]),
        OrganizationNode("SCHOOL-001", "institution", "example", "REGION-001", ["school_ops"], ["school"], ["manage"], [], ["ADMIN-001"]),
    ]


def synthetic_authorities() -> List[AuthorityRecord]:
    return [
        AuthorityRecord(
            "AUTH-STUDENT-001", "STUDENT-001", "student",
            ["STUDENT-001"], ["own_case"], ["create", "view_own"],
            "example", "synthetic_demo", "2026-01-01", "2027-01-01", "VALID",
            human_authority_required=False, evidence_required=False, privacy_constraints=["own_only"],
        ),
        AuthorityRecord(
            "AUTH-PARENT-001", "PARENT-001", "parent",
            ["STUDENT-001"], ["student_case_status"], ["view"],
            "example", "synthetic_demo", "2026-01-01", "2027-01-01", "VALID",
            human_authority_required=False, evidence_required=True, privacy_constraints=["subject_specific"],
        ),
        AuthorityRecord(
            "AUTH-PARENT-EXPIRED", "PARENT-001", "parent",
            ["STUDENT-001"], ["student_case_status"], ["view"],
            "example", "synthetic_demo", "2020-01-01", "2021-01-01", "EXPIRED",
            human_authority_required=False, evidence_required=True,
        ),
        AuthorityRecord(
            "AUTH-TEACHER-001", "TEACHER-001", "teacher",
            ["STUDENT-001"], ["student_case_status"], ["view", "request", "escalate"],
            "example", "synthetic_demo", "2026-01-01", "2027-01-01", "VALID",
            human_authority_required=False, evidence_required=True, privacy_constraints=["no_private_history"],
        ),
        AuthorityRecord(
            "AUTH-ADMIN-001", "ADMIN-001", "admin",
            ["STUDENT-001"], ["student_case_status", "case_evidence"], ["view", "provide_evidence", "escalate"],
            "example", "synthetic_demo", "2026-01-01", "2027-01-01", "VALID",
            human_authority_required=True, evidence_required=True,
        ),
        AuthorityRecord(
            "AUTH-MINISTRY-001", "MINISTRY-001", "ministry",
            ["*"], ["aggregate_report"], ["view_aggregate"],
            "example", "synthetic_demo", "2026-01-01", "2027-01-01", "VALID",
            human_authority_required=True, evidence_required=True, privacy_constraints=["aggregate_only"],
        ),
    ]


def run_synthetic_demo(*, source_commit: str = "UNBOUND") -> Dict[str, Any]:
    """Run the prescribed synthetic path. Never invents success."""
    orgs = synthetic_org()
    auths = synthetic_authorities()
    ledger: List[Dict[str, Any]] = []
    receipts: List[Dict[str, Any]] = []
    score = {
        "ALLOWED": 0, "BLOCKED": 0, "WITHHELD": 0, "ESCALATED": 0,
        "AWAITING": 0, "RESOLVED": 0, "UNKNOWN": 0, "EXPIRED": 0, "REVOKED": 0,
        "authority_failures": 0, "evidence_failures": 0, "privacy_failures": 0,
    }

    def record(step: str, result: Dict[str, Any]) -> None:
        d = result["decision"]
        score[d] = score.get(d, 0) + 1
        if "NO AUTHORITY" in " ".join(result["reasons"]) or "EXPIRED" in d or "REVOKED" in d:
            score["authority_failures"] += 1
        if any("EVIDENCE" in r or "adequate" in r for r in result["reasons"]):
            score["evidence_failures"] += 1
        if any("PRIVACY" in r or "WITHHELD" in r for r in result["reasons"]):
            score["privacy_failures"] += 1
        ledger.append({"step": step, **{k: result[k] for k in ("decision", "reasons", "e_exists", "e_adequate", "s9_proven")}})
        receipts.append(result["receipt"])

    case = Case("CASE-001", "STUDENT-001", "STUDENT-001", "CREATED", jurisdiction="example")
    case.status = "RECEIVED"
    ledger.append({"step": "1_case_created", "case": case.to_dict()})

    req_t = AccessRequest(
        "REQ-T-001", "TEACHER-001", "STUDENT-001", "student_case_status", "view",
        "instructional_need", "example", authority_ref="AUTH-TEACHER-001",
        evidence_refs=[], source_commit=source_commit,
    )
    r1 = evaluate_access(
        req_t, auths, evidence=[], law=[], governance=[], security=[], human=[],
        source_commit=source_commit,
    )
    record("4_teacher_view_missing_LGH_evidence", r1)

    req_priv = AccessRequest(
        "REQ-T-PRIV", "TEACHER-001", "STUDENT-001", "student_private_history", "view",
        "curiosity", "example", authority_ref="AUTH-TEACHER-001", source_commit=source_commit,
    )
    r_priv = evaluate_access(
        req_priv, auths,
        evidence=[{"evidence_id": "E1", "relevance": "PASS", "freshness": "PASS", "scope": "PASS", "provenance": "PASS", "integrity": "PASS"}],
        law=["c"], governance=["c"], security=["c"], human=["c"], constraints=["c"],
        source_commit=source_commit,
    )
    record("privacy_withhold_private_history", r_priv)

    esc = EscalationRecord(
        "ESC-001", "CASE-001", "AUTH-TEACHER-001", "AUTH-ADMIN-001",
        "need case evidence", "teacher_request_blocked", [], ["AUTH-TEACHER-001"],
        ["no_private_history"], "ESCALATED", receipts[-1]["receipt_id"] if receipts else "RCPT-0",
    )
    score["ESCALATED"] += 1
    ledger.append({"step": "7_escalate", "escalation": esc.to_dict()})
    case.status = "ESCALATED"

    evidence_admin = [{
        "evidence_id": "E-ADMIN-001", "exists": True,
        "relevance": "PASS", "freshness": "PASS", "scope": "PASS",
        "provenance": "PASS", "integrity": "PASS",
    }]
    req_a = AccessRequest(
        "REQ-A-001", "ADMIN-001", "STUDENT-001", "case_evidence", "provide_evidence",
        "escalation_response", "example", authority_ref="AUTH-ADMIN-001",
        evidence_refs=["E-ADMIN-001"], source_commit=source_commit,
    )
    r_admin = evaluate_access(
        req_a, auths, evidence=evidence_admin,
        law=["system_integrity"], governance=["system_integrity"], security=["system_integrity"],
        human=[], constraints=["system_integrity"], source_commit=source_commit,
    )
    record("11_admin_evidence_awaiting_human", r_admin)
    case.status = "AWAITING"

    r_admin2 = evaluate_access(
        req_a, auths, evidence=evidence_admin,
        law=["system_integrity"], governance=["system_integrity"], security=["system_integrity"],
        human=["system_integrity"], constraints=["system_integrity"], source_commit=source_commit,
    )
    record("13_reeval_with_H", r_admin2)

    req_x = AccessRequest(
        "REQ-X-001", "STUDENT-001", "STUDENT-002", "own_case", "view_own",
        "attack", "example", authority_ref="AUTH-STUDENT-001", source_commit=source_commit,
    )
    r_x = evaluate_access(req_x, auths, evidence=[], source_commit=source_commit)
    record("attack_cross_student", r_x)

    req_pe = AccessRequest(
        "REQ-P-EXP", "PARENT-001", "STUDENT-001", "student_case_status", "view",
        "expired", "example", authority_ref="AUTH-PARENT-EXPIRED", source_commit=source_commit,
    )
    r_pe = evaluate_access(
        req_pe, auths,
        evidence=[{"evidence_id": "E", "relevance": "PASS", "freshness": "PASS", "scope": "PASS", "provenance": "PASS", "integrity": "PASS"}],
        law=["c"], governance=["c"], security=["c"], human=["c"], constraints=["c"],
        source_commit=source_commit,
    )
    record("attack_expired_parent", r_pe)

    req_m = AccessRequest(
        "REQ-M-001", "MINISTRY-001", "STUDENT-001", "student_case_status", "view",
        "individual", "example", authority_ref="AUTH-MINISTRY-001", source_commit=source_commit,
    )
    r_m = evaluate_access(req_m, auths, evidence=[], source_commit=source_commit)
    record("ministry_individual_outside_aggregate", r_m)

    wh = WithholdRecord(
        "WH-001", "CASE-001", "student_private_history", "privacy_boundary",
        "WITHHELD_PRIVACY", "TEACHER-001", "ADMIN-001", "explicit_human_release",
        [], ["AUTH-TEACHER-001"], receipts[0]["receipt_id"] if receipts else "RCPT-0",
    )
    ledger.append({"step": "16_withhold", "withhold": wh.to_dict()})
    score["WITHHELD"] += 1

    if case_transition_allowed(case.status, "RESOLVED"):
        case.status = "RESOLVED"
        score["RESOLVED"] += 1
        ledger.append({"step": "17_resolve", "status": case.status})
    if case_transition_allowed("RESOLVED", "RECONCILED"):
        case.status = "RECONCILED"
        ledger.append({"step": "18_reconcile", "status": case.status})
    if case_transition_allowed("RECONCILED", "ARCHIVED"):
        case.status = "ARCHIVED"
        ledger.append({"step": "19_archive", "status": case.status})

    invalid_ok = not case_transition_allowed("BLOCKED", "ALLOWED")
    ledger.append({"step": "invalid_transition_blocked_to_allowed", "blocked": invalid_ok})

    return {
        "status": "EXPERIMENTAL_DEMONSTRATION",
        "s9_proven": False,
        "production_authorized": False,
        "source_commit": source_commit,
        "organizations": [o.to_dict() for o in orgs],
        "authorities": [a.to_dict() for a in auths],
        "case": case.to_dict(),
        "ledger": ledger,
        "receipts": receipts,
        "scoreboard": score,
        "note": "Organizational levels are NOT automatic authority. Demonstration only.",
    }
