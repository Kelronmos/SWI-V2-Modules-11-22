"""Lane B — frozen canonicalization for integrity digests (V2).

Contract id: canonicalization_v0 — algorithm matched to V1 swi_core.canonical.
STATUS: IMPLEMENTED / TESTED (not sealed).
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

CANONICALIZATION_VERSION = "canonicalization_v0"
_SEPARATORS = (",", ":")


def canonical_dumps(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=_SEPARATORS, default=str)


def canonical_bytes(obj: Any) -> bytes:
    return canonical_dumps(obj).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def foundation_integrity_material(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> dict[str, Any]:
    return {
        "payload": payload,
        "foundation_version": foundation_version,
        "evidence_schema_version": evidence_schema_version,
        "evidence_id": evidence_id,
        "source_reference": source_reference,
    }


def compute_integrity_reference(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> str:
    material = foundation_integrity_material(
        payload,
        foundation_version,
        evidence_schema_version,
        evidence_id,
        source_reference,
    )
    return canonical_hash(material)
