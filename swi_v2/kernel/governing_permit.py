"""SWI governing authorization predicate.

STATUS: IMPLEMENTATION CANDIDATE — not sealed, not production authorized.

Governing formula:
    Permit(a) ⟺ ∀L,G,S,H: C(a) ⊆ L ∩ G ∩ S ∩ H  ∧  E(a) ≠ ∅

Distinctions preserved:
    DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
    TESTED ≠ PROVEN
    PROVEN ≠ SEALED
    SEALED ≠ PRODUCTION AUTHORIZED
    UNKNOWN ≠ PERMITTED
    SIGNATURE ≠ AUTHORIZATION
    OBSERVATION ≠ AUTHORITY

This module is a pure, deterministic evaluator. It does not grant action rights,
does not seal, and does not set production_authorized.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, FrozenSet, Iterable, Mapping, Optional


class PermitOutcome(str, Enum):
    PERMITTED = "PERMITTED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"  # unresolved required layer → never PERMITTED


@dataclass(frozen=True)
class GoverningEvaluation:
    """Record of a single evaluation of the governing formula.

    This record is evidence of the evaluation, not authorization itself.
    """

    outcome: PermitOutcome
    reason: str
    conditions: FrozenSet[str]
    layer_status: Mapping[str, str]  # L|G|S|H → "ok" | "fail" | "unknown"
    evidence_present: bool
    failed_layers: tuple[str, ...]
    contract_id: str = "governing_permit_v0"
    # Explicit non-claims
    proven: bool = False
    sealed: bool = False
    production_authorized: bool = False

    def is_permitted(self) -> bool:
        return self.outcome is PermitOutcome.PERMITTED


def _as_frozenset(value: Optional[Iterable[str]]) -> Optional[FrozenSet[str]]:
    """None means UNKNOWN layer; empty set is known but empty."""
    if value is None:
        return None
    return frozenset(value)


def _evidence_exists(evidence: Any) -> bool:
    """E(a) ≠ ∅. Empty container / None / False → no evidence."""
    if evidence is None:
        return False
    if evidence is False:
        return False
    if isinstance(evidence, (str, bytes, bytearray)):
        return len(evidence) > 0
    if isinstance(evidence, (list, tuple, set, frozenset, dict)):
        return len(evidence) > 0
    return True


def evaluate_governing_permit(
    *,
    conditions: Iterable[str],
    L: Optional[Iterable[str]] = None,
    G: Optional[Iterable[str]] = None,
    S: Optional[Iterable[str]] = None,
    H: Optional[Iterable[str]] = None,
    evidence: Any = None,
) -> GoverningEvaluation:
    """Evaluate Permit(a) under the SWI governing formula.

    Parameters
    ----------
    conditions : C(a) — required condition identifiers for the action.
    L, G, S, H : layer sets. None = UNKNOWN (not the same as empty).
    evidence : E(a). Absence or empty → E(a) = ∅.

    Returns
    -------
    GoverningEvaluation with outcome in {PERMITTED, REJECTED, UNKNOWN}.

    Rules
    -----
    - If any of L,G,S,H is UNKNOWN → outcome UNKNOWN (never PERMITTED).
    - If any known layer fails C(a) ⊆ layer → REJECTED.
    - If E(a) = ∅ → REJECTED (when layers are otherwise resolved).
    - PERMITTED only when all layers known, all subsets hold, and evidence exists.
    - Observation objects, signatures, or prior evaluations do not satisfy H
      merely by existing; H must be supplied as an explicit layer set.
    """
    C = frozenset(conditions)
    layers: dict[str, Optional[FrozenSet[str]]] = {
        "L": _as_frozenset(L),
        "G": _as_frozenset(G),
        "S": _as_frozenset(S),
        "H": _as_frozenset(H),
    }

    layer_status: dict[str, str] = {}
    failed: list[str] = []
    unknown_layers: list[str] = []

    for name, layer in layers.items():
        if layer is None:
            layer_status[name] = "unknown"
            unknown_layers.append(name)
            continue
        if not C.issubset(layer):
            layer_status[name] = "fail"
            failed.append(name)
        else:
            layer_status[name] = "ok"

    evidence_present = _evidence_exists(evidence)

    if unknown_layers:
        return GoverningEvaluation(
            outcome=PermitOutcome.UNKNOWN,
            reason=f"required_layer_unknown:{','.join(sorted(unknown_layers))}",
            conditions=C,
            layer_status=layer_status,
            evidence_present=evidence_present,
            failed_layers=tuple(failed),
        )

    if failed:
        return GoverningEvaluation(
            outcome=PermitOutcome.REJECTED,
            reason=f"condition_not_subset_of:{','.join(sorted(failed))}",
            conditions=C,
            layer_status=layer_status,
            evidence_present=evidence_present,
            failed_layers=tuple(sorted(failed)),
        )

    if not evidence_present:
        return GoverningEvaluation(
            outcome=PermitOutcome.REJECTED,
            reason="evidence_empty",
            conditions=C,
            layer_status=layer_status,
            evidence_present=False,
            failed_layers=(),
        )

    return GoverningEvaluation(
        outcome=PermitOutcome.PERMITTED,
        reason="all_layers_satisfied_and_evidence_present",
        conditions=C,
        layer_status=layer_status,
        evidence_present=True,
        failed_layers=(),
    )


def observation_does_not_satisfy_H(observation: Any) -> bool:
    """Explicit non-implication: an observation/CEK result is not H."""
    return True


def signature_does_not_authorize(signature: Any) -> bool:
    """Explicit non-implication: a cryptographic signature is not authorization."""
    return True


def prior_evaluation_requires_revalidation(
    prior: GoverningEvaluation,
    *,
    conditions: Iterable[str],
    L: Optional[Iterable[str]] = None,
    G: Optional[Iterable[str]] = None,
    S: Optional[Iterable[str]] = None,
    H: Optional[Iterable[str]] = None,
    evidence: Any = None,
) -> GoverningEvaluation:
    """Re-evaluate under current conditions. Prior result is never auto-reused."""
    return evaluate_governing_permit(
        conditions=conditions, L=L, G=G, S=S, H=H, evidence=evidence
    )
