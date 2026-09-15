"""Module 12 — DESIGN PENDING / IMPLEMENTATION PENDING.

Accepts only AdmittedInput from Module 11. Raw input must be rejected.
"""
from swi_v2.kernel.contracts import AdmittedInput
from swi_v2.kernel.errors import ModuleKernelError


def process(value):
    """Placeholder downstream entry: require AdmittedInput only."""
    if not isinstance(value, AdmittedInput):
        raise ModuleKernelError(
            "module_12 rejects raw input; Module 11 admission required"
        )
    return {"status": "accepted_placeholder", "evidence_id": value.evidence_id}
