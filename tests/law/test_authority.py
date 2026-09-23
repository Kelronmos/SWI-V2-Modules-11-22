"""Adversarial authority tests for law registry.

STATUS: RESEARCH / EXPERIMENTAL
Composes with existing kernel require_authorization_for_action.
"""
from __future__ import annotations

import pytest

from experimental.law.models import LawArtifact, LawStatus
from experimental.law.canonical import compute_content_hash, compute_law_canonical_hash
from experimental.law.registry import LawRegistry
from experimental.law.authority import LAW_REGISTRY_ADMIN_SCOPE
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
