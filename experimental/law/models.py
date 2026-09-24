"""SWI experimental law artefact models.

STATUS:
  RESEARCH / EXPERIMENTAL
  IMPLEMENTED
  NOT SEALED
  NOT PRODUCTION AUTHORIZED
  LEGAL COMPLIANCE NOT CLAIMED
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LawStatus(str, Enum):
    INGEST_ONLY = "INGEST_ONLY"
    VERIFIED = "VERIFIED"
    QUARANTINED = "QUARANTINED"
    SUPERSEDED = "SUPERSEDED"
    REVOKED = "REVOKED"


class LifecycleEventType(str, Enum):
    INGEST = "INGEST"
    VERIFY = "VERIFY"
    SUPERSEDE = "SUPERSEDE"
    QUARANTINE = "QUARANTINE"
    REVOKE = "REVOKE"


@dataclass(frozen=True)
class LawArtifact:
    """Immutable representation of one retrieved legal-source version.

    status describes state at creation only.
    It is NOT an authorization.
    """

    law_id: str
    jurisdiction: str
    title: str
    issuing_authority: str
    source_uri: str
    publication_date: str
    effective_date: Optional[str]
    version: str
    retrieved_at: str

    content_hash: str
    canonical_hash: str
    content: str

    ingestion_event_id: str

    status: LawStatus = LawStatus.INGEST_ONLY

    def __post_init__(self) -> None:
        required = {
            "law_id": self.law_id,
            "jurisdiction": self.jurisdiction,
            "title": self.title,
            "version": self.version,
            "ingestion_event_id": self.ingestion_event_id,
        }
        for name, value in required.items():
            if not value:
                raise ValueError(f"{name} is required")


@dataclass(frozen=True)
class LawLifecycleEvent:
    """Immutable event describing a registry transition.

    Lifecycle changes never rewrite the original LawArtifact.
    """

    event_id: str
    event_type: LifecycleEventType

    law_id: str
    version: str

    actor: str
    authority_scope: str

    created_at: str

    previous_status: Optional[LawStatus]
    resulting_status: LawStatus

    related_version: Optional[str] = None

    event_hash: str = ""
