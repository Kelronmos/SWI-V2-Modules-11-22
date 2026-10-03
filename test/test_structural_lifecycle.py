"""Structural maturity + continuous review tests (T01–T35 themes).

PROVEN: NO | SEALED: NO | PRODUCTION_AUTHORIZED: NO
No fabricated 99.9%/100% without measured ratio input.
"""
from __future__ import annotations

from swi_v2.kernel.structural_lifecycle import (
    AuthorityRequestStatus,
    LifecycleState,
    OperatingStatus,
    ReadinessStatus,
    StandardOwnership,
    StructuralStatus,
    apply_human_authority_decision,
    at_review_threshold,
    create_authority_request,
    enter_controlled_operation,
    freeze_affected_scope,
    funded_not_fully_ready,
    is_production_authorized,
    jurisdiction_mismatch,
    mark_repair_done_requires_revalidation,
    mark_structure_complete,
    material_change_requires_revalidation,
    observation_is_not_authority,
    people_ready,
    scope_is_frozen,
    self_analysis_cannot_authorize,
    self_analysis_findings,
    signature_is_not_authority,
    structural_complete_does_not_authorize,
    trigger_99_9_review_pause,
    unrelated_scope_may_operate,
)


def _base(**kw) -> LifecycleState:
    return LifecycleState(scope_id="scope-a", **kw)


def test_t01_funded_but_not_fully_ready():
    s = _base(funding=True, structural=StructuralStatus.STRUCTURE_BUILDING)
    assert funded_not_fully_ready(s) is True
    assert is_production_authorized(s) is False


def test_t02_t03_controlled_operation_with_continuing_review():
    s = enter_controlled_operation(_base(funding=True))
    assert s.operating is OperatingStatus.CONTROLLED_OPERATION
    assert s.continuous_review is True
    assert s.production_authorization is False


def test_t04_t05_threshold_pause_not_authorization():
    s0 = _base(structural_ratio=None)
    assert at_review_threshold(s0) is False
    s1 = trigger_99_9_review_pause(_base(structural_ratio=0.999))
    assert s1.structural is StructuralStatus.STRUCTURE_99_9_REVIEW_GATE
    assert s1.production_authorization is False


def test_t06_t07_self_analysis_detects_cannot_authorize():
    findings = self_analysis_findings(
        _base(authority_status="UNKNOWN"),
        ownership=None,
        evidence_present=False,
        training_complete=False,
    )
    assert "ownership_gap" in findings
    assert "evidence_gap" in findings
    assert self_analysis_cannot_authorize(findings, _base()) is True


def test_t08_t09_freeze_scope_independence():
    s = freeze_affected_scope(_base(), ["mod-a"])
    assert scope_is_frozen(s, "mod-a") is True
    assert unrelated_scope_may_operate(s, "mod-b", independent=True) is True
    assert unrelated_scope_may_operate(s, "mod-b", independent=False) is False
    assert unrelated_scope_may_operate(s, "mod-a", independent=True) is False


def test_t10_t11_repair_requires_revalidation():
    s = mark_repair_done_requires_revalidation(
        freeze_affected_scope(_base(), ["mod-a"])
    )
    assert s.revalidation_status == "REVALIDATION_REQUIRED"
    assert s.production_authorization is False


def test_t12_t13_t14_t15_authority_request_no_self_approve():
    req = create_authority_request(
        request_id="ar-1",
        action="resume",
        reason="repair",
        affected_scope=["mod-a"],
        requested_authority="human-owner",
    )
    assert req.status is AuthorityRequestStatus.AUTHORITY_REQUIRED
    assert req.self_approve().status is AuthorityRequestStatus.AUTHORITY_REQUIRED
    rejected = apply_human_authority_decision(req, granted=False, by_human=True)
    assert rejected.status is AuthorityRequestStatus.AUTHORITY_REJECTED
    still = apply_human_authority_decision(req, granted=True, by_human=False)
    assert still.status is AuthorityRequestStatus.AUTHORITY_REQUIRED
    granted = apply_human_authority_decision(req, granted=True, by_human=True)
    assert granted.status is AuthorityRequestStatus.AUTHORITY_GRANTED


def test_t16_t17_t18_t19_material_change_revalidation():
    s = material_change_requires_revalidation(_base(funding=True))
    assert s.revalidation_status == "REVALIDATION_REQUIRED"
    assert s.production_authorization is False


def test_t20_t21_people_readiness_training():
    assert people_ready(
        training_complete=False, competency_check=False, authority_status="ok"
    ) is ReadinessStatus.TRAINING_REQUIRED
    assert people_ready(
        training_complete=True, competency_check=True, authority_status="UNKNOWN"
    ) is ReadinessStatus.NOT_READY
    assert people_ready(
        training_complete=True, competency_check=True, authority_status="granted"
    ) is ReadinessStatus.READY


def test_t22_t23_ownership_and_section():
    incomplete = StandardOwnership(
        standard="",
        section="s1",
        jurisdiction="BW",
        owner="",
        accountable_authority="a",
        responsible_team="t",
        version="1",
        approval_status="UNKNOWN",
    )
    assert incomplete.ownership_complete() is False
    complete = StandardOwnership(
        standard="ISO",
        section="s1",
        jurisdiction="BW",
        owner="owner",
        accountable_authority="acct",
        responsible_team="team",
        version="1.0",
        approval_status="APPROVED",
    )
    assert complete.ownership_complete() is True


def test_t24_t25_evidence_gaps_in_self_analysis():
    f = self_analysis_findings(
        _base(evidence_status="STALE"),
        ownership=StandardOwnership(
            standard="S", section="1", jurisdiction="BW", owner="o",
            accountable_authority="a", responsible_team="t", version="1",
            approval_status="APPROVED",
        ),
        evidence_present=False,
        training_complete=True,
    )
    assert "evidence_gap" in f


def test_t26_jurisdiction_mismatch():
    own = StandardOwnership(
        standard="S", section="1", jurisdiction="BW", owner="o",
        accountable_authority="a", responsible_team="t", version="1",
        approval_status="APPROVED",
    )
    assert jurisdiction_mismatch(own, "ZA") is True
    assert jurisdiction_mismatch(own, "BW") is False


def test_t27_t28_t29_authority_boundaries():
    assert observation_is_not_authority({"cek": True}) is True
    assert signature_is_not_authority({"sig": "x"}) is True
    s = _base(authority_status="MISSING")
    f = self_analysis_findings(s, evidence_present=True, training_complete=True)
    assert "authority_gap" in f


def test_t30_replay_not_fresh_authorization():
    s = _base()
    assert s.production_authorization is False


def test_t31_t32_t33_complete_not_auto_auth_and_review_continues():
    s = mark_structure_complete(_base(funding=True))
    assert s.structural is StructuralStatus.STRUCTURE_COMPLETE
    assert s.production_authorization is False
    assert s.continuous_review is True
    assert structural_complete_does_not_authorize(s) is True
    s2 = material_change_requires_revalidation(s)
    assert s2.revalidation_status == "REVALIDATION_REQUIRED"


def test_t34_t35_repair_retest_evidence_bound():
    s = mark_repair_done_requires_revalidation(_base())
    assert s.structural is StructuralStatus.STRUCTURE_REVALIDATING
    assert s.proven is False
    assert s.sealed is False
    assert s.production_authorization is False
