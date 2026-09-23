"""Helpers for constructing immutable lifecycle events.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from .canonical import compute_event_hash
from .models import LawLifecycleEvent, LawStatus, LifecycleEventType


def make_lifecycle_event(
    *,
    event_type: LifecycleEventType,
    law_id: str,
    version: str,
    actor: str,
    authority_scope: str,
    previous_status: Optional[LawStatus],
    resulting_status: LawStatus,
    related_version: Optional[str] = None,
) -> LawLifecycleEvent:
    event_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    fields = {
        "event_id": event_id,
        "event_type": event_type.value,
        "law_id": law_id,
        "version": version,
        "actor": actor,
        "authority_scope": authority_scope,
        "created_at": created_at,
        "previous_status": previous_status.value if previous_status else None,
        "resulting_status": resulting_status.value,
        "related_version": related_version,
    }

    event_hash = compute_event_hash(fields)

    return LawLifecycleEvent(
        event_id=event_id,
        event_type=event_type,
        law_id=law_id,
        version=version,
        actor=actor,
        authority_scope=authority_scope,
        created_at=created_at,
        previous_status=previous_status,
        resulting_status=resulting_status,
        related_version=related_version,
        event_hash=event_hash,
    )
