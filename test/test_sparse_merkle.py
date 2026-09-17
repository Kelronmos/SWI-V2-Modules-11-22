"""Sparse Merkle Tree + compact sparse proof tests."""
from __future__ import annotations

from swi_v2.kernel.sparse_merkle import (
    SparseMerkleTree,
    verify_compact_sparse_proof,
)


def test_empty_root_stable():
    t = SparseMerkleTree(depth=8)
    r1 = t.root()
    r2 = t.empty_root
    assert r1 == r2


def test_set_changes_root():
    t = SparseMerkleTree(depth=8)
    r0 = t.root()
    t.set(b"\x01", b"value-a")
    assert t.root() != r0


def test_membership_proof():
    t = SparseMerkleTree(depth=8)
    t.set(b"\x02", b"hello")
    proof = t.prove(b"\x02")
    assert proof.membership is True
    assert proof.value == b"hello"
    assert verify_compact_sparse_proof(proof) is True


def test_non_membership_proof():
    t = SparseMerkleTree(depth=8)
    t.set(b"\x03", b"present")
    proof = t.prove(b"\x04")  # absent
    assert proof.membership is False
    assert proof.value is None
    assert verify_compact_sparse_proof(proof) is True


def test_tampered_value_fails():
    t = SparseMerkleTree(depth=8)
    t.set(b"\x05", b"real")
    proof = t.prove(b"\x05")
    from dataclasses import replace

    bad = replace(proof, value=b"fake")
    assert verify_compact_sparse_proof(bad) is False


def test_tampered_root_fails():
    t = SparseMerkleTree(depth=8)
    t.set(b"\x06", b"x")
    proof = t.prove(b"\x06")
    from dataclasses import replace

    bad = replace(proof, root=b"\x00" * 32)
    assert verify_compact_sparse_proof(bad) is False


def test_compact_mask_omits_empty():
    t = SparseMerkleTree(depth=8)
    t.set(b"\x07", b"solo")
    proof = t.prove(b"\x07")
    assert proof.sibling_mask != (1 << 8) - 1 or len(proof.siblings) <= 8
    assert len(proof.siblings) == bin(proof.sibling_mask).count("1")
    assert verify_compact_sparse_proof(proof) is True


def test_delete_restores_empty_membership():
    t = SparseMerkleTree(depth=8)
    t.set(b"\x08", b"tmp")
    t.delete(b"\x08")
    proof = t.prove(b"\x08")
    assert proof.membership is False
    assert verify_compact_sparse_proof(proof) is True


def test_two_keys_independent_proofs():
    t = SparseMerkleTree(depth=8)
    t.set(b"\x0a", b"A")
    t.set(b"\xff", b"B")
    p_a = t.prove(b"\x0a")
    p_b = t.prove(b"\xff")
    assert verify_compact_sparse_proof(p_a)
    assert verify_compact_sparse_proof(p_b)
    assert p_a.root == p_b.root == t.root()
