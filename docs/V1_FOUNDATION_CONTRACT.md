# V1 Foundation Evidence Contract

**STATUS:** V1 producer **IMPLEMENTED** (unsigned) · V2 accepts fixture **and** `v1_trainer_pipeline_completed`

## Producer (V1)

`swi_core/foundation_evidence.py` → `export_foundation_evidence(PipelineResult)`

| Field | Value |
|-------|--------|
| foundation_version | `1.0-proposed` |
| evidence_schema_version | `1.0-proposed` |
| verification_status | `v1_trainer_pipeline_completed` |
| integrity_reference | SHA-256 canonical JSON (shared with V2) |

## Still pending

CRTG / signed envelope · cross-repo CI integration test · Foundation Seal 5 · M11 SEAL

Fixtures with `foundation_verified_test_fixture` remain valid unit tests only.
