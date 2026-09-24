"""Adversarial supersession tests.

STATUS: RESEARCH / EXPERIMENTAL
Most important proof: a later authorized state transition does not rewrite
the historical evidence artifact.
"""
from __future__ import annotations

import pytest

from experimental.law.models import LawArtifact, LawStatus, LifecycleEventType
from experimental.law.canonical import compute_content_hash, compute_law_canonical_hash
from experimental.law.registry import LawRegistry, LawRegistryError
from experimental.law.authority import LAW_REGISTRY_ADMIN_SCOPE
from experimental.law.events import make_lifecycle_event
from swi_v2.kernel.errors import AuthorityHalt


def _make_artifact(version: str, content: str = "Section 1. Example provision.") -> LawArtifact:
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


def test_supersede_does_not_rewrite_old_artifact():
    registry = LawRegistry()

    v1 = _make_artifact("v001")
    v2 = _make_artifact("v002", content="Section 1. Updated provision.")

    registry.ingest(
        v1,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )

    event = make_lifecycle_event(
        event_type=LifecycleEventType.SUPERSEDE,
        law_id="BW-DPA",
        version="v001",
        actor="test-actor",
        authority_scope=LAW_REGISTRY_ADMIN_SCOPE,
        previous_status=LawStatus.INGEST_ONLY,
        resulting_status=LawStatus.SUPERSEDED,
        related_version="v002",
    )

    registry.supersede(
        v1,
        v2,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
        event=event,
    )

    stored_v1 = registry.get("BW-DPA", "v001")
    stored_v2 = registry.get("BW-DPA", "v002")

    assert stored_v1 is not None
    assert stored_v1 == v1
    assert stored_v1.status == LawStatus.INGEST_ONLY
    assert stored_v2 == v2
    assert "v001" in registry.list_versions("BW-DPA")
    assert "v002" in registry.list_versions("BW-DPA")


def test_unauthorized_supersede_halts():
    registry = LawRegistry()
    v1 = _make_artifact("v001")
    v2 = _make_artifact("v002")

    registry.ingest(
        v1,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )

    event = make_lifecycle_event(
        event_type=LifecycleEventType.SUPERSEDE,
        law_id="BW-DPA",
        version="v001",
        actor="test-actor",
        authority_scope=LAW_REGISTRY_ADMIN_SCOPE,
        previous_status=LawStatus.INGEST_ONLY,
        resulting_status=LawStatus.SUPERSEDED,
        related_version="v002",
    )

    with pytest.raises(AuthorityHalt):
        registry.supersede(
            v1,
            v2,
            authorization_present=False,
            authorization_scope=None,
            event=event,
        )


def test_duplicate_version_rejected():
    registry = LawRegistry()
    v1 = _make_artifact("v001")

    registry.ingest(
        v1,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )

    with pytest.raises(LawRegistryError, match="cannot be overwritten"):
        registry.ingest(
            v1,
            authorization_present=True,
            authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
        )
