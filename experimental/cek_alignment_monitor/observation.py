"""
CEK Observation layer.

REQUEST → CONTEXT → MEASUREMENT → PROVENANCE → EVIDENCE REFERENCE → CEK OBSERVATION

CEK answers:
  What can be observed?
  What can be traced?
  Where does observation stop?
  What is unknown?

CEK does NOT answer:
  Should this execute?
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

from .measurement import Measurement
from .provenance import ProvenanceRecord
from .visibility import VisibilityAnalyzer, VisibilityReport, VisibilityLevel


class ObservationError(ValueError):
    """Raised on invalid observation construction (fail-closed)."""


OBSERVATION_VERSION = "cek-observation-1.0-experimental"


@dataclass(frozen=True, slots=True)
class CEKObservation:
    """
    Immutable CEK observation record.

    authority_established is hard-coded False.
    execution_permitted is hard-coded False.
    """

    observation_id: str
    measurement: Measurement
    provenance: ProvenanceRecord
    visibility: VisibilityReport
    context: Mapping[str, Any]
    evidence_reference: Optional[str] = None
    observation_version: str = OBSERVATION_VERSION
    created_at: float = field(default_factory=time.time)

    @classmethod
    def create(
        cls,
        measurement: Measurement,
        provenance: ProvenanceRecord,
        context: Mapping[str, Any] | None = None,
        evidence_reference: Optional[str] = None,
        visibility_steps: list[tuple[str, VisibilityLevel, str]] | None = None,
        observation_id: Optional[str] = None,
    ) -> "CEKObservation":
        if not isinstance(measurement, Measurement):
            raise ObservationError("measurement required")
        if not isinstance(provenance, ProvenanceRecord):
            raise ObservationError("provenance required")

        analyzer = VisibilityAnalyzer()
        if visibility_steps is not None:
            visibility = analyzer.analyze(visibility_steps)
        else:
            visibility = analyzer.analyze(
                [
                    ("ORIGIN", VisibilityLevel.OBSERVABLE, "default origin"),
                    ("MEASUREMENT", VisibilityLevel.KNOWN, "measurement present"),
                    ("PROVENANCE", VisibilityLevel.TRACEABLE, "provenance present"),
                ]
            )

        ctx = dict(context or {})
        for forbidden in (
            "authorized",
            "permit",
            "execute",
            "seal",
            "admit",
            "approved",
            "authority",
        ):
            ctx.pop(forbidden, None)

        return cls(
            observation_id=observation_id or str(uuid.uuid4()),
            measurement=measurement,
            provenance=provenance,
            visibility=visibility,
            context=ctx,
            evidence_reference=evidence_reference,
            observation_version=OBSERVATION_VERSION,
            created_at=time.time(),
        )

    def authority_established(self) -> bool:
        """Always False. Observation never establishes authority."""
        return False

    def execution_permitted(self) -> bool:
        """Always False. Observation never permits execution."""
        return False

    def is_authoritative(self) -> bool:
        return False

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "measurement_id": self.measurement.measurement_id,
            "provenance_id": self.provenance.provenance_id,
            "visibility": self.visibility.summary(),
            "evidence_reference": self.evidence_reference,
            "observation_version": self.observation_version,
        }

    def content_hash(self) -> str:
        payload = json.dumps(
            self.canonical_dict(), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        d = self.canonical_dict()
        d["context"] = dict(self.context)
        d["created_at"] = self.created_at
        d["content_hash"] = self.content_hash()
        d["authority_established"] = self.authority_established()
        d["execution_permitted"] = self.execution_permitted()
        return d
