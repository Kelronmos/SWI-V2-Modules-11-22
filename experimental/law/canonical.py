"""Canonical hashing for experimental law artefacts.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED
Re-uses swi_v2.kernel.canonical for deterministic hashing.
"""
from __future__ import annotations

from typing import Any, Mapping

from swi_v2.kernel.canonical import canonical_hash


def compute_content_hash(content: str) -> str:
    return canonical_hash({"content": content})


def law_integrity_material(fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "law_id": fields["law_id"],
        "jurisdiction": fields["jurisdiction"],
        "title": fields["title"],
        "issuing_authority": fields["issuing_authority"],
        "source_uri": fields["source_uri"],
        "publication_date": fields["publication_date"],
        "effective_date": fields.get("effective_date"),
        "version": fields["version"],
        "content_hash": fields["content_hash"],
        "ingestion_event_id": fields["ingestion_event_id"],
    }


def compute_law_canonical_hash(fields: Mapping[str, Any]) -> str:
    return canonical_hash(law_integrity_material(fields))


def lifecycle_event_material(event_fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event_fields["event_id"],
        "event_type": event_fields["event_type"],
        "law_id": event_fields["law_id"],
        "version": event_fields["version"],
        "actor": event_fields["actor"],
        "authority_scope": event_fields["authority_scope"],
        "created_at": event_fields["created_at"],
        "previous_status": event_fields.get("previous_status"),
        "resulting_status": event_fields["resulting_status"],
        "related_version": event_fields.get("related_version"),
    }


def compute_event_hash(event_fields: Mapping[str, Any]) -> str:
    return canonical_hash(lifecycle_event_material(event_fields))
