"""Experimental Common Sense monitoring and diagnostic boundary.

Research-only implementation.

This package does not provide execution authority, promotion authority,
seal authority, or authorization authority.
"""

from .monitor import (
    AuthorizationContext,
    CommonSenseDecision,
    CommonSenseMonitor,
    EvidenceRecord,
    HarmProfile,
    PatternObservation,
    RiskWeights,
    Sensitivity,
    SimulationCase,
)

__all__ = [
    "AuthorizationContext",
    "CommonSenseDecision",
    "CommonSenseMonitor",
    "EvidenceRecord",
    "HarmProfile",
    "PatternObservation",
    "RiskWeights",
    "Sensitivity",
    "SimulationCase",
]
