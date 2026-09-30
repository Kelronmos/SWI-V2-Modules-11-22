"""SWI Gate PASS/FAIL system-error tests.

For each IMPLEMENTED gate:
  PASS path → may continue / execute when all match
  FAIL path → HALT + evidence + execution_counter==0 + no protected op

Critical: decision layer != execution enforcement.
Do not invent gates that are NOT_PRESENT in the repository.
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
from swi_v2.kernel.enforcement import halt, require_admitted
from swi_v2.kernel.errors import StateTransitionError


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


def _assert_no_execution(gate, result, code=None):
    """Downstream consequence of FAIL — not just return value."""
    assert result.decision in (Decision.HALT, Decision.ESCALATE)
    assert result.execution_occurred is False
    assert result.evidence.execution_allowed is False
    assert gate.execution_counter == 0
    assert result.evidence.evidence_hash
    assert len(result.evidence.evidence_hash) == 64
    if code is not None:
        assert code in result.reasons
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 0


def test_gate_execution_pass(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    assert gate.node_state == NodeState.QUARANTINED
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.EXECUTION_ALLOWED
    assert r.execution_occurred is True
    assert gate.execution_counter == 1
    assert r.evidence.evidence_hash


@pytest.mark.parametrize(
    "gate_name,field,value,code",
    [
        ("Admission", "admission_hash", None, FailureReason.NOT_ADMITTED),
        ("Admission", "admission_hash", "A-FAKE", FailureReason.ADMISSION_MISMATCH),
        ("Node", "node_id", "N-EVIL", FailureReason.NODE_MISMATCH),
        ("Identity", "workflow_id", "W-BAD", FailureReason.WORKFLOW_MISMATCH),
        ("Route", "route_hash", "R-NEW", FailureReason.ROUTE_CHANGED),
        ("Input", "input_hash", "I-NEW", FailureReason.INPUT_CHANGED),
        ("Policy", "policy_hash", "P-EVIL", FailureReason.POLICY_CHANGED),
    ],
)
def test_gate_fail_halts_no_execution(admitted, last_exec, gate_name, field, value, code):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.check(_node(admitted, **{field: value}))
    _assert_no_execution(gate, r, code)


def test_continuity_fail_no_execution(admitted):
    bad = ExecutionRecord("E-BAD", "W-OTHER", "N-7", "R-abc", "I-1", 10.0)
    gate = ExecutionIntegrityGate(admitted, bad)
    r = gate.check(_node(admitted))
    _assert_no_execution(gate, r, FailureReason.LAST_EXECUTION_MISMATCH)


def test_new_information_fail_no_execution(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.check(_node(admitted, route_hash="R-NEW", input_hash="I-NEW"))
    _assert_no_execution(gate, r)
    assert FailureReason.ROUTE_CHANGED in r.reasons
    assert FailureReason.INPUT_CHANGED in r.reasons


def test_chain_pass_then_route_fail_no_execution(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.check(_node(admitted, route_hash="R-POISON"))
    _assert_no_execution(gate, r, FailureReason.ROUTE_CHANGED)
    r2 = gate.execute(_node(admitted, route_hash="R-POISON"))
    assert r2.decision == Decision.HALT
    assert gate.execution_counter == 0


def test_halt_then_retry_execute_without_revalidation(admitted, last_exec):
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
    assert r.evidence.escalated is True


def test_fail_then_pass_requires_new_check(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    gate.check(_node(admitted, route_hash="R-NEW"))
    assert gate.execution_counter == 0
    r = gate.execute(_node(admitted))
    assert r.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1


def test_authorization_forged_permit_no_execution(admitted, last_exec):
    from swi_v2.execution_integrity import _ExecutionPermit

    gate = ExecutionIntegrityGate(admitted, last_exec)
    with pytest.raises(PermissionError):
        gate._demo_action(_ExecutionPermit(id(gate), 999))
    assert gate.execution_counter == 0


def test_authorization_direct_call_no_execution(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 0


def test_mutation_gate_admitted_immutable(admitted, last_exec):
    original = copy.deepcopy(admitted)
    gate = ExecutionIntegrityGate(admitted, last_exec)
    gate.check(_node(admitted, route_hash="R-POISON"))
    assert admitted.route_hash == original.route_hash
    assert gate.execution_counter == 0
    with pytest.raises(Exception):
        admitted.route_hash = "R-MUTATED"  # type: ignore[misc]


def test_evidence_gate_on_halt(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.check(_node(admitted, route_hash="R-NEW"))
    assert r.evidence.event == "EXECUTION_INTEGRITY_FAILURE"
    assert r.evidence.expected["route_hash"] == "R-abc"
    assert r.evidence.received["route_hash"] == "R-NEW"
    assert len(r.evidence.evidence_hash) == 64
    hr = gate.to_halt_record(r)
    assert hr.execution_allowed is False
    assert hr.execution_occurred is False
    assert len(hr.evidence_hash) == 64


def test_evidence_gate_on_pass(admitted, last_exec):
    gate = ExecutionIntegrityGate(admitted, last_exec)
    r = gate.execute(_node(admitted))
    assert r.evidence.event == "EXECUTION_INTEGRITY_PASS"
    assert len(r.evidence.evidence_hash) == 64


def test_kernel_halted_workflow_blocks_require_admitted():
    hw = halt("test", "ROUTE_CHANGED", "CHECK_PIPE", workflow_id="W-104")
    assert hw.may_execute() is False
    with pytest.raises(StateTransitionError):
        require_admitted(hw, module="test")


def test_report_gate_generator_runs():
    from swi_v2.reports.test_report import TestReportBuilder, TestResultRecord, write_reports
    import tempfile

    b = TestReportBuilder(report_type="gate_matrix_selfcheck", root=ROOT)
    b.set_command("pytest test/adversarial/test_gate_pass_fail_matrix.py")
    b.add_test(
        TestResultRecord(
            test_id="self",
            test_name="report_gate_smoke",
            status="PASS",
            expected_decision="HALT",
            actual_decision="HALT",
            actual_execution_occurred=False,
        )
    )
    with tempfile.TemporaryDirectory() as td:
        paths = write_reports(b, Path(td))
        assert paths["json"].exists()
        assert paths["md"].exists()
        assert paths["sha256"].exists()
        assert len(paths["sha256"].read_text().strip()) == 64
