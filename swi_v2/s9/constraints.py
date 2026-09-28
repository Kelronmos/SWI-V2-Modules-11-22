"""S9 constraint mapping — C(a), L, G, S, H, E(a). Does not infer missing values."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Set


def _as_set(items: Optional[Sequence[str]]) -> Set[str]:
    return set(items or [])


def map_constraints(action: Mapping[str, Any]) -> Dict[str, Any]:
    """Map action fields to S9 inputs. Missing sets stay empty — never inferred satisfied."""
    c = _as_set(action.get("constraints"))
    l = _as_set(action.get("law"))
    g = _as_set(action.get("governance"))
    s = _as_set(action.get("security"))
    h = _as_set(action.get("human"))
    e = list(action.get("evidence") or [])
    intersection = l & g & s & h
    coverage = c.issubset(intersection) if c else False
    if not c:
        coverage = False
        coverage_note = "C(a) empty — cannot establish subset coverage"
    elif not h:
        coverage = False
        coverage_note = "H empty — missing human authority set"
    elif not coverage:
        missing = sorted(c - intersection)
        coverage_note = f"C(a) not subset of L∩G∩S∩H; missing={missing}"
    else:
        coverage_note = "C(a) ⊆ L∩G∩S∩H"
    return {
        "action_id": action.get("action_id"),
        "C_a": sorted(c),
        "L": sorted(l),
        "G": sorted(g),
        "S": sorted(s),
        "H": sorted(h),
        "E_a": e,
        "L_intersect_G_S_H": sorted(intersection),
        "constraint_coverage": coverage,
        "coverage_note": coverage_note,
        "evidence_exists": len(e) > 0,
    }


def layer_status(layer: Sequence[str], name: str) -> str:
    if not layer:
        return "MISSING"
    return "PRESENT"
