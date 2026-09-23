"""Policy must not contaminate or escalate law artifacts.

STATUS: RESEARCH / EXPERIMENTAL
"""
from __future__ import annotations

from experimental.law.models import LawArtifact, LawStatus
from experimental.law.policy import PolicyMapping
from experimental.law.canonical import compute_content_hash, compute_law_canonical_hash


def test_policy_mapping_does_not_alter_artifact():
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
        "version": "v001",
        "content_hash": content_hash,
        "ingestion_event_id": "evt-001",
    }
    art = LawArtifact(
        **fields,
        retrieved_at="2026-09-23T10:00:00Z",
        canonical_hash=compute_law_canonical_hash(fields),
        content=content,
        status=LawStatus.INGEST_ONLY,
    )

    mapping = PolicyMapping(
        mapping_id="MAP-001",
        law_id=art.law_id,
        law_version=art.version,
        source_reference="s.1",
        policy_statement="REQUIRES_AUTHORITY",
        interpretation_basis="demo",
        mapping_hash="abc123",
    )

    # Mapping exists; artifact remains unchanged and still INGEST_ONLY
    assert art.status == LawStatus.INGEST_ONLY
    assert mapping.status == "INTERPRETIVE_MAPPING"
    assert mapping.law_id == art.law_id
    # No mutation path from PolicyMapping back into LawArtifact
