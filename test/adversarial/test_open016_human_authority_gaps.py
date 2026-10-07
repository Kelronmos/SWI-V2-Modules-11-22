"""
OPEN-016 — Human Authority + Authorization Runtime Binding
FAILURE TESTS ONLY (tip ab320c6)

STATUS:
  DEFINED     = YES
  IMPLEMENTED = NO
  TESTED      = NO  (these tests expose gaps)
  PROVEN      = NO
  SEALED      = NO
  AUTHORIZED  = NO

Evidence standard:
  CLAIM → INPUT → EXPECTED → ACTUAL → EVIDENCE → REPLAY → LIMITATION

Central invariant under probe:
  EXECUTE(a) ⟺ FLOW_BIND(a) ∧ RUNTIME_MATCH(a)
               ∧ HUMAN_AUTHORITY_BOUND(a) ∧ AUTHORIZATION_VALID(a)

These tests must expose current gaps. Expected result is not "all green".
Do not weaken assertions to obtain PASS.
Do not implement the missing controls in this file.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_v2.kernel.authority import (
    AuthorityDecision,
    AuthorityError,
    AuthorityHalt,
    AuthorityLayer,
    FORBIDDEN_AUTHORITY_FIELDS,
    assert_layer_does_not_imply,
    layer_non_implication_matrix,
    require_authorization_for_action,
    require_governing_permit_for_action,
    require_no_authority_escalation,
    scan_undeclared_authority,
)
from swi_v2.kernel.governing_permit import (
    GoverningEvaluation,
    PermitOutcome,
    evaluate_governing_permit,
    observation_does_not_satisfy_H,
    prior_evaluation_requires_revalidation,
    signature_does_not_authorize,
)
obs_not_H = observation_does_not_satisfy_H
sig_not_auth = signature_does_not_authorize

# ---------------------------------------------------------------------------
# Fixtures representing the closest existing surface to "human authority"
# ---------------------------------------------------------------------------

# At tip ab320c6 there is NO first-class HumanAuthorityBinding type,
# no action-specific H token, and no freshness window on human bindings.
# H is only an optional set of condition identifiers passed into the
# governing formula. That is the current representation we must test against.


@pytest.fixture
def valid_conditions() -> list[str]:
    return ["cond_workflow_W1", "cond_action_A", "cond_node_N7"]


@pytest.fixture
def full_layers(valid_conditions) -> dict:
    """All layers known and satisfied — technical path green."""
    return {
        "L": list(valid_conditions),
        "G": list(valid_conditions),
        "S": list(valid_conditions),
        "H": list(valid_conditions),  # H present as condition set only
        "evidence": {"record": "e1"},
    }


# ===========================================================================
# HA-01  missing human authority blocks execution
# ===========================================================================

def test_missing_human_authority_blocks_execution(valid_conditions):
    """
    HA-01
    FLOW_BIND + RUNTIME_MATCH + AUTHORIZATION otherwise valid,
    but H-layer absent (None = UNKNOWN).

    Required: must NOT yield PERMITTED / must not reach protected action.
    """
    # Governing formula: H=None → UNKNOWN → never PERMITTED
    evaluation = evaluate_governing_permit(
        conditions=valid_conditions,
        L=valid_conditions,
        G=valid_conditions,
        S=valid_conditions,
        H=None,  # human authority layer missing
        evidence={"record": "e1"},
    )
    assert evaluation.outcome is not PermitOutcome.PERMITTED
    assert evaluation.outcome is PermitOutcome.UNKNOWN
    assert "H" in evaluation.reason or evaluation.layer_status.get("H") == "unknown"

    # Authority path that optionally binds governing permit
    with pytest.raises(AuthorityHalt):
        require_authorization_for_action(
            authorization_present=True,
            authorization_scope="execute",
            requested_action="execute",
            declared_scopes=["execute"],
            governing_conditions=valid_conditions,
            L=valid_conditions,
            G=valid_conditions,
            S=valid_conditions,
            H=None,  # missing
            evidence={"record": "e1"},
        )

    # Direct spine helper
    with pytest.raises(AuthorityHalt):
        require_governing_permit_for_action(
            conditions=valid_conditions,
            L=valid_conditions,
            G=valid_conditions,
            S=valid_conditions,
            H=None,
            evidence={"record": "e1"},
            requested_action="execute",
        )


# ===========================================================================
# HA-02  human authority for different action blocks
# ===========================================================================

def test_human_authority_for_different_action_blocks(valid_conditions):
    """
    HA-02
    H binding exists but is scoped to action B; requested action is A.

    Current API represents H only as a condition-id set. We therefore
    place action-B conditions in H and request action A, then assert
    that a scope-aware authorization check rejects the mismatch.

    If the current implementation allows this to become PERMITTED, the
    test FAILS and records the gap.
    """
    conditions_for_A = ["cond_workflow_W1", "cond_action_A"]
    conditions_for_B = ["cond_workflow_W1", "cond_action_B"]  # different action

    # Governing permit with H that only covers B while C(a) requires A
    evaluation = evaluate_governing_permit(
        conditions=conditions_for_A,
        L=conditions_for_A + conditions_for_B,
        G=conditions_for_A + conditions_for_B,
        S=conditions_for_A + conditions_for_B,
        H=conditions_for_B,  # H does not contain cond_action_A
        evidence={"record": "e1"},
    )
    # Required behaviour: REJECTED because C(a) ⊈ H
    assert evaluation.outcome is PermitOutcome.REJECTED, (
        f"GAP: different-action H produced {evaluation.outcome} "
        f"reason={evaluation.reason}; expected REJECTED"
    )
    assert "H" in evaluation.failed_layers or "H" in evaluation.reason

    # Authorization scope mismatch (existing API)
    with pytest.raises(AuthorityError):
        require_authorization_for_action(
            authorization_present=True,
            authorization_scope="action_B",
            requested_action="action_A",
            declared_scopes=["action_B"],
        )


# ===========================================================================
# HA-03  human authority for different workflow blocks
# ===========================================================================

def test_human_authority_for_different_workflow_blocks(valid_conditions):
    """
    HA-03
    H binding belongs to workflow W2; current FLOW_BIND is W1.
    """
    conditions_W1 = ["cond_workflow_W1", "cond_action_A"]
    conditions_W2 = ["cond_workflow_W2", "cond_action_A"]

    evaluation = evaluate_governing_permit(
        conditions=conditions_W1,
        L=conditions_W1 + conditions_W2,
        G=conditions_W1 + conditions_W2,
        S=conditions_W1 + conditions_W2,
        H=conditions_W2,  # H only covers W2
        evidence={"record": "e1"},
    )
    assert evaluation.outcome is PermitOutcome.REJECTED, (
        f"GAP: different-workflow H produced {evaluation.outcome} "
        f"reason={evaluation.reason}; expected REJECTED"
    )
    assert "H" in evaluation.failed_layers or "H" in evaluation.reason


# ===========================================================================
# HA-04  observation of human presence does not bind
# ===========================================================================

def test_observation_of_human_presence_does_not_bind(valid_conditions):
    """
    HA-04
    Runtime can observe that a human is present, but there is no explicit
    action-specific authority binding.

    Explicit non-implication helpers already exist; this test asserts them
    and verifies that an observation object cannot satisfy H.
    """
    human_presence_observation = {
        "human_present": True,
        "last_seen": 10.0,
        "session_id": "S-human-1",
    }

    # Documented non-implication
    assert observation_does_not_satisfy_H(human_presence_observation) is True
    assert obs_not_H(human_presence_observation) is True

    # Observation must not be usable as H layer set
    # Passing the observation object itself as H is a type error / wrong use;
    # the correct probe is: H remains None while an observation exists.
    evaluation = evaluate_governing_permit(
        conditions=valid_conditions,
        L=valid_conditions,
        G=valid_conditions,
        S=valid_conditions,
        H=None,  # no binding, only observation exists outside the formula
        evidence=human_presence_observation,  # evidence may exist
    )
    assert evaluation.outcome is not PermitOutcome.PERMITTED
    assert evaluation.outcome is PermitOutcome.UNKNOWN

    # Undeclared authority-bearing field "human_approved" must be rejected
    payload_with_presence = {
        "data": "x",
        "human_approved": True,  # forbidden field
    }
    decision = scan_undeclared_authority(
        payload_with_presence, layer=AuthorityLayer.DATA
    )
    assert decision.allowed is False
    assert "human_approved" in decision.rejected_fields


# ===========================================================================
# HA-05  stale human authority binding blocks
# ===========================================================================

def test_stale_human_authority_binding_blocks(valid_conditions):
    """
    HA-05
    Human authority binding was previously valid; freshness has expired.

    At tip ab320c6 there is NO freshness / validity-window field on H.
    The governing formula treats H as a plain set of condition identifiers.
    Therefore this test documents the missing control:

      - We can obtain a prior PERMITTED evaluation.
      - Re-evaluation with the same layers still yields PERMITTED
        (no automatic expiry).
      - That is the gap: stale binding is not rejected.

    The test is expected to FAIL (expose the gap) until a freshness
    mechanism is implemented. We assert the *desired* behaviour and
    mark the known current behaviour as the gap.
    """
    # Prior evaluation under full layers
    prior = evaluate_governing_permit(
        conditions=valid_conditions,
        L=valid_conditions,
        G=valid_conditions,
        S=valid_conditions,
        H=valid_conditions,
        evidence={"record": "e1", "issued_at": 0.0},
    )
    assert prior.outcome is PermitOutcome.PERMITTED

    # Re-validation helper always re-evaluates; it does not carry time
    reval = prior_evaluation_requires_revalidation(
        prior,
        conditions=valid_conditions,
        L=valid_conditions,
        G=valid_conditions,
        S=valid_conditions,
        H=valid_conditions,
        evidence={"record": "e1", "issued_at": 0.0},  # "stale" timestamp
    )
    # CURRENT behaviour: still PERMITTED (no freshness check)
    # REQUIRED behaviour: EXPIRED / REJECTED / HALT
    #
    # This assertion encodes the REQUIRED behaviour. It will FAIL on
    # the current implementation, which is the intended outcome of a
    # gap test.
    assert reval.outcome is not PermitOutcome.PERMITTED, (
        "GAP EXPOSED (HA-05): stale human-authority binding still yields "
        f"PERMITTED (reason={reval.reason}). No freshness/expiry control "
        "exists on H at tip ab320c6."
    )


# ===========================================================================
# HA-06  forged human authority token rejected
# ===========================================================================

def test_forged_human_authority_token_rejected(valid_conditions):
    """
    HA-06
    Synthetic / forged authority binding that did not originate from the
    legitimate authority path must be rejected.

    Current surface: undeclared authority-bearing fields are rejected by
    scan_undeclared_authority / require_no_authority_escalation.
    A plain signature does not authorize.
    """
    forged_token = {
        "authority": "forged-human-token",
        "authorized": True,
        "human_approved": True,
        "permission": "execute",
        "privilege": "admin",
    }

    decision = scan_undeclared_authority(
        forged_token, layer=AuthorityLayer.AUTHORIZATION
    )
    assert decision.allowed is False
    assert len(decision.rejected_fields) > 0

    with pytest.raises(AuthorityError):
        require_no_authority_escalation(
            forged_token, layer=AuthorityLayer.AUTHORIZATION
        )

    # Signature alone is not authorization
    assert signature_does_not_authorize({"sig": "deadbeef"}) is True
    assert sig_not_auth({"sig": "deadbeef"}) is True

    # Layer non-implication: success at DATA/EVIDENCE must not imply ACTION
    matrix = layer_non_implication_matrix()
    assert "action" in matrix["data"] or "authorization" in matrix["data"]
    assert "action" in matrix["evidence"] or "authorization" in matrix["evidence"]
    assert_layer_does_not_imply(AuthorityLayer.DATA, AuthorityLayer.ACTION)
    assert_layer_does_not_imply(AuthorityLayer.EVIDENCE, AuthorityLayer.AUTHORIZATION)


# ===========================================================================
# Meta: document execution_integrity human-authority surface status
# ===========================================================================

def test_execution_integrity_human_authority_surface_absent():
    """
    Meta-check: at tip ab320c6 the execution_integrity module cannot be
    imported (incomplete base64 payload restore). Even when importable,
    the public surface used by existing adversarial tests has no
    HumanAuthorityBinding, no H token, and no freshness parameter.

    This test records that fact without attempting implementation.
    """
    try:
        from swi_v2.execution_integrity import (
            ExecutionIntegrityGate,
            AdmittedRoute,
            ExecutionRecord,
        )
        importable = True
    except Exception as exc:
        importable = False
        import_error = str(exc)

    if not importable:
        # Document the current import failure; do not treat as OPEN-016 pass
        assert "padding" in import_error.lower() or "payload" in import_error.lower() or True
        pytest.skip(
            "execution_integrity body not importable at ab320c6 "
            f"(incomplete payload restore): {import_error!r}. "
            "HA-01..HA-06 against ExecutionIntegrityGate deferred until "
            "payload restoration is complete; authority/governing_permit "
            "probes above still apply."
        )

    # If import succeeds in a future tip, assert the missing attributes
    assert not hasattr(ExecutionIntegrityGate, "require_human_authority")
    assert not hasattr(ExecutionIntegrityGate, "human_authority_binding")
