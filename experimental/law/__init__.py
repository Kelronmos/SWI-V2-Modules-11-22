"""SWI V2 experimental law-ingestion lane.

STATUS:
  RESEARCH / EXPERIMENTAL
  IMPLEMENTED (skeleton)
  NOT SEALED
  NOT PRODUCTION AUTHORIZED
  LEGAL COMPLIANCE NOT CLAIMED

Invariant preserved:
  DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
  LAW INGESTED ≠ VERIFIED ≠ ADMITTED ≠ AUTHORIZED ≠ EXECUTED

Law artifacts are immutable evidence.
Lifecycle changes are separate immutable events.
Nothing rewrites the original law record.
"""

from .models import LawArtifact, LawStatus, LawLifecycleEvent, LifecycleEventType
from .integrity import verify_integrity, IntegrityResult, IntegrityOutcome
from .registry import LawRegistry, LawRegistryError
from .authority import LawMutation, authorize_law_mutation, LAW_REGISTRY_ADMIN_SCOPE
from .replay import LawReplayGuard
from .policy import PolicyMapping

__all__ = [
    "LawArtifact",
    "LawStatus",
    "LawLifecycleEvent",
    "LifecycleEventType",
    "verify_integrity",
    "IntegrityResult",
    "IntegrityOutcome",
    "LawRegistry",
    "LawRegistryError",
    "LawMutation",
    "authorize_law_mutation",
    "LAW_REGISTRY_ADMIN_SCOPE",
    "LawReplayGuard",
    "PolicyMapping",
]
