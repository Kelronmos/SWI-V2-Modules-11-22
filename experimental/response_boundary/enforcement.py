"""PR-009 — Response rejection enforcement (experimental).

Gate (ReturnGate) answers: may this response be admitted?
Enforcement answers: can a rejected/halted outcome cross into privileged execution?

Reuses V2 kernel HaltedWorkflow (may_execute() == False). Does not rewrite ReturnGate.
Does not claim production security, formal module seal, or automatic recovery.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, TypeVar

from swi_v2.kernel.halt import HaltedWorkflow, HaltRecord
from swi_v2.kernel.errors import StateTransitionError, ModuleKernelError

from .core import (
    AuthorityScope,
    BoundaryDecision,
    RequestBinding,
    ResponseEnvelope,
    ReturnGate,
)

T = TypeVar("T")

MODULE_ID = "pre_r_pr009"


@dataclass(frozen=True)
class AdmittedResponse:
    """Token issued only after ReturnGate ADMIT. Privileged paths must require this type."""

    envelope: ResponseEnvelope
    decision: str = BoundaryDecision.ADMIT

    def may_execute(self) -> bool:
        return True


def enforce(
    envelope: ResponseEnvelope,
    originating_request: RequestBinding,
    originating_authority: AuthorityScope,
    now: datetime,
    *,
    expected_destination: str,
    action: str,
    resource: str,
    principal: str,
    policy_allows: bool = True,
    gate: ReturnGate | None = None,
) -> AdmittedResponse | HaltedWorkflow:
    """Run ReturnGate then bind the decision to an executable or non-executable outcome."""
    g = gate if gate is not None else ReturnGate()
    decision = g.evaluate(
        envelope,
        originating_request,
        originating_authority,
        now,
        expected_destination=expected_destination,
        action=action,
        resource=resource,
        principal=principal,
        policy_allows=policy_allows,
    )
    if decision == BoundaryDecision.ADMIT:
        return AdmittedResponse(envelope=envelope, decision=decision)
    reason = {
        BoundaryDecision.REJECT: "RESPONSE_BOUNDARY_REJECT",
        BoundaryDecision.HALT: "RESPONSE_BOUNDARY_HALT",
    }.get(decision, "RESPONSE_BOUNDARY_DENY")
    return HaltedWorkflow(
        HaltRecord(
            module=MODULE_ID,
            reason_code=reason,
            stage="return_gate",
            detail=f"decision={decision}",
        )
    )


def require_executable(value: Any, *, module: str = MODULE_ID) -> AdmittedResponse:
    """Fail-safe: only AdmittedResponse may proceed. HaltedWorkflow and raw types cannot."""
    if isinstance(value, HaltedWorkflow):
        raise StateTransitionError(
            f"{module}: cannot execute while HALTED ({value.record.reason_code})"
        )
    if not isinstance(value, AdmittedResponse):
        raise ModuleKernelError(
            f"{module}: requires AdmittedResponse after enforcement; got {type(value).__name__}"
        )
    if not value.may_execute():
        raise StateTransitionError(f"{module}: may_execute is False")
    return value


def privileged_action(
    value: Any,
    fn: Callable[[ResponseEnvelope], T],
    *,
    module: str = MODULE_ID,
) -> T:
    """Run a privileged function only if enforcement produced an AdmittedResponse."""
    admitted = require_executable(value, module=module)
    return fn(admitted.envelope)


def attempt_recovery_without_authority(value: Any) -> Any:
    """Explicitly does not clear halt or invent authority. Returns value unchanged.

    Automatic recovery is NOT implemented (PR-011). Callers must obtain a new
    admission decision via enforce() with valid inputs.
    """
    return value
