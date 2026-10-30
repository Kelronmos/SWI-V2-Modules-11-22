"""Regression: empty C must not PERMIT via vacuous subset truth.

PROVEN=NO SEALED=NO PRODUCTION_AUTHORIZED=NO
"""
from __future__ import annotations

from swi_v2.kernel.governing_permit import (
    PermitOutcome,
    evaluate_governing_permit,
)


def test_empty_conditions_never_permit_with_layers_and_evidence():
    ev = evaluate_governing_permit(
        conditions=frozenset(),
        L=frozenset({"x"}),
        G=frozenset({"x"}),
        S=frozenset({"x"}),
        H=frozenset({"x"}),
        evidence={"receipt": "e1"},
    )
    assert ev.outcome is not PermitOutcome.PERMITTED
    assert ev.is_permitted() is False
    assert ev.production_authorized is False


def test_empty_conditions_never_permit_with_empty_layers():
    ev = evaluate_governing_permit(
        conditions=frozenset(),
        L=frozenset(),
        G=frozenset(),
        S=frozenset(),
        H=frozenset(),
        evidence={"e": 1},
    )
    assert ev.outcome is not PermitOutcome.PERMITTED
    assert ev.is_permitted() is False


def test_nonempty_conditions_still_can_permit():
    C = frozenset({"scope:read"})
    ev = evaluate_governing_permit(
        conditions=C, L=C, G=C, S=C, H=C, evidence={"receipt": "ok"}
    )
    assert ev.outcome is PermitOutcome.PERMITTED
