# V1 → V2 Architecture Alignment Review
**Date:** 2026-11-06  
**Working branch:** `fix/zip-recovery-integration-2026-11-06`  
**Source main (V2):** `378c856e9081cbaea580a2c433881ea24c54b7e9`  
**V1 public reference:** `Kelronmos/SWI-V1-Module-1-10` (V1.1 Modules 00–11 + ScarStore)

## Governing rule
V1 Modules 00–10 (plus ScarStore / continuity) are the foundation.  
V2 Modules 11–22 are the continuation.  
The **V1 Foundation Evidence Contract** is the only permitted interface.  
V2 must independently verify incoming evidence. It must **not** import V1 implementation internals as a substitute for evidence admission.

## V1 core facts (from source, not invented)

| Item | Status (V1 docs) |
|------|------------------|
| Pipeline | M03 → M02 → M05 → M06 → M07/M09 → `export_foundation_evidence()` → `FoundationEvidenceEnvelope` |
| Foundation evidence export | **IMPLEMENTED / TESTED · unsigned · not Seal 5 · not CRTG** |
| ScarStore / SCAR | **IMPLEMENTED / TESTED** (local integrity; not truth engine) |
| Authority boundary | IMPLEMENTED / TESTED · tip CI · **not sealed** |
| Foundation Seal 5 | **NOT READY** |
| Source admission + replay | TESTED / REPLAYABLE_BOUNDED |
| Production trust | **NOT CLAIMED** |

Key integrity note (V1): envelope digest covers payload, foundation_version, evidence_schema_version, evidence_id, source_reference.  
`created_at` is **excluded**. Hash match proves field integrity, **not** authenticated sender.

## V2 core facts (from `docs/MODULE_STATUS.md`)

| Component | Status |
|-----------|--------|
| M11 | SEALED (historical) |
| M12 | FROZEN until Gates A–D |
| Replay | NOT IMPLEMENTED (ReplayGuard partial in-memory only) |
| Foundation Seal 5 (V1) | NOT READY |
| **Firefly** | **DESIGN / DEFERRED — NO IMPLEMENTATION AUTHORIZED** |
| SCAR → Firefly docs | DESIGN FROZEN |
| SCAR (V1) | IMPLEMENTED / TESTED (lives in V1) |
| M13–22 | BLOCKED |

## Distinction that must be preserved
```
MEMORY ≠ TRUTH ≠ ADMISSION ≠ AUTHORIZATION
INSTRUCTION ≠ AUTHORIZATION
CAPABILITY ≠ PERMISSION
OBSERVATION ≠ EVIDENCE
EVIDENCE ≠ AUTHORIZATION
TESTED ≠ PROVEN ≠ SEALED ≠ PRODUCTION AUTHORIZED
```

## Package alignment summary

| Package | Classification | Relationship to V1 / V2 |
|---------|----------------|-------------------------|
| Educational / Multiplatform device-bound | V1 educational application / independent experiment | Does **not** produce `FoundationEvidenceEnvelope`. Does **not** implement SCAR or V1 pipeline modules. Fail-closed local authorization is a **demonstration**, not the V1/V2 spine. |
| Firefly replay evidence | Downstream evidence / memory subsystem · Independent experiment | Explicitly **NO IMPLEMENTATION AUTHORIZED** in V2. Historical replay may be inspected; replay does **not** authorize implementation or upgrade evidence status. |

## Documentation conflict (to be resolved without rewriting history)
V1 `FOUNDATION_EVIDENCE_PRODUCER.md` states the producer is **IMPLEMENTED / TESTED** (unsigned).  
Any architecture diagram that labels the same producer as only **PROPOSED** is out of date relative to the producer document.  
Resolution: keep the producer document status; mark diagram status as “diagram lag / needs update”, do **not** silently change historical claim language.

## Authority ceiling after this review
```
PROVEN=NO
SEALED=NO
PRODUCTION_AUTHORIZED=NO
```
No package from the three ZIPs is permitted to alter this ceiling.
