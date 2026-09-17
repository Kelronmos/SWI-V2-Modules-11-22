"""M11 post-admission cryptographic seal: AdmittedInput only + adversarial matrix."""
from __future__ import annotations

from dataclasses import replace

import pytest

from swi_v2.kernel.admission import admit_foundation_input, compute_integrity_reference
from swi_v2.kernel.contracts import AdmittedInput, FoundationEvidenceEnvelope
from swi_v2.kernel.ed25519_sig import generate_keypair
from swi_v2.kernel.merkle import MerkleTree
from swi_v2.kernel.seal import create_seal, verify_seal


def _envelope(**overrides):
    base = {
        "payload": {"text": "hello", "pipeline": "fixture"},
        "foundation_version": "1.0-proposed",
        "evidence_schema_version": "1.0-proposed",
        "evidence_id": "seal-test-001",
        "verification_status": "foundation_verified_test_fixture",
        "source_reference": "TEST FIXTURE / seal path",
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
    return base


def _admit(**overrides) -> AdmittedInput:
    return admit_foundation_input(_envelope(**overrides))


def test_happy_path_admit_seal_verify():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    assert verify_seal(admitted, sealed) is True


def test_cannot_seal_raw_dict():
    with pytest.raises(TypeError, match="AdmittedInput"):
        create_seal({"payload": "x"}, b"\x00" * 32, b"\x00" * 32)  # type: ignore[arg-type]


def test_cannot_seal_envelope_directly():
    env = FoundationEvidenceEnvelope(
        payload={"a": 1},
        foundation_version="1.0-proposed",
        evidence_schema_version="1.0-proposed",
        evidence_id="e",
        integrity_reference="0" * 64,
        verification_status="foundation_verified_test_fixture",
        source_reference="t",
    )
    with pytest.raises(TypeError, match="AdmittedInput"):
        create_seal(env, b"\x00" * 32, b"\x00" * 32)  # type: ignore[arg-type]


def test_payload_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, payload={"text": "TAMPERED"})
    assert verify_seal(tampered, sealed) is False


def test_evidence_id_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, evidence_id="OTHER-ID")
    assert verify_seal(tampered, sealed) is False


def test_integrity_reference_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, integrity_reference="ab" * 32)
    assert verify_seal(tampered, sealed) is False


def test_source_reference_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, source_reference="evil")
    assert verify_seal(tampered, sealed) is False


def test_foundation_version_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, foundation_version="9.9-evil")
    assert verify_seal(tampered, sealed) is False


def test_schema_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, evidence_schema_version="9.9-evil")
    assert verify_seal(tampered, sealed) is False


def test_admitted_by_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    tampered = replace(admitted, admitted_by="not_module_11")
    assert verify_seal(tampered, sealed) is False


def test_signature_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    sig = bytearray(sealed.signature)
    sig[0] ^= 0xFF
    bad = replace(sealed, signature=bytes(sig))
    assert verify_seal(admitted, bad) is False


def test_wrong_public_key_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    _, other_pub = generate_keypair()
    bad = replace(sealed, public_key=other_pub)
    assert verify_seal(admitted, bad) is False


def test_chain_hash_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    bad = replace(sealed, chain_hash="cd" * 32)
    assert verify_seal(admitted, bad) is False


def test_merkle_root_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub)
    bad = replace(sealed, merkle_root="ef" * 32)
    assert verify_seal(admitted, bad) is False


def test_previous_hash_mutation_fails():
    admitted = _admit()
    priv, pub = generate_keypair()
    sealed = create_seal(admitted, priv, pub, previous_chain_hash="aa" * 32)
    assert verify_seal(admitted, sealed) is True
    bad = replace(sealed, previous_chain_hash="bb" * 32)
    assert verify_seal(admitted, bad) is False


def test_canonical_key_order_stable():
    from swi_v2.kernel.seal import seal_canonicalize, seal_material_from_admitted

    a = _admit(payload={"b": 2, "a": 1})
    a2 = replace(a, payload={"a": 1, "b": 2})
    assert seal_canonicalize(seal_material_from_admitted(a)) == seal_canonicalize(
        seal_material_from_admitted(a2)
    )


def test_seal_rejects_bytes_in_payload():
    from swi_v2.kernel.seal import SealCanonicalizationError, seal_canonicalize

    with pytest.raises(SealCanonicalizationError):
        seal_canonicalize({"x": b"not-json"})


def test_merkle_tree_unit():
    leaves = [b"one", b"two", b"three"]
    tree = MerkleTree(leaves)
    for i in range(3):
        proof = tree.prove(i)
        assert MerkleTree.verify(proof) is True
