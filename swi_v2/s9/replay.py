"""S9 package replay compare — reuses conceptual replay; marks durable scope."""
from __future__ import annotations

from typing import Any, Dict, Mapping

from .evaluator import evaluate_s9


def replay_evaluate(action: Mapping[str, Any], original: Mapping[str, Any]) -> Dict[str, Any]:
    """Re-run pure evaluator; compare to original result dict."""
    again = evaluate_s9(action).to_dict()
    equiv = (
        again.get("system_result") == original.get("system_result")
        and again.get("documented_equation_result") == original.get("documented_equation_result")
        and again.get("evidence_adequacy_result") == original.get("evidence_adequacy_result")
    )
    return {
        "original_result": original.get("system_result"),
        "replay_result": again.get("system_result"),
        "equivalent": equiv,
        "replay_scope": "in-process pure function only",
        "DURABLE_REPLAY": "NOT IMPLEMENTED",
        "replay_detail": again,
    }
