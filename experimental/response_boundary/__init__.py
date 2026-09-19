"""SWI pre-R experimental response boundary.

Experimental only. No formal SWI module claim.
PR-009 adds enforcement: REJECT/HALT → HaltedWorkflow (may_execute False).
"""
from .core import (
    AuthorityScope,
    BoundaryDecision,
    EvidenceCarrier,
    IntegrityVerifier,
    RequestBinding,
    ResponseEnvelope,
    ReturnGate,
    CertificateScope,
    Receipt,
    build_response,
)
from .enforcement import (
    AdmittedResponse,
    enforce,
    require_executable,
    privileged_action,
    attempt_recovery_without_authority,
    MODULE_ID,
)

__all__ = [
    "AuthorityScope",
    "BoundaryDecision",
    "EvidenceCarrier",
    "IntegrityVerifier",
    "RequestBinding",
    "ResponseEnvelope",
    "ReturnGate",
    "CertificateScope",
    "Receipt",
    "build_response",
    "AdmittedResponse",
    "enforce",
    "require_executable",
    "privileged_action",
    "attempt_recovery_without_authority",
    "MODULE_ID",
]
