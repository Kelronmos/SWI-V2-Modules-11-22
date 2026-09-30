"""Universal HALT error contract + mapping from execution integrity."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_v2.kernel.halt import HaltRecord, HaltedWorkflow
from swi_v2.kernel.enforcement import halt, require_admitted
from swi_v2.kernel.errors import StateTransitionError
from swi_v2.execution_integrity import (
    AdmittedRoute,
    Decision,
    ExecutionIntegrityGate,
    ExecutionRecord,
    IncomingNode,
)


def test_halt_record_blocks_may_execute():
    hw = halt("test", "ROUTE_CHANGED", "CHECK_PIPE", workflow_id="W-104")
    assert hw.may_execute() is False
    assert hw.state == "HALTED"
    assert hw.record.execution_allowed is False


def test_halt_record_serializable_and_hashed():
    rec = HaltRecord(
        module="execution_integrity",
        reason_code="ROUTE_CHANGED",
        stage="CHECK_PIPE",
        workflow_id="W-104",
        route_id="R-abc",
        node_id="N-7",
        expected_state={"route_hash": "R-abc"},
        received_state={"route_hash": "R-NEW"},
        execution_allowed=False,
        execution_occurred=False,
    ).with_evidence_hash()
    d = rec.to_dict()
    assert d["decision"] == "HALT"
    assert d["execution_allowed"] is False
    assert d["execution_occurred"] is False
    assert len(d["evidence_hash"]) == 64
    rec2 = HaltRecord(
        module="execution_integrity",
        reason_code="ROUTE_CHANGED",
        stage="CHECK_PIPE",
        workflow_id="W-104",
        route_id="R-abc",
        node_id="N-7",
        expected_state={"route_hash": "R-abc"},
        received_state={"route_hash": "R-NEW"},
        execution_allowed=False,
        execution_occurred=False,
        timestamp=rec.timestamp,
    ).with_evidence_hash()
    assert rec2.evidence_hash == rec.evidence_hash


def test_require_admitted_blocks_halted_workflow():
    hw = halt("test", "NOT_ADMITTED", "ADMISSION")
    with pytest.raises(StateTransitionError):
        require_admitted(hw, module="test")


def test_integrity_halt_maps_to_common_record():
    admitted = AdmittedRoute("W-104", "R-abc", "N-7", "I-1", "P-22", "A-9")
    last = ExecutionRecord("E-103", "W-104", "N-7", "R-abc", "I-1", 10.0)
    gate = ExecutionIntegrityGate(admitted, last)
    node = IncomingNode("N-7", "W-104", "R-NEW", "I-1", "P-22", "A-9", 10.0)
    result = gate.check(node)
    assert result.decision == Decision.HALT
    assert gate.execution_counter == 0
    rec = gate.to_halt_record(result)
    assert rec.reason_code == "ROUTE_CHANGED"
    assert rec.execution_allowed is False
    assert rec.execution_occurred is False
    assert rec.decision == "HALT"
    assert len(rec.evidence_hash) == 64
    hw = gate.to_halted_workflow(result)
    assert hw.may_execute() is False


def test_positive_path_still_executes():
    admitted = AdmittedRoute("W-104", "R-abc", "N-7", "I-1", "P-22", "A-9")
    last = ExecutionRecord("E-103", "W-104", "N-7", "R-abc", "I-1", 10.0)
    gate = ExecutionIntegrityGate(admitted, last)
    node = IncomingNode("N-7", "W-104", "R-abc", "I-1", "P-22", "A-9", 10.0)
    result = gate.execute(node)
    assert result.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1
