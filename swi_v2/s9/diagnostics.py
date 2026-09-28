"""Failure diagnostic objects for the S9 package."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


def failure_diagnostic(
    *,
    what: str,
    where: str,
    when: str = "",
    why: str = "",
    expected: str = "",
    observed: str = "",
    rule: str = "",
    evidence: Optional[List[str]] = None,
    dependency: Optional[List[str]] = None,
    authority: Optional[List[str]] = None,
    why_not_detected: str = "",
    reproducible: bool = True,
    corrective_action: str = "",
    regression_required: bool = True,
) -> Dict[str, Any]:
    return {
        "what": what,
        "where": where,
        "when": when,
        "why": why,
        "expected": expected,
        "observed": observed,
        "rule": rule,
        "evidence": evidence or [],
        "dependency": dependency or [],
        "authority": authority or [],
        "why_not_detected": why_not_detected,
        "reproducible": reproducible,
        "corrective_action": corrective_action,
        "regression_required": regression_required,
    }
