"""Minimal authority-binding objects for experimental S9.

All objects are frozen diagnostic / control records.
None of these objects are execution tokens by themselves.

CLAIM level:
  - Demonstrates structural separation of Review → Authority → Command → Binding
  - Does NOT claim cryptographic authenticity
  - Does NOT claim production security
  - Does NOT seal any module
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .integrity import (
    CRYPTO_CLAIM,
    KEY_STATUS,
    SIGNATURE_STATUS,
    command_digest,
)


@dataclass(frozen=True)
class ReviewRecord:
    """Outcome of human / authority review. Review alone does not authorize execution."""

    decision: str  # e.g. "APPROVE", "REJECT", "ESCALATE_FURTHER"
    reviewer_id: str
    comment: str = ""
    timestamp: str = ""

    def carries_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class AuthorityGrant:
    """Declared authority grant. Must be bound to a specific command/scope.

    Placeholders for signature and key material are explicitly NOT_IMPLEMENTED.
    """

    authority_id: str
    scope: str
    command_digest: str
    signature_placeholder: str = SIGNATURE_STATUS
    key_id_placeholder: str = KEY_STATUS
    crypto_claim: str = CRYPTO_CLAIM

    def is_cryptographically_verified(self) -> bool:
        """Always False until a real signature mechanism is implemented and tested."""
        return False


@dataclass(frozen=True)
class SignedCommand:
    """Command surface + its deterministic digest.

    The 'signature' field is a placeholder. Integrity is demonstrated via digest
    equality only. Do not treat this as a real digital signature.
    """

    action: str
    scope: str
    resource: str
    principal: str
    digest: str
    signature_placeholder: str = SIGNATURE_STATUS

    @classmethod
    def create(cls, action: str, scope: str, resource: str, principal: str) -> "SignedCommand":
        d = command_digest(action, scope, resource, principal)
        return cls(
            action=action,
            scope=scope,
            resource=resource,
            principal=principal,
            digest=d,
        )


@dataclass(frozen=True)
class AuthorityBinding:
    """Binds a SignedCommand to an AuthorityGrant and optional ReviewRecord.

    This is the object that must be verified at the execution gate.
    """

    command: SignedCommand
    grant: AuthorityGrant
    review: Optional[ReviewRecord] = None
    evidence_ref: str = ""

    def binding_digest(self) -> str:
        from .integrity import digest

        return digest(
            {
                "command_digest": self.command.digest,
                "authority_id": self.grant.authority_id,
                "grant_scope": self.grant.scope,
                "grant_command_digest": self.grant.command_digest,
                "evidence_ref": self.evidence_ref,
            }
        )


@dataclass(frozen=True)
class VerificationResult:
    """Result of binding verification. Never an execution token."""

    ok: bool
    reason_code: str
    stage: str
    detail: str = ""
    binding_digest: str = ""

    def may_execute(self) -> bool:
        return False  # VerificationResult itself never executes


@dataclass(frozen=True)
class EscalationRecord:
    """Escalation carries zero authority.

    Detecting a violation and escalating must not invent or propagate authority.
    """

    reason_codes: tuple[str, ...]
    stage: str
    source: str = "s9_authority_chain"
    authority_carried: bool = False  # always False by construction
    detail: str = ""

    def may_execute(self) -> bool:
        return False

    def carries_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class ExecutionProceedToken:
    """Issued only after successful binding verification at the ExecutionGate.

    Still experimental. Does not constitute production authorization.
    """

    binding: AuthorityBinding
    verification: VerificationResult
    issued_by: str = "s9_execution_gate"

    def may_execute(self) -> bool:
        return self.verification.ok
