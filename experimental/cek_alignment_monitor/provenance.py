"""
Provenance record — traceable origin of a measurement.

ORIGIN → INPUT → TRANSFORM → MEASUREMENT → RESULT

The provenance record is evidence *about* the measurement.
It does NOT become authority.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

from .measurement import Measurement


class ProvenanceError(ValueError):
    """Raised on invalid provenance construction (fail-closed)."""


PROVENANCE_VERSION = "cek-provenance-1.0-experimental"


@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    """
    Immutable provenance chain for a measurement.

    Explicitly contains no authorization, permit, or execution fields.
    """

    provenance_id: str
    measurement_id: str
    source_identifier: str
    origin_identifier: str
    input_hash: str
    output_hash: str
    transformation_description: str
    parent_reference: Optional[str] = None
    provenance_version: str = PROVENANCE_VERSION
    created_at: float = field(default_factory=time.time)

    @classmethod
    def from_measurement(
        cls,
        measurement: Measurement,
        source_identifier: str,
        origin_identifier: str,
        transformation_description: str = "vector→distance→classification",
        parent_reference: Optional[str] = None,
        provenance_id: Optional[str] = None,
    ) -> "ProvenanceRecord":
        if not isinstance(measurement, Measurement):
            raise ProvenanceError("measurement must be a Measurement instance")
        if not source_identifier or not origin_identifier:
            raise ProvenanceError("source_identifier and origin_identifier required")

        input_payload = json.dumps(
            {
                "vector": measurement.vector.as_dict(),
                "target": measurement.target.as_dict(),
                "weights": list(measurement.weights),
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        input_hash = hashlib.sha256(input_payload).hexdigest()
        output_hash = measurement.content_hash()

        return cls(
            provenance_id=provenance_id or str(uuid.uuid4()),
            measurement_id=measurement.measurement_id,
            source_identifier=source_identifier,
            origin_identifier=origin_identifier,
            input_hash=input_hash,
            output_hash=output_hash,
            transformation_description=transformation_description,
            parent_reference=parent_reference,
            provenance_version=PROVENANCE_VERSION,
            created_at=time.time(),
        )

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "provenance_id": self.provenance_id,
            "measurement_id": self.measurement_id,
            "source_identifier": self.source_identifier,
            "origin_identifier": self.origin_identifier,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "transformation_description": self.transformation_description,
            "parent_reference": self.parent_reference,
            "provenance_version": self.provenance_version,
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
        return d

    def is_authoritative(self) -> bool:
        return False

    def permits_execution(self) -> bool:
        return False
