"""Lifecycle event hash verification.

STATUS: RESEARCH / EXPERIMENTAL
"""
from __future__ import annotations

import pytest

from experimental.law.models import (
    LawLifecycleEvent,
    LawStatus,
    LifecycleEventType,
)
from experimental.law.registry import LawRegistry, LawRegistryError
from experimental.law.events import make_lifecycle_event
from experimental.law.authority import LAW_REGISTRY_ADMIN_SCOPE


def test_valid_event_accepted():
    reg = LawRegistry()
    event = make_lifecycle_event(
        event_type=LifecycleEventType.SUPERSEDE,
        law_id="BW-DPA",
        version="v001",
        actor="test",
        authority_scope=LAW_REGISTRY_ADMIN_SCOPE,
        previous_status=LawStatus.INGEST_ONLY,
        resulting_status=LawStatus.SUPERSEDED,
        related_version="v002",
    )
    stored = reg.append_event(event)
    assert stored.event_id == event.event_id


def test_forged_hash_rejected():
    reg = LawRegistry()
    event = make_lifecycle_event(
        event_type=LifecycleEventType.SUPERSEDE,
        law_id="BW-DPA",
        version="v001",
        actor="test",
        authority_scope=LAW_REGISTRY_ADMIN_SCOPE,
        previous_status=LawStatus.INGEST_ONLY,
        resulting_status=LawStatus.SUPERSEDED,
        related_version="v002",
    )
    # Forge a different hash while keeping all other fields
    forged = LawLifecycleEvent(
        event_id=event.event_id,
        event_type=event.event_type,
        law_id=event.law_id,
        version=event.version,
        actor=event.actor,
        authority_scope=event.authority_scope,
        created_at=event.created_at,
        previous_status=event.previous_status,
        resulting_status=event.resulting_status,
        related_version=event.related_version,
        event_hash="0" * 64,
    )
    with pytest.raises(LawRegistryError, match="hash mismatch"):
        reg.append_event(forged)


def test_empty_hash_rejected():
    reg = LawRegistry()
    event = LawLifecycleEvent(
        event_id="evt-empty",
        event_type=LifecycleEventType.INGEST,
        law_id="BW-DPA",
        version="v001",
        actor="test",
        authority_scope=LAW_REGISTRY_ADMIN_SCOPE,
        created_at="2026-09-23T10:00:00Z",
        previous_status=None,
        resulting_status=LawStatus.INGEST_ONLY,
        related_version=None,
        event_hash="",
    )
    with pytest.raises(LawRegistryError, match="must be hashed"):
        reg.append_event(event)
