"""
Sparse Merkle Tree (SMT) with compact sparse proofs.

STATUS: IMPLEMENTED / TESTED (research primitive)
Does NOT replace dense merkle.py used in M11 post-admission seal.
Does NOT implement CRTG, consensus, ZK, or production key custody.

Key space: 2^depth positions (MSB-first key bits).
Empty subtrees use precomputed empty hashes.
Compact proofs omit empty siblings via sibling_mask.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


def _h(*parts: bytes) -> bytes:
    return hashlib.sha256(b"".join(parts)).digest()


def _leaf_hash(key: bytes, value: bytes) -> bytes:
    return _h(b"SWI-SMT-LEAF\x00", key, value)


def _node_hash(left: bytes, right: bytes) -> bytes:
    return _h(b"SWI-SMT-NODE\x00", left, right)


def _empty_hashes(depth: int) -> Tuple[bytes, ...]:
    e = [b""] * (depth + 1)
    e[depth] = _h(b"SWI-SMT-EMPTY-LEAF\x00")
    for i in range(depth - 1, -1, -1):
        e[i] = _node_hash(e[i + 1], e[i + 1])
    return tuple(e)


def _key_bits(key: bytes, depth: int) -> List[int]:
    need = (depth + 7) // 8
    if len(key) < need:
        key = key + b"\x00" * (need - len(key))
    bits: List[int] = []
    for i in range(depth):
        bits.append((key[i // 8] >> (7 - (i % 8))) & 1)
    return bits


@dataclass(frozen=True)
class CompactSparseProof:
    """Membership or non-membership proof with empty siblings elided."""

    key: bytes
    value: Optional[bytes]
    depth: int
    siblings: Tuple[bytes, ...]
    sibling_mask: int
    root: bytes
    membership: bool


class SparseMerkleTree:
    def __init__(self, depth: int = 16):
        if depth < 1 or depth > 256:
            raise ValueError("depth must be in 1..256")
        self.depth = depth
        self._empty = _empty_hashes(depth)
        self._values: Dict[bytes, bytes] = {}

    @property
    def empty_root(self) -> bytes:
        return self._empty[0]

    def root(self) -> bytes:
        return self._compute_root()

    def set(self, key: bytes, value: bytes) -> None:
        key = self._normalize_key(key)
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("value must be bytes")
        self._values[key] = bytes(value)

    def delete(self, key: bytes) -> None:
        self._values.pop(self._normalize_key(key), None)

    def get(self, key: bytes) -> Optional[bytes]:
        return self._values.get(self._normalize_key(key))

    def _normalize_key(self, key: bytes) -> bytes:
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes")
        need = (self.depth + 7) // 8
        k = bytes(key)[:need]
        return k + b"\x00" * (need - len(k))

    def _compute_root(self) -> bytes:
        if not self._values:
            return self._empty[0]
        level: Dict[Tuple[int, ...], bytes] = {}
        for key, val in self._values.items():
            level[tuple(_key_bits(key, self.depth))] = _leaf_hash(key, val)
        for height in range(self.depth - 1, -1, -1):
            parents: Dict[Tuple[int, ...], bytes] = {}
            for prefix in set(p[:-1] for p in level):
                left = level.get(prefix + (0,), self._empty[height + 1])
                right = level.get(prefix + (1,), self._empty[height + 1])
                parents[prefix] = _node_hash(left, right)
            level = parents
        return level.get((), self._empty[0])

    def _subtree_root(self, prefix_bits: List[int], depth_start: int) -> bytes:
        matching = [
            k
            for k in self._values
            if _key_bits(k, self.depth)[:depth_start] == prefix_bits
        ]
        if not matching:
            return self._empty[depth_start]
        level: Dict[Tuple[int, ...], bytes] = {
            tuple(_key_bits(k, self.depth)): _leaf_hash(k, self._values[k])
            for k in matching
        }
        for height in range(self.depth - 1, depth_start - 1, -1):
            parents: Dict[Tuple[int, ...], bytes] = {}
            seen = set()
            for path in level:
                pref = path[:height]
                if pref in seen:
                    continue
                seen.add(pref)
                parents[pref] = _node_hash(
                    level.get(pref + (0,), self._empty[height + 1]),
                    level.get(pref + (1,), self._empty[height + 1]),
                )
            level = parents
        return level.get(tuple(prefix_bits), self._empty[depth_start])

    def _root_from_parts(
        self, bits: List[int], leaf: bytes, siblings: List[bytes], mask: int
    ) -> bytes:
        current = leaf
        sib_i = 0
        for h in range(self.depth):
            bit = bits[self.depth - 1 - h]
            if mask & (1 << h):
                sib = siblings[sib_i]
                sib_i += 1
            else:
                sib = self._empty[h + 1]
            current = _node_hash(current, sib) if bit == 0 else _node_hash(sib, current)
        return current

    def prove(self, key: bytes) -> CompactSparseProof:
        key = self._normalize_key(key)
        bits = _key_bits(key, self.depth)
        membership = key in self._values
        value = self._values.get(key)
        siblings: List[bytes] = []
        mask = 0
        for h in range(self.depth):
            bit_index = self.depth - 1 - h
            bit = bits[bit_index]
            sib_hash = self._subtree_root(
                bits[:bit_index] + [1 - bit], bit_index + 1
            )
            if sib_hash != self._empty[h + 1]:
                mask |= 1 << h
                siblings.append(sib_hash)
        leaf = (
            _leaf_hash(key, value)
            if membership and value is not None
            else self._empty[self.depth]
        )
        root = self._root_from_parts(bits, leaf, siblings, mask)
        return CompactSparseProof(
            key=key,
            value=value if membership else None,
            depth=self.depth,
            siblings=tuple(siblings),
            sibling_mask=mask,
            root=root,
            membership=membership,
        )


def verify_compact_sparse_proof(proof: CompactSparseProof) -> bool:
    depth = proof.depth
    empty = _empty_hashes(depth)
    bits = _key_bits(proof.key, depth)
    if proof.membership:
        if proof.value is None:
            return False
        current = _leaf_hash(proof.key, proof.value)
    else:
        if proof.value is not None:
            return False
        current = empty[depth]
    sib_i = 0
    for h in range(depth):
        bit = bits[depth - 1 - h]
        if proof.sibling_mask & (1 << h):
            if sib_i >= len(proof.siblings):
                return False
            sib = proof.siblings[sib_i]
            sib_i += 1
        else:
            sib = empty[h + 1]
        current = _node_hash(current, sib) if bit == 0 else _node_hash(sib, current)
    if sib_i != len(proof.siblings):
        return False
    return current == proof.root
