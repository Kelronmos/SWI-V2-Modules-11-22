# SCAR → Firefly Consume / Refuse Contract

**Status:** DESIGN PENDING — NO IMPLEMENTATION AUTHORIZED  
**Date:** 17 September 2026  
**Companion:** `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md`  
**SCAR evidence:** V1 `docs/SCAR_STATUS.md` · `swi_core/scar.py`  
**M11:** Untouched — seal and historical evidence remain as recorded

```text
SCAR → Consume/Refuse Contract → Firefly design → contract tests → implementation
```

**Not:**

```text
SCAR → Firefly → retroactively decide what the data meant
```

---

## Critical distinction

| Phrase | Meaning |
|--------|--------|
| **MAY CONSUME ≠ TRUST** | Taking a field in does not grant trust |
| **PRESERVE ≠ VERIFY** | Keeping a value does not re-validate the world |
| **INTEGRITY ≠ TRUTH** | Hash/root checks local consistency, not factual truth |
| **MEMORY ≠ AUTHORITY** | Storage does not create admission, replay, or policy power |

V1 SCAR is frozen as **evidence of what was stored and integrity-checked locally**, not as authority over V2 admission or truth.

---

## Four boundaries

### 1. MAY CONSUME

- SCAR record ID (`scar_id`)
- content (opaque text fields)
- content hash
- priority metadata (`priority_score`, `scar_class`, `protection_level`)
- integrity-root reference (store snapshot at capture)
- source/provenance metadata (`created_by`, `created_at`, `source_event_id`, `version`)
- M07 `scar_integrity` / `validate_integrity` **result as reported status at capture time**

### 2. MUST PRESERVE

- original identity/reference (`scar_id`)
- provenance fields as received (no invention)
- source integrity information (`content_hash`, capture-time `integrity_root`)
- validation status labels without upgrade
- distinctions among OBSERVED / CLAIMED / TESTED / … (adapter must not collapse them into “true”)
- the fact that the record **came from SCAR** (`source_system = swi_v1_scar`)

### 3. MUST REJECT

- malformed SCAR records
- missing fields required by this contract
- contradictory provenance
- content / hash mismatch
- invalid integrity metadata
- attempts to turn an unverified record into an **admitted** record (M11) or M12 input

### 4. MUST NEVER INFER

- factual truth
- human intent
- semantic meaning that SCAR does not establish
- M11 admission
- replay success
- authorization
- security / trustworthiness beyond “hash matched at T0”
- external anchoring
- “AI memory” merely because the record is stored

---

## Field matrix (V1 `Scar` → Firefly action → reason → failure)

Canonical hash inputs:  
`scar_class | title | description | trigger_context | failure_signature | recommended_response | embedding_model`

| SCAR field | Firefly action | Reason | Failure behaviour |
|------------|----------------|--------|-------------------|
| `scar_id` | MAY consume; MUST preserve as source ref | Identity of record | Missing/empty → **REJECT** |
| `version` | MAY consume as `scar_version` | Local scar version ≠ Firefly schema | Do not treat as contract_version |
| `scar_class` | MAY consume as metadata only | Classification, not authority | Never set authority/admission bits |
| `status` | MUST preserve without upgrade | ACTIVE/ARCHIVED/PRUNED/SUSPECT are SCAR labels | Policy choice: REJECT or accept-as-flagged for SUSPECT/PRUNED |
| `title` | MAY preserve opaque | Text is not verified meaning | No NLP / intent extraction |
| `description` | MAY preserve opaque | Same | Same |
| `trigger_context` | MAY preserve opaque | Same | Same |
| `failure_signature` | MAY preserve opaque | Same | Same |
| `recommended_response` | MAY preserve opaque | Advice text ≠ executable policy | Must not execute or elevate to authorization |
| `embedding` | **Default: do not consume** (v1) | Implies semantic memory SCAR does not claim | Ignore or **REJECT** if policy forbids vectors |
| `embedding_model` | MAY preserve string only | In content_hash; not quality proof | No model-trust claim |
| `embedding_dim` | MAY copy as metadata | Dimensionality only | Ignore vectors |
| `content_hash` | MUST preserve; MUST verify match | Integrity of content bundle | Mismatch → **REJECT** |
| `previous_scar_hash` | MAY preserve as hint | Not a global ledger | Must not claim full-chain proof |
| `created_at` | MUST preserve if present | SCAR-reported time, not authenticated clock | Label as source-reported |
| `created_by` | MUST preserve | Free-string actor, not identity proof | Missing under strict policy → **REJECT/HALT** |
| `source_event_id` | MAY preserve | May be null | Null → leave null; do not invent |
| `priority_score` | MAY as metadata | Ranking hint inside ScarStore | Not trust rank |
| `protection_level` | MAY as metadata | SCAR prune/access remnant | Not V2 security clearance |
| `tags` | MAY opaque | Free-form | No taxonomy authority |
| `metadata` | **Allowlist only** | Open dict can smuggle claims | Unknown claim-like keys → **REJECT** or strip per policy |
| Store `integrity_root` | MAY at capture | Snapshot of active hashes at T0 | Missing when required → **REJECT**; not continuous proof |
| M07 validation result | MAY record as reported status | One-shot local check | Record “reported at T0” only; never upgrade to sealed/true |

### Policy ambiguities (must resolve before any adapter code)

1. Exact `metadata` allowlist / deny list  
2. SUSPECT/PRUNED: hard REJECT vs accept-as-flagged  
3. Empty `title`/`description`: allow or require non-empty  
4. Embeddings: remain out of first adapter (recommended: yes)

---

## Failure path (canonical)

```text
SCAR record
    → Firefly adapter
    → missing / contradictory provenance
       OR content/hash mismatch
       OR manufactured admission/truth flag
    → REJECT or HALT
    → NO MEMORY AUTHORITY CREATED
```

---

## Conceptual tests (before implementation)

| # | Input | Expected |
|---|--------|----------|
| T1 | Valid active Scar, hash matches, root present | Accept candidate; status OBSERVED/CLAIMED only |
| T2 | Content edited, hash stale | REJECT |
| T3 | Missing `scar_id` or `content_hash` | REJECT |
| T4 | Output attempts `admitted=true` / M11 bypass | HALT |
| T5 | Sovereign class | Still no truth/admission inference |
| T6 | `metadata.verified = true` | REJECT or strip per allowlist |
| T7 | Embedding present | Out of scope / ignore / REJECT per policy |
| T8 | M07 valid at T0, later store broken | Firefly still only “reported valid at T0” |

---

## Chain and gates

```text
SCAR (V1 evidence)
  → this Consume/Refuse Contract (DESIGN PENDING)
  → Firefly design
  → contract tests against real Scar fields
  → implementation (only if authorized)
```

**Implementation authorized only when:**

- [x] V1 SCAR_STATUS frozen  
- [x] This contract exists  
- [ ] Four policy ambiguities resolved in writing  
- [ ] Conceptual tests T1–T8 agreed  
- [ ] Adapter API cannot express M11 admission or factual truth  
- [ ] Explicit **NO IMPLEMENTATION AUTHORIZED** lifted by project decision  

**M11 seal record:** do not edit.  
**Firefly code:** do not write until the gate above is closed.

---

## Claim language

| Allowed now | Forbidden now |
|-------------|----------------|
| “Consume/refuse contract is design-pending and field-mapped” | “Firefly is implemented” |
| “SCAR is V1 IMPLEMENTED/TESTED evidence” | “SCAR proves truth / admission” |
| “No implementation authorized” | “Hashed memory is trustworthy” |

«MAY CONSUME ≠ TRUST. PRESERVE ≠ VERIFY. INTEGRITY ≠ TRUTH. MEMORY ≠ AUTHORITY.»
