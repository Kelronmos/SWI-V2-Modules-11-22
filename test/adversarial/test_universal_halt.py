"""Universal HALT mapping for execution integrity."""
from __future__ import annotations

from swi_v2.execution_integrity import (
    HumanAuthority,
    validate_human_authority,
)

def _bind_default(gate, admitted, action_id="default_action"):
    ha = HumanAuthority(
        authority_id="AUTH-TEST",
        workflow_id=admitted.workflow_id,
        action_id=action_id,
        token="tok-test",
    )
    gate.bind_authority(
        validate_human_authority(ha, workflow_id=admitted.workflow_id, action_id=action_id),
        action_id=action_id,
    )

import pytest
from swi_v2.execution_integrity import (
    AdmittedRoute,
    Decision,
    ExecutionIntegrityGate,
    ExecutionRecord,
    FailureReason,
    IncomingNode,
)
from swi_v2.kernel.halt import HaltRecord


@pytest.fixture
def admitted():
    return AdmittedRoute(
        workflow_id="W-104",
        route_hash="R-abc",
        node_id="N-7",
        input_hash="I-1",
        policy_hash="P-22",
        admission_hash="A-9",
    )


@pytest.fixture
def last():
    return ExecutionRecord(
        execution_id="E-103",
        workflow_id="W-104",
        node_id="N-7",
        route_hash="R-abc",
        input_hash="I-1",
        timestamp=10.0,
    )


def test_positive_path_still_executes(admitted, last):
    gate = ExecutionIntegrityGate(admitted, last)
    _bind_default(gate, admitted)
    node = IncomingNode("N-7", "W-104", "R-abc", "I-1", "P-22", "A-9", 10.0)
    result = gate.execute(node)
    assert result.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1


def test_halt_maps_to_halt_record(admitted, last):
    gate = ExecutionIntegrityGate(admitted, last)
    _bind_default(gate, admitted)
    node = IncomingNode("N-EVIL", "W-104", "R-abc", "I-1", "P-22", "A-9", 10.0)
    result = gate.execute(node)
    assert result.decision == Decision.HALT
    rec = gate.to_halt_record(result)
    assert isinstance(rec, HaltRecord)
    assert rec.execution_occurred is False
