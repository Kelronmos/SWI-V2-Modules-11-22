"""Kernel must not accept raw / unvalidated input (closing gate)."""
from __future__ import annotations

import pytest

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.enforcement import require_admitted
from swi_v2.kernel.errors import ModuleKernelError
from swi_v2.module12 import process as module12_process


def _valid_envelope():
    payload = {"allowed": True, "reason": None}
    base = {
        "payload": payload,
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "iso-1",
        "verification_status": "v1_trainer_pipeline_completed",
        "source_reference": "test",
    }
    base["integrity_reference"] = compute_integrity_reference(
        base["payload"],
        base["foundation_version"],
        base["evidence_schema_version"],
        base["evidence_id"],
        base["source_reference"],
    )
    return base


def test_require_admitted_rejects_dict():
    with pytest.raises(ModuleKernelError):
        require_admitted({"payload": {}}, module="test")  # type: ignore[arg-type]


def test_require_admitted_rejects_string():
    with pytest.raises(ModuleKernelError):
        require_admitted("raw", module="test")  # type: ignore[arg-type]


def test_module12_rejects_raw_dict():
    with pytest.raises(ModuleKernelError):
        module12_process(_valid_envelope())  # not AdmittedInput


def test_module12_accepts_only_after_m11():
    admitted = admit_foundation_input(_valid_envelope())
    require_admitted(admitted, module="test")
    out = module12_process(admitted)
    assert out["status"] == "accepted_placeholder"
