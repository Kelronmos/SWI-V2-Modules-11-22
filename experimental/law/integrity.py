"""Fail-closed integrity verification.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .canonical import compute_content_hash, compute_law_canonical_hash
from .models import LawArtifact


class IntegrityOutcome(str, Enum):
    PASS = "PASS"
    REJECT = "REJECT"
    HALT = "HALT"


@dataclass(frozen=True)
class IntegrityResult:
    outcome: IntegrityOutcome
    reason: str

    expected_content_hash: str
    observed_content_hash: str

    expected_canonical_hash: str
    observed_canonical_hash: str


def verify_integrity(artifact: LawArtifact) -> IntegrityResult:
    """Recompute hashes; any mismatch → REJECT (never repair)."""
    expected_content = compute_content_hash(artifact.content)

    fields = {
        "law_id": artifact.law_id,
        "jurisdiction": artifact.jurisdiction,
        "title": artifact.title,
        "issuing_authority": artifact.issuing_authority,
        "source_uri": artifact.source_uri,
        "publication_date": artifact.publication_date,
        "effective_date": artifact.effective_date,
        "version": artifact.version,
        "content_hash": expected_content,
        "ingestion_event_id": artifact.ingestion_event_id,
    }

    expected_canonical = compute_law_canonical_hash(fields)

    if (
        artifact.content_hash == expected_content
        and artifact.canonical_hash == expected_canonical
    ):
        return IntegrityResult(
            outcome=IntegrityOutcome.PASS,
            reason="hashes_match",
            expected_content_hash=expected_content,
            observed_content_hash=artifact.content_hash,
            expected_canonical_hash=expected_canonical,
            observed_canonical_hash=artifact.canonical_hash,
        )

    return IntegrityResult(
        outcome=IntegrityOutcome.REJECT,
        reason="hash_mismatch",
        expected_content_hash=expected_content,
        observed_content_hash=artifact.content_hash,
        expected_canonical_hash=expected_canonical,
        observed_canonical_hash=artifact.canonical_hash,
    )
