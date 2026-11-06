"""Educational model helpers — research/demo only."""
from __future__ import annotations

def learning_objectives():
    return [
        "Distinguish observation from evidence",
        "Distinguish evidence from authorization",
        "Practice fail-closed local checks",
        "Never promote demo PASS to PRODUCTION_AUTHORIZED",
    ]

def claim_language():
    return {
        "PROVEN": "NO",
        "SEALED": "NO",
        "PRODUCTION_AUTHORIZED": "NO",
    }
