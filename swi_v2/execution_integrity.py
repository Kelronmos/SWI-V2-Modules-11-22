"""SWI Execution Integrity public surface.

Restored from 77ee326 + MATCH≠PERMIT closure.
Body: execution_integrity_impl.py

Status: RESEARCH · NOT SEALED · NOT PRODUCTION_AUTHORIZED
"""
from __future__ import annotations

from swi_v2.execution_integrity_impl import (  # noqa: F401
    AdmittedRoute,
    CheckResult,
    Decision,
    ExecutionIntegrityGate,
    ExecutionRecord,
    FailureReason,
    HumanAuthority,
    IncomingNode,
    IntegrityEvidence,
    NewInformation,
    NodeState,
    ValidatedAuthority,
    validate_human_authority,
    _ExecutionPermit,
)
