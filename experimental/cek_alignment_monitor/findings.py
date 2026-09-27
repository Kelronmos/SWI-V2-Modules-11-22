"""
Structured findings produced by the CEK observation layer.

Allowed results:
  VISIBLE, PARTIALLY_VISIBLE, UNKNOWN, UNTRACEABLE, INVALID, HALTED

finding ≠ authority
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from .observation import CEKObservation


class FindingKind(str, Enum):
    VISIBLE = "VISIBLE"
    PARTIALLY_VISIBLE = "PARTIALLY_VISIBLE"
    UNKNOWN = "UNKNOWN"
    UNTRACEABLE = "UNTRACEABLE"
    INVALID = "INVALID"
    HALTED = "HALTED"


FINDING_VERSION = "cek-finding-1.0-experimental"


@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: str
    observation_id: str
    scope: str
    visibility: FindingKind
    reason: str
    frontier: Optional[str] = None
    evidence_reference: Optional[str] = None
    finding_version: str = FINDING_VERSION
    created_at: float = field(default_factory=time.time)

    @classmethod
    def from_observation(
        cls,
        observation: CEKObservation,
        scope: str = "cek_observation",
        reason: str = "",
        finding_id: Optional[str] = None,
    ) -> "Finding":
        vis = observation.visibility
        if vis.has_unknown_edge:
            kind = FindingKind.UNKNOWN
            frontier = vis.frontier
            reason = reason or f"Unknown edge at {frontier}"
        elif any(n.level.value == "HALTED" for n in vis.nodes):
            kind = FindingKind.HALTED
            frontier = vis.frontier
            reason = reason or "Halted visibility path"
        else:
            kind = FindingKind.VISIBLE
            frontier = None
            reason = reason or "Full path visible within instrumentation"

        return cls(
            finding_id=finding_id or str(uuid.uuid4()),
            observation_id=observation.observation_id,
            scope=scope,
            visibility=kind,
            reason=reason,
            frontier=frontier,
            evidence_reference=observation.evidence_reference,
            finding_version=FINDING_VERSION,
            created_at=time.time(),
        )

    def is_authoritative(self) -> bool:
        """Always False — findings never confer authority."""
        return False

    def permits_execution(self) -> bool:
        return False

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "observation_id": self.observation_id,
            "scope": self.scope,
            "visibility": self.visibility.value,
            "reason": self.reason,
            "frontier": self.frontier,
            "evidence_reference": self.evidence_reference,
            "finding_version": self.finding_version,
        }

    def content_hash(self) -> str:
        payload = json.dumps(
            self.canonical_dict(), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        d = self.canonical_dict()
        d["created_at"] = self.created_at
        d["content_hash"] = self.content_hash()
        d["is_authoritative"] = self.is_authoritative()
        return d
