# Sparse Merkle Trees and Compact Sparse Proofs

**Status:** IMPLEMENTED / TESTED (research primitive in `swi_v2/kernel/sparse_merkle.py`)  
**Does not:** replace M11 dense Merkle seal path · CRTG · production deployment

## Role in SWI

| Component | Role |
|-----------|------|
| `merkle.py` | Dense Merkle over few post-admission seal leaves |
| `sparse_merkle.py` | Key-addressed map + membership **and** non-membership |
| Compact proofs | Omit empty siblings via `sibling_mask` |

## Construction

- Fixed depth $d$ (tests use 8; up to 256 supported).
- Leaf: `SHA256(SWI-SMT-LEAF || key || value)`.
- Node: `SHA256(SWI-SMT-NODE || left || right)`.
- Empty leaf / empty subtrees: precomputed $E_d \ldots E_0$.

## Compact proof

```text
siblings      = only non-empty sibling hashes along the path
sibling_mask  = bit h set ⇒ siblings list contains a hash for height h
              bit h clear ⇒ use empty hash E_{h+1}
```

Verifier recomputes the root; result must equal `proof.root`.

## Explicit non-claims

- Not wired into `create_seal` by default (seal keeps dense Merkle).
- Not a global SWI state commitment unless a future module adopts it.
- M11 remains NOT SEALED until the existing release gate is met.
