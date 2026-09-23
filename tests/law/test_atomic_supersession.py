"""Atomic supersession: no partial write on validation failure.

STATUS: RESEARCH / EXPERIMENTAL
"""
from __future__ import annotations

import pytest

from experimental.law.models import LawArtifact, LawStatus, LifecycleEventType
from experimental.law.canonical import compute_content_hash, compute_law_canonical_hash
from experimental.law.registry import LawRegistry, LawRegistryError
from experimental.law.authority import LAW_REGISTRY_ADMIN_SCOPE
from experimental.law.events import make_lifecycle_event


def _artifact(version: str, content: str = "Section 1.") -> LawArtifact:
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


def test_invalid_event_leaves_no_partial_write():
    reg = LawRegistry()
    v1 = _artifact("v001")
    v2 = _artifact("v002", content="Updated.")

    reg.ingest(
        v1,
        authorization_present=True,
        authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
    )

    # Event claims wrong related_version → must reject before any write
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

    with pytest.raises(LawRegistryError, match="supersession event mismatch"):
        reg.supersede(
            v1,
            v2,
            authorization_present=True,
            authorization_scope=LAW_REGISTRY_ADMIN_SCOPE,
            event=bad_event,
        )

    # v002 must NOT have been stored
    assert reg.get("BW-DPA", "v002") is None
    assert reg.list_versions("BW-DPA") == ["v001"]
    # v001 remains exactly as ingested
    assert reg.get("BW-DPA", "v001") == v1
