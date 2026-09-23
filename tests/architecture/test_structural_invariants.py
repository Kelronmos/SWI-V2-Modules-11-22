"""SWI Structural Invariants — constitutional architecture guardrail.

Verifies core doctrine inequalities and constitutional floor against
live experimental code only. Does not invent unimplemented modules.

Status: RESEARCH / EXPERIMENTAL
Seal: NOT CLAIMED
Production: NOT AUTHORIZED
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from experimental.common_sense.monitor import (
    AuthorizationContext,
    CommonSenseDecision,
    CommonSenseMonitor,
    HarmProfile,
    PatternObservation,
    Sensitivity,
    SimulationCase,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _now():
    return datetime.now(timezone.utc)


def _auth(now, **kwargs):
    defaults = dict(
        principal="research-human",
        scope=frozenset({"diagnostic"}),
        purpose="research",
        started_at=now - timedelta(minutes=5),
        expires_at=now + timedelta(minutes=5),
        conditions=frozenset({"human_review"}),
        revoked=False,
    )
    defaults.update(kwargs)
    return AuthorizationContext(**defaults)


def _case(now=None, **overrides):
    now = now or _now()
    values = dict(
        case_id="INV-001",
        sensitivity=Sensitivity.PUBLIC,
        required_scope=frozenset({"diagnostic"}),
        required_conditions=frozenset({"human_review"}),
        now=now,
        authorization=_auth(now),
        harm=HarmProfile(),
        pattern=PatternObservation(name="baseline"),
        equation_match=True,
        privacy_minimized=True,
        security_boundary_intact=True,
    )
    values.update(overrides)
    return SimulationCase(**values)


# ---------------------------------------------------------------------------
# Core doctrine inequalities
# ---------------------------------------------------------------------------

def test_invariant_data_not_evidence_not_admission_not_authorization_not_action():
    monitor = CommonSenseMonitor()
    evidence = monitor.inspect(_case())
    assert evidence is not None
    assert evidence.decision is CommonSenseDecision.CONTINUE
    assert monitor.may_cross_downstream_pipe(_case()) is False


def test_invariant_proof_not_authorization():
    monitor = CommonSenseMonitor()
    evidence = monitor.inspect(_case())
    assert evidence.decision in {
        CommonSenseDecision.CONTINUE,
        CommonSenseDecision.RECHECK,
        CommonSenseDecision.HALT,
        CommonSenseDecision.ESCALATE,
    }
    for action in (
        "AUTHORIZE",
        "EXECUTE",
        "PROMOTE",
        "SEAL",
        "EXTEND_AUTHORIZATION",
        "RENEW_AUTHORIZATION",
    ):
        with pytest.raises(PermissionError):
            monitor.request_action(action)


def test_invariant_common_sense_not_authority():
    monitor = CommonSenseMonitor()
    forbidden = monitor.FORBIDDEN
    for action in (
        "EXECUTE",
        "PROMOTE",
        "SEAL",
        "AUTHORIZE",
        "EXTEND_AUTHORIZATION",
        "RENEW_AUTHORIZATION",
    ):
        assert action in forbidden


def test_invariant_role_not_unlimited_authority():
    now = _now()
    auth = _auth(now, scope=frozenset({"diagnostic"}))
    case = _case(
        now=now,
        authorization=auth,
        required_scope=frozenset({"diagnostic", "payroll"}),
    )
    evidence = CommonSenseMonitor().inspect(case)
    assert evidence.decision is CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in evidence.reason_codes


def test_invariant_failure_halts():
    monitor = CommonSenseMonitor()
    assert monitor.inspect(_case(equation_match=False)).decision is CommonSenseDecision.HALT
    assert monitor.inspect(_case(privacy_minimized=False)).decision is CommonSenseDecision.HALT
    assert monitor.inspect(_case(security_boundary_intact=False)).decision is CommonSenseDecision.HALT


def test_invariant_terminal_failure_blocks_downstream():
    monitor = CommonSenseMonitor()
    case = _case(equation_match=False)
    evidence = monitor.inspect(case)
    assert evidence.decision is CommonSenseDecision.HALT
    assert monitor.may_cross_downstream_pipe(case) is False


def test_invariant_expired_authorization_halts():
    now = _now()
    auth = AuthorizationContext(
        principal="research-human",
        scope=frozenset({"diagnostic"}),
        purpose="research",
        started_at=now - timedelta(hours=2),
        expires_at=now - timedelta(hours=1),
        conditions=frozenset({"human_review"}),
    )
    evidence = CommonSenseMonitor().inspect(_case(now=now, authorization=auth))
    assert evidence.decision is CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in evidence.reason_codes


def test_invariant_revoked_authorization_halts():
    now = _now()
    evidence = CommonSenseMonitor().inspect(_case(now=now, authorization=_auth(now, revoked=True)))
    assert evidence.decision is CommonSenseDecision.HALT


def test_invariant_sensitive_payload_not_retained():
    evidence = CommonSenseMonitor().inspect(
        _case(
            sensitivity=Sensitivity.VULNERABLE,
            harm=HarmProfile(vulnerable_population=1.0),
        )
    )
    assert evidence.payload_retained is False
    assert evidence.sensitive_payload_retained is False
    assert "HEIGHTENED_DATA_PROTECTION" in evidence.reason_codes


def test_invariant_execution_cannot_be_requested_from_cek():
    with pytest.raises(PermissionError):
        CommonSenseMonitor().request_action("EXECUTE")


# ---------------------------------------------------------------------------
# Constitutional floor inequalities (docs + structure; no invented modules)
# ---------------------------------------------------------------------------

def test_invariant_experimental_not_production():
    assert (REPO_ROOT / "experimental" / "common_sense").is_dir()
    assert not (REPO_ROOT / "swi_v2" / "common_sense").exists()
    assert (REPO_ROOT / "experimental" / "response_boundary").is_dir()
    assert not (REPO_ROOT / "swi_v2" / "response_boundary").exists()


def test_invariant_tested_not_sealed_claim_in_cek():
    """CEK module docstring and status must not claim SEALED or PRODUCTION."""
    monitor_src = (REPO_ROOT / "experimental" / "common_sense" / "monitor.py").read_text(
        encoding="utf-8"
    )
    assert "NOT SEALED" in monitor_src or "NOT PRODUCTION" in monitor_src
    assert "Research status" in monitor_src or "EXPERIMENTAL" in monitor_src


def test_invariant_diagnosis_not_authority():
    """Diagnosis / escalate produces evidence path, never execution authority."""
    monitor = CommonSenseMonitor()
    case = _case(
        harm=HarmProfile(
            physical_harm=0.9,
            downstream_consequence=0.9,
            reversibility=0.1,
        )
    )
    evidence = monitor.inspect(case)
    assert evidence.decision is CommonSenseDecision.ESCALATE
    assert monitor.may_cross_downstream_pipe(case) is False
    with pytest.raises(PermissionError):
        monitor.request_action("AUTHORIZE")


def test_invariant_no_weapon_or_population_selector_modules_in_production():
    """Protected-humanity: no production modules that select targets or populations."""
    production = REPO_ROOT / "swi_v2"
    forbidden_names = {
        "weapon",
        "target_selector",
        "population_selector",
        "displacement",
        "civilization_control",
    }
    found = []
    if production.exists():
        for p in production.rglob("*"):
            name = p.name.lower()
            for f in forbidden_names:
                if f in name:
                    found.append(str(p.relative_to(REPO_ROOT)))
    assert not found, f"Forbidden production paths: {found}"


def test_invariant_no_autonomous_authority_interface_on_cek():
    """CEK must expose no method that grants, extends, or renews authority."""
    monitor = CommonSenseMonitor()
    for name in ("authorize", "grant_authority", "extend_authorization", "renew_authorization"):
        assert not hasattr(monitor, name) or not callable(getattr(monitor, name, None))


def test_invariant_vote_not_encoded_as_unlimited_authority_in_cek():
    """CEK must not treat a vote count or similar as automatic authority."""
    monitor = CommonSenseMonitor()
    # No vote-based authorization method
    assert not hasattr(monitor, "authorize_by_vote")
    assert not hasattr(monitor, "apply_vote")
    with pytest.raises(PermissionError):
        monitor.request_action("AUTHORIZE")
