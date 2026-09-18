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


def _reject_nonfinite(obj: Any, path: str = "$") -> None:
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            raise ValueError(
                f"non-finite float at {path} is not allowed in canonical material"
            )
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _reject_nonfinite(v, f"{path}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            _reject_nonfinite(v, f"{path}[{i}]")


def canonical_dumps(obj: Any) -> str:
    _reject_nonfinite(obj)
    return json.dumps(
        obj, sort_keys=True, separators=_SEPARATORS, default=str, allow_nan=False
    )


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
