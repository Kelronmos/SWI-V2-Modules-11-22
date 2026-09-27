"""
Replay engine — deterministic recompute and compare.

Given the same input, target, weights, version and provenance
the replay MUST produce the same measurement result.

Mutation of any material input → mismatch.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .distance import DistanceCalculator
from .measurement import Measurement, MEASUREMENT_VERSION
from .vector import AlignmentVector


class ReplayError(ValueError):
    """Raised when replay cannot be performed or comparison fails unexpectedly."""


@dataclass(frozen=True, slots=True)
class ReplayResult:
    original_hash: str
    replay_hash: str
    match: bool
    original_distance: float
    replay_distance: float
    original_classification: str
    replay_classification: str


class ReplayEngine:
    """
    Recomputes a measurement from the original vector + calculator settings
    and compares content hashes / distances / classifications.
    """

    def replay(
        self,
        original: Measurement,
        calculator: Optional[DistanceCalculator] = None,
    ) -> ReplayResult:
        if not isinstance(original, Measurement):
            raise ReplayError("original must be a Measurement")

        calc = calculator or DistanceCalculator(
            target=original.target,
            weights=original.weights,
        )
        if calc.target != original.target:
            calc = DistanceCalculator(
                target=original.target,
                weights=original.weights,
            )

        recomputed = Measurement.create(
            vector=original.vector,
            calculator=calc,
            measurement_id=original.measurement_id,
        )

        match = (
            recomputed.content_hash() == original.content_hash()
            and abs(recomputed.distance - original.distance) < 1e-12
            and recomputed.classification == original.classification
        )

        return ReplayResult(
            original_hash=original.content_hash(),
            replay_hash=recomputed.content_hash(),
            match=match,
            original_distance=original.distance,
            replay_distance=recomputed.distance,
            original_classification=original.classification.value,
            replay_classification=recomputed.classification.value,
        )

    def assert_match(self, original: Measurement) -> None:
        result = self.replay(original)
        if not result.match:
            raise ReplayError(
                f"Replay mismatch: orig_hash={result.original_hash} "
                f"replay_hash={result.replay_hash}"
            )
