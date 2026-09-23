"""Controlled ingestion entry point.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from .models import LawArtifact, LawStatus
from .canonical import compute_content_hash, compute_law_canonical_hash
from .registry import LawRegistry
from .replay import LawReplayGuard


def ingest_law(
    *,
    registry: LawRegistry,
    replay_guard: LawReplayGuard,
    law_id: str,
    jurisdiction: str,
    title: str,
    issuing_authority: str,
    source_uri: str,
    publication_date: str,
    content: str,
    version: str,
    effective_date: Optional[str] = None,
    authorization_present: bool,
    authorization_scope: Optional[str],
) -> LawArtifact:
    """Single controlled path from source text → immutable artefact."""
    event_id = str(uuid4())
    replay_guard.check_and_record(event_id)

    content_hash = compute_content_hash(content)
    fields = {
        "law_id": law_id,
        "jurisdiction": jurisdiction,
        "title": title,
        "issuing_authority": issuing_authority,
        "source_uri": source_uri,
        "publication_date": publication_date,
        "effective_date": effective_date,
        "version": version,
        "content_hash": content_hash,
        "ingestion_event_id": event_id,
    }
    canonical_hash = compute_law_canonical_hash(fields)

    artifact = LawArtifact(
        law_id=law_id,
        jurisdiction=jurisdiction,
        title=title,
        issuing_authority=issuing_authority,
        source_uri=source_uri,
        publication_date=publication_date,
        effective_date=effective_date,
        version=version,
        retrieved_at=datetime.now(timezone.utc).isoformat(),
        content_hash=content_hash,
        canonical_hash=canonical_hash,
        content=content,
        status=LawStatus.INGEST_ONLY,
        ingestion_event_id=event_id,
    )

    return registry.ingest(
        artifact,
        authorization_present=authorization_present,
        authorization_scope=authorization_scope,
    )
