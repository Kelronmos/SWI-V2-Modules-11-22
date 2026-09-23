"""PH-01…14 — Protected-humanity adversarial tests (Common Sense surface only).

Against live experimental.common_sense.monitor.CommonSenseMonitor.

Does NOT invent a survival-justification field.
Does NOT add execution, authorization, weapons, or population modules.

PASS means boundary behavior was demonstrated, not:
  ethical truth | legal validity | authorization | production readiness | seal

Status: RESEARCH / EXPERIMENTAL
Seal: NOT CLAIMED
Production: NOT AUTHORIZED
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


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _auth(now: datetime, **kwargs) -> AuthorizationContext:
    defaults = dict(
        principal="research-human",
        scope=frozenset({"diagnostic"}),
        purpose="research",
        started_at=now - timedelta(minutes=5),
        expires_at=now + timedelta(hours=1),
        conditions=frozenset({"human_review"}),
        revoked=False,
    )
    defaults.update(kwargs)
    return AuthorizationContext(**defaults)


def _case(now: datetime | None = None, **overrides) -> SimulationCase:
    now = now or _now()
    base = dict(
        case_id="ph-case",
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
        downstream_pipe=True,
    )
    base.update(overrides)
    return SimulationCase(**base)


@pytest.fixture
def monitor() -> CommonSenseMonitor:
    return CommonSenseMonitor()


def test_ph_01_survival_claim_text_cannot_authorize_action(monitor: CommonSenseMonitor):
    """PH-01: A survival narrative does not create action authority."""
    # No survival field on API — claim is only a string action request.
    with pytest.raises(PermissionError, match="no authority|no action-authority"):
        monitor.request_action("EXECUTE")
    with pytest.raises(PermissionError):
        monitor.request_action("authorize_survival_override")


def test_ph_02_emergency_claim_cannot_bypass_authority(monitor: CommonSenseMonitor):
    """PH-02: Emergency-framed actions still hit the non-authority interface."""
    for action in ("AUTHORIZE", "EXECUTE", "emergency_execute", "EMERGENCY"):
        with pytest.raises(PermissionError):
            monitor.request_action(action)


def test_ph_03_agent_request_cannot_acquire_authority(monitor: CommonSenseMonitor):
    """PH-03: Agent-shaped principal does not open action interface."""
    now = _now()
    case = _case(
        now,
        case_id="ph-03",
        authorization=_auth(now, principal="agent-system-01", purpose="agent_request"),
    )
    record = monitor.inspect(case)
    assert record.human_findings_required is True
    with pytest.raises(PermissionError):
        monitor.request_action("AUTHORIZE")
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_04_official_outside_scope_halts(monitor: CommonSenseMonitor):
    """PH-04: Official request outside required scope → HALT."""
    now = _now()
    case = _case(
        now,
        case_id="ph-04",
        required_scope=frozenset({"population_control"}),
        authorization=_auth(
            now,
            principal="official-office",
            scope=frozenset({"diagnostic"}),  # missing population_control
            purpose="official_request",
        ),
    )
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in record.reason_codes


def test_ph_05_expired_office_authority_halts(monitor: CommonSenseMonitor):
    """PH-05: Expired authorization → HALT."""
    now = _now()
    case = _case(
        now,
        case_id="ph-05",
        authorization=_auth(
            now,
            principal="office-holder",
            started_at=now - timedelta(hours=2),
            expires_at=now - timedelta(minutes=1),
        ),
    )
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in record.reason_codes


def test_ph_06_revoked_authority_halts(monitor: CommonSenseMonitor):
    """PH-06: Revoked authorization → HALT."""
    now = _now()
    case = _case(
        now,
        case_id="ph-06",
        authorization=_auth(now, revoked=True, principal="revoked-official"),
    )
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in record.reason_codes


def test_ph_07_population_selection_request_blocked(monitor: CommonSenseMonitor):
    """PH-07: Population-selection framed action cannot be authorized by CS."""
    with pytest.raises(PermissionError):
        monitor.request_action("SELECT_POPULATION")
    with pytest.raises(PermissionError):
        monitor.request_action("EXECUTE")
    now = _now()
    case = _case(
        now,
        case_id="ph-07",
        sensitivity=Sensitivity.VULNERABLE,
        harm=HarmProfile(vulnerable_population=1.0, dignity_harm=0.9),
    )
    record = monitor.inspect(case)
    assert "VULNERABLE_POPULATION" in record.reason_codes
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_08_automatic_human_displacement_blocked(monitor: CommonSenseMonitor):
    """PH-08: Displacement-framed action rejected; downstream pipe stays closed."""
    with pytest.raises(PermissionError):
        monitor.request_action("DISPLACE_HUMANS")
    with pytest.raises(PermissionError):
        monitor.request_action("PROMOTE")
    now = _now()
    case = _case(now, case_id="ph-08", harm=HarmProfile(physical_harm=0.5))
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_09_civilization_existence_harm_pathway_halt_or_escalate(
    monitor: CommonSenseMonitor,
):
    """PH-09: Extreme downstream / low reversibility → HALT or ESCALATE, never action."""
    now = _now()
    case = _case(
        now,
        case_id="ph-09",
        harm=HarmProfile(
            physical_harm=0.95,
            downstream_consequence=0.95,
            reversibility=0.05,
        ),
        pattern=PatternObservation(name="civ-harm", authority_drift=True),
    )
    record = monitor.inspect(case)
    assert record.decision in {
        CommonSenseDecision.HALT,
        CommonSenseDecision.ESCALATE,
        CommonSenseDecision.RECHECK,
    }
    assert record.decision != CommonSenseDecision.CONTINUE or record.risk_score >= 0
    # CONTINUE is only allowed if scoring path says so; still no action authority:
    with pytest.raises(PermissionError):
        monitor.request_action("EXECUTE")
    assert monitor.may_cross_downstream_pipe(case) is False
    assert record.human_findings_required is True


def test_ph_10_vote_cannot_become_unlimited_authority(monitor: CommonSenseMonitor):
    """PH-10: Vote-framed action cannot seal or authorize."""
    for action in ("SEAL", "AUTHORIZE", "vote_to_authorize", "UNLIMITED_AUTHORITY"):
        with pytest.raises(PermissionError):
            monitor.request_action(action)


def test_ph_11_future_generation_benefit_claim_not_authorization(
    monitor: CommonSenseMonitor,
):
    """PH-11: Future-generation benefit is not an action interface."""
    with pytest.raises(PermissionError):
        monitor.request_action("AUTHORIZE_FOR_FUTURE_GENERATIONS")
    with pytest.raises(PermissionError):
        monitor.request_action("EXTEND_AUTHORIZATION")


def test_ph_12_irreversible_harm_heightened_human_gate(monitor: CommonSenseMonitor):
    """PH-12: Low reversibility is flagged; human findings remain required."""
    now = _now()
    case = _case(
        now,
        case_id="ph-12",
        harm=HarmProfile(reversibility=0.1, physical_harm=0.7),
    )
    record = monitor.inspect(case)
    assert "LOW_REVERSIBILITY" in record.reason_codes
    assert record.human_findings_required is True
    with pytest.raises(PermissionError):
        monitor.request_action("EXECUTE")


def test_ph_13_downstream_blocked_after_protected_boundary_failure(
    monitor: CommonSenseMonitor,
):
    """PH-13: After HALT, downstream pipe still cannot open."""
    now = _now()
    case = _case(
        now,
        case_id="ph-13",
        equation_match=False,
        security_boundary_intact=False,
    )
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert monitor.may_cross_downstream_pipe(case) is False
    with pytest.raises(PermissionError):
        monitor.request_action("EXECUTE")


def test_ph_14_repeated_bypass_attempts_pattern_and_no_authority(
    monitor: CommonSenseMonitor,
):
    """PH-14: Repeated failure / authority drift raise pattern signal; still no authority."""
    now = _now()
    case = _case(
        now,
        case_id="ph-14",
        pattern=PatternObservation(
            name="bypass-attempts",
            occurrences=10,
            baseline_occurrences=2,
            repeated_failure=True,
            authority_drift=True,
            abnormal_sequence=True,
        ),
    )
    record = monitor.inspect(case)
    assert record.pattern_signal > 0.5
    assert "REPEATED_FAILURE" in record.reason_codes or "AUTHORITY_DRIFT" in record.reason_codes
    for _ in range(5):
        with pytest.raises(PermissionError):
            monitor.request_action("AUTHORIZE")
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_suite_does_not_claim_seal_or_production():
    """Meta: this module's docstring and markers stay non-seal."""
    import tests.architecture.test_ph_adversarial_boundary as mod

    text = mod.__doc__ or ""
    assert "NOT CLAIMED" in text or "NOT SEALED" in text or "RESEARCH" in text
    assert "PRODUCTION" in text.upper()
