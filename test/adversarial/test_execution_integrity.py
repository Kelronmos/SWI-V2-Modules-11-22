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
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    result = gate.check(node)
    assert result.decision == Decision.HALT
    assert FailureReason.ROUTE_CHANGED in result.reasons
    assert gate.execution_counter == 0


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
        execution_id="E-BAD", workflow_id="W-OTHER", node_id="N-7",
        route_hash="R-abc", input_hash="I-1", timestamp=10.0,
    )
    gate = ExecutionIntegrityGate(admitted, bad_last)
    result = gate.check(_matching_node(admitted))
    assert FailureReason.LAST_EXECUTION_MISMATCH in result.reasons
    assert gate.execution_counter == 0


def test_time_continuity_failure_halts(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, time_tolerance=0.0008)
    result = gate.check(_matching_node(admitted, t=10.0000 + 0.001))
    assert FailureReason.TIME_CONTINUITY_EXCEEDED in result.reasons
    assert gate.execution_counter == 0


def test_new_information_cannot_silently_change_admitted_route(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    poisoned = IncomingNode(
        node_id="N-7", workflow_id="W-104", route_hash="R-NEW",
        input_hash="I-NEW", policy_hash="P-22", admission_hash="A-9", current_time=10.0000,
    )
    result = gate.check(poisoned)
    assert result.decision == Decision.HALT
    assert FailureReason.ROUTE_CHANGED in result.reasons
    assert FailureReason.INPUT_CHANGED in result.reasons
    assert gate.execution_counter == 0
    assert admitted.route_hash == "R-abc"


def test_retry_does_not_grant_authority(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, max_retries=2)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    assert gate.check(node).decision == Decision.HALT
    assert gate.check(node, attempt_retry=True).decision == Decision.HALT
    assert gate.execution_counter == 0


def test_persistent_failure_escalates(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, max_retries=2)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    gate.check(node)
    gate.check(node, attempt_retry=True)
    r3 = gate.check(node, attempt_retry=True)
    assert r3.decision == Decision.ESCALATE
    assert gate.execution_counter == 0


def test_evidence_is_replayable_and_hashed(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    result = gate.check(node)
    assert len(result.evidence.evidence_hash) == 64


def test_admitted_route_immutable_under_poison(admitted, last_exec):
    original = copy.deepcopy(admitted)
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.route_hash = "R-POISON"
    gate.check(node)
    assert admitted.route_hash == original.route_hash


def test_direct_protected_operation_cannot_bypass_integrity_boundary(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 0


def test_execution_after_halt_is_blocked(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    result = gate.check(node)
    assert result.decision == Decision.HALT
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 0


def test_alternate_execution_path_cannot_bypass_integrity_gate(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    poison = IncomingNode(
        node_id="N-7", workflow_id="W-104", route_hash="R-NEW",
        input_hash="I-NEW", policy_hash="P-22", admission_hash="A-9", current_time=10.0000,
    )
    result = gate.execute(poison)
    assert result.decision == Decision.HALT
    assert gate.execution_counter == 0


def test_failed_integrity_check_never_reaches_protected_operation(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _matching_node(admitted)
    node.policy_hash = "P-EVIL"
    result = gate.check(node)
    assert result.decision == Decision.HALT
    assert gate.execution_counter == 0


def test_successful_integrity_check_reaches_protected_operation(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    result = gate.execute(_matching_node(admitted, t=10.0000))
    assert result.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1


def test_retry_cannot_execute_without_revalidation(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, max_retries=2)
    node = _matching_node(admitted)
    node.route_hash = "R-NEW"
    gate.check(node)
    r = gate.execute(node, attempt_retry=True)
    assert r.decision == Decision.HALT
    assert gate.execution_counter == 0


def test_forged_permit_is_rejected(admitted, last_exec):
    from swi_v2.execution_integrity import _ExecutionPermit
    gate = ExecutionIntegrityGate(admitted, last_exec)
    forged = _ExecutionPermit(gate_id=id(gate), nonce=999999)
    with pytest.raises(PermissionError):
        gate._demo_action(forged)
    assert gate.execution_counter == 0


def test_stale_permit_after_halt_is_rejected(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r1 = gate.check(_matching_node(admitted, t=10.0000))
    assert r1.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 1
