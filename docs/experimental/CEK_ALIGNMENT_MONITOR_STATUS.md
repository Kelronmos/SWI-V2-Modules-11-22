# SWI-CEK Alignment Monitor — Experimental Status

Date: 2026-09-27

## Classification

RESEARCH / EXPERIMENTAL

Production: NOT AUTHORIZED  
Seal: NO  
Runtime: NOT INTEGRATED  
M11: UNTOUCHED  

## Scope

This track demonstrates measurement, provenance, observation,
visibility analysis, replay, and adversarial authority-boundary testing.

It does not authorize, execute, admit, bind, seal, or promote workflows.

## Stage Status

| Stage | Description | Status |
|---|---|---|
| 1 | Mathematical measurement | PASS (local + prior clean-clone) |
| 2 | Provenance / observation / visibility | PASS (local + prior clean-clone) |
| 3 | Authority-boundary matrix | PASS (local) — sources must be on branch |
| 4 | 300-scenario adversarial suite | PASS (local) — sources must be on branch |
| 5 | Clean-checkout reproducibility | PARTIAL — basename collision fixed; full sources re-upload required |
| 6 | CI verification | PENDING (PR #5 status total_count 0) |
| 7 | Independent review | PENDING |

## Current Evidence

### Stage 3 (local experimental scope)

- 45 forbidden transition attempts
- 45 correctly rejected
- 0 unexpected authorization
- 0 unexpected execution
- 0 unexpected sealing

### Stage 4 (local experimental scope)

- 300 planned adversarial scenarios
- 301 scenario-related pytest cases including ledger export
- 428 CEK tests reported locally
- 0 unexpected authorization

### G17 clean-checkout (prior run with sources injected)

- CEK: 428 passed
- Full SWI: 621 passed, 1 failed (`tests/law/test_evidence_freshness.py` — also fails on main)
- M11: unmodified
- No production import of `cek_alignment_monitor`

## Evidence Classification

**LOCAL TEST EVIDENCE** — results from sandbox or ad-hoc checkout with files present.

**REPOSITORY-REPRODUCIBLE EVIDENCE** — complete test sources, ledger, and docs committed on `experimental/cek-alignment-monitor` and executed from a fresh clone without external file injection.

As of this document, Stage 3–4 suite sources must be confirmed present on the remote branch before claiming repository-reproducible Stage 4 evidence.

## Important limitation

The reported results are experimental evidence within the tested scope.
They do not establish production security, universal safety, truth,
ethical correctness, legal compliance, or runtime authorization.

## M11

M11 is outside this experimental track and remains untouched.

## Runtime

No runtime integration is authorized by this experiment.

## Invariant

```
MEASURE → OBSERVE → TRACE → REPORT
                      X
                      ├── AUTHORITY
                      ├── BINDING
                      ├── EXECUTION
                      └── SEAL
```
