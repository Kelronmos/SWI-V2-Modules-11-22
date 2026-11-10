"""Adversarial: MATCH alone must not authorize execute (HA-before-execute).

Library-level only. Does not claim production authorization.
"""
from __future__ import annotations

import pytest

from swi_v2.execution_integrity import (
    AdmittedRoute,
    Decision,
    ExecutionIntegrityGate,
    ExecutionRecord,
    FailureReason,
    HumanAuthority,
    IncomingNode,
    validate_human_authority,
)


@pytest.fixture
def admitted() -> AdmittedRoute:
    return AdmittedRoute(
        workflow_id="W-104",
        route_hash="R-abc",
        node_id="N-7",
        input_hash="I-1",
        policy_hash="P-22",
        admission_hash="A-9",
    )


@pytest.fixture
def last_exec(admitted) -> ExecutionRecord:
    return ExecutionRecord("E-103", admitted.workflow_id, admitted.node_id, admitted.route_hash, admitted.input_hash, 10.0)


def _node(admitted: AdmittedRoute) -> IncomingNode:
    return IncomingNode(
        node_id=admitted.node_id,
        workflow_id=admitted.workflow_id,
        route_hash=admitted.route_hash,
        input_hash=admitted.input_hash,
        policy_hash=admitted.policy_hash,
        admission_hash=admitted.admission_hash,
        current_time=10.0,
    )


def test_match_without_human_authority_does_not_execute(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.UNKNOWN
    assert FailureReason.AUTHORITY_REQUIRED in r.reasons
    assert r.execution_occurred is False
    assert gate.execution_counter == 0


def test_match_with_bound_authority_may_execute(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    auth = validate_human_authority(
        HumanAuthority("H1", admitted.workflow_id, "default_action", "tok"),
        workflow_id=admitted.workflow_id,
        action_id="default_action",
    )
    gate.bind_authority(auth, action_id="default_action")
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.EXECUTION_ALLOWED
    assert r.execution_occurred is True
    assert gate.execution_counter == 1


def test_wrong_action_authority_does_not_execute(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    auth = validate_human_authority(
        HumanAuthority("H1", admitted.workflow_id, "other_action", "tok"),
        workflow_id=admitted.workflow_id,
        action_id="other_action",
    )
    gate.bind_authority(auth, action_id="other_action")
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.UNKNOWN
    assert FailureReason.AUTHORITY_INVALID in r.reasons
    assert r.execution_occurred is False
    assert gate.execution_counter == 0
    gate2 = ExecutionIntegrityGate(admitted, last_exec)
    with pytest.raises(ValueError):
        validate_human_authority(
            HumanAuthority("H1", "W-OTHER", "default_action", "tok"),
            workflow_id=admitted.workflow_id,
            action_id="default_action",
        )


def test_internal_permit_is_not_human_authority(admitted, last_exec):
    from swi_v2.execution_integrity import _ExecutionPermit

    gate = ExecutionIntegrityGate(admitted, last_exec)
    with pytest.raises(PermissionError):
        gate._demo_action(_ExecutionPermit(id(gate), 1))
    assert gate.execution_counter == 0
