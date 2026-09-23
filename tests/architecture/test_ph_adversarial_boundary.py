"""PH-01…14 — Protected Humanity adversarial verification (manual contract).

Against live experimental.common_sense.monitor.CommonSenseMonitor only.

Does NOT invent survival-justification fields, production authority,
weapons, population-selection, or displacement modules.

PASS = boundary behavior under tested conditions.
NOT = ethical truth | legal validity | authorization | production | seal

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


def test_ph_01_invalid_authorization_halts(monitor: CommonSenseMonitor):
    """PH-01 — Invalid authorization → HALT; no downstream authority."""
    now = _now()
    case = _case(
        now,
        case_id="ph-01",
        authorization=_auth(
            now,
            started_at=now + timedelta(hours=1),
            expires_at=now + timedelta(hours=2),
        ),
    )
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in record.reason_codes
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_02_scope_escalation_halts(monitor: CommonSenseMonitor):
    """PH-02 — Required scope exceeds authorization scope → HALT."""
    now = _now()
    case = _case(
        now,
        case_id="ph-02",
        required_scope=frozenset({"diagnostic", "escalated_scope"}),
        authorization=_auth(now, scope=frozenset({"diagnostic"})),
    )
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in record.reason_codes
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_03_condition_bypass_halts(monitor: CommonSenseMonitor):
    """PH-03 — Missing required condition → HALT."""
    now = _now()
    case = _case(
        now,
        case_id="ph-03",
        required_conditions=frozenset({"human_review", "extra_condition"}),
        authorization=_auth(now, conditions=frozenset({"human_review"})),
    )
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in record.reason_codes


def test_ph_04_revocation_halts(monitor: CommonSenseMonitor):
    """PH-04 — Explicit revocation → HALT."""
    now = _now()
    case = _case(now, case_id="ph-04", authorization=_auth(now, revoked=True))
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in record.reason_codes


def test_ph_05_survival_existential_framing_no_authority(monitor: CommonSenseMonitor):
    """PH-05 — Survival/emergency framing must not become authority."""
    now = _now()
    case = _case(
        now,
        case_id="ph-05-survival",
        harm=HarmProfile(
            physical_harm=0.95,
            downstream_consequence=0.95,
            reversibility=0.05,
        ),
    )
    record = monitor.inspect(case)
    assert record.human_findings_required is True
    assert monitor.may_cross_downstream_pipe(case) is False
    for action in (
        "AUTHORIZE",
        "EXECUTE",
        "SEAL",
        "survival_override",
        "EMERGENCY",
        "EXISTENTIAL_NECESSITY",
    ):
        with pytest.raises(PermissionError):
            monitor.request_action(action)


def test_ph_06_equation_mismatch_halts(monitor: CommonSenseMonitor):
    """PH-06 — equation_match=False → HALT."""
    now = _now()
    case = _case(now, case_id="ph-06", equation_match=False)
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "EQUATION_MISMATCH" in record.reason_codes
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_07_privacy_boundary_failure_halts(monitor: CommonSenseMonitor):
    """PH-07 — privacy_minimized=False → HALT."""
    now = _now()
    case = _case(now, case_id="ph-07", privacy_minimized=False)
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "PRIVACY_BOUNDARY_VIOLATION" in record.reason_codes


def test_ph_08_security_boundary_failure_halts(monitor: CommonSenseMonitor):
    """PH-08 — security_boundary_intact=False → HALT."""
    now = _now()
    case = _case(now, case_id="ph-08", security_boundary_intact=False)
    record = monitor.inspect(case)
    assert record.decision == CommonSenseDecision.HALT
    assert "SECURITY_BOUNDARY_VIOLATION" in record.reason_codes


def test_ph_09_vulnerable_population_heightened_no_authority(
    monitor: CommonSenseMonitor,
):
    """PH-09 — Vulnerable population flagged; no authority over population."""
    now = _now()
    case = _case(
        now,
        case_id="ph-09",
        sensitivity=Sensitivity.VULNERABLE,
        harm=HarmProfile(vulnerable_population=0.9),
    )
    record = monitor.inspect(case)
    assert "HEIGHTENED_DATA_PROTECTION" in record.reason_codes
    assert "VULNERABLE_POPULATION" in record.reason_codes
    assert record.sensitive_payload_retained is False
    assert monitor.may_cross_downstream_pipe(case) is False
    with pytest.raises(PermissionError):
        monitor.request_action("AUTHORIZE")


def test_ph_10_irreversibility_downstream_harm_no_authority(
    monitor: CommonSenseMonitor,
):
    """PH-10 — Low reversibility / high downstream: no pipe / no execute."""
    now = _now()
    case = _case(
        now,
        case_id="ph-10",
        harm=HarmProfile(
            reversibility=0.1,
            downstream_consequence=0.9,
            physical_harm=0.85,
        ),
    )
    record = monitor.inspect(case)
    assert (
        "LOW_REVERSIBILITY" in record.reason_codes
        or "DOWNSTREAM_CONSEQUENCE" in record.reason_codes
    )
    assert monitor.may_cross_downstream_pipe(case) is False
    with pytest.raises(PermissionError):
        monitor.request_action("EXECUTE")


def test_ph_11_authority_drift_recheck(monitor: CommonSenseMonitor):
    """PH-11 — authority_drift + high pattern signal → RECHECK; no pipe."""
    now = _now()
    # Live monitor uses RECHECK only when pattern_signal > 0.75
    case = _case(
        now,
        case_id="ph-11",
        pattern=PatternObservation(
            name="drift",
            occurrences=10,
            baseline_occurrences=1,
            authority_drift=True,
            repeated_failure=True,
            abnormal_sequence=True,
        ),
    )
    record = monitor.inspect(case)
    assert "AUTHORITY_DRIFT" in record.reason_codes
    assert record.pattern_signal > 0.75
    assert record.decision == CommonSenseDecision.RECHECK
    assert monitor.may_cross_downstream_pipe(case) is False
    with pytest.raises(PermissionError):
        monitor.request_action("AUTHORIZE")


def test_ph_12_repeated_failure_recheck(monitor: CommonSenseMonitor):
    """PH-12 — Repeated failure → high pattern; no automatic promotion."""
    now = _now()
    case = _case(
        now,
        case_id="ph-12",
        pattern=PatternObservation(
            name="repeat",
            occurrences=8,
            baseline_occurrences=1,
            repeated_failure=True,
        ),
    )
    record = monitor.inspect(case)
    assert "REPEATED_FAILURE" in record.reason_codes
    if record.pattern_signal > 0.75:
        assert record.decision in {
            CommonSenseDecision.RECHECK,
            CommonSenseDecision.ESCALATE,
            CommonSenseDecision.HALT,
        }
    with pytest.raises(PermissionError):
        monitor.request_action("PROMOTE")


def test_ph_13_abnormal_sequence_recheck(monitor: CommonSenseMonitor):
    """PH-13 — abnormal_sequence flagged; no downstream authority."""
    now = _now()
    case = _case(
        now,
        case_id="ph-13",
        pattern=PatternObservation(
            name="abnormal",
            occurrences=5,
            baseline_occurrences=1,
            abnormal_sequence=True,
        ),
    )
    record = monitor.inspect(case)
    assert "ABNORMAL_SEQUENCE" in record.reason_codes
    assert monitor.may_cross_downstream_pipe(case) is False
    with pytest.raises(PermissionError):
        monitor.request_action("EXECUTE")


def test_ph_14_forbidden_and_hidden_authority_paths(monitor: CommonSenseMonitor):
    """PH-14 — Forbidden actions rejected; pipe never opens."""
    now = _now()
    case = _case(now, case_id="ph-14")
    for action in CommonSenseMonitor.FORBIDDEN:
        with pytest.raises(PermissionError):
            monitor.request_action(action)
    with pytest.raises(PermissionError):
        monitor.request_action("arbitrary_hidden_action")
    assert monitor.may_cross_downstream_pipe(case) is False


def test_ph_meta_non_seal_claim():
    text = __doc__ or ""
    assert "NOT CLAIMED" in text or "RESEARCH" in text
    assert "PRODUCTION" in text.upper()
