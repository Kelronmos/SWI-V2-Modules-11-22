"""
Merkle commitment for M11 post-admission seal path.

STATUS: IMPLEMENTED / TESTED (crypto commitment helper for post-admission seal)
Does NOT implement CRTG, consensus, or production key management.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List, Sequence, Tuple


def _hash_leaf(data: bytes) -> bytes:
    return hashlib.sha256(b"SWI-MERKLE-LEAF\x00" + data).digest()


def _parent(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"SWI-MERKLE-NODE\x00" + left + right).digest()


@dataclass(frozen=True)
class MerkleProof:
    leaf: bytes
    index: int
    siblings: Tuple[bytes, ...]
    root: bytes


class MerkleTree:
    def __init__(self, leaves: Sequence[bytes]):
        if not leaves:
            raise ValueError("MerkleTree requires at least one leaf")

        self._leaves = tuple(_hash_leaf(bytes(leaf)) for leaf in leaves)
        self._levels: List[Tuple[bytes, ...]] = [self._leaves]

        level = list(self._leaves)
        while len(level) > 1:
            next_level: List[bytes] = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else left
                next_level.append(_parent(left, right))
            level = next_level
            self._levels.append(tuple(level))

    @property
    def root(self) -> bytes:
        return self._levels[-1][0]

    def prove(self, index: int) -> MerkleProof:
        if index < 0 or index >= len(self._leaves):
            raise IndexError("Merkle leaf index out of range")

        siblings: List[bytes] = []
        position = index
        for level in self._levels[:-1]:
            sibling = position ^ 1
            if sibling >= len(level):
                sibling = position
            siblings.append(level[sibling])
            position //= 2

        return MerkleProof(
            leaf=self._leaves[index],
            index=index,
            siblings=tuple(siblings),
            root=self.root,
        )

    @staticmethod
    def verify(proof: MerkleProof) -> bool:
        current = proof.leaf
        position = proof.index
        for sibling in proof.siblings:
            if position % 2 == 0:
                current = _parent(current, sibling)
            else:
                current = _parent(sibling, current)
            position //= 2
        return current == proof.root
