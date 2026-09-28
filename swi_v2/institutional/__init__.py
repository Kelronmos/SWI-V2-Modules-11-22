"""Institutional multi-level demonstration — EXPERIMENTAL.

STATUS: DESIGN / CONTROLLED DEVELOPMENT
S9: NOT PROVEN (unchanged)
Production: NOT AUTHORIZED
Does not issue human authority, seal, or promote production.
Organizational levels are NOT automatically authority levels.
"""
from .models import OrganizationNode, AuthorityRecord, AccessRequest, Case
from .decision import evaluate_access
from .demo import run_synthetic_demo

__all__ = [
    "OrganizationNode",
    "AuthorityRecord",
    "AccessRequest",
    "Case",
    "evaluate_access",
    "run_synthetic_demo",
]
