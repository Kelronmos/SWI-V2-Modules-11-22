"""Expanded adversarial surface for the experimental law lane.

STATUS: RESEARCH / EXPERIMENTAL
Covers remaining mutation surface beyond the core matrix.
"""
from __future__ import annotations

import pytest

from experimental.law.models import (
    LawArtifact,
    LawLifecycleEvent,
    LawStatus,
    LifecycleEventType,
)
from experimental.law.canonical import (
    compute_content_hash,
    compute_law_canonical_hash,
    compute_event_hash,
)
from experimental.law.integrity import verify_integrity, IntegrityOutcome
from experimental.law.registry import LawRegistry, LawRegistryError
from experimental.law.authority import LAW_REGISTRY_ADMIN_SCOPE
from experimental.law.events import make_lifecycle_event
from experimental.law.replay import LawReplayGuard
from swi_v2.kernel.errors import AuthorityHalt, AuthorityError, ReplayError


def _fields(
    *,
    version: str = "v001",
    content: str = "Section 1. Example provision.",
    **overrides,
) -> dict:
    content_hash = compute_content_hash(content)
    base = {
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
    base.update(overrides)
    return base


def _artifact(**kwargs) -> LawArtifact:
    content = kwargs.pop("content", "Section 1. Example provision.")
    fields = _fields(content=content, **kwargs)
    return LawArtifact(
        **fields,
        retrieved_at="2026-09-23T10:00:00Z",
        canonical_hash=compute_law_canonical_hash(fields),
        content=content,
        status=LawStatus.INGEST_ONLY,
    )


# ---------------------------------------------------------------------------
# 1. Every canonical metadata field tampering
# ---------------------------------------------------------------------------

CANONICAL_FIELDS = [
    "law_id",
    "jurisdiction",
    "title",
    "issuing_authority",
    "source_uri",
    "publication_date",
    "effective_date",
    "version",
    "ingestion_event_id",
]


@pytest.mark.parametrize("field", CANONICAL_FIELDS)
def test_each_canonical_field_tamper_rejects(field: str):
    art = _artifact()
    # Rebuild with one field altered after hash was computed
    kwargs = {
        "law_id": art.law_id,
        "jurisdiction": art.jurisdiction,
        "title": art.title,
        "issuing_authority": art.issuing_authority,
        "source_uri": art.source_uri,
        "publication_date": art.publication_date,
        "effective_date": art.effective_date,
        "version": art.version,
        "retrieved_at": art.retrieved_at,
        "content_hash": art.content_hash,
        "canonical_hash": art.canonical_hash,
        "content": art.content,
        "status": art.status,
        "ingestion_event_id": art.ingestion_event_id,
    }
    if field == "effective_date":
        kwargs[field] = "2099-01-01"
    else:
        kwargs[field] = kwargs[field] + "-TAMPERED"

    tampered = LawArtifact(**kwargs)
    result = verify_integrity(tampered)
    assert result.outcome == IntegrityOutcome.REJECT
    assert result.reason == "hash_mismatch"


# ---------------------------------------------------------------------------
# 2. Canonical-hash substitution
# ---------------------------------------------------------------------------

def test_canonical_hash_substitution_rejects():
    art = _artifact()
    tampered = LawArtifact(
        law_id=art.law_id,
        jurisdiction=art.jurisdiction,
        title=art.title,
        issuing_authority=art.issuing_authority,
        source_uri=art.source_uri,
        publication_date=art.publication_date,
        effective_date=art.effective_date,
        version=art.version,
        retrieved_at=art.retrieved_at,
        content_hash=art.content_hash,
        canonical_hash="f" * 64,  # substituted
        content=art.content,
        status=art.status,
        ingestion_event_id=art.ingestion_event_id,
    )
    result = verify_integrity(tampered)
    assert result.outcome == IntegrityOutcome.REJECT


# ---------------------------------------------------------------------------
# 3. Forged event-field mutation
# ---------------------------------------------------------------------------

def test_forged_event_field_mutation_rejects():
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
    # Mutate actor after hash was computed
    forged = LawLifecycleEvent(
        event_id=event.event_id,
        event_type=event.event_type,
        law_id=event.law_id,
        version=event.version,
        actor="FORGED-ACTOR",
        authority_scope=event.authority_scope,
        created_at=event.created_at,
        previous_status=event.previous_status,
        resulting_status=event.resulting_status,
        related_version=event.related_version,
        event_hash=event.event_hash,  # old hash
    )
    with pytest.raises(LawRegistryError, match="hash mismatch"):
        reg.append_event(forged)


# ---------------------------------------------------------------------------
# 4. Empty event hash
# ---------------------------------------------------------------------------

def test_empty_event_hash_rejects():
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


# ---------------------------------------------------------------------------
# 5. Event hash coverage of related_version
# ---------------------------------------------------------------------------

def test_related_version_in_event_hash_coverage():
    """Changing related_version without recomputing hash must fail."""
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
        related_version="v999",  # changed
        event_hash=event.event_hash,  # old hash
    )
    with pytest.raises(LawRegistryError, match="hash mismatch"):
        reg.append_event(forged)


# ---------------------------------------------------------------------------
# 6. Invalid supersession → zero new writes
# ---------------------------------------------------------------------------

def test_invalid_supersession_zero_writes():
    reg = LawRegistry()
    v1 = _artifact(version="v001")
    v2 = _artifact(version="v002", content="Updated.")

    reg.ingest(
        v1,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )

    bad_event = make_lifecycle_event(
        event_type=LifecycleEventType.SUPERSEDE,
        law_id="BW-DPA",
        version="v001",
        actor="test",
        authority_scope=LAW_REGISTRY_ADMIN_SCOPE,
        previous_status=LawStatus.INGEST_ONLY,
        resulting_status=LawStatus.SUPERSEDED,
        related_version="v999",  # mismatch
    )

    with pytest.raises(LawRegistryError):
        reg.supersede(
            v1,
            v2,
            authorization_present=True,
            authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
            event=bad_event,
        )

    assert reg.get("BW-DPA", "v002") is None
    assert reg.list_versions("BW-DPA") == ["v001"]
    assert len(reg.events("BW-DPA", "v001")) == 0


# ---------------------------------------------------------------------------
# 7. Old artifact field-for-field preservation
# ---------------------------------------------------------------------------

def test_old_artifact_field_for_field_preservation():
    reg = LawRegistry()
    v1 = _artifact(version="v001")
    v2 = _artifact(version="v002", content="Updated provision.")

    reg.ingest(
        v1,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )

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

    reg.supersede(
        v1,
        v2,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
        event=event,
    )

    stored = reg.get("BW-DPA", "v001")
    assert stored is not None
    assert stored == v1
    # Field-for-field
    assert stored.law_id == v1.law_id
    assert stored.jurisdiction == v1.jurisdiction
    assert stored.title == v1.title
    assert stored.issuing_authority == v1.issuing_authority
    assert stored.source_uri == v1.source_uri
    assert stored.publication_date == v1.publication_date
    assert stored.effective_date == v1.effective_date
    assert stored.version == v1.version
    assert stored.content_hash == v1.content_hash
    assert stored.canonical_hash == v1.canonical_hash
    assert stored.content == v1.content
    assert stored.status == LawStatus.INGEST_ONLY
    assert stored.ingestion_event_id == v1.ingestion_event_id
