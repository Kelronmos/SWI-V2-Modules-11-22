# SCAR → Firefly Adapter Test Specification

**Status:** DESIGN PENDING — NO IMPLEMENTATION AUTHORIZED  
**Date:** 17 September 2026  
**Contract:** `docs/SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md`  
**Audit:** `docs/SCAR_FIREFLY_CONTRACT_AUDIT.md`  
**Teaching:** `docs/SCAR_FIREFLY_TEACHING_MANUAL.md`  
**Contract version (proposed):** `scar-firefly-0.1`

Converts the consume/refuse design into **explicit test vectors**.  
These are acceptance criteria for a future adapter — not executable tests yet.

---

## Conventions

| Symbol | Meaning |
|--------|--------|
| **ACCEPT** | Candidate memory record created; evidence_status ∈ {OBSERVED, CLAIMED} only |
| **REJECT** | No memory authority; typed failure (see vocabulary) |
| **HALT** | Contract/authority violation; harder stop than REJECT |
| Opaque | Bytes/strings stored without semantic interpretation |

**Failure codes:** `INVALID_INPUT` · `CONTRACT_FAILURE` · `INTEGRITY_FAILURE` · `PROVENANCE_FAILURE` · `AUTHORITY_FAILURE` · `OUTPUT_FAILURE` · `HALT`

---

## P — Positive (acceptance)

| ID | Fixture (conceptual) | Expected |
|----|----------------------|----------|
| P1 | Active Scar; all required fields; content_hash matches compute; integrity_root present | **ACCEPT**; source_system=`swi_v1_scar`; source_reference=scar_id; contract_version stamped |
| P2 | Same as P1 with empty title and empty description | **ACCEPT** (descriptive fields not foundational unless policy changes) |
| P3 | P1 + scar_class=sovereign, high priority_score | **ACCEPT**; class/priority as **metadata only** |
| P4 | P1 + status=active + M07 reported valid at capture | **ACCEPT**; m07 result stored as reported-at-T0 only |
| P5 | P1 twice with identical scar_id + hash | Deterministic linkage; **no** status upgrade on second pass |
| P6 | status=suspect, otherwise valid | **ACCEPT as SUSPECT** (status preserved; not erased; not upgraded) |
| P7 | status=pruned, otherwise valid | **ACCEPT as PRUNED** (historical; not auto-FALSE) |

**Assert on every ACCEPT:** provenance preserved; content_hash preserved; status not upgraded; no admitted/true/replay flags.

---

## N — Negative (reject / halt)

| ID | Fixture | Expected code |
|----|---------|----------------|
| N1 | Missing scar_id | INVALID_INPUT / REJECT |
| N2 | Missing content_hash | INVALID_INPUT / REJECT |
| N3 | Non-object / malformed payload | INVALID_INPUT / REJECT |
| N4 | content_hash ≠ hash of canonical content fields | INTEGRITY_FAILURE / REJECT |
| N5 | Required provenance missing under strict policy (e.g. empty created_by) | PROVENANCE_FAILURE / REJECT or HALT |
| N6 | Contradictory provenance for same scar_id without version story | PROVENANCE_FAILURE / REJECT |
| N7 | Embedding present under v1 policy (embeddings excluded) | CONTRACT_FAILURE / REJECT |
| N8 | Unknown metadata key (default deny) | CONTRACT_FAILURE / REJECT |

---

## M — Mutation

| ID | Fixture | Expected |
|----|---------|----------|
| M1 | Valid consume at T0; later description changed in source without hash update | Snapshot at T0 unchanged; re-consume of mutated source → INTEGRITY_FAILURE / REJECT |
| M2 | Adapter offered “fix” by recomputing hash to match new content | **Must refuse**; overwriting hash to pass is **forbidden** |
| M3 | Live ScarStore diverges after consume | Firefly record must not claim live-store validity |

---

## V — Provenance

| ID | Fixture | Expected |
|----|---------|----------|
| V1 | created_by, created_at, source_event_id, scar version present | All preserved on candidate; labeled SCAR-reported |
| V2 | source_event_id null | Leave null; do not invent |
| V3 | Missing mandatory provenance | PROVENANCE_FAILURE / REJECT or HALT |
| V4 | Output omits “came from SCAR” (source_system) | OUTPUT_FAILURE / REJECT |

---

## A — Authority injection (critical)

| ID | Fixture | Expected |
|----|---------|----------|
| A1 | metadata `{"truth": true}` | AUTHORITY_FAILURE / REJECT |
| A2 | metadata `{"trusted": true}` | AUTHORITY_FAILURE / REJECT |
| A3 | metadata `{"m11_admitted": true}` without M11 admission ref | AUTHORITY_FAILURE / REJECT |
| A4 | metadata `{"replay_verified": true}` without replay evidence | AUTHORITY_FAILURE / REJECT |
| A5 | Adapter output type or field equivalent to AdmittedInput | **HALT** |
| A6 | evidence_status set to SEALED or TRUE by adapter alone | **HALT** |
| A7 | scar_class=sovereign → trust=high or permission grant | AUTHORITY_FAILURE / HALT |
| A8 | recommended_response treated as authorization | AUTHORITY_FAILURE / HALT |
| A9 | priority_score used as security clearance | AUTHORITY_FAILURE / HALT |
| A10 | protection_level used as V2 access grant | AUTHORITY_FAILURE / HALT |

**Pass rule for future implementation:** failing any A1–A10 means **not authorized** under this project.

---

## I — Non-inference (must fail to “believe”)

| ID | Forbidden transformation | Test idea |
|----|--------------------------|----------|
| I1 | hash → truth | Valid hash must not set true/factual flags |
| I2 | storage → trust | ACCEPT must not set trusted=true |
| I3 | M07 → M11 | m07 valid must not set admitted |
| I4 | memory → replay | No REPLAY_MATCH from SCAR alone |
| I5 | text → intent | No intent/summary field from description |
| I6 | priority → permission | High priority must not grant execute/authz |
| I7 | similarity → fact | (v1: no embeddings; if present, REJECT) |

---

## R — Integrity root honesty

| ID | Fixture | Expected |
|----|---------|----------|
| R1 | integrity_root at capture | Stored as capture-time reference only |
| R2 | Flag external_anchored=true without evidence | AUTHORITY_FAILURE / REJECT |

---

## Contract version

| ID | Fixture | Expected |
|----|---------|----------|
| C1 | Every ACCEPT | `contract_version = scar-firefly-0.1` (or frozen id) present |
| C2 | Future contract 0.2 | Must not rewrite historical 0.1 records to look like 0.2 |

---

## Implementation gate (from teaching manual)

Before any adapter code:

- [ ] metadata allowlist frozen  
- [ ] forbidden metadata categories frozen  
- [ ] suspect/pruned behaviour frozen (this spec: accept-as-status)  
- [ ] empty descriptive-field policy frozen (this spec: allow empty)  
- [ ] embeddings excluded from adapter v1  
- [ ] provenance requirements frozen  
- [ ] failure semantics frozen  
- [ ] adversarial vectors written (this document)  
- [ ] SCAR field audit complete  
- [ ] contract version assigned  

Then only: CONTRACT → TESTS → IMPLEMENTATION → CI → AUDIT

**No Firefly implementation. No M11 changes. No M12 changes. No new cryptographic authority layer.**

---

## Related

- `docs/SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md`  
- `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md`  
- `docs/SCAR_FIREFLY_CONTRACT_AUDIT.md`  
- `docs/SCAR_FIREFLY_TEACHING_MANUAL.md`  
- V1 `docs/SCAR_STATUS.md`  
- `docs/M11_SEAL_RECORD.md`
