"""SWI closed transition / repair engine.

STATUS:
  RESEARCH / EXPERIMENTAL
  DESIGN LOCKED
  NOT SEALED
  NOT PRODUCTION AUTHORIZED
"""
from experimental.repair.transition_engine import (
    TransitionDecision,
    TransitionResult,
    TransitionContext,
    StateRegistry,
    TransitionRegistry,
    GateSpec,
    attempt_transition,
    DEFAULT_STATES,
    DEFAULT_TRANSITIONS,
)

__all__ = [
    "TransitionDecision",
    "TransitionResult",
    "TransitionContext",
    "StateRegistry",
    "TransitionRegistry",
    "GateSpec",
    "attempt_transition",
    "DEFAULT_STATES",
    "DEFAULT_TRANSITIONS",
]
