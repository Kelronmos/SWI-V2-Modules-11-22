"""Evidence quality checks — separate from E(a) ≠ ∅."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional


def evaluate_evidence_item(item: Mapping[str, Any]) -> Dict[str, Any]:
    """Score one evidence object. Does not invent PASS for missing fields."""
    exists = bool(item.get("exists", True)) and bool(item.get("evidence_id") or item.get("id"))
    relevance = item.get("relevance")
    freshness = item.get("freshness")
    scope = item.get("scope")
    provenance = item.get("provenance")
    integrity = item.get("integrity")

    def norm(v: Optional[str]) -> str:
        if v is None:
            return "UNRESOLVED"
        v = str(v).upper()
        if v in {"PASS", "FAIL", "UNRESOLVED"}:
            return v
        return "UNRESOLVED"

    return {
        "evidence_id": item.get("evidence_id") or item.get("id"),
        "exists": exists,
        "relevance": norm(relevance),
        "freshness": norm(freshness),
        "scope": norm(scope),
        "provenance": norm(provenance),
        "integrity": norm(integrity),
    }


def evidence_adequacy(items: List[Mapping[str, Any]]) -> Dict[str, Any]:
    if not items:
        return {
            "evidence_exists": False,
            "adequate": False,
            "items": [],
            "reason": "E(a) empty",
        }
    scored = [evaluate_evidence_item(x) for x in items]
    dims = ("relevance", "freshness", "scope", "provenance", "integrity")
    adequate = True
    reasons = []
    for s in scored:
        if not s["exists"]:
            adequate = False
            reasons.append(f"{s['evidence_id']}: not exists")
            continue
        for d in dims:
            if s[d] != "PASS":
                adequate = False
                reasons.append(f"{s['evidence_id']}:{d}={s[d]}")
    return {
        "evidence_exists": True,
        "adequate": adequate,
        "items": scored,
        "reason": "OK" if adequate else "; ".join(reasons) or "inadequate",
    }
