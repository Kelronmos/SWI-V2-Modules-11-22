"""Module 12 — PROPOSED / DESIGN PENDING (Evidence Normalization).

Current code: type boundary only — requires AdmittedInput.
Does NOT implement normalization.
"""
from swi_v2.kernel.enforcement import require_admitted


def process(value):
    admitted = require_admitted(value, module="module_12")
    return {
        "status": "accepted_placeholder",
        "evidence_id": admitted.evidence_id,
        "note": "DESIGN PENDING — not NormalizedEvidence yet",
    }
