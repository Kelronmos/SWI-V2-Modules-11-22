# Sparse Merkle Trees and Compact Sparse Proofs

**Status:** RESEARCH PRIMITIVE · M11 INTEGRATION: NONE · SEAL DEPENDENCY: NONE · PRODUCTION CLAIM: NONE

## Role in SWI

| Component | Role |
|-----------|------|
| `merkle.py` | Dense Merkle over post-admission seal leaves (**M11 seal path**) |
| `sparse_merkle.py` | Key-addressed map + membership/non-membership (**not used by M11**) |

Do not wire SMT into `create_seal` merely because it exists.

## Construction (research)

Fixed depth, domain-separated leaves/nodes, compact proofs omit empty siblings via `sibling_mask`.

## Explicit non-claims

- Not part of M11 closure evidence
- Not CRTG / production deployment
- M11 remains NOT SEALED until release gate passes
