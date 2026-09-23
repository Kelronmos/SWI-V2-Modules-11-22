"""Adversarial integrity tests.

STATUS: RESEARCH / EXPERIMENTAL
"""
from __future__ import annotations

import pytest

from experimental.law.models import LawArtifact, LawStatus
from experimental.law.canonical import compute_content_hash, compute_law_canonical_hash
from experimental.law.integrity import verify_integrity, IntegrityOutcome


def _valid_artifact() -> LawArtifact:
    content = "Section 1. Example provision."
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
    return LawArtifact(
        **fields,
        retrieved_at="2026-09-23T10:00:00Z",
        canonical_hash=compute_law_canonical_hash(fields),
        content=content,
        status=LawStatus.INGEST_ONLY,
    )


def test_valid_artifact_passes():
    art = _valid_artifact()
    result = verify_integrity(art)
    assert result.outcome == IntegrityOutcome.PASS


def test_content_tampering_rejects():
    art = _valid_artifact()
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
        canonical_hash=art.canonical_hash,
        content=art.content + " TAMPERED",
        status=art.status,
        ingestion_event_id=art.ingestion_event_id,
    )
    result = verify_integrity(tampered)
    assert result.outcome == IntegrityOutcome.REJECT
    assert result.reason == "hash_mismatch"


def test_metadata_tampering_rejects():
    art = _valid_artifact()
    tampered = LawArtifact(
        law_id=art.law_id,
        jurisdiction="XX",  # changed
        title=art.title,
        issuing_authority=art.issuing_authority,
        source_uri=art.source_uri,
        publication_date=art.publication_date,
        effective_date=art.effective_date,
        version=art.version,
        retrieved_at=art.retrieved_at,
        content_hash=art.content_hash,
        canonical_hash=art.canonical_hash,
        content=art.content,
        status=art.status,
        ingestion_event_id=art.ingestion_event_id,
    )
    result = verify_integrity(tampered)
    assert result.outcome == IntegrityOutcome.REJECT


def test_hash_substitution_rejects():
    art = _valid_artifact()
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
        content_hash="0" * 64,  # substituted
        canonical_hash=art.canonical_hash,
        content=art.content,
        status=art.status,
        ingestion_event_id=art.ingestion_event_id,
    )
    result = verify_integrity(tampered)
    assert result.outcome == IntegrityOutcome.REJECT
