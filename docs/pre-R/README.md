# V2 pre-R / PRE architecture package

| Field | Value |
|-------|--------|
| Status | EXPERIMENTAL response boundary + docs-only PRE registry |
| Formal module promotion | **NOT AUTHORIZED** |
| SEALED (pre-R) | **NO** |
| PRE-CONSEQUENCES | **Separate architecture — NOT IMPLEMENTED** |

## Implemented & tested

| Layer | State |
|-------|--------|
| ReturnGate (admission) | TESTED (~20 tests) |
| PR-009 enforce / privileged_action | TESTED (T20) |
| CI workflow | `tests/pre_r/` full suite · Py 3.10–3.12 |

## Architectural separation

**PRE-CONSEQUENCES is not part of the existing SWI surface.**

See `PRE_CONSEQUENCES_SURFACE_SEPARATION.md`.

- PRE-CONSEQUENCES ≠ ReturnGate
- PRE-CONSEQUENCES ≠ PR-009
- PRE-CONSEQUENCES ≠ standing / authorization
- No implementation of PRE-CONSEQUENCES is authorized in this repository
- No equivalence or interoperability claim is made

Existing ReturnGate and PR-009 remain SWI experimental work.

## Read order

1. `PRE_CONSEQUENCES_SURFACE_SEPARATION.md` — architectural separation (read first)
2. `TECHNICAL_DIAGNOSTIC_AND_NEXT_PHASE_MANUAL.md` — full diagnostic & phase sequence
3. `PRE_MODULE_REGISTRY.md`
4. `PR009_ENFORCEMENT.md`
5. `TEST_MATRIX.md` / `TEST_COVERAGE_FAIL_CLOSED_FAIL_SAFE.md`
6. `FAIL_CLOSED_FAIL_SAFE_REBUILD_MANUAL.md`
7. `LIMITATIONS.md`
8. `IMPLEMENTATION_AUTHORIZATION.md`

## Doctrine

```text
DATA ≠ AUTHORITY · TESTED ≠ SEALED
FAIL-CLOSED = admission · FAIL-SAFE = enforcement (PR-009)
ARCHITECTURAL SEPARATION ≠ INTEROPERABILITY
```
