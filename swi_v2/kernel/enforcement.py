"""V2 kernel enforcement helpers — state and type boundary checks."""
from __future__ import annotations

from .contracts import AdmittedInput
from .errors import ModuleKernelError, StateTransitionError
from .halt import HaltedWorkflow, HaltRecord

KERNEL_STATES = (
    "RAW",
    "RECEIVED",
    "VALIDATING",
    "REJECTED",
    "ADMITTED",
    "HALTED",
    "EXECUTING",
    "COMPLETED",
    "FAILED",
)


def require_admitted(value, *, module: str) -> AdmittedInput:
    if isinstance(value, HaltedWorkflow):
        raise StateTransitionError(
            f"{module}: cannot execute while HALTED ({value.record.reason_code})"
        )
    if not isinstance(value, AdmittedInput):
        raise ModuleKernelError(
            f"{module}: requires AdmittedInput; got {type(value).__name__}"
        )
    return value


def halt(module: str, reason_code: str, stage: str, **kwargs) -> HaltedWorkflow:
    return HaltedWorkflow(
        HaltRecord(module=module, reason_code=reason_code, stage=stage, **kwargs)
    )
