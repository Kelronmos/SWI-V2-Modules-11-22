# V2 pre-R Return Boundary

**Date:** 2026-09-19  
**Tip reference:** see `docs/PRE_R_IMPLEMENTATION_STATUS.md`  

| Field | Value |
|-------|--------|
| Status | **EXPERIMENTAL** |
| Target | SWI V2 only |
| V1 dependency | NONE |
| Formal module | **NOT AUTHORIZED** |
| SEALED | **NO** |
| Production | **NOT AUTHORIZED** |
| Security claim | **NONE** |

## Question (narrow)

> Can a result cross a return boundary while preserving defined evidence, integrity, identity, destination and authority scope, without the return path, intermediary backend, or UI creating new authority?

## Current evidence posture

| Layer | State |
|-------|--------|
| Spec | `RETURN_BOUNDARY_SPEC.md` |
| Executable slice | `experimental/response_boundary/` |
| Unit tests | `tests/pre_r/test_response_boundary.py` — **20 local PASS** |
| Workflow | `.github/workflows/pre_r_boundary.yml` |
| Historical gap (`64bf105`) | Workflow present, test path incomplete → **NOT TESTED** (integration) |
| After `0cbc42e` | Test path + core aligned → assertions reached |
| Independent audit | NOT YET |
| SEALED | NO |

## Doctrine

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
RESULT ≠ RESPONSE ≠ AUTHORITY ≠ NEW ACTION
Aᵣ ⊆ A₀ · UNKNOWN ⇏ ALLOW
TESTED ≠ SEALED · IMPLEMENTED ≠ AUTHORIZED
```

## Documents

| File | Role |
|------|------|
| `RETURN_BOUNDARY_SPEC.md` | Build guide |
| `TEST_MATRIX.md` | Mutation → expected |
| `LIMITATIONS.md` | Limitation register |
| `PROMOTION_CRITERIA.md` | When (not) to promote |
| `IMPLEMENTATION_AUTHORIZATION.md` | Experimental · not promote/seal |
| `PRE_R_REPAIR_RECORD.md` | F1 path failure + evidence |
| `RESPONSE_BOUNDARY_REPAIR_AND_VERIFICATION_MANUAL.md` | Repair doctrine |

## Next

Expand adversarial depth (contract-first) · keep V2 + two-checkout regression green · audit before promote.
