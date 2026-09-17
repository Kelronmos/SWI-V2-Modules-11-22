"""Boundary attacks on post-admission seal (proof substitution, domain, types)."""
from __future__ import annotations

from dataclasses import replace

import pytest

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.ed25519_sig import generate_keypair
from swi_v2.kernel.seal import (
    SealCanonicalizationError,
    create_seal,
    seal_canonicalize,
    verify_seal,
    _canonical_admitted_input,
)


def _admit(**overrides):
    base = {
        "payload": {"text": "hello", "n": 1},
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "bound-001",
        "verification_status": "foundation_verified_test_fixture",
        "source_reference": "boundary",
    }
    base.update(overrides)
    if "integrity_reference" not in base:
        base["integrity_reference"] = compute_integrity_reference(
            payload=base["payload"],
            foundation_version=base["foundation_version"],
            evidence_schema_version=base["evidence_schema_version"],
            evidence_id=base["evidence_id"],
            source_reference=base["source_reference"],
        )
    return admit_foundation_input(base)


def test_proof_from_other_evidence_rejected():
    a = _admit(evidence_id="bound-001")
    b = _admit(evidence_id="bound-002", payload={"text": "other"})
    priv, pub = generate_keypair()
    sa = create_seal(a, priv, pub)
    sb = create_seal(b, priv, pub)
    mixed = replace(sa, merkle_proof=sb.merkle_proof, merkle_root=sb.merkle_root)
    assert verify_seal(a, mixed) is False


def test_canonical_key_order_via_helper():
    a = _admit(payload={"b": 2, "a": 1})
    a2 = replace(a, payload={"a": 1, "b": 2})
    assert _canonical_admitted_input(a) == _canonical_admitted_input(a2)


def test_reject_bytes_in_seal_canonicalize():
    with pytest.raises(SealCanonicalizationError):
        seal_canonicalize({"x": b"no"})


def test_wrong_domain_on_sealed_fails():
    a = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(a, priv, pub)
    bad = replace(sealed, domain="OTHER-DOMAIN")
    assert verify_seal(a, bad) is False


def test_reconstructed_proof_matches_create():
    a = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(a, priv, pub)
    assert verify_seal(a, sealed) is True
