"""
Distance calculation and experimental classification.

Weighted Euclidean distance:

    D(V, V*) = sqrt( sum_i  w_i * (v_i - v_i*)^2 )

Weights are normalized so the result is deterministic.
Thresholds are EXPERIMENTAL labels only — they are NOT
safety, legal, authorization, or production thresholds.

Classification never becomes PERMIT / BLOCK / EXECUTE.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence, Tuple

from .vector import AlignmentVector, DIMENSIONS, DIM_COUNT, VectorValidationError


class DistanceError(ValueError):
    """Raised on invalid distance / weight configuration (fail-closed)."""


class Classification(str, Enum):
    """Experimental drift labels. NEVER treated as authority."""

    STABLE = "STABLE"
    MODERATE_DRIFT = "MODERATE_DRIFT"
    HIGH_DRIFT = "HIGH_DRIFT"


# Default experimental thresholds (explicitly labelled experimental)
DEFAULT_MODERATE_THRESHOLD = 0.25
DEFAULT_HIGH_THRESHOLD = 0.55

# Default equal weights (will be normalized)
DEFAULT_WEIGHTS: Tuple[float, ...] = (1.0,) * DIM_COUNT


@dataclass(frozen=True, slots=True)
class DistanceResult:
    distance: float
    classification: Classification
    weights: Tuple[float, ...]
    moderate_threshold: float
    high_threshold: float


class DistanceCalculator:
    """
    Pure mathematical distance + experimental classification.

    No authorization, admission, execution, or sealing interface.
    """

    def __init__(
        self,
        target: AlignmentVector | None = None,
        weights: Sequence[float] | Mapping[str, float] | None = None,
        moderate_threshold: float = DEFAULT_MODERATE_THRESHOLD,
        high_threshold: float = DEFAULT_HIGH_THRESHOLD,
    ) -> None:
        self.target = target or AlignmentVector(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
        self.weights = self._normalize_weights(weights)
        self._validate_thresholds(moderate_threshold, high_threshold)
        self.moderate_threshold = float(moderate_threshold)
        self.high_threshold = float(high_threshold)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compute(self, vector: AlignmentVector) -> DistanceResult:
        if not isinstance(vector, AlignmentVector):
            raise DistanceError("vector must be an AlignmentVector instance")

        diffs = [
            (getattr(vector, d) - getattr(self.target, d)) ** 2
            for d in DIMENSIONS
        ]
        weighted_sum = sum(w * diff for w, diff in zip(self.weights, diffs))
        if weighted_sum < 0:  # numerical guard (should not occur)
            raise DistanceError("negative weighted sum (numerical anomaly)")
        distance = math.sqrt(weighted_sum)

        classification = self._classify(distance)
        return DistanceResult(
            distance=distance,
            classification=classification,
            weights=self.weights,
            moderate_threshold=self.moderate_threshold,
            high_threshold=self.high_threshold,
        )

    def distance(self, vector: AlignmentVector) -> float:
        return self.compute(vector).distance

    def classify(self, vector: AlignmentVector) -> Classification:
        return self.compute(vector).classification

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _classify(self, distance: float) -> Classification:
        if distance < self.moderate_threshold:
            return Classification.STABLE
        if distance < self.high_threshold:
            return Classification.MODERATE_DRIFT
        return Classification.HIGH_DRIFT

    @staticmethod
    def _normalize_weights(
        weights: Sequence[float] | Mapping[str, float] | None,
    ) -> Tuple[float, ...]:
        if weights is None:
            raw = list(DEFAULT_WEIGHTS)
        elif isinstance(weights, Mapping):
            missing = [d for d in DIMENSIONS if d not in weights]
            extra = [k for k in weights if k not in DIMENSIONS]
            if missing:
                raise DistanceError(f"Missing weight dimensions: {missing}")
            if extra:
                raise DistanceError(f"Unknown weight dimensions: {extra}")
            raw = [float(weights[d]) for d in DIMENSIONS]
        else:
            raw = [float(w) for w in weights]
            if len(raw) != DIM_COUNT:
                raise DistanceError(
                    f"Expected {DIM_COUNT} weights, got {len(raw)}"
                )

        for i, w in enumerate(raw):
            if math.isnan(w):
                raise DistanceError(f"Weight[{i}] is NaN (fail-closed)")
            if math.isinf(w):
                raise DistanceError(f"Weight[{i}] is infinite (fail-closed)")
            if w < 0.0:
                raise DistanceError(f"Weight[{i}]={w} is negative (fail-closed)")

        total = sum(raw)
        if total == 0.0:
            raise DistanceError("Total weight is zero (fail-closed)")

        normalized = tuple(w / total for w in raw)
        return normalized

    @staticmethod
    def _validate_thresholds(moderate: float, high: float) -> None:
        for name, val in (("moderate", moderate), ("high", high)):
            if math.isnan(val) or math.isinf(val):
                raise DistanceError(f"{name}_threshold is NaN/Inf (fail-closed)")
            if val < 0.0:
                raise DistanceError(f"{name}_threshold must be >= 0")
        if moderate >= high:
            raise DistanceError(
                "moderate_threshold must be strictly less than high_threshold"
            )
