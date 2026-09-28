"""Pure S9 evaluator — no authorize, seal, repair, or execute."""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Mapping, Optional

from .constraints import map_constraints, layer_status
from .evidence import evidence_adequacy


ALLOWED_RESULTS = frozenset({"SATISFIED", "BLOCKED", "UNRESOLVED", "NOT_PROVEN"})


@dataclass
class EvaluationResult:
    action_id: str
    documented_equation_result: str
    evidence_adequacy_result: str
    system_result: str
    constraint_coverage: bool
    law: str
    governance: str
    security: str
    human: str
    evidence_exists: bool
    evidence_adequate: bool
    reasons: List[str] = field(default_factory=list)
    mapping: Dict[str, Any] = field(default_factory=dict)
    evidence_detail: Dict[str, Any] = field(default_factory=dict)
    promotion_eligible: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def evaluate_s9(action: Mapping[str, Any]) -> EvaluationResult:
    """Evaluate Permit inputs without side effects.

    UNKNOWN / missing never become PASS.
    Documented equation (E≠∅) reported separately from evidence adequacy.
    """
    mapping = map_constraints(action)
    ev = evidence_adequacy(list(action.get("evidence") or []))
    reasons: List[str] = []

    law = layer_status(mapping["L"], "L")
    gov = layer_status(mapping["G"], "G")
    sec = layer_status(mapping["S"], "S")
    hum = layer_status(mapping["H"], "H")

    if mapping["constraint_coverage"] and mapping["evidence_exists"]:
        doc = "SATISFIED"
    elif not mapping["evidence_exists"]:
        doc = "BLOCKED"
        reasons.append("E(a) empty")
    else:
        doc = "BLOCKED"
        reasons.append(mapping["coverage_note"])

    if law == "MISSING":
        reasons.append("L MISSING")
    if gov == "MISSING":
        reasons.append("G MISSING")
    if sec == "MISSING":
        reasons.append("S MISSING")
    if hum == "MISSING":
        reasons.append("H MISSING")

    if not ev["evidence_exists"]:
        adeq = "BLOCKED"
    elif not ev["adequate"]:
        adeq = "BLOCKED"
        reasons.append(f"evidence adequacy: {ev['reason']}")
    else:
        adeq = "SATISFIED"

    deps = action.get("dependencies") or []
    unresolved_deps = [d for d in deps if isinstance(d, dict) and d.get("status") in {"UNRESOLVED", "UNKNOWN", "MISSING"}]
    unknown_flags = action.get("unknown_conditions") or []
    if unresolved_deps:
        reasons.append(f"unresolved dependencies: {len(unresolved_deps)}")
    if unknown_flags:
        reasons.append("UNKNOWN conditions present")

    if unknown_flags or unresolved_deps:
        system = "UNRESOLVED"
    elif doc == "SATISFIED" and adeq == "SATISFIED" and hum != "MISSING":
        system = "SATISFIED"
    elif doc == "BLOCKED" or adeq == "BLOCKED" or hum == "MISSING":
        system = "BLOCKED"
    else:
        system = "NOT_PROVEN"

    promotion = False

    auth = action.get("authority") or {}
    if auth.get("required") and not auth.get("present"):
        system = "BLOCKED"
        reasons.append("required authority not present")
        promotion = False

    return EvaluationResult(
        action_id=str(action.get("action_id") or ""),
        documented_equation_result=doc,
        evidence_adequacy_result=adeq,
        system_result=system,
        constraint_coverage=mapping["constraint_coverage"],
        law=law,
        governance=gov,
        security=sec,
        human=hum,
        evidence_exists=mapping["evidence_exists"],
        evidence_adequate=ev["adequate"],
        reasons=reasons,
        mapping=mapping,
        evidence_detail=ev,
        promotion_eligible=promotion,
    )
