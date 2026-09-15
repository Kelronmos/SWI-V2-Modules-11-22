# V1 Foundation Evidence Contract

**Producer (V1):** IMPLEMENTED / TESTED (unsigned)  
**Verifier (V2 M11):** accepts fixture **or** `v1_trainer_pipeline_completed` + matching integrity

## Integrity-covered fields

`payload` · `foundation_version` · `evidence_schema_version` · `evidence_id` · `source_reference`

**`created_at` (if present) is NOT part of the digest.**

## verification_status

| Value | Role |
|-------|------|
| `foundation_verified_test_fixture` | Unit tests only — **not** production V1 output |
| `v1_trainer_pipeline_completed` | V1 `export_foundation_evidence` status |

Integrity ≠ authenticated origin. Origin requires future signed TaskEnvelope + CRTG.

## Still pending

Real cross-repo CI integration test · CRTG · Foundation Seal 5 · M11 SEAL
