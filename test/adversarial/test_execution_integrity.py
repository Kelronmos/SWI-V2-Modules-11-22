"""
Adversarial tests for SWI Execution Integrity / Node Quarantine.

Evidence standard:
  CLAIM → INPUT → EXPECTED → ACTUAL → EVIDENCE → REPLAY → LIMITATION

Critical invariant:
  decision == HALT  AND  execution_counter remains 0  AND  evidence recorded.
"""
from __future__ import annotations

import copy
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
    FailureReason,
    IncomingNode,
    NodeState,
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
def last_exec() -> ExecutionRecord:
    return ExecutionRecord(
        execution_id="E-103",
        workflow_id="W-104",
        node_id="N-7",
        route_hash="R-abc",
        input_hash="I-1",
        timestamp=10.0000,
    )


def _matching_node(admitted: AdmittedRoute, t: float = 10.0000) -> IncomingNode:
    return IncomingNode(
        node_id=admitted.node_id,
        workflow_id=admitted.workflow_id,
        route_hash=admitted.route_hash,
        input_hash=admitted.input_hash,
        policy_hash=admitted.policy_hash,
        admission_hash=admitted.admission_hash,
        current_time=t,
    )


def test_matching_route_reaches_execution_boundary(admitted, last_exec):
    """CLAIM: unchanged admitted route may execute (harmless demo only)."""
    gate = ExecutionIntegrityGate(admitted, last_exec, time_tolerance=0.0008)
    node = _matching_node(admitted, t=10.0000)
    result = gate.check(node)

    assert result.decision == Decision.EXECUTION_ALLOWED
    assert result.execution_occurred is True
    assert gate.execution_counter == 1
    assert result.evidence.execution_allowed is True
    assert result.evidence.evidence_hash


def test_unapproved_node_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.node_id = "N-EVIL"
    result = gate.check(node)

    assert result.decision == Decision.HALT
    assert FailureReason.NODE_MISMATCH in result.reasons
    assert gate.execution_counter == 0
    assert result.execution_occurred is False
    assert result.evidence.execution_occurred is False


def test_node_identity_mismatch_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.node_id = "N-99"
    result = gate.check(node)
    assert result.decision == Decision.HALT
    assert gate.execution_counter == 0


def test_workflow_mismatch_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.workflow_id = "W-999"
    result = gate.check(node)
    assert FailureReason.WORKFLOW_MISMATCH in result.reasons
    assert gate.execution_counter == 0


def test_route_change_halts(admitted, last_exec):
    """Centrepiece: new information must not silently rewrite admitted route."""
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    result = gate.check(node)

    assert result.decision == Decision.HALT
    assert FailureReason.ROUTE_CHANGED in result.reasons
    assert gate.execution_counter == 0
    assert result.evidence.event == "EXECUTION_INTEGRITY_FAILURE"
    assert result.evidence.expected["route_hash"] == "R-abc"
    assert result.evidence.received["route_hash"] == "R-NEW"
    assert result.node_state == NodeState.HALTED


def test_input_change_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.input_hash = "I-NEW"
    result = gate.check(node)
    assert FailureReason.INPUT_CHANGED in result.reasons
    assert gate.execution_counter == 0


def test_policy_change_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.policy_hash = "P-EVIL"
    result = gate.check(node)
    assert FailureReason.POLICY_CHANGED in result.reasons
    assert gate.execution_counter == 0


def test_admission_change_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.admission_hash = "A-FAKE"
    result = gate.check(node)
    assert FailureReason.ADMISSION_MISMATCH in result.reasons
    assert gate.execution_counter == 0


def test_not_admitted_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.admission_hash = None
    result = gate.check(node)
    assert FailureReason.NOT_ADMITTED in result.reasons
    assert gate.execution_counter == 0


def test_last_execution_mismatch_halts(admitted):
    bad_last = ExecutionRecord(
        execution_id="E-BAD",
        workflow_id="W-OTHER",
        node_id="N-7",
        route_hash="R-abc",
        input_hash="I-1",
        timestamp=10.0,
    )
    gate = ExecutionIntegrityGate(admitted, bad_last)
    node = _matching_node(admitted)
    result = gate.check(node)
    assert FailureReason.LAST_EXECUTION_MISMATCH in result.reasons
    assert gate.execution_counter == 0


def test_time_continuity_failure_halts(admitted, last_exec):
    """0.0008 is experimental configured threshold only — not universal."""
    gate = ExecutionIntegrityGate(admitted, last_exec, time_tolerance=0.0008)
    node = _matching_node(admitted, t=10.0000 + 0.001)
    result = gate.check(node)
    assert FailureReason.TIME_CONTINUITY_EXCEEDED in result.reasons
    assert gate.execution_counter == 0


def test_new_information_cannot_silently_change_admitted_route(admitted, last_exec):
    """
    Critical attack: inject route+input change after admission, immediately
    before execution. SWI must detect, quarantine, halt, record, not execute.
    """
    gate = ExecutionIntegrityGate(admitted, last_exec)
    poisoned = IncomingNode(
        node_id="N-7",
        workflow_id="W-104",
        route_hash="R-NEW",
        input_hash="I-NEW",
        policy_hash="P-22",
        admission_hash="A-9",
        current_time=10.0000,
    )
    result = gate.check(poisoned)

    assert result.decision == Decision.HALT
    assert FailureReason.ROUTE_CHANGED in result.reasons
    assert FailureReason.INPUT_CHANGED in result.reasons
    assert gate.execution_counter == 0
    assert result.execution_occurred is False
    assert result.evidence.execution_occurred is False
    assert result.evidence.retry_required is True
    assert admitted.route_hash == "R-abc"
    assert admitted.input_hash == "I-1"


def test_retry_does_not_grant_authority(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, max_retries=2)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    r1 = gate.check(node)
    assert r1.decision == Decision.HALT
    assert gate.execution_counter == 0

    r2 = gate.check(node, attempt_retry=True)
    assert r2.decision == Decision.HALT
    assert gate.execution_counter == 0
    assert gate.retry_count == 1


def test_persistent_failure_escalates(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, max_retries=2)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"

    gate.check(node)
    gate.check(node, attempt_retry=True)
    r3 = gate.check(node, attempt_retry=True)

    assert r3.decision == Decision.ESCALATE
    assert FailureReason.RETRY_LIMIT_EXCEEDED in r3.reasons
    assert r3.evidence.escalated is True
    assert gate.execution_counter == 0
    assert r3.node_state == NodeState.ESCALATED


def test_evidence_is_replayable_and_hashed(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    result = gate.check(node)
    ev = result.evidence
    assert len(ev.evidence_hash) == 64
    assert ev.event == "EXECUTION_INTEGRITY_FAILURE"
    assert "ROUTE_CHANGED" in ev.reasons


def test_admitted_route_immutable_under_poison(admitted, last_exec):
    """Incoming data remains candidate; admitted object never rewritten."""
    original = copy.deepcopy(admitted)
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.route_hash = "R-POISON"
    gate.check(node)
    assert admitted.route_hash == original.route_hash
    assert admitted.identity_tuple() == original.identity_tuple()
