"""SWI Structural Invariants — architecture guardrail.

Verifies the core doctrine inequalities against live experimental code.
Does not claim business modules that do not yet exist.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

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


def test_invariant_data_not_evidence_not_admission_not_authorization_not_action():
    """Doctrine inequality must hold as separable concepts in Common Sense decisions."""
    monitor = CommonSenseMonitor()
    evidence = monitor.inspect(_case())

    # Evidence is produced, but it is not authorization and not action
    assert evidence is not None
    assert evidence.decision is CommonSenseDecision.CONTINUE
    # Monitor never opens the downstream execution pipe
    assert monitor.may_cross_downstream_pipe(_case()) is False


def test_invariant_proof_not_authorization():
    """A successful inspection produces evidence, never authorization."""
    monitor = CommonSenseMonitor()
    evidence = monitor.inspect(_case())

    assert evidence.decision in {
        CommonSenseDecision.CONTINUE,
        CommonSenseDecision.RECHECK,
        CommonSenseDecision.HALT,
        CommonSenseDecision.ESCALATE,
    }
    # Explicitly forbidden actions must raise
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
    """COMMON_SENSE ∩ {EXECUTION, PROMOTION, SEAL, AUTHORIZATION} = ∅"""
    monitor = CommonSenseMonitor()
    forbidden = monitor.FORBIDDEN
    assert "EXECUTE" in forbidden
    assert "PROMOTE" in forbidden
    assert "SEAL" in forbidden
    assert "AUTHORIZE" in forbidden
    assert "EXTEND_AUTHORIZATION" in forbidden
    assert "RENEW_AUTHORIZATION" in forbidden


def test_invariant_role_not_unlimited_authority():
    """Authorization with wrong scope must be invalid."""
    now = _now()
    auth = _auth(now, scope=frozenset({"diagnostic"}))
    case = _case(
        now=now,
        authorization=auth,
        required_scope=frozenset({"diagnostic", "payroll"}),  # extra scope required
    )
    monitor = CommonSenseMonitor()
    evidence = monitor.inspect(case)
    assert evidence.decision is CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in evidence.reason_codes


def test_invariant_failure_halts():
    """Terminal failure conditions produce HALT."""
    monitor = CommonSenseMonitor()

    # Equation mismatch
    e1 = monitor.inspect(_case(equation_match=False))
    assert e1.decision is CommonSenseDecision.HALT

    # Privacy boundary
    e2 = monitor.inspect(_case(privacy_minimized=False))
    assert e2.decision is CommonSenseDecision.HALT

    # Security boundary
    e3 = monitor.inspect(_case(security_boundary_intact=False))
    assert e3.decision is CommonSenseDecision.HALT


def test_invariant_terminal_failure_blocks_downstream():
    """TERMINAL_FAILURE ↛ DOWNSTREAM"""
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
    auth = _auth(now, revoked=True)
    evidence = CommonSenseMonitor().inspect(_case(now=now, authorization=auth))
    assert evidence.decision is CommonSenseDecision.HALT


def test_invariant_sensitive_payload_not_retained():
    """Sensitive / vulnerable cases must not retain payload in evidence."""
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
    monitor = CommonSenseMonitor()
    with pytest.raises(PermissionError):
        monitor.request_action("EXECUTE")
