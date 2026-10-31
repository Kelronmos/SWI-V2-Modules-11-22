# End-to-End Acceptance Report

**Authoritative commit (local = remote):** `f118ebf585e712f48b36c3d7b7ba52f048907723`

Branch: `repair/iso-evidence-replay-integrity`

## Repository state

- Local tip equals `origin/repair/iso-evidence-replay-integrity`
- Ancestors include `1af8193`, `c3de482`
- Local-only commits `3a08032` / `9363634` are **not** on remote

## Acceptance matrix

| Field | Status |
|-------|--------|
| REPOSITORY_STATE_VERIFIED | PASS |
| ACTIVE_EVIDENCE_SCHEMA_VALIDATION | **FAIL** (0 valid / 21 pack records — historical pack does not match repaired schema) |
| HISTORICAL_RECORD_CLASSIFICATION | PARTIAL |
| SERIAL_UNIQUENESS | PASS (engine adversarial) |
| SERIAL_MONOTONICITY | PASS |
| LEDGER_INTEGRITY | PASS (tamper/reorder/dup reject) |
| CRYPTOGRAPHIC_VERIFICATION | PARTIAL |
| REPLAY_CONSISTENCY | PARTIAL |
| SWI_KERNEL_TESTS | PASS (536: cek_alignment_monitor + law + pre_r) |
| ISO_CLAUSE_TRACEABILITY | PARTIAL |
| ISO_CLAUSE_COMPATIBILITY | NOT_ASSESSED |
| INDEPENDENT_REPLAY | NOT_RUN |
| CLEAN_CLONE_VERIFICATION | NOT_RUN |
| CI_STATUS | PRESENT |

## Evidence totals (pack overlay)

TOTAL=21 VALID=0 INVALID=21

Historical pack records were **not** rewritten. Invalid remains identifiable.

## Governance

```
PROVEN=NO
SEALED=NO
AUTHORIZED=NO
PRODUCTION_AUTHORIZED=NO
ISO_COMPLIANCE=NOT_ESTABLISHED
MAIN_MERGE=NOT_AUTHORIZED
```
