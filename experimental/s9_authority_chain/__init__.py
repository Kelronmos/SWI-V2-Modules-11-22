"""Experimental S9 authority-chain lane.

Status: RESEARCH / EXPERIMENTAL
Production authorization: NOT AUTHORIZED
Formal module seal: NOT CLAIMED
Cryptographic authenticity: NOT IMPLEMENTED

Separates:
  ReviewRecord
  AuthorityGrant
  SignedCommand
  AuthorityBinding
  VerificationResult
  EscalationRecord
  ExecutionProceedToken

from PR-009 response-boundary enforcement.

Invariants (experimental scope):
  ESCALATION ⇏ AUTHORIZATION
  EXECUTION   ⇒ Verify(Command, Scope, Authority, Digest, Evidence)
  Verify=FAIL ⇒ ESCALATE ∧ ¬EXECUTE
"""
from .models import (
    AuthorityBinding,
    AuthorityGrant,
    EscalationRecord,
    ExecutionProceedToken,
    ReviewRecord,
    SignedCommand,
    VerificationResult,
)
from .gate import (
    ExecutionGate,
    escalate,
    privileged_action,
    require_proceed,
    verify_binding,
)
from .integrity import CRYPTO_CLAIM, KEY_STATUS, SIGNATURE_STATUS

__all__ = [
    "AuthorityBinding",
    "AuthorityGrant",
    "CRYPTO_CLAIM",
    "EscalationRecord",
    "ExecutionGate",
    "ExecutionProceedToken",
    "KEY_STATUS",
    "ReviewRecord",
    "SIGNATURE_STATUS",
    "SignedCommand",
    "VerificationResult",
    "escalate",
    "privileged_action",
    "require_proceed",
    "verify_binding",
]
