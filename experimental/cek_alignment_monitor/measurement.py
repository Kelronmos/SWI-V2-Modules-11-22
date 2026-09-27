"""
Measurement object — deterministic record of a distance calculation.

Contains only measurement data. Explicitly excludes any authority,
admission, execution, sealing, or permit fields.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

from .distance import Classification, DistanceCalculator, DistanceResult
from .vector import AlignmentVector


class MeasurementError(ValueError):
    """Raised on invalid measurement construction (fail-closed)."""


MEASUREMENT_VERSION = "cek-measurement-1.0-experimental"


@dataclass(frozen=True, slots=True)
class Measurement:
    """
    Immutable measurement record.

    Fields are restricted to pure measurement semantics.
    No 'authorized', 'permit', 'execute', 'seal', 'admit', 'approved'
    operational fields are permitted.
    """

    measurement_id: str
    vector: AlignmentVector
    target: AlignmentVector
    weights: tuple[float, ...]
    distance: float
    classification: Classification
    measurement_version: str = MEASUREMENT_VERSION
    created_at: float = field(default_factory=time.time)

    @classmethod
    def create(
        cls,
        vector: AlignmentVector,
        calculator: DistanceCalculator | None = None,
        measurement_id: str | None = None,
    ) -> "Measurement":
        if not isinstance(vector, AlignmentVector):
            raise MeasurementError("vector must be AlignmentVector")
        calc = calculator or DistanceCalculator()
        result: DistanceResult = calc.compute(vector)
        mid = measurement_id or str(uuid.uuid4())
        return cls(
            measurement_id=mid,
            vector=vector,
            target=calc.target,
            weights=result.weights,
            distance=result.distance,
            classification=result.classification,
            measurement_version=MEASUREMENT_VERSION,
            created_at=time.time(),
        )

    def canonical_dict(self) -> dict[str, Any]:
        """Stable dict for hashing / serialization (excludes wall-clock time)."""
        return {
            "measurement_id": self.measurement_id,
            "vector": self.vector.as_dict(),
            "target": self.target.as_dict(),
            "weights": list(self.weights),
            "distance": round(self.distance, 12),
            "classification": self.classification.value,
            "measurement_version": self.measurement_version,
        }

    def canonical_json(self) -> str:
        return json.dumps(self.canonical_dict(), sort_keys=True, separators=(",", ":"))

    def content_hash(self) -> str:
        """SHA-256 of the canonical content (excluding created_at)."""
        payload = self.canonical_json().encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        d = self.canonical_dict()
        d["created_at"] = self.created_at
        d["content_hash"] = self.content_hash()
        return d

    def is_authoritative(self) -> bool:
        """Always False — measurement never confers authority."""
        return False

    def permits_execution(self) -> bool:
        """Always False — measurement never permits execution."""
        return False

    def admits(self) -> bool:
        """Always False — measurement never performs admission."""
        return False

    def seals(self) -> bool:
        """Always False — measurement never seals."""
        return False
