"""
AlignmentVector — Stage 1 mathematical foundation.

V = (S, T, Q, E, Se, U)

S  = Safety
T  = Truthfulness
Q  = Quality
E  = Ethics
Se = Sentiment
U  = Engagement

Every coordinate MUST satisfy 0 ≤ v_i ≤ 1.

These are experimental measurement labels only.
A numerical alignment value is an experimental representation of an input signal.
It is NOT a proof of truthfulness, safety, ethical correctness, or human wellbeing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence, Tuple


DIMENSIONS: Tuple[str, ...] = ("S", "T", "Q", "E", "Se", "U")
DIM_COUNT = len(DIMENSIONS)


class VectorValidationError(ValueError):
    """Raised when a vector cannot be constructed (fail-closed)."""


@dataclass(frozen=True, slots=True)
class AlignmentVector:
    """
    Immutable 6-dimensional alignment vector with closed-interval validation.

    Coordinates are labelled measurement signals, not objective claims of
    safety, truth, ethics, or wellbeing.
    """

    S: float
    T: float
    Q: float
    E: float
    Se: float
    U: float

    def __post_init__(self) -> None:
        for name, value in self.as_dict().items():
            if not isinstance(value, (int, float)):
                raise VectorValidationError(
                    f"Dimension '{name}' must be numeric, got {type(value).__name__}"
                )
            if math.isnan(value):
                raise VectorValidationError(f"Dimension '{name}' is NaN (fail-closed)")
            if math.isinf(value):
                raise VectorValidationError(f"Dimension '{name}' is infinite (fail-closed)")
            if value < 0.0 or value > 1.0:
                raise VectorValidationError(
                    f"Dimension '{name}'={value} outside [0, 1] (fail-closed)"
                )

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_sequence(cls, values: Sequence[float]) -> "AlignmentVector":
        if len(values) != DIM_COUNT:
            raise VectorValidationError(
                f"Expected exactly {DIM_COUNT} coordinates, got {len(values)}"
            )
        cleaned = []
        for i, v in enumerate(values):
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                raise VectorValidationError(
                    f"Coordinate[{i}] must be int/float, got {type(v).__name__}"
                )
            cleaned.append(float(v))
        return cls(*cleaned)

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, float]) -> "AlignmentVector":
        missing = [d for d in DIMENSIONS if d not in mapping]
        extra = [k for k in mapping if k not in DIMENSIONS]
        if missing:
            raise VectorValidationError(f"Missing dimensions: {missing}")
        if extra:
            raise VectorValidationError(f"Unknown dimensions: {extra}")
        cleaned = {}
        for d in DIMENSIONS:
            v = mapping[d]
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                raise VectorValidationError(
                    f"Dimension '{d}' must be int/float, got {type(v).__name__}"
                )
            cleaned[d] = float(v)
        return cls(**cleaned)

    @classmethod
    def from_dict(cls, d: Mapping[str, float]) -> "AlignmentVector":
        return cls.from_mapping(d)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def as_tuple(self) -> Tuple[float, ...]:
        return (self.S, self.T, self.Q, self.E, self.Se, self.U)

    def as_dict(self) -> dict[str, float]:
        return {
            "S": self.S,
            "T": self.T,
            "Q": self.Q,
            "E": self.E,
            "Se": self.Se,
            "U": self.U,
        }

    def as_list(self) -> list[float]:
        return list(self.as_tuple())

    # ------------------------------------------------------------------
    # Deterministic serialization (for hashing / provenance)
    # ------------------------------------------------------------------

    def canonical_repr(self) -> str:
        """Stable, deterministic string representation for hashing."""
        parts = [f"{name}={getattr(self, name):.10f}" for name in DIMENSIONS]
        return "AlignmentVector(" + ",".join(parts) + ")"

    def __repr__(self) -> str:
        return self.canonical_repr()
