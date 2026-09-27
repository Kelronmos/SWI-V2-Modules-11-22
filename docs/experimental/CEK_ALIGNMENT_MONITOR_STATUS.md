# SWI-CEK Alignment Monitor — Experimental Status

Date: 2026-09-27

## Classification

RESEARCH / EXPERIMENTAL  
Production: NOT AUTHORIZED  
Seal: NO  
Runtime: NOT INTEGRATED  
M11: UNTOUCHED  

## Evidence classes

| Class | Status |
|-------|--------|
| LOCAL sandbox 489 PASS | YES |
| CLEAN CLONE (no injection) | **PARTIAL — 9 passed** at tip `a08d80d` under `tests/cek_alignment_monitor/` |
| Full Stage 3–4 matrix/scenario on branch | **NOT YET** (sources in ZIP/sandbox) |
| CI PR #5 | PENDING (draft; verify after full sources) |
| Independent review | PENDING |

## G17 findings fixed on branch

1. pytest basename collision → `test_cek_*`
2. `tests/experimental` shadowed package `experimental` → tests moved to `tests/cek_alignment_monitor/`; `pytest.ini` pythonpath=.; conftest forces repo-root on sys.path

## Full SWI regression (prior clean-clone with injected full suite)

621 passed, 1 failed: `tests/law/test_evidence_freshness.py` (also fails on main)

## Invariant

```
MEASURE → OBSERVE → TRACE → REPORT
                      X → AUTHORITY | BINDING | EXECUTION | SEAL
```

## Non-claims

TESTED ≠ SEALED · CI PASS ≠ SEAL · EVIDENCE ≠ AUTHORITY · OBSERVATION ≠ AUTHORIZATION
