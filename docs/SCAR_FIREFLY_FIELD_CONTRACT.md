# SCAR → Firefly — Field Contract

**Status:** DESIGN / ALIGNED TO POLICY RESOLUTION  
**Date:** 2026-09-19  
**Policy:** `docs/SCAR_FIREFLY_POLICY_RESOLUTION.md` (FROZEN)  
**Contract version (when implemented):** `scar-firefly-adapter-1`  
**Implementation:** NOT AUTHORIZED  

---

## Source identity (required)

| Field | Rule |
|-------|------|
| `scar_id` | Required; missing → **REJECT**; never invent UUID |
| `version` | Preserve SCAR version |
| `source_type` (output) | Always `swi_v1_scar` |
| `source_reference` (output) | Equals `scar_id` |

## Status (Policy B)

Copy active/archived/suspect/pruned unchanged. Other → REJECT. No upgrades.

## Content

Empty title/description allowed (Policy C). Opaque text fields. SOVEREIGN ≠ TRUE. recommended_response never executable.

## Integrity

content_hash required; recompute via V1 SCAR formula. Covers only class|title|description|trigger|failure|response|embedding_model. Valid hash ≠ whole-record immutability.

## Embeddings (Policy D)

embedding / embedding_dim excluded from MemoryAtom. embedding_model only for hash recompute.

## Provenance (Policy E)

created_by SCAR-reported only. created_at preserved. captured_at is adapter time.

## Metadata (Policy A)

Allowlist: `note`, `adapter_comment` only. Unknown or authority keys → REJECT (no silent strip).

## evidence_status

ACCEPT → OBSERVED or CLAIMED only. Never SEALED/TRUE/TRUSTED/AUTHORIZED.

## Outcomes (Policy F)

ACCEPTED · REJECTED · HALTED. No silent repair. No M11/M12/replay manufacture.
