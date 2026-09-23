"""L0 formal properties P01–P14 as executable invariants.

Parallel to PH-01…14. Does not require TLC.
Does not claim seal, legal validity, or production readiness.
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
    d = dict(
        principal="research-human",
        scope=frozenset({"diagnostic"}),
        purpose="research",
        started_at=now - timedelta(minutes=5),
        expires_at=now + timedelta(hours=1),
        conditions=frozenset({"human_review"}),
        revoked=False,
    )
    d.update(kwargs)
    return AuthorizationContext(**d)


def _case(now=None, **overrides):
    now = now or _now()
    base = dict(
        case_id="p-formal",
        sensitivity=Sensitivity.PUBLIC,
        required_scope=frozenset({"diagnostic"}),
        required_conditions=frozenset({"human_review"}),
        now=now,
        authorization=_auth(now),
        harm=HarmProfile(),
        pattern=PatternObservation(name="p"),
        equation_match=True,
        privacy_minimized=True,
        security_boundary_intact=True,
    )
    base.update(overrides)
    return SimulationCase(**base)


@pytest.fixture
def m():
    return CommonSenseMonitor()


def test_p01_request_action_always_permission_error(m):
    for action in list(CommonSenseMonitor.FORBIDDEN) + ["x", "SURVIVAL", ""]:
        with pytest.raises(PermissionError):
            m.request_action(action or "noop")


def test_p02_may_cross_downstream_always_false(m):
    now = _now()
    for case in (
        _case(now),
        _case(now, equation_match=False),
        _case(now, authorization=_auth(now, revoked=True)),
    ):
        assert m.may_cross_downstream_pipe(case) is False


def test_p03_revoked_halts(m):
    now = _now()
    r = m.inspect(_case(now, authorization=_auth(now, revoked=True)))
    assert r.decision == CommonSenseDecision.HALT


def test_p04_expired_halts(m):
    now = _now()
    r = m.inspect(
        _case(
            now,
            authorization=_auth(
                now,
                started_at=now - timedelta(hours=2),
                expires_at=now - timedelta(seconds=1),
            ),
        )
    )
    assert r.decision == CommonSenseDecision.HALT


def test_p05_scope_mismatch_halts(m):
    now = _now()
    r = m.inspect(
        _case(
            now,
            required_scope=frozenset({"diagnostic", "extra"}),
            authorization=_auth(now, scope=frozenset({"diagnostic"})),
        )
    )
    assert r.decision == CommonSenseDecision.HALT


def test_p06_condition_mismatch_halts(m):
    now = _now()
    r = m.inspect(
        _case(
            now,
            required_conditions=frozenset({"human_review", "x"}),
            authorization=_auth(now, conditions=frozenset({"human_review"})),
        )
    )
    assert r.decision == CommonSenseDecision.HALT


def test_p07_equation_mismatch_halts(m):
    r = m.inspect(_case(equation_match=False))
    assert r.decision == CommonSenseDecision.HALT


def test_p08_privacy_failure_halts(m):
    r = m.inspect(_case(privacy_minimized=False))
    assert r.decision == CommonSenseDecision.HALT


def test_p09_security_failure_halts(m):
    r = m.inspect(_case(security_boundary_intact=False))
    assert r.decision == CommonSenseDecision.HALT


def test_p10_survival_framing_not_authorization(m):
    with pytest.raises(PermissionError):
        m.request_action("AUTHORIZE")
    with pytest.raises(PermissionError):
        m.request_action("EXECUTE")


def test_p11_authority_drift_recheck(m):
    now = _now()
    r = m.inspect(
        _case(
            now,
            pattern=PatternObservation(
                name="d",
                occurrences=10,
                baseline_occurrences=1,
                authority_drift=True,
                repeated_failure=True,
                abnormal_sequence=True,
            ),
        )
    )
    assert "AUTHORITY_DRIFT" in r.reason_codes
    assert r.decision == CommonSenseDecision.RECHECK


def test_p12_repeated_failure_no_promote(m):
    with pytest.raises(PermissionError):
        m.request_action("PROMOTE")


def test_p13_abnormal_no_pipe(m):
    now = _now()
    case = _case(
        now,
        pattern=PatternObservation(
            name="a", occurrences=3, baseline_occurrences=1, abnormal_sequence=True
        ),
    )
    m.inspect(case)
    assert m.may_cross_downstream_pipe(case) is False


def test_p14_inspect_does_not_grant_forbidden_authority(m):
    r = m.inspect(_case())
    assert r.decision.value not in {"EXECUTE", "AUTHORIZE", "PROMOTE", "SEAL"}
    assert r.decision in {
        CommonSenseDecision.CONTINUE,
        CommonSenseDecision.RECHECK,
        CommonSenseDecision.ESCALATE,
        CommonSenseDecision.HALT,
    }
