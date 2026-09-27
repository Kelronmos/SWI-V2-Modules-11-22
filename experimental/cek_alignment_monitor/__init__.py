"""
SWI-CEK Alignment Monitor — RESEARCH / EXPERIMENTAL

Classification: RESEARCH / EXPERIMENTAL
Production: NOT AUTHORIZED
Seal: NO
M11: UNTOUCHED
Runtime: NOT INTEGRATED

This package implements a pure measurement + provenance + observation layer.
It deliberately exposes NO path to:
  - ADMISSION
  - AUTHORITY
  - BINDING
  - EXECUTION
  - SEAL

SEEING ≠ AUTHORIZING
MEASURING ≠ PROVING TRUTH
EVIDENCE ≠ AUTHORITY
UNKNOWN ≠ PERMITTED
SIGNATURE ≠ AUTHORIZATION
TESTED ≠ SEALED
"""

from .vector import AlignmentVector, VectorValidationError
from .distance import DistanceCalculator, Classification, DistanceError
from .measurement import Measurement, MeasurementError
from .provenance import ProvenanceRecord, ProvenanceError
from .observation import CEKObservation, ObservationError
from .visibility import VisibilityLevel, VisibilityAnalyzer
from .findings import Finding, FindingKind
from .replay import ReplayEngine, ReplayError
from .monitor import AlignmentMonitor

__all__ = [
    "AlignmentVector",
    "VectorValidationError",
    "DistanceCalculator",
    "Classification",
    "DistanceError",
    "Measurement",
    "MeasurementError",
    "ProvenanceRecord",
    "ProvenanceError",
    "CEKObservation",
    "ObservationError",
    "VisibilityLevel",
    "VisibilityAnalyzer",
    "Finding",
    "FindingKind",
    "ReplayEngine",
    "ReplayError",
    "AlignmentMonitor",
]

__version__ = "0.1.0-experimental"
__status__ = "RESEARCH"
__production__ = False
__sealed__ = False
