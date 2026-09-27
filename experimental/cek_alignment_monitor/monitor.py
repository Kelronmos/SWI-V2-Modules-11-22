"""
AlignmentMonitor facade.

Provides a single entry point for:
  - vector construction
  - distance / classification
  - measurement
  - provenance
  - observation
  - visibility (including hidden-edge demo)
  - findings
  - replay

NO authorization, admission, execution or sealing methods exist.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from .distance import Classification, DistanceCalculator, DistanceResult
from .findings import Finding
from .measurement import Measurement
from .observation import CEKObservation
from .provenance import ProvenanceRecord
from .replay import ReplayEngine, ReplayResult
from .vector import AlignmentVector
from .visibility import VisibilityAnalyzer, VisibilityLevel, VisibilityReport


class AlignmentMonitor:
    """
    Experimental CEK Alignment Monitor.

    RESEARCH / EXPERIMENTAL only.
    Production: NOT AUTHORIZED
    Seal: NO
    M11: UNTOUCHED
    """

    def __init__(
        self,
        target: Optional[AlignmentVector] = None,
        weights: Optional[Sequence[float] | Mapping[str, float]] = None,
        moderate_threshold: float = 0.25,
        high_threshold: float = 0.55,
    ) -> None:
        self.calculator = DistanceCalculator(
            target=target,
            weights=weights,
            moderate_threshold=moderate_threshold,
            high_threshold=high_threshold,
        )
        self.visibility = VisibilityAnalyzer()
        self.replay_engine = ReplayEngine()

    def measure(
        self,
        vector: AlignmentVector | Sequence[float] | Mapping[str, float],
        measurement_id: Optional[str] = None,
    ) -> Measurement:
        if isinstance(vector, AlignmentVector):
            v = vector
        elif isinstance(vector, Mapping):
            v = AlignmentVector.from_mapping(vector)
        else:
            v = AlignmentVector.from_sequence(vector)
        return Measurement.create(v, self.calculator, measurement_id=measurement_id)

    def distance(self, vector: AlignmentVector | Sequence[float] | Mapping[str, float]) -> float:
        m = self.measure(vector)
        return m.distance

    def classify(
        self, vector: AlignmentVector | Sequence[float] | Mapping[str, float]
    ) -> Classification:
        m = self.measure(vector)
        return m.classification

    def observe(
        self,
        vector: AlignmentVector | Sequence[float] | Mapping[str, float],
        source_identifier: str = "experimental",
        origin_identifier: str = "cek_monitor",
        context: Optional[Mapping[str, Any]] = None,
        evidence_reference: Optional[str] = None,
        visibility_steps: Optional[list[tuple[str, VisibilityLevel, str]]] = None,
    ) -> CEKObservation:
        measurement = self.measure(vector)
        provenance = ProvenanceRecord.from_measurement(
            measurement,
            source_identifier=source_identifier,
            origin_identifier=origin_identifier,
        )
        return CEKObservation.create(
            measurement=measurement,
            provenance=provenance,
            context=context,
            evidence_reference=evidence_reference,
            visibility_steps=visibility_steps,
        )

    def finding_from_observation(self, observation: CEKObservation) -> Finding:
        return Finding.from_observation(observation)

    def hidden_edge_demo(self) -> VisibilityReport:
        """Canonical demonstration of the visibility frontier."""
        return self.visibility.hidden_edge_demo()

    def full_hidden_edge_observation(self) -> tuple[CEKObservation, Finding, VisibilityReport]:
        """
        End-to-end demonstration that produces the expected Stage-2 proof:

        ORIGIN             = VISIBLE
        CONTEXT            = VISIBLE
        EVIDENCE           = VISIBLE
        ADMISSION          = VISIBLE
        NEXT EDGE          = UNKNOWN
        EXECUTION          = OBSERVED
        AUTHORITY          = NOT ESTABLISHED
        VISIBILITY FRONTIER= UNKNOWN EDGE
        """
        steps = [
            ("ORIGIN", VisibilityLevel.OBSERVABLE, "request origin visible"),
            ("CONTEXT", VisibilityLevel.OBSERVABLE, "context captured"),
            ("EVIDENCE", VisibilityLevel.TRACEABLE, "evidence reference present"),
            ("ADMISSION", VisibilityLevel.TRACEABLE, "admission record present"),
            ("NEXT_EDGE", VisibilityLevel.UNKNOWN, "hidden / uninstrumented transition"),
            ("EXECUTION", VisibilityLevel.OBSERVABLE, "execution outcome observed"),
        ]
        obs = self.observe(
            vector=[0.9, 0.9, 0.9, 0.9, 0.9, 0.9],
            source_identifier="hidden_edge_demo",
            origin_identifier="cek_stage2",
            context={"demo": "hidden_edge"},
            evidence_reference="demo-evidence-ref",
            visibility_steps=steps,
        )
        finding = self.finding_from_observation(obs)
        report = obs.visibility
        return obs, finding, report

    def replay(self, measurement: Measurement) -> ReplayResult:
        return self.replay_engine.replay(measurement, self.calculator)

    def authority_established(self) -> bool:
        return False

    def execution_permitted(self) -> bool:
        return False

    def admits(self) -> bool:
        return False

    def seals(self) -> bool:
        return False
