# Test Results — ZIP Recovery 2026-11-06

## Educational package
- Command: `python3 -m pytest -q tests/`
- Result: **20 passed** in 12.46s (exit 0)

## Multiplatform package
- Command: `python3 -m pytest -q tests/`
- Result: **13 passed** in 9.86s (exit 0)

## Firefly small independent replay
- Command: `python3 swi_firefly.py --transactions 100 --subjects 20`
- Result: PASS, `production_authorization=NOT_GRANTED`, `target_3_5B_1_2s=NOT_TESTED`

## Main repository baseline suite
- Status: **NOT_RUN**

## Security negative paths (device package)
Covered by package tests: missing human auth, unverified authority, device/workflow/action mismatch, consent false, cost limit, missing evidence → all PAUSE / EXECUTE=False.

Authority ceiling remains PROVEN=NO SEALED=NO PRODUCTION_AUTHORIZED=NO.
