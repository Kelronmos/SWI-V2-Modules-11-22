"""Truthful service and component status for SWI Android local runtime.

STATUS: PROTOTYPE — TESTED locally only when tests pass.
PROVEN = NO · SEALED = NO · PRODUCTION_AUTHORIZED = NO

Rules:
- Missing evidence → UNKNOWN or STALE, never GREEN / OK.
- Observation is not authorization.
- Status records are evidence of observation, not permission to act.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional
import time


class ServiceState(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    DEGRADED = "DEGRADED"
    UNKNOWN = "UNKNOWN"
    STALE = "STALE"
    FAILED = "FAILED"


# Explicit non-green outcomes that must never be upgraded automatically.
NON_OK = frozenset(
    {
        ServiceState.STOPPED,
        ServiceState.DEGRADED,
        ServiceState.UNKNOWN,
        ServiceState.STALE,
        ServiceState.FAILED,
    }
)


@dataclass(frozen=True)
class StatusRecord:
    """Immutable observation of a component.

    This is DATA / OBSERVATION. It is not EVIDENCE of authorization,
    not ADMISSION, and not a PERMIT.
    """

    component: str
    state: ServiceState
    observed_at: float  # unix timestamp
    detail: str = ""
    evidence_present: bool = False
    source: str = "local_runtime"
    # Explicit non-claims
    proven: bool = False
    sealed: bool = False
    production_authorized: bool = False

    def is_ok(self) -> bool:
        return self.state is ServiceState.RUNNING and self.evidence_present

    def age_seconds(self, now: Optional[float] = None) -> float:
        now = now if now is not None else time.time()
        return max(0.0, now - self.observed_at)


def mark_stale_if_old(
    record: StatusRecord,
    *,
    max_age_seconds: float = 300.0,
    now: Optional[float] = None,
) -> StatusRecord:
    """If a RUNNING record is older than max_age, return STALE copy.

    Does not invent success. Does not upgrade any NON_OK state.
    """
    if record.state is not ServiceState.RUNNING:
        return record
    if record.age_seconds(now) <= max_age_seconds:
        return record
    return StatusRecord(
        component=record.component,
        state=ServiceState.STALE,
        observed_at=record.observed_at,
        detail=f"stale: age>{max_age_seconds}s; {record.detail}".strip(),
        evidence_present=record.evidence_present,
        source=record.source,
    )


def missing_evidence(component: str, detail: str = "no evidence supplied") -> StatusRecord:
    """Factory for honest UNKNOWN when evidence is absent."""
    return StatusRecord(
        component=component,
        state=ServiceState.UNKNOWN,
        observed_at=time.time(),
        detail=detail,
        evidence_present=False,
    )


def from_mapping(data: Mapping[str, Any]) -> StatusRecord:
    """Reconstruct a StatusRecord; fail closed to UNKNOWN on bad input."""
    try:
        state = ServiceState(str(data.get("state", "UNKNOWN")))
    except ValueError:
        state = ServiceState.UNKNOWN
    return StatusRecord(
        component=str(data.get("component", "unknown")),
        state=state,
        observed_at=float(data.get("observed_at", 0.0)),
        detail=str(data.get("detail", "")),
        evidence_present=bool(data.get("evidence_present", False)),
        source=str(data.get("source", "local_runtime")),
        proven=False,
        sealed=False,
        production_authorized=False,
    )
