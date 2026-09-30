"""Gate PASS/FAIL matrix — decision + downstream no-execution on FAIL."""
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


def _assert_halt(gate, result, code=None):
    assert result.decision == Decision.HALT
    assert result.execution_occurred is False
    assert result.evidence.execution_allowed is False
    assert gate.execution_counter == 0
    if code is not None:
        assert code in result.reasons


def test_gate_execution_pass(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1


@pytest.mark.parametrize(
    "field,value,code",
    [
        ("admission_hash", None, FailureReason.NOT_ADMITTED),
        ("node_id", "N-EVIL", FailureReason.NODE_MISMATCH),
        ("workflow_id", "W-BAD", FailureReason.WORKFLOW_MISMATCH),
        ("route_hash", "R-NEW", FailureReason.ROUTE_CHANGED),
        ("input_hash", "I-NEW", FailureReason.INPUT_CHANGED),
        ("policy_hash", "P-EVIL", FailureReason.POLICY_CHANGED),
        ("admission_hash", "A-FAKE", FailureReason.ADMISSION_MISMATCH),
    ],
)
def test_gate_fail_halts_no_execution(admitted, last_exec, field, value, code):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    node = _node(admitted, **{field: value})
    r = gate.check(node)
    _assert_halt(gate, r, code)
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 0


def test_continuity_fail(admitted):
    bad = ExecutionRecord("E-BAD", "W-OTHER", "N-7", "R-abc", "I-1", 10.0)
    gate = ExecutionIntegrityGate(admitted, bad)
    r = gate.check(_node(admitted))
    _assert_halt(gate, r, FailureReason.LAST_EXECUTION_MISMATCH)


def test_halt_then_execute_blocked(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.check(_node(admitted, route_hash="R-NEW"))
    _assert_halt(gate, r)
    r2 = gate.execute(_node(admitted, route_hash="R-NEW"), attempt_retry=True)
    assert r2.decision == Decision.HALT
    assert gate.execution_counter == 0


def test_retry_without_revalidation_no_execution(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, max_retries=2)
    node = _node(admitted, route_hash="R-NEW")
    gate.check(node)
    r = gate.execute(node, attempt_retry=True)
    assert r.decision == Decision.HALT
    assert gate.execution_counter == 0


def test_persistent_fail_escalates_no_execution(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec, max_retries=2)
    node = _node(admitted, route_hash="R-NEW")
    gate.check(node)
    gate.check(node, attempt_retry=True)
    r = gate.check(node, attempt_retry=True)
    assert r.decision == Decision.ESCALATE
    assert gate.execution_counter == 0


def test_mutation_gate(admitted, last_exec):
    original = copy.deepcopy(admitted)
    gate = ExecutionIntegrityGate(admitted, last_exec)
    gate.check(_node(admitted, route_hash="R-POISON"))
    assert admitted.route_hash == original.route_hash
    assert gate.execution_counter == 0


def test_authorization_forged_permit(admitted, last_exec):
    from swi_v2.execution_integrity import _ExecutionPermit

    gate = ExecutionIntegrityGate(admitted, last_exec)
    with pytest.raises(PermissionError):
        gate._demo_action(_ExecutionPermit(id(gate), 999))
    assert gate.execution_counter == 0
