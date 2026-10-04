"""Adversarial attacks on new-information evidence boundary."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_v2.execution_integrity import (
    AdmittedRoute,
    Decision,
    ExecutionIntegrityGate,
    ExecutionRecord,
    HumanAuthority,
    IncomingNode,
    NewInformation,
    validate_human_authority,
)


@pytest.fixture
def admitted():
    return AdmittedRoute("W-104", "R-abc", "N-7", "I-1", "P-22", "A-9")


@pytest.fixture
def last_exec():
    return ExecutionRecord("E-103", "W-104", "N-7", "R-abc", "I-1", 10.0)


def _node(admitted, **kw):
    d = dict(
        node_id=admitted.node_id,
        workflow_id=admitted.workflow_id,
        route_hash=admitted.route_hash,
        input_hash=admitted.input_hash,
        policy_hash=admitted.policy_hash,
        admission_hash=admitted.admission_hash,
        current_time=10.0,
    )
    d.update(kw)
    return IncomingNode(**d)


def test_human_yes_string_is_not_authority(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    gate.execute(_node(admitted))
    gate.apply_new_information(
        NewInformation(description="boundary shift", affects_evidence_boundary=True, information_id="NI-YES"),
        action_id="approve_file",
    )
    r = gate.recheck(_node(admitted), action_id="approve_file")
    assert r.decision == Decision.UNKNOWN
    assert r.execution_occurred is False
    assert gate.execution_counter == 1


def test_authority_different_action_blocked(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    gate.execute(_node(admitted))
    gate.apply_new_information(
        NewInformation(description="x", affects_evidence_boundary=True, information_id="NI-ACT"),
        action_id="approve_file",
    )
    with pytest.raises(ValueError):
        validate_human_authority(
            HumanAuthority("H1", workflow_id="W-104", action_id="delete_file", token="tok"),
            workflow_id="W-104",
            action_id="approve_file",
        )
    r = gate.recheck(_node(admitted), action_id="approve_file")
    assert r.decision == Decision.UNKNOWN
    assert gate.execution_counter == 1


def test_execute_while_unknown_blocked(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    gate.execute(_node(admitted))
    r0 = gate.apply_new_information(
        NewInformation(description="x", affects_evidence_boundary=True, information_id="NI-U"),
        action_id="approve_file",
    )
    assert r0.decision == Decision.UNKNOWN
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.UNKNOWN
    assert r.execution_occurred is False
    assert gate.execution_counter == 1


def test_stale_pass_after_boundary_change_cannot_execute(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    assert gate.execute(_node(admitted)).decision == Decision.EXECUTION_ALLOWED
    gate.apply_new_information(
        NewInformation(description="authority-relevant", affects_evidence_boundary=True, information_id="NI-E"),
        action_id="approve_file",
    )
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.UNKNOWN
    assert r.evidence.execution_allowed is False
    assert r.execution_occurred is False


def test_direct_demo_action_while_unknown(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    gate.execute(_node(admitted))
    gate.apply_new_information(
        NewInformation(description="x", affects_evidence_boundary=True, information_id="NI-D"),
        action_id="approve_file",
    )
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 1
