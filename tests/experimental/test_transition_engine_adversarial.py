"""P0 adversarial tests for the closed transition engine.

STATUS: RESEARCH / EXPERIMENTAL
NOT SEALED
PRODUCTION: BLOCKED

Proves decision semantics, not merely that the function runs:

1. undefined transition → REJECT
2. known transition + missing authority → BLOCK
3. known transition + invalid integrity → QUARANTINE
4. known transition + valid integrity/evidence/authority → ALLOW
5. rejected transition leaves state unchanged
6. blocked transition leaves state unchanged
7. quarantined path cannot re-enter trusted path via shortcut
8. adding a state does not automatically create transitions into it
9. adding a transition does not automatically satisfy its gates
10. technical signatures cannot substitute for human authority
"""
from __future__ import annotations

import pytest

from experimental.repair.transition_engine import (
    TransitionDecision,
    TransitionContext,
    StateRegistry,
    TransitionRegistry,
    GateSpec,
    attempt_transition,
    DEFAULT_STATES,
)


def _ctx(**kwargs) -> TransitionContext:
    return TransitionContext(**kwargs)


# ---------------------------------------------------------------------------
# 1. Undefined transition → REJECT
# ---------------------------------------------------------------------------

def test_undefined_transition_rejects():
    result = attempt_transition(
        "DEFINED",
        "SEALED",  # illegal shortcut
        _ctx(),
    )
    assert result.decision == TransitionDecision.REJECT
    assert "UNDEFINED_TRANSITION" in result.reason
    assert result.state_mutated is False


def test_tampered_to_verified_rejects():
    result = attempt_transition("TAMPERED", "VERIFIED", _ctx(integrity_valid=True))
    assert result.decision == TransitionDecision.REJECT
    assert result.state_mutated is False


def test_tampered_to_sealed_rejects():
    result = attempt_transition("TAMPERED", "SEALED", _ctx())
    assert result.decision == TransitionDecision.REJECT


def test_tampered_to_authorized_rejects():
    result = attempt_transition("TAMPERED", "AUTHORIZED", _ctx())
    assert result.decision == TransitionDecision.REJECT


def test_tampered_to_action_rejects():
    result = attempt_transition("TAMPERED", "ACTION", _ctx())
    assert result.decision == TransitionDecision.REJECT


def test_tested_to_authorized_rejects():
    result = attempt_transition("TESTED", "AUTHORIZED", _ctx())
    assert result.decision == TransitionDecision.REJECT


def test_ci_green_path_does_not_exist():
    # There is no transition that treats CI as authority
    result = attempt_transition("TESTED", "AUTHORIZED", _ctx(ci_green=True))
    assert result.decision == TransitionDecision.REJECT


# ---------------------------------------------------------------------------
# 2. Known transition + missing authority → BLOCK
# ---------------------------------------------------------------------------

def test_known_transition_missing_authority_blocks():
    result = attempt_transition(
        "HUMAN_REVIEW",
        "REPAIR_AUTHORIZED",
        _ctx(integrity_valid=True, authority_present=False),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert "AUTHORITY_MISSING" in result.gate_failures
    assert result.state_mutated is False


def test_seal_review_to_sealed_missing_authority_blocks():
    result = attempt_transition(
        "SEAL_REVIEW",
        "SEALED",
        _ctx(integrity_valid=True, evidence_valid=True, authority_present=False),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert "AUTHORITY_MISSING" in result.gate_failures


# ---------------------------------------------------------------------------
# 3. Known transition + invalid integrity → QUARANTINE
# ---------------------------------------------------------------------------

def test_known_transition_invalid_integrity_quarantines():
    result = attempt_transition(
        "UNASSESSED",
        "INTACT",
        _ctx(integrity_valid=False),
    )
    assert result.decision == TransitionDecision.QUARANTINE
    assert "INTEGRITY_FAILURE" in result.gate_failures
    assert result.state_mutated is False


def test_repaired_to_revalidated_invalid_integrity_quarantines():
    result = attempt_transition(
        "REPAIRED",
        "REVALIDATED",
        _ctx(integrity_valid=False, evidence_valid=True),
    )
    assert result.decision == TransitionDecision.QUARANTINE


# ---------------------------------------------------------------------------
# 4. Known transition + all gates pass → ALLOW
# ---------------------------------------------------------------------------

def test_known_transition_all_gates_pass_allows():
    result = attempt_transition(
        "HUMAN_REVIEW",
        "REPAIR_AUTHORIZED",
        _ctx(
            integrity_valid=True,
            authority_present=True,
            authority_is_human=True,
        ),
    )
    assert result.decision == TransitionDecision.ALLOW
    assert result.gate_failures == ()
    # Engine itself never mutates; caller applies
    assert result.state_mutated is False


def test_authorized_to_action_with_privacy_allows():
    result = attempt_transition(
        "AUTHORIZED",
        "ACTION",
        _ctx(
            integrity_valid=True,
            evidence_valid=True,
            authority_present=True,
            authority_is_human=True,
            privacy_satisfied=True,
            privacy_decision="ALLOW",
        ),
    )
    assert result.decision == TransitionDecision.ALLOW


# ---------------------------------------------------------------------------
# 5 & 6. Rejected / blocked leave state unchanged
# ---------------------------------------------------------------------------

def test_reject_leaves_state_unchanged():
    current = "DEFINED"
    result = attempt_transition(current, "ACTION", _ctx())
    assert result.decision == TransitionDecision.REJECT
    assert result.current_state == current
    assert result.state_mutated is False


def test_block_leaves_state_unchanged():
    current = "HUMAN_REVIEW"
    result = attempt_transition(
        current,
        "REPAIR_AUTHORIZED",
        _ctx(integrity_valid=True, authority_present=False),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert result.current_state == current
    assert result.state_mutated is False


# ---------------------------------------------------------------------------
# 7. Quarantined cannot re-enter trusted path via shortcut
# ---------------------------------------------------------------------------

def test_quarantined_to_verified_rejects():
    result = attempt_transition("QUARANTINED", "VERIFIED", _ctx(integrity_valid=True))
    assert result.decision == TransitionDecision.REJECT


def test_quarantined_to_sealed_rejects():
    result = attempt_transition("QUARANTINED", "SEALED", _ctx())
    assert result.decision == TransitionDecision.REJECT


def test_quarantined_to_authorized_rejects():
    result = attempt_transition("QUARANTINED", "AUTHORIZED", _ctx())
    assert result.decision == TransitionDecision.REJECT


def test_quarantined_only_to_repair_requested():
    result = attempt_transition("QUARANTINED", "REPAIR_REQUESTED", _ctx())
    assert result.decision == TransitionDecision.ALLOW


# ---------------------------------------------------------------------------
# 8. Adding a state does not automatically create transitions into it
# ---------------------------------------------------------------------------

def test_new_state_does_not_auto_create_transitions():
    states = StateRegistry(set(DEFAULT_STATES) | {"CUSTOM_STATE"})
    trans = TransitionRegistry()  # default transitions only
    result = attempt_transition(
        "DEFINED",
        "CUSTOM_STATE",
        _ctx(),
        states=states,
        transitions=trans,
    )
    assert result.decision == TransitionDecision.REJECT
    assert "UNDEFINED_TRANSITION" in result.reason


# ---------------------------------------------------------------------------
# 9. Adding a transition does not automatically satisfy its gates
# ---------------------------------------------------------------------------

def test_new_transition_still_requires_gates():
    trans = TransitionRegistry()
    trans.register(
        "CUSTOM_A",
        "CUSTOM_B",
        GateSpec(authority_required=True, integrity_required=True),
    )
    result = attempt_transition(
        "CUSTOM_A",
        "CUSTOM_B",
        _ctx(integrity_valid=True, authority_present=False),
        transitions=trans,
    )
    assert result.decision == TransitionDecision.BLOCK
    assert "AUTHORITY_MISSING" in result.gate_failures


# ---------------------------------------------------------------------------
# 10. Technical signatures cannot substitute for human authority
# ---------------------------------------------------------------------------

def test_ci_green_cannot_substitute_for_human_authority():
    result = attempt_transition(
        "HUMAN_REVIEW",
        "REPAIR_AUTHORIZED",
        _ctx(
            integrity_valid=True,
            authority_present=True,
            authority_is_human=False,
            ci_green=True,
        ),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert (
        "AUTHORITY_NOT_HUMAN" in result.gate_failures
        or "CI_GREEN_NOT_AUTHORITY" in result.gate_failures
    )


def test_signature_valid_cannot_substitute_for_human_authority():
    result = attempt_transition(
        "SEAL_REVIEW",
        "SEALED",
        _ctx(
            integrity_valid=True,
            evidence_valid=True,
            authority_present=True,
            authority_is_human=False,
            signature_valid=True,
        ),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert (
        "AUTHORITY_NOT_HUMAN" in result.gate_failures
        or "SIGNATURE_NOT_AUTHORITY" in result.gate_failures
    )


def test_technical_verification_cannot_substitute_for_human_authority():
    result = attempt_transition(
        "PRODUCTION_REVIEW",
        "AUTHORIZED",
        _ctx(
            integrity_valid=True,
            evidence_valid=True,
            authority_present=True,
            authority_is_human=False,
            technical_verification=True,
            privacy_satisfied=True,
            privacy_decision="ALLOW",
        ),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert (
        "AUTHORITY_NOT_HUMAN" in result.gate_failures
        or "TECHNICAL_NOT_HUMAN_AUTHORITY" in result.gate_failures
    )


# ---------------------------------------------------------------------------
# Privacy gate integration (privacy is a gate, not a transition permission)
# ---------------------------------------------------------------------------

def test_privacy_gate_blocks_when_not_satisfied():
    result = attempt_transition(
        "AUTHORIZED",
        "ACTION",
        _ctx(
            integrity_valid=True,
            evidence_valid=True,
            authority_present=True,
            authority_is_human=True,
            privacy_satisfied=False,
            privacy_decision="BLOCK",
        ),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert any("PRIVACY" in f for f in result.gate_failures)


def test_privacy_escalate_blocks_transition():
    result = attempt_transition(
        "AUTHORIZED",
        "ACTION",
        _ctx(
            integrity_valid=True,
            evidence_valid=True,
            authority_present=True,
            authority_is_human=True,
            privacy_decision="ESCALATE",
        ),
    )
    assert result.decision == TransitionDecision.BLOCK
    assert "PRIVACY_ESCALATE" in result.gate_failures
