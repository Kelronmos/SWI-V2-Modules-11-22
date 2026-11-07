from swi_v2.execution_integrity import (
    AdmittedRoute,
    ExecutionIntegrityGate,
    ExecutionRecord,
    IncomingNode,
    NewInformation,
    HumanAuthority,
    validate_human_authority,
    Decision,
)
import pytest


@pytest.fixture
def setup_gate():
    admitted = AdmittedRoute(
        "W-104", "R-abc", "N-7", "I-1", "P-22", "A-9"
    )
    last = ExecutionRecord(
        "E-103", "W-104", "N-7", "R-abc", "I-1", 10.0
    )
    node = IncomingNode(
        node_id="N-7",
        workflow_id="W-104",
        route_hash="R-abc",
        input_hash="I-1",
        policy_hash="P-22",
        admission_hash="A-9",
        current_time=10.0,
    )
    return admitted, last, node


def test_non_boundary_information_invalidates_execution(setup_gate):
    admitted, last, node = setup_gate
    gate = ExecutionIntegrityGate(admitted, last)

    assert gate.execute(node).decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1

    gate.apply_new_information(
        NewInformation(
            description="new information",
            affects_evidence_boundary=False,
            information_id="NI-NB",
        )
    )

    result = gate.execute(node)

    assert result.decision != Decision.EXECUTION_ALLOWED
    assert result.execution_occurred is False
    assert gate.execution_counter == 1


@pytest.mark.parametrize(
    "field,value",
    [
        ("proposed_policy_hash", "P-NEW"),
        ("proposed_route_hash", "R-NEW"),
        ("proposed_input_hash", "I-NEW"),
    ],
)
def test_proposed_hash_change_does_not_reuse_old_admission(
    setup_gate, field, value
):
    admitted, last, node = setup_gate
    gate = ExecutionIntegrityGate(admitted, last)

    assert gate.execute(node).decision == Decision.EXECUTION_ALLOWED

    info = NewInformation(
        description="proposed state change",
        affects_evidence_boundary=True,
        information_id="NI-HASH",
        **{field: value},
    )
    gate.apply_new_information(info, action_id="approve_file")

    authority = validate_human_authority(
        HumanAuthority(
            "H1", "W-104", "approve_file", "human-ok"
        ),
        workflow_id="W-104",
        action_id="approve_file",
    )

    result = gate.recheck(
        node,
        authority=authority,
        action_id="approve_file",
    )

    assert result.decision != Decision.EXECUTION_ALLOWED
    assert result.execution_occurred is False
    assert gate.execution_counter == 1
