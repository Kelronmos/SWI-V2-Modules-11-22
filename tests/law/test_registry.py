"""Registry append-only and overwrite resistance.

STATUS: RESEARCH / EXPERIMENTAL
"""
from __future__ import annotations

import pytest

from experimental.law.models import LawArtifact, LawStatus
from experimental.law.canonical import compute_content_hash, compute_law_canonical_hash
from experimental.law.registry import LawRegistry, LawRegistryError
from experimental.law.authority import LAW_REGISTRY_ADMIN_SCOPE


def _artifact(version: str, law_id: str = "BW-DPA") -> LawArtifact:
    content = f"Content for {version}"
    content_hash = compute_content_hash(content)
    fields = {
        "law_id": law_id,
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


def test_duplicate_version_rejected():
    reg = LawRegistry()
    art = _artifact("v001")
    reg.ingest(art, authorization_present=True, authorization_scope=LAW_REGISTRY_ADMIN_SCOPE)
    with pytest.raises(LawRegistryError, match="cannot be overwritten"):
        reg.ingest(art, authorization_present=True, authorization_scope=LAW_REGISTRY_ADMIN_SCOPE)


def test_list_versions_returns_all():
    reg = LawRegistry()
    reg.ingest(_artifact("v001"), authorization_present=True, authorization_scope=LAW_REGISTRY_ADMIN_SCOPE)
    reg.ingest(_artifact("v002"), authorization_present=True, authorization_scope=LAW_REGISTRY_ADMIN_SCOPE)
    assert reg.list_versions("BW-DPA") == ["v001", "v002"]
