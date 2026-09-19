"""Determinism verification for dense Merkle and related seal digests."""
from __future__ import annotations

from swi_v2.kernel.merkle import MerkleTree, MerkleProof
from swi_v2.kernel.contracts import AdmittedInput
from swi_v2.kernel.seal import commitment_from_admitted, create_seal, verify_seal
from swi_v2.kernel.ed25519_sig import generate_keypair


def test_merkle_root_stable_across_reconstructions():
    leaves = [b"leaf-0", b"leaf-1", b"leaf-2", b"leaf-3"]
    roots = [MerkleTree(leaves).root for _ in range(20)]
    assert len(set(roots)) == 1


def test_merkle_proof_verify_stable():
    tree = MerkleTree([b"a", b"b", b"c"])
    proof = tree.prove(2)
    for _ in range(20):
        assert MerkleTree.verify(proof) is True
    bad = MerkleProof(proof.leaf, proof.index, proof.siblings, b"\xff" * 32)
    assert MerkleTree.verify(bad) is False


def test_commitment_deterministic_for_same_admitted():
    adm = AdmittedInput(
        payload={"k": 1},
        foundation_version="1.0-proposed",
        evidence_schema_version="1.0-proposed",
        evidence_id="e1",
        integrity_reference="a" * 64,
        source_reference="src",
        admitted_by="m11",
    )
    digests = [commitment_from_admitted(adm) for _ in range(20)]
    assert len(set(digests)) == 1


def test_seal_verify_repeatable():
    priv, pub = generate_keypair()
    adm = AdmittedInput(
        payload={"x": True},
        foundation_version="1.0-proposed",
        evidence_schema_version="1.0-proposed",
        evidence_id="e2",
        integrity_reference="b" * 64,
        source_reference="src",
        admitted_by="m11",
    )
    sealed = create_seal(adm, priv, pub)
    for _ in range(10):
        assert verify_seal(adm, sealed) is True
