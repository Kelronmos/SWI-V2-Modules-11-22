"""Executable tests for the SWI governing authorization formula.

Formula:
    Permit(a) ⟺ ∀L,G,S,H: C(a) ⊆ L ∩ G ∩ S ∩ H  ∧  E(a) ≠ ∅

STATUS: TESTED candidate only.
PROVEN: NO
SEALED: NO
PRODUCTION_AUTHORIZED: NO
"""
from __future__ import annotations

import pytest

from swi_v2.kernel.governing_permit import (
    GoverningEvaluation,
    PermitOutcome,
    evaluate_governing_permit,
    observation_does_not_satisfy_H,
    prior_evaluation_requires_revalidation,
    signature_does_not_authorize,
)


C = frozenset({"scope:read", "target:sandbox"})


def test_1_all_conditions_and_evidence_permitted():
    """TEST 1 — ALL CONDITIONS + EVIDENCE → PERMITTED"""
    ev = evaluate_governing_permit(
        conditions=C,
        L=C | {"extra_law"},
        G=C | {"policy:a"},
        S=C | {"sandbox:ok"},
        H=C | {"human:operator"},
        evidence={"receipt_id": "e-1", "kind": "authorization_evidence"},
    )
    assert ev.outcome is PermitOutcome.PERMITTED
    assert ev.is_permitted() is True
    assert ev.evidence_present is True
    assert ev.proven is False
    assert ev.sealed is False
    assert ev.production_authorized is False


def test_2_law_failure_not_permitted():
    """TEST 2 — LAW FAILURE → NOT PERMITTED"""
    ev = evaluate_governing_permit(
        conditions=C,
        L=frozenset({"other"}),
        G=C,
        S=C,
        H=C,
        evidence={"receipt_id": "e-2"},
    )
    assert ev.outcome is PermitOutcome.REJECTED
    assert "L" in ev.failed_layers
    assert ev.is_permitted() is False


def test_3_governance_failure_not_permitted():
    """TEST 3 — GOVERNANCE FAILURE → NOT PERMITTED"""
    ev = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=frozenset(),
        S=C,
        H=C,
        evidence={"receipt_id": "e-3"},
    )
    assert ev.outcome is PermitOutcome.REJECTED
    assert "G" in ev.failed_layers


def test_4_system_failure_not_permitted():
    """TEST 4 — SYSTEM FAILURE → NOT PERMITTED"""
    ev = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=frozenset({"sandbox:other"}),
        H=C,
        evidence={"receipt_id": "e-4"},
    )
    assert ev.outcome is PermitOutcome.REJECTED
    assert "S" in ev.failed_layers


def test_5_human_authority_failure_not_permitted():
    """TEST 5 — HUMAN AUTHORITY FAILURE → NOT PERMITTED"""
    ev = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=frozenset({"human:other"}),
        evidence={"receipt_id": "e-5"},
    )
    assert ev.outcome is PermitOutcome.REJECTED
    assert "H" in ev.failed_layers


def test_6_no_evidence_not_permitted():
    """TEST 6 — NO EVIDENCE → NOT PERMITTED"""
    ev = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=C,
        evidence=None,
    )
    assert ev.outcome is PermitOutcome.REJECTED
    assert ev.reason == "evidence_empty"
    assert ev.evidence_present is False

    ev_empty = evaluate_governing_permit(
        conditions=C, L=C, G=C, S=C, H=C, evidence={}
    )
    assert ev_empty.outcome is PermitOutcome.REJECTED


def test_7_unknown_condition_never_permitted():
    """TEST 7 — UNKNOWN CONDITION → UNKNOWN / never PERMITTED"""
    ev = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=None,
        evidence={"receipt_id": "e-7"},
    )
    assert ev.outcome is PermitOutcome.UNKNOWN
    assert ev.is_permitted() is False
    assert ev.layer_status["H"] == "unknown"

    ev_l = evaluate_governing_permit(
        conditions=C, L=None, G=C, S=C, H=C, evidence={"x": 1}
    )
    assert ev_l.outcome is PermitOutcome.UNKNOWN


def test_8_observation_is_not_authority():
    """TEST 8 — OBSERVATION IS NOT AUTHORITY (does not satisfy H)"""
    observation = {"cek": "aligned", "score": 0.9, "kind": "observation"}
    assert observation_does_not_satisfy_H(observation) is True
    ev = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=None,
        evidence=observation,
    )
    assert ev.outcome is PermitOutcome.UNKNOWN
    assert ev.is_permitted() is False


def test_9_signature_is_not_authorization():
    """TEST 9 — SIGNATURE IS NOT AUTHORIZATION"""
    sig = {"alg": "Ed25519", "sig": "aabbcc", "valid_crypto": True}
    assert signature_does_not_authorize(sig) is True
    ev = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=None,
        evidence=sig,
    )
    assert ev.outcome is PermitOutcome.UNKNOWN
    assert ev.is_permitted() is False
    ev2 = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=frozenset({"unrelated"}),
        evidence=sig,
    )
    assert ev2.outcome is PermitOutcome.REJECTED
    assert "H" in ev2.failed_layers


def test_10_revalidation_prior_not_auto_reused():
    """TEST 10 — REVALIDATION after condition change"""
    prior = evaluate_governing_permit(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=C,
        evidence={"receipt_id": "prior"},
    )
    assert prior.outcome is PermitOutcome.PERMITTED

    current = prior_evaluation_requires_revalidation(
        prior,
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=frozenset({"human:revoked"}),
        evidence={"receipt_id": "prior"},
    )
    assert current.outcome is PermitOutcome.REJECTED
    assert current.is_permitted() is False
    assert prior.outcome is PermitOutcome.PERMITTED


def test_non_claims_on_permitted_result():
    """Explicit non-claims remain false even on PERMITTED outcome."""
    ev = evaluate_governing_permit(
        conditions=C, L=C, G=C, S=C, H=C, evidence={"ok": True}
    )
    assert ev.outcome is PermitOutcome.PERMITTED
    assert ev.proven is False
    assert ev.sealed is False
    assert ev.production_authorized is False
