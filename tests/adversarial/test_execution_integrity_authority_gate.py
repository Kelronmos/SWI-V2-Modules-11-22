import pytest

from swi_v2.execution_integrity import (
    AdmittedRoute, Decision, ExecutionIntegrityGate, FailureReason,
    HumanAuthority, IncomingNode, NewInformation, ValidatedAuthority,
    validate_human_authority,
)

def case():
    admitted = AdmittedRoute(
        workflow_id="W-AUTH-1", route_hash="R-1", node_id="N-1",
        input_hash="I-1", policy_hash="P-1", admission_hash="A-1"
    )
    node = IncomingNode(
        node_id="N-1", workflow_id="W-AUTH-1", route_hash="R-1",
        input_hash="I-1", policy_hash="P-1", admission_hash="A-1",
        current_time=100.0
    )
    return node, ExecutionIntegrityGate(admitted)

def valid_authority(action="default_action"):
    return validate_human_authority(
        HumanAuthority(
            "H-TEST", workflow_id="W-AUTH-1",
            action_id=action, token="TEST-ONLY"
        ),
        workflow_id="W-AUTH-1", action_id=action
    )

def test_match_without_authority_is_unknown():
    node, gate = case()
    r = gate.execute(node)
    assert r.decision == Decision.UNKNOWN
    assert FailureReason.AUTHORITY_REQUIRED in r.reasons
    assert r.execution_occurred is False
    assert gate.execution_counter == 0
    assert gate._permit_nonce == 0
    assert len(r.evidence.evidence_hash) == 64

def test_match_with_authority_executes():
    node, gate = case()
    r = gate.execute(node, authority=valid_authority())
    assert r.decision == Decision.EXECUTION_ALLOWED
    assert r.execution_occurred is True
    assert gate.execution_counter == 1
    assert gate._bound_authority is None

def test_wrong_action_authority_blocked():
    node, gate = case()
    wrong = ValidatedAuthority(
        authority_id="H-WRONG", workflow_id="W-AUTH-1",
        action_id="delete_file", bound=True
    )
    r = gate.execute(node, authority=wrong, action_id="approve_file")
    assert r.decision == Decision.UNKNOWN
    assert FailureReason.AUTHORITY_INVALID in r.reasons
    assert gate.execution_counter == 0
    assert gate._permit_nonce == 0

def test_wrong_workflow_authority_blocked():
    node, gate = case()
    wrong = ValidatedAuthority(
        authority_id="H-WRONG", workflow_id="W-OTHER",
        action_id="default_action", bound=True
    )
    r = gate.execute(node, authority=wrong)
    assert r.decision == Decision.UNKNOWN
    assert gate.execution_counter == 0

def test_permit_mint_requires_authority():
    _, gate = case()
    with pytest.raises(PermissionError):
        gate._mint_permit()
    assert gate._permit_nonce == 0

def test_direct_demo_action_blocked():
    _, gate = case()
    with pytest.raises(PermissionError):
        gate._demo_action()
    assert gate.execution_counter == 0

def test_new_information_invalidates_authority():
    node, gate = case()
    r0 = gate.execute(node, authority=valid_authority())
    assert r0.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 1

    gate.apply_new_information(
        NewInformation(
            description="policy boundary changed",
            affects_evidence_boundary=True,
            information_id="NI-1"
        ),
        action_id="default_action"
    )
    assert gate._bound_authority is None

    blocked = gate.recheck(node, action_id="default_action")
    assert blocked.decision == Decision.UNKNOWN
    assert gate.execution_counter == 1

    resumed = gate.recheck(
        node, authority=valid_authority(), action_id="default_action"
    )
    assert resumed.decision == Decision.EXECUTION_ALLOWED
    assert gate.execution_counter == 2

def test_new_information_invalidates_old_permit():
    _, gate = case()
    gate.bind_authority(valid_authority(), action_id="default_action")
    permit = gate._mint_permit()
    gate.apply_new_information(
        NewInformation(
            description="boundary changed",
            affects_evidence_boundary=True,
            information_id="NI-2"
        ),
        action_id="default_action"
    )
    with pytest.raises(PermissionError):
        gate._demo_action(permit)
    assert gate.execution_counter == 0

def test_invalid_authority_does_not_fall_back_to_old_binding():
    node, gate = case()
    gate.bind_authority(valid_authority(), action_id="default_action")
    invalid = ValidatedAuthority(
        authority_id="H-INVALID", workflow_id="W-AUTH-1",
        action_id="other", bound=True
    )
    r = gate.execute(node, authority=invalid)
    assert r.decision == Decision.UNKNOWN
    assert FailureReason.AUTHORITY_INVALID in r.reasons
    assert gate.execution_counter == 0
