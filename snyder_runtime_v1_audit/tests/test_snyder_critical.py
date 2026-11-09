import inspect
import pytest

from swi_v2.kernel.authority import (
    AuthorityLayer,
    require_authorization_for_action,
    scan_undeclared_authority,
    layer_non_implication_matrix,
)
from swi_v2.kernel.admission import (
    admit_foundation_input,
    compute_integrity_reference,
)
from swi_v2.kernel.enforcement import require_admitted, halt
from swi_v2.kernel.errors import (
    AuthorityError,
    AuthorityHalt,
    ModuleKernelError,
    StateTransitionError,
)
from swi_v2.kernel.contracts import AdmittedInput
from swi_v2.module12 import process
from swi_v2.s9.evaluator import evaluate_s9
from swi_v2.s9.replay import replay_evaluate


def valid_envelope():
    payload = {"allowed": True, "reason": None}
    e = {
        "payload": payload,
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "snyder-critical-fixture",
        "verification_status": "foundation_verified_test_fixture",
        "source_reference": "local-test",
    }
    e["integrity_reference"] = compute_integrity_reference(
        payload,
        e["foundation_version"],
        e["evidence_schema_version"],
        e["evidence_id"],
        e["source_reference"],
    )
    return e


def test_sny_001_raw_input_rejected():
    with pytest.raises(ModuleKernelError):
        require_admitted({"payload": {}}, module="snyder")


def test_sny_002_authority_laundering_rejected():
    d = scan_undeclared_authority(
        {"trusted": True, "authority": "system"},
        layer=AuthorityLayer.DATA,
    )
    assert d.allowed is False
    assert set(d.rejected_fields) == {"trusted", "authority"}
    assert d.next_state == "REJECT"


def test_sny_003_layer_non_implication():
    m = layer_non_implication_matrix()
    assert "authorization" in m["admission"]
    assert "action" in m["admission"]


def test_sny_004_missing_authority_halts():
    with pytest.raises(AuthorityHalt):
        require_authorization_for_action(
            authorization_present=False,
            authorization_scope=None,
            requested_action="transfer",
        )


def test_sny_005_empty_scope_is_not_unrestricted():
    # Snyder requirement: empty declared scopes must not become a wildcard.
    with pytest.raises(AuthorityError):
        require_authorization_for_action(
            authorization_present=True,
            authorization_scope="transfer",
            requested_action="transfer",
            declared_scopes=(),
        )


def test_sny_006_scope_mismatch_rejected():
    with pytest.raises(AuthorityError):
        require_authorization_for_action(
            authorization_present=True,
            authorization_scope="read",
            requested_action="transfer",
            declared_scopes=("read",),
        )


def test_sny_007_valid_explicit_scope_accepted():
    d = require_authorization_for_action(
        authorization_present=True,
        authorization_scope="transfer",
        requested_action="transfer",
        declared_scopes=("transfer",),
    )
    assert d.allowed is True


def test_sny_008_authority_envelope_contract_exists():
    from swi_v2 import kernel
    assert hasattr(kernel, "AuthorityEnvelope")


def test_sny_009_expiry_is_bound_to_authorization():
    params = inspect.signature(
        require_authorization_for_action
    ).parameters
    assert "t_expiry" in params or "expires_at" in params


def test_sny_010_corridor_is_bound_to_authorization():
    params = inspect.signature(
        require_authorization_for_action
    ).parameters
    assert "corridor_id" in params


def test_sny_011_tampered_evidence_rejected():
    e = valid_envelope()
    admit_foundation_input(e)

    e["payload"]["allowed"] = False

    with pytest.raises(Exception):
        admit_foundation_input(e)


def test_sny_012_admission_is_not_action_authorization():
    admitted = admit_foundation_input(valid_envelope())
    assert isinstance(admitted, AdmittedInput)

    with pytest.raises((AuthorityError, AuthorityHalt, ModuleKernelError)):
        require_authorization_for_action(
            authorization_present=bool(admitted),
            authorization_scope=None,
            requested_action="transfer",
            declared_scopes=(),
        )


def test_sny_013_module12_normalization_implemented():
    result = process(admit_foundation_input(valid_envelope()))
    assert result.get("status") != "accepted_placeholder"


def test_sny_014_halt_blocks_admission_path():
    stopped = halt("snyder", "TEST_HALT", "critical")

    assert stopped.state == "HALTED"
    assert stopped.may_execute() is False

    with pytest.raises(StateTransitionError):
        require_admitted(stopped, module="snyder")


def test_sny_015_durable_decision_receipt_exists():
    from swi_v2 import kernel
    assert hasattr(kernel, "DecisionReceipt")


def test_sny_016_execution_ledger_precondition_exists():
    from swi_v2 import kernel
    assert (
        hasattr(kernel, "ExecutionLedger")
        or hasattr(kernel, "verify_ledger_chain")
    )


def test_sny_017_rollback_and_stop_right_binding_exists():
    from swi_v2 import kernel
    assert hasattr(kernel, "AuthorityEnvelope")


def test_sny_018_first_class_escalation_exists():
    from swi_v2 import kernel
    assert (
        hasattr(kernel, "ESCALATE")
        or hasattr(kernel, "EscalationDecision")
    )


def test_sny_019_s9_replay_scope_is_reported_correctly():
    original = evaluate_s9({"action": "audit"})
    result = replay_evaluate(
        {"action": "audit"},
        original.to_dict(),
    )
    assert result["replay_scope"] == "in-process pure function only"
    assert result["DURABLE_REPLAY"] == "NOT IMPLEMENTED"


def test_sny_020_module12_placeholder_is_not_misrepresented():
    source = inspect.getsource(process)
    assert (
        "accepted_placeholder" in source
        or "DESIGN PENDING" in source
    )
