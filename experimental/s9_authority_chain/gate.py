"""Experimental S9 ExecutionGate and escalation helpers.

Invariants enforced here (within experimental scope):

  ESCALATION ⇏ AUTHORIZATION
  EXECUTION   ⇒ Verify(Command, Scope, Authority, Digest, Evidence)
  Verify=FAIL ⇒ ESCALATE ∧ ¬EXECUTE

No real digital signatures. Integrity is deterministic digest matching only.
"""
from __future__ import annotations

from typing import Any, Sequence

from swi_v2.kernel.errors import ModuleKernelError, StateTransitionError

from .models import (
    AuthorityBinding,
    AuthorityGrant,
    EscalationRecord,
    ExecutionProceedToken,
    ReviewRecord,
    SignedCommand,
    VerificationResult,
)

MODULE_ID = "s9_authority_chain"


def escalate(
    reason_codes: Sequence[str],
    *,
    stage: str = "escalation",
    detail: str = "",
) -> EscalationRecord:
    """Create an escalation that carries zero authority."""
    return EscalationRecord(
        reason_codes=tuple(reason_codes),
        stage=stage,
        authority_carried=False,
        detail=detail,
    )


def verify_binding(binding: AuthorityBinding) -> VerificationResult:
    """Verify structural + digest binding. Not cryptographic authenticity.

    Checks:
    1. command.digest matches the command surface
    2. grant.command_digest matches command.digest
    3. grant.scope matches command.scope
    4. placeholders remain explicit NOT_IMPLEMENTED (no silent upgrade)
    """
    cmd = binding.command
    grant = binding.grant

    expected_digest = SignedCommand.create(
        cmd.action, cmd.scope, cmd.resource, cmd.principal
    ).digest
    if cmd.digest != expected_digest:
        return VerificationResult(
            ok=False,
            reason_code="COMMAND_DIGEST_MISMATCH",
            stage="verify_binding",
            detail="command surface does not match its declared digest",
            binding_digest=binding.binding_digest(),
        )

    if grant.command_digest != cmd.digest:
        return VerificationResult(
            ok=False,
            reason_code="AUTHORITY_COMMAND_DIGEST_MISMATCH",
            stage="verify_binding",
            detail="authority grant is not bound to this command digest",
            binding_digest=binding.binding_digest(),
        )

    if grant.scope != cmd.scope:
        return VerificationResult(
            ok=False,
            reason_code="AUTHORITY_SCOPE_MISMATCH",
            stage="verify_binding",
            detail=f"grant.scope={grant.scope!r} != command.scope={cmd.scope!r}",
            binding_digest=binding.binding_digest(),
        )

    # Explicit non-claim: signature / key remain NOT_IMPLEMENTED
    if grant.signature_placeholder != "NOT_IMPLEMENTED":
        return VerificationResult(
            ok=False,
            reason_code="UNEXPECTED_SIGNATURE_CLAIM",
            stage="verify_binding",
            detail="signature field must remain NOT_IMPLEMENTED until real crypto is present",
            binding_digest=binding.binding_digest(),
        )

    return VerificationResult(
        ok=True,
        reason_code="BINDING_OK",
        stage="verify_binding",
        detail="structural + digest binding matched (integrity only; no crypto claim)",
        binding_digest=binding.binding_digest(),
    )


class ExecutionGate:
    """Final experimental gate before any privileged action.

    Requires a verified AuthorityBinding.
    Escalation or failed verification never produces an ExecutionProceedToken.
    """

    def evaluate(
        self,
        value: Any,
    ) -> ExecutionProceedToken | EscalationRecord:
        if isinstance(value, EscalationRecord):
            # Escalation must not be convertible into execution
            return value

        if not isinstance(value, AuthorityBinding):
            return escalate(
                ["UNSUPPORTED_INPUT"],
                stage="execution_gate",
                detail=f"expected AuthorityBinding, got {type(value).__name__}",
            )

        result = verify_binding(value)
        if not result.ok:
            return escalate(
                [result.reason_code],
                stage="execution_gate",
                detail=result.detail,
            )

        return ExecutionProceedToken(binding=value, verification=result)


def require_proceed(value: Any, *, module: str = MODULE_ID) -> ExecutionProceedToken:
    """Fail-closed: only a verified ExecutionProceedToken may continue."""
    if isinstance(value, EscalationRecord):
        raise StateTransitionError(
            f"{module}: cannot execute while escalated "
            f"({','.join(value.reason_codes)}); authority_carried={value.authority_carried}"
        )
    if not isinstance(value, ExecutionProceedToken):
        raise ModuleKernelError(
            f"{module}: requires ExecutionProceedToken; got {type(value).__name__}"
        )
    if not value.may_execute():
        raise StateTransitionError(f"{module}: may_execute is False")
    return value


def privileged_action(value: Any, fn, *, module: str = MODULE_ID):
    """Run a privileged function only after a verified proceed token."""
    token = require_proceed(value, module=module)
    return fn(token)
