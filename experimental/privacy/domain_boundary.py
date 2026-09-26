"""Privacy-domain isolation boundary for SWI.

STATUS:
  RESEARCH / EXPERIMENTAL
  IMPLEMENTED (gate only)
  NOT SEALED
  NOT PRODUCTION AUTHORIZED

Invariants (from SWI-ATM-001 / Repair Manual):

  IDENTITY_ACCESS  ≠ MEDICAL_ACCESS
  IDENTITY_ACCESS  ≠ FAMILY_ACCESS
  EDUCATION_ACCESS ≠ MEDICAL_ACCESS
  FAMILY_ACCESS    ≠ IDENTITY_ADMINISTRATION

  Same person  ≠ same permission
  Same account ≠ same permission
  Same workflow ≠ same permission
  Same node    ≠ same permission

A technical signature, certificate, or previous approval does NOT
automatically grant cross-domain access.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class PrivacyDomain(str, Enum):
    IDENTITY = "IDENTITY"
    MEDICAL = "MEDICAL"
    EDUCATION = "EDUCATION"
    FAMILY = "FAMILY"
    FINANCIAL = "FINANCIAL"
    EMPLOYMENT = "EMPLOYMENT"
    LEGAL = "LEGAL"
    OTHER_PRIVATE = "OTHER_PRIVATE"


class PrivacyDecision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"
    REDACT = "REDACT"


class PrivacyBoundaryError(Exception):
    """Raised when a privacy-domain check fails closed."""

    def __init__(self, decision: PrivacyDecision, reason: str):
        self.decision = decision
        self.reason = reason
        super().__init__(f"{decision.value}: {reason}")


@dataclass(frozen=True)
class PrivacyAccessRequest:
    """Explicit request to access a protected domain.

    All fields are required for a decision. Missing authority is fail-closed.
    """

    subject_id: str
    requester_id: str
    domain: PrivacyDomain
    purpose: str
    scope: str
    authority_domain: Optional[PrivacyDomain]
    authority_present: bool
    authority_expired: bool = False
    authority_purpose: Optional[str] = None
    is_learner_diagnostic: bool = False
    contains_private_payload: bool = False


@dataclass(frozen=True)
class PrivacyAccessResult:
    decision: PrivacyDecision
    reason: str
    request: PrivacyAccessRequest
    decided_at: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def check_privacy_access(request: PrivacyAccessRequest) -> PrivacyAccessResult:
    """Fail-closed privacy-domain gate.

    Decision order (first match wins):

    1. Learner diagnostic attempting to expose private data → REDACT
    2. Missing authority → BLOCK
    3. Expired authority → BLOCK
    4. Authority domain does not match requested domain → BLOCK
       (or ESCALATE when cross-domain escalation is explicit)
    5. Authority purpose does not match request purpose → BLOCK
    6. Otherwise → ALLOW

    No silent inheritance. No technical signature substitution.
    """
    # PRIV-A08: learner diagnostic must not leak private data
    if request.is_learner_diagnostic and request.contains_private_payload:
        return PrivacyAccessResult(
            decision=PrivacyDecision.REDACT,
            reason="Learner diagnostic must not expose private payload",
            request=request,
            decided_at=_utc_now(),
        )

    # PRIV-A01 / A02 / A03 / A04 / A05 / A06 base: missing authority
    if not request.authority_present:
        return PrivacyAccessResult(
            decision=PrivacyDecision.BLOCK,
            reason="No privacy-domain authority presented",
            request=request,
            decided_at=_utc_now(),
        )

    # PRIV-A05: expired domain authority
    if request.authority_expired:
        return PrivacyAccessResult(
            decision=PrivacyDecision.BLOCK,
            reason="Privacy-domain authority has expired",
            request=request,
            decided_at=_utc_now(),
        )

    # PRIV-A01 / A02 / A03 / A04: cross-domain without matching authority
    if request.authority_domain is None:
        return PrivacyAccessResult(
            decision=PrivacyDecision.BLOCK,
            reason="Authority domain is missing",
            request=request,
            decided_at=_utc_now(),
        )

    if request.authority_domain != request.domain:
        # PRIV-A07: explicit cross-domain escalation attempt
        return PrivacyAccessResult(
            decision=PrivacyDecision.ESCALATE,
            reason=(
                f"Authority domain {request.authority_domain.value} "
                f"does not match requested domain {request.domain.value}; "
                "escalation required"
            ),
            request=request,
            decided_at=_utc_now(),
        )

    # PRIV-A06: wrong-purpose access
    if (
        request.authority_purpose is not None
        and request.authority_purpose != request.purpose
    ):
        return PrivacyAccessResult(
            decision=PrivacyDecision.BLOCK,
            reason=(
                f"Authority purpose '{request.authority_purpose}' "
                f"does not match requested purpose '{request.purpose}'"
            ),
            request=request,
            decided_at=_utc_now(),
        )

    return PrivacyAccessResult(
        decision=PrivacyDecision.ALLOW,
        reason="Domain authority matches request",
        request=request,
        decided_at=_utc_now(),
    )


def require_privacy_access(request: PrivacyAccessRequest) -> PrivacyAccessResult:
    """Raise PrivacyBoundaryError on any non-ALLOW decision."""
    result = check_privacy_access(request)
    if result.decision != PrivacyDecision.ALLOW:
        raise PrivacyBoundaryError(result.decision, result.reason)
    return result
