"""Shared golden vectors (must match V1 canonicalization_v0)."""
from __future__ import annotations

import json
from pathlib import Path

from swi_v2.kernel.canonical import canonical_hash

_VECTORS = Path(__file__).resolve().parent / "fixtures" / "canonical_vectors.json"


def test_golden_vectors_match_v1():
    data = json.loads(_VECTORS.read_text(encoding="utf-8"))
    for row in data:
        assert canonical_hash(row["input"]) == row["expected_digest"], row["name"]
