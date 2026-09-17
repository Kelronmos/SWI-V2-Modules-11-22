# SCAR → Firefly Adapter Contract

**Status:** DESIGN / PROPOSED — not implemented  
**Date:** 17 September 2026  
**Repos:** Kelronmos/SWI-V2-Modules-11-22 (design), Kelronmos/SWI-V1-Module-1-10 (SCAR source)  
**Doctrine:** MEMORY ≠ TRUTH · SCAR ≠ M11 · no Firefly bypass of admission

This document freezes the **first** Firefly integration seam: how a Firefly layer may accept records originating from V1 SCAR / ScarStore without upgrading SCAR claims.

---

## 1. Purpose

Define a minimal, fail-closed adapter:

```text
SCAR record (V1)
        │
        ▼
FIREFLY ADAPTER
        │
        ├── provenance
        ├── source reference
        ├── integrity reference
        ├── status (unchanged)
        └── relationship metadata
        │
        ▼
FIREFLY MEMORY RECORD (candidate)
```

The adapter **transfers structured data under a contract**. It does **not** certify truth, admission, or replay success.

---

## 2. Non-goals

The adapter must **not**:

| Forbidden inference | Why |
|---------------------|-----|
| SCAR content is factually true | MEMORY ≠ TRUTH |
| ScarStore is tamper-proof / externally anchored | V1 SCAR_STATUS: NOT CLAIMED |
| M11 admission is satisfied | Separate boundary (V2 M11) |
| Replay has succeeded | Replay is a different strand |
| SCAR supersedes Firefly or vice versa | Distinct components |
| Semantic meaning of the scar text | No NLP / understanding claim |
| Automatic M12 input | M12 is frozen; requires AdmittedInput path |
| Distributed trust | Local contract only |

If required fields are missing or integrity fails → **REJECT** or **HALT** per §7. No “best effort” invention.

---

## 3. Source (what SCAR may supply)

From V1 `Scar` / `ScarStore` (see V1 `docs/SCAR_STATUS.md`), the following fields are **eligible** as adapter input when present and consistent:

| Field | Required for accept? | Notes |
|-------|----------------------|--------|
| `scar_id` | **Yes** | Stable identity |
| `scar_class` | **Yes** | `sovereign` \| `functional` |
| `status` | **Yes** | `active` \| `archived` \| `pruned` \| `suspect` |
| `content_hash` | **Yes** | Must match recomputation over canonical content |
| `title` | Yes | Opaque string; not interpreted |
| `description` | Yes | Opaque string; not interpreted |
| `failure_signature` | No | If absent, record as empty; do not invent |
| `trigger_context` | No | Same |
| `recommended_response` | No | Same |
| `created_at` | Yes | Numeric/UTC as stored; do not “correct” |
| `created_by` | Yes | As stored |
| `source_event_id` | No | Pass through if present |
| `protection_level` | No | Pass through |
| `tags` | No | Pass through list as-is |
| `version` | Yes | Scar version field |
| Store `integrity_root` snapshot | **Yes** at adapt time | Hash over active content hashes at export |

**Not consumed as proof:** embeddings (if any), informal metadata that claims verification levels above SCAR’s status.

---

## 4. Adapter output (candidate Firefly memory record)

Design shape (not implemented schema freeze for full Firefly MemoryAtom — this is the **SCAR-origin subset**):

```text
ScarFireflyRecord
├── memory_id          # adapter-assigned or deterministic from scar_id + root
├── source_system      # "swi_v1_scar"
├── source_reference   # scar_id
├── source_repo        # "Kelronmos/SWI-V1-Module-1-10" (or configured)
├── captured_at        # adapter wall time (labeled as capture, not event time)
├── content            # opaque bundle of allowed SCAR text fields
├── content_hash       # SCAR content_hash (copied, not recomputed as "truth")
├── integrity_reference# integrity_root at capture
├── scar_class         # copied
├── scar_status        # copied — MUST NOT be upgraded
├── provenance         # created_by, source_event_id, scar version
├── evidence_status    # always starts as CLAIMED or OBSERVED — never SEALED/TRUE
├── parent_reference   # optional
└── contract_version   # e.g. "scar-firefly-adapter-1"
```

### evidence_status rules

| On accept from SCAR | Initial `evidence_status` |
|---------------------|---------------------------|
| Valid fields + matching content_hash + integrity_root provided | `OBSERVED` or `CLAIMED` only |
| After Firefly-local tests (future) | May become `TESTED` only with Firefly tests |
| Never set by this adapter alone | `SEALED`, `INDEPENDENTLY_VERIFIED`, or any “TRUE” label |

---

## 5. What Firefly may do with the record

- Store and retrieve by `memory_id` / `source_reference`  
- Relate to other memory records via explicit `parent_reference` / links  
- Surface provenance and integrity_reference to callers  
- Refuse downstream use when `scar_status` is `suspect` or `pruned` if policy says so  

## 6. What Firefly must refuse to infer

- Factual truth of title/description/failure_signature  
- That V2 M11 would admit this record  
- That replay would match  
- That Sovereign class implies higher “truth”  
- That integrity_root proves external non-tampering  
- That presence in Firefly upgrades SCAR’s IMPLEMENTED/TESTED status to sealed/verified  

---

## 7. Rejection and HALT conditions

| Condition | Response |
|-----------|----------|
| Missing `scar_id`, `content_hash`, `scar_class`, or `status` | **REJECT** |
| `content_hash` ≠ hash of canonical SCAR content fields | **REJECT** |
| `status == suspect` and policy = strict | **REJECT** (or accept only as `OBSERVED` with flag — policy must be explicit) |
| Missing integrity_root at capture when contract requires it | **REJECT** |
| Adapter asked to set evidence_status to SEALED/TRUE | **HALT** (contract violation) |
| Request to treat output as M11 AdmittedInput | **HALT** |
| Request to feed M12 without admission path | **HALT** |

No silent repair of malformed SCAR payloads.

---

## 8. Relationship to other strands

```text
SCAR (V1) --adapter--> Firefly candidate record
                              │
                              ✗ does not create AdmittedInput
                              ✗ does not satisfy Replay
                              ✗ does not implement M12

V1 evidence export --> M11 admit --> AdmittedInput --> (future) M12
```

SCAR→Firefly is a **memory strand**.  
V1 foundation evidence → M11 is an **admission strand**.  
They must not be collapsed.

---

## 9. Test plan (when implementation is authorized)

**Positive**

- Valid active Scar + matching hash + integrity_root → accept → `evidence_status` ∈ {OBSERVED, CLAIMED}

**Negative**

- Missing scar_id → REJECT  
- Tampered description without hash update → REJECT  
- Attempt to mark SEALED at adapt → HALT  

**Non-inference**

- Tests assert adapter documentation/API cannot expose a `is_true` or `admitted` flag derived only from SCAR  

**Determinism**

- Same Scar snapshot + same contract_version → same content_hash and integrity_reference on output  

Until these tests exist: status remains **DESIGN / PROPOSED**.

---

## 10. Implementation gate

Do **not** implement this adapter until:

- [x] SCAR status frozen (V1 `docs/SCAR_STATUS.md`)  
- [x] This contract frozen  
- [ ] Replay direction clear for memory claims (at least design)  
- [ ] No M11 bypass in API shape  
- [ ] Explicit REJECT/HALT behaviour specified in code tests  

Firefly distributed memory remains **BLOCKED**.

---

## 11. Claim language

| Statement | Allowed? |
|-----------|----------|
| “SCAR→Firefly adapter contract is designed” | Yes |
| “Adapter is implemented” | Only after code + tests |
| “Firefly remembers SCAR scars” | Only after implementation |
| “Firefly verifies SCAR truth” | **Never** under this contract |
| “SCAR via Firefly is M11-admitted” | **Never** without separate admission |

---

## 12. Related documents

- V1: `docs/SCAR_STATUS.md`  
- V2: `docs/V2_MEMORY_WEB_STATUS.md`  
- V2: `docs/M11_SEAL_RECORD.md` (unchanged by this design)  
- V2: `docs/M12_CONTRACT.md` (downstream; frozen)  

«SCAR preserves scars. Firefly may relate records. Neither establishes factual truth.»
