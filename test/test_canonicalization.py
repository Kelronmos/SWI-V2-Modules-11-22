"""Lane B canonicalization tests (V2)."""
from __future__ import annotations

from swi_v2.kernel.admission import compute_integrity_reference as admit_compute
from swi_v2.kernel.canonical import (
    CANONICALIZATION_VERSION,
    canonical_dumps,
    canonical_hash,
    compute_integrity_reference,
)


def test_key_order_independent():
    assert canonical_hash({"b": 1, "a": 2}) == canonical_hash({"a": 2, "b": 1})


def test_compact_separators():
    assert canonical_dumps({"a": 1}) == '{"a":1}'


def test_matches_admission_delegate():
    args = ({"allowed": True}, "1.0-proposed", "1.0-proposed", "id", "src")
    assert compute_integrity_reference(*args) == admit_compute(*args)


def test_payload_mutation_changes_hash():
    h1 = compute_integrity_reference({"a": 1}, "1.0-proposed", "1.0-proposed", "e", "s")
    h2 = compute_integrity_reference({"a": 2}, "1.0-proposed", "1.0-proposed", "e", "s")
    assert h1 != h2


def test_version_constant():
    assert CANONICALIZATION_VERSION == "canonicalization_v0"
