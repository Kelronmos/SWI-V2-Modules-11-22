# Full Test Run Record — 2026-09-19

**Scope:** pre-R, PR-009, M11 seal/Merkle, sparse Merkle, determinism, V1 foundation.

## V2 results

| Suite | Result |
|-------|--------|
| `test/` + `tests/pre_r/` | **138 passed** |
| Gate pre-R + PR-009 T20 | PASS |
| M11 seal / E2E / boundary | PASS |
| Sparse Merkle | PASS (research) |
| Dense Merkle determinism | PASS (`test_merkle_determinism.py`) |

## V1 results

| Suite | Result |
|-------|--------|
| Full pytest (with jsonschema) | **190 passed** |

## Added this run

- `test/test_merkle_determinism.py` — root stability, proof verify, commitment stability, seal verify repeatability
- This record

## Still out of scope

Multi-agent NATS · CRTG · PRE-R SEALED · production_ready · API-bypass outside PR-009

```text
Local PASS ≠ system production-ready
M11 SEALED only per existing M11_SEAL_RECORD.md
```
