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


def make_authorization(
    *,
    now: datetime,
    revoked: bool = False,
    conditions=frozenset({"human_review"}),
):
    return AuthorizationContext(
        principal="research-human",
        scope=frozenset({"diagnostic"}),
        purpose="research",
        started_at=now - timedelta(minutes=5),
        expires_at=now + timedelta(minutes=5),
        conditions=conditions,
        revoked=revoked,
    )


def make_case(**overrides):
    now = datetime.now(timezone.utc)

    values = dict(
        case_id="CS-001",
        sensitivity=Sensitivity.PUBLIC,
        required_scope=frozenset({"diagnostic"}),
        required_conditions=frozenset({"human_review"}),
        now=now,
        authorization=make_authorization(now=now),
        harm=HarmProfile(),
        pattern=PatternObservation(name="baseline"),
        equation_match=True,
        privacy_minimized=True,
        security_boundary_intact=True,
    )

    values.update(overrides)
    return SimulationCase(**values)


def test_valid_low_risk_produces_evidence_without_authority():
    monitor = CommonSenseMonitor()

    evidence = monitor.inspect(make_case())

    assert evidence.decision is CommonSenseDecision.CONTINUE
    assert evidence.payload_retained is False
    assert evidence.sensitive_payload_retained is False
    assert evidence.human_findings_required is True


def test_sensitive_and_vulnerable_data_is_not_retained():
    monitor = CommonSenseMonitor()

    evidence = monitor.inspect(
        make_case(
            sensitivity=Sensitivity.VULNERABLE,
            harm=HarmProfile(vulnerable_population=1.0),
        )
    )

    assert evidence.payload_retained is False
    assert evidence.sensitive_payload_retained is False
    assert "HEIGHTENED_DATA_PROTECTION" in evidence.reason_codes


def test_privacy_boundary_violation_halts():
    monitor = CommonSenseMonitor()

    case = make_case(privacy_minimized=False)

    evidence = monitor.inspect(case)

    assert evidence.decision is CommonSenseDecision.HALT
    assert monitor.may_cross_downstream_pipe(case) is False


def test_security_boundary_violation_halts():
    monitor = CommonSenseMonitor()

    evidence = monitor.inspect(
        make_case(security_boundary_intact=False)
    )

    assert evidence.decision is CommonSenseDecision.HALT


def test_equation_mismatch_is_terminal():
    monitor = CommonSenseMonitor()

    case = make_case(equation_match=False)

    evidence = monitor.inspect(case)

    assert evidence.decision is CommonSenseDecision.HALT
    assert "EQUATION_MISMATCH" in evidence.reason_codes
    assert monitor.may_cross_downstream_pipe(case) is False


def test_expired_authorization_halts():
    monitor = CommonSenseMonitor()

    now = datetime.now(timezone.utc)

    authorization = AuthorizationContext(
        principal="research-human",
        scope=frozenset({"diagnostic"}),
        purpose="research",
        started_at=now - timedelta(hours=2),
        expires_at=now - timedelta(hours=1),
        conditions=frozenset({"human_review"}),
    )

    evidence = monitor.inspect(
        make_case(
            now=now,
            authorization=authorization,
        )
    )

    assert evidence.decision is CommonSenseDecision.HALT
    assert "AUTHORIZATION_INVALID" in evidence.reason_codes


def test_revoked_authorization_halts():
    monitor = CommonSenseMonitor()

    now = datetime.now(timezone.utc)

    evidence = monitor.inspect(
        make_case(
            authorization=make_authorization(
                now=now,
                revoked=True,
            )
        )
    )

    assert evidence.decision is CommonSenseDecision.HALT


def test_missing_authorization_condition_halts():
    monitor = CommonSenseMonitor()

    now = datetime.now(timezone.utc)

    authorization = make_authorization(
        now=now,
        conditions=frozenset(),
    )

    evidence = monitor.inspect(
        make_case(
            now=now,
            authorization=authorization,
            required_conditions=frozenset({"human_review"}),
        )
    )

    assert evidence.decision is CommonSenseDecision.HALT


def test_pattern_analysis_detects_repeated_failure_and_authority_drift():
    monitor = CommonSenseMonitor()

    case = make_case(
        pattern=PatternObservation(
            name="authority-drift",
            occurrences=10,
            baseline_occurrences=10,
            authority_drift=True,
            repeated_failure=True,
            abnormal_sequence=True,
        )
    )

    evidence = monitor.inspect(case)

    assert evidence.pattern_signal > 0.75
    assert evidence.decision is CommonSenseDecision.RECHECK
    assert "AUTHORITY_DRIFT" in evidence.reason_codes
    assert "REPEATED_FAILURE" in evidence.reason_codes


def test_risk_weights_include_irreversibility_and_downstream_harm():
    monitor = CommonSenseMonitor()

    case = make_case(
        harm=HarmProfile(
            reversibility=0.0,
            downstream_consequence=1.0,
        )
    )

    score = monitor.risk_score(case)

    assert score >= 3.5


def test_waiting_risk_escalates_without_authorizing_action():
    monitor = CommonSenseMonitor()

    case = make_case(
        harm=HarmProfile(
            physical_harm=0.9,
            downstream_consequence=0.9,
            reversibility=0.1,
        )
    )

    evidence = monitor.inspect(case)

    assert evidence.decision is CommonSenseDecision.ESCALATE
    assert "DELAY_MAY_INCREASE_HARM" in evidence.reason_codes
    assert monitor.may_cross_downstream_pipe(case) is False


@pytest.mark.parametrize(
    "action",
    [
        "EXECUTE",
        "PROMOTE",
        "SEAL",
        "AUTHORIZE",
        "EXTEND_AUTHORIZATION",
        "RENEW_AUTHORIZATION",
    ],
)
def test_common_sense_cannot_assume_authority(action):
    monitor = CommonSenseMonitor()

    with pytest.raises(PermissionError):
        monitor.request_action(action)


def test_non_forbidden_action_still_has_no_action_interface():
    monitor = CommonSenseMonitor()

    with pytest.raises(PermissionError):
        monitor.request_action("DO_SOMETHING")


def test_terminal_case_cannot_become_replay_chain():
    monitor = CommonSenseMonitor()

    case = make_case(equation_match=False)

    evidence = monitor.inspect(case)

    assert evidence.decision is CommonSenseDecision.HALT
    assert monitor.may_cross_downstream_pipe(case) is False
