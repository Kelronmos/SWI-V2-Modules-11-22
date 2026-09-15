"""V2 kernel enforcement — HALT terminal, admitted type boundary."""
import pytest

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.enforcement import require_admitted, halt, KERNEL_STATES
from swi_v2.kernel.errors import ModuleKernelError, StateTransitionError
from swi_v2.module12 import process as module12_process


def _fixture():
    base = {
        "payload": {"text": "x"},
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "k1",
        "verification_status": "foundation_verified_test_fixture",
        "source_reference": "TEST FIXTURE",
    }
    base["integrity_reference"] = compute_integrity_reference(
        base["payload"],
        base["foundation_version"],
        base["evidence_schema_version"],
        base["evidence_id"],
        base["source_reference"],
    )
    return base


def test_kernel_states_documented():
    assert "ADMITTED" in KERNEL_STATES and "HALTED" in KERNEL_STATES


def test_require_admitted_rejects_raw():
    with pytest.raises(ModuleKernelError):
        require_admitted({"verified": True}, module="test")


def test_require_admitted_accepts_admitted():
    adm = admit_foundation_input(_fixture())
    assert require_admitted(adm, module="test") is adm


def test_execution_after_halt_fails():
    hw = halt("module_11", "TEST_HALT", "validating")
    assert hw.may_execute() is False
    with pytest.raises(StateTransitionError):
        require_admitted(hw, module="module_12")


def test_module12_still_rejects_raw():
    with pytest.raises(ModuleKernelError):
        module12_process("raw")
