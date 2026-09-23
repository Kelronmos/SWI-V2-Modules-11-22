"""Adversarial authority tests for law registry.

STATUS: RESEARCH / EXPERIMENTAL
Composes with existing kernel require_authorization_for_action.
"""
from __future__ import annotations

import pytest

from experimental.law.models import (
    LawArtifact,
    LawLifecycleEvent,
    LawStatus,
    LifecycleEventType,
)
from experimental.law.canonical import compute_content_hash, compute_law_canonical_hash
from experimental.law.registry import LawRegistry, LawRegistryError
from experimental.law.authority import LAW_REGISTRY_ADMIN_SCOPE
from experimental.law.events import make_lifecycle_event
from swi_v2.kernel.errors import AuthorityHalt, AuthorityError


def _artifact(version: str = "v001") -> LawArtifact:
    content = "Section 1."
    content_hash = compute_content_hash(content)
    fields = {
        "law_id": "BW-DPA",
        "jurisdiction": "BW",
        "title": "Data Protection Act",
        "issuing_authority": "Parliament of Botswana",
        "source_uri": "https://example.bw/dpa",
        "publication_date": "2018-01-01",
        "effective_date": None,
        "version": version,
        "content_hash": content_hash,
        "ingestion_event_id": f"evt-{version}",
    }
    return LawArtifact(
        **fields,
        retrieved_at="2026-09-23T10:00:00Z",
        canonical_hash=compute_law_canonical_hash(fields),
        content=content,
        status=LawStatus.INGEST_ONLY,
    )


def _valid_event() -> LawLifecycleEvent:
    return make_lifecycle_event(
        event_type=LifecycleEventType.INGEST,
        law_id="BW-DPA",
        version="v001",
        actor="test",
        authority_scope=LAW_REGISTRY_ADMIN_SCOPE,
        previous_status=None,
        resulting_status=LawStatus.INGEST_ONLY,
        related_version=None,
    )


def test_missing_authorization_halts():
    reg = LawRegistry()
    with pytest.raises(AuthorityHalt):
        reg.ingest(
            _artifact(),
            authorization_present=False,
            authorization_scope=None,
        )


def test_wrong_scope_rejects():
    reg = LawRegistry()
    with pytest.raises(AuthorityError):
        reg.ingest(
            _artifact(),
            authorization_present=True,
            authorization_scope="SOME_OTHER_SCOPE",
        )


def test_correct_scope_allows():
    reg = LawRegistry()
    art = _artifact()
    stored = reg.ingest(
        art,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )
    assert stored == art


# ---------------------------------------------------------------------------
# append_event authority matrix (audit fix)
# ---------------------------------------------------------------------------

def test_append_event_missing_authority_halts_zero_writes():
    reg = LawRegistry()
    event = _valid_event()
    with pytest.raises(AuthorityHalt):
        reg.append_event(
            event,
            authorization_present=False,
            authorization_scope=None,
        )
    assert len(reg.events("BW-DPA", "v001")) == 0


def test_append_event_wrong_scope_rejects_zero_writes():
    reg = LawRegistry()
    event = _valid_event()
    with pytest.raises(AuthorityError):
        reg.append_event(
            event,
            authorization_present=True,
            authorization_scope="SOME_OTHER_SCOPE",
        )
    assert len(reg.events("BW-DPA", "v001")) == 0


def test_append_event_correct_scope_valid_hash_accepts():
    reg = LawRegistry()
    event = _valid_event()
    stored = reg.append_event(
        event,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )
    assert stored.event_id == event.event_id
    assert len(reg.events("BW-DPA", "v001")) == 1


def test_append_event_correct_scope_forged_hash_rejects_zero_writes():
    reg = LawRegistry()
    event = _valid_event()
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
        reg.append_event(
            forged,
            authorization_present=True,
            authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
        )
    assert len(reg.events("BW-DPA", "v001")) == 0


def test_append_event_correct_scope_empty_hash_rejects_zero_writes():
    reg = LawRegistry()
    event = LawLifecycleEvent(
        event_id="evt-empty-auth",
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
        reg.append_event(
            event,
            authorization_present=True,
            authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
        )
    assert len(reg.events("BW-DPA", "v001")) == 0
