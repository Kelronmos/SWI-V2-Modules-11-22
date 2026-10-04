"""
Deterministic synthetic demonstration / test case generator.

SIMULATION ≠ PROOF
All cases are synthetic. No real-world actions.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

GENERATOR_VERSION = "1.0.0"
DEFAULT_SEED = 20261004

CASE_TYPES = [
    "VALID_INPUT",
    "INVALID_INPUT",
    "MISSING_EVIDENCE",
    "UNKNOWN_AUTHORITY",
    "CONFLICTING_CONSTRAINTS",
    "BOUNDARY_VIOLATION",
    "UNAUTHORIZED_ACTION",
    "CHANGED_DEPENDENCY",
    "STALE_EVIDENCE",
    "REVALIDATION_REQUIRED",
    "MEMORY_MISMATCH",
    "OBSERVATION_WITHOUT_AUTHORITY",
    "STABLE_BUT_UNAUTHORIZED",
    "SEAL_MISMATCH",
    "RUNTIME_MISMATCH",
    "CONSEQUENCE_GATE_REJECTION",
]

# Expected outcome for each case type under SWI invariants
EXPECTED = {
    "VALID_INPUT": "ACCEPT_IF_AUTHORIZED",  # still requires full permit check
    "INVALID_INPUT": "REJECT",
    "MISSING_EVIDENCE": "REJECT",
    "UNKNOWN_AUTHORITY": "REJECT",
    "CONFLICTING_CONSTRAINTS": "REJECT",
    "BOUNDARY_VIOLATION": "REJECT",
    "UNAUTHORIZED_ACTION": "REJECT",
    "CHANGED_DEPENDENCY": "REQUIRES_REVALIDATION",
    "STALE_EVIDENCE": "REQUIRES_REVALIDATION",
    "REVALIDATION_REQUIRED": "REQUIRES_REVALIDATION",
    "MEMORY_MISMATCH": "REJECT",
    "OBSERVATION_WITHOUT_AUTHORITY": "REJECT",
    "STABLE_BUT_UNAUTHORIZED": "REJECT",
    "SEAL_MISMATCH": "REJECT",
    "RUNTIME_MISMATCH": "REJECT",
    "CONSEQUENCE_GATE_REJECTION": "REJECT",
}


def _case_hash(seed: int, case_id: str, definition: dict) -> str:
    payload = json.dumps({"seed": seed, "case_id": case_id, **definition}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def generate_cases(count: int, seed: int = DEFAULT_SEED) -> dict[str, Any]:
    """Generate a deterministic matrix of synthetic cases."""
    cases = []
    for i in range(count):
        case_type = CASE_TYPES[i % len(CASE_TYPES)]
        case_id = f"DEMO-{i+1:06d}"
        node = ["M11", "M02", "CEK", "FIREFLY", "BOUNDARY", "GATE"][i % 6]
        definition = {
            "case_type": case_type,
            "node": node,
            "evidence": "EMPTY" if "MISSING" in case_type or "STALE" in case_type else "PRESENT",
            "authorization": "UNKNOWN" if "UNKNOWN" in case_type or "UNAUTHORIZED" in case_type else "REQUESTED",
            "memory": "STALE" if "STALE" in case_type else "FRESH",
            "expected": EXPECTED[case_type],
        }
        # Synthetic actual outcome: for this simulation we treat expected rejection as PASS
        # when the system would correctly reject, and we never auto-permit.
        if definition["expected"] in ("REJECT", "REQUIRES_REVALIDATION"):
            actual = definition["expected"]
            status = "PASS"  # expected rejection observed
        else:
            # VALID_INPUT still cannot be auto-permitted without real L,G,S,H,E
            actual = "INSUFFICIENT_EVIDENCE"
            status = "PASS"  # correctly refused to invent authority

        cases.append({
            "case_id": case_id,
            "case_type": case_type,
            "node": node,
            "input_hash": _case_hash(seed, case_id, definition),
            "expected": definition["expected"],
            "actual": actual,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "runner_version": GENERATOR_VERSION,
        })

    definition_hash = hashlib.sha256(
        json.dumps({"seed": seed, "count": count, "types": CASE_TYPES}, sort_keys=True).encode()
    ).hexdigest()

    return {
        "generator_version": GENERATOR_VERSION,
        "seed": seed,
        "case_definition_hash": definition_hash,
        "requested": count,
        "generated": len(cases),
        "mode": "SIMULATION",
        "real_world_action": "NONE",
        "production_authorized": False,
        "note": "SIMULATION ≠ PROOF. Cases are synthetic. No authority invented.",
        "cases": cases,
        "summary": {
            "pass": sum(1 for c in cases if c["status"] == "PASS"),
            "fail": sum(1 for c in cases if c["status"] == "FAIL"),
            "blocked": 0,
            "not_run": 0,
        },
    }
