# SCAR → Firefly Consume / Refuse Contract

**Status:** DESIGN / PROPOSED — not implemented  
**Date:** 17 September 2026  
**Companion:** `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md` (adapter shape)  
**SCAR source of truth:** V1 `docs/SCAR_STATUS.md` + `swi_core/scar.py`

```text
SCAR RECORD
   │
   ├── What Firefly MAY consume
   ├── What Firefly MUST preserve
   ├── What Firefly MUST reject
   └── What Firefly MUST NEVER infer
```

**Central rule:** Firefly may consume *evidence about* a SCAR record; it must not *manufacture meaning* from that record.

**Failure path (mandatory):**

```text
SCAR → Firefly adapter → missing / contradictory provenance
        → REJECT or HALT → NO MEMORY AUTHORITY CREATED
```

---

## 1. Four-question seam

### 1.1 MAY consume

| SCAR information | Firefly |
|------------------|--------|
| `scar_id` / record identity | MAY consume |
| Text content (`title`, `description`, `trigger_context`, `failure_signature`, `recommended_response`) | MAY preserve as opaque bytes/strings |
| `content_hash` | MAY preserve |
| Store `integrity_root` at capture | MAY preserve as reference |
| `scar_class`, `priority_score`, `protection_level` | MAY preserve as **metadata only** |
| `status` | MAY preserve **without upgrade** |
| `created_at`, `created_by`, `source_event_id`, `version` | MAY consume as provenance inputs |
| `previous_scar_hash` | MAY preserve as chain hint (not proof of global history) |
| `tags` | MAY preserve as opaque labels |
| M07 `validate_integrity()` / `scar_integrity` result | MAY **record as a reported status** at capture time |

### 1.2 MUST preserve

| Item | Rule |
|------|------|
| Provenance (`created_by`, `source_event_id`, `created_at`, source repo/system) | MUST preserve; MUST NOT invent if absent |
| Source reference (`scar_id`) | MUST preserve |
| `content_hash` as stated | MUST preserve; MUST NOT replace with a “better” hash silently |
| `status` label | MUST preserve; MUST NOT promote `active` → sealed/true |
| Contract version of this consume path | MUST stamp on output |

### 1.3 MUST reject

| Condition | Response |
|-----------|----------|
| Missing `scar_id` | **REJECT** |
| Missing `content_hash` | **REJECT** |
| `content_hash` ≠ recomputation over V1 canonical fields | **REJECT** |
| Missing provenance required by policy (e.g. empty `created_by` when policy requires it) | **REJECT** or **HALT** |
| Contradictory provenance (two different `created_by` for same id without version story) | **REJECT** |
| Payload asks adapter to set factual-true / M11-admitted / replay-match flags | **HALT** |
| Treat SCAR output as `AdmittedInput` or M12 input | **HALT** |

### 1.4 MUST NEVER infer

| Inference | Rule |
|-----------|------|
| “This is factually true” | MUST NOT infer |
| “This person intended X” (from text fields) | MUST NOT infer |
| “This memory is trustworthy because it is hashed” | MUST NOT infer |
| M11 admission | MUST NOT manufacture |
| Replay result | MUST NOT manufacture |
| Semantic understanding of scar text | MUST NOT silently invent |
| Sovereign class ⇒ higher truth | MUST NOT infer |
| Integrity root ⇒ external non-tampering | MUST NOT infer |
| Embedding similarity ⇒ related meaning | MUST NOT infer under this contract |

---

## 2. Field-by-field ambiguity audit (V1 `Scar`)

Canonical content hash fields (from `compute_content_hash`):  
`scar_class | title | description | trigger_context | failure_signature | recommended_response | embedding_model`

| Field | Consume? | Ambiguity | Resolution |
|-------|----------|-----------|------------|
| `scar_id` | MAY / MUST preserve as source ref | None if non-empty UUID/string | REJECT if missing/empty |
| `version` | MAY | Local scar version ≠ Firefly schema version | Store as `scar_version`; separate `contract_version` |
| `scar_class` | MAY as metadata | “Sovereign” sounds like authority | Metadata only; never authority bit |
| `status` | MAY / MUST preserve | `suspect` vs accept | Default: allow store as OBSERVED with status copied; policy may REJECT `suspect`/`pruned` |
| `title` | MAY opaque | Looks like a claim | Opaque; no NLP |
| `description` | MAY opaque | Same | Opaque |
| `trigger_context` | MAY opaque | Same | Opaque |
| `failure_signature` | MAY opaque | Same | Opaque |
| `recommended_response` | MAY opaque | Could be read as policy order | Opaque advice text only; not executable authority |
| `embedding` | **Default: DO NOT consume** in v1 adapter | Implies semantic memory | Out of scope unless a later contract; refuse silent use |
| `embedding_model` | In content_hash only | Model name ≠ quality | Preserve string if present; no quality claim |
| `embedding_dim` | Optional metadata | None | MAY copy if embedding out of scope still ignore vectors |
| `content_hash` | MUST | Stale hash if fields edited | REJECT on mismatch |
| `previous_scar_hash` | MAY | Suggests full chain existence | Hint only; no global ledger claim |
| `created_at` | MUST preserve if present | Clock not authenticated | Label as SCAR-reported time |
| `created_by` | MUST preserve | Free string | No identity proof |
| `source_event_id` | MAY | May be null | Null ≠ invented id |
| `priority_score` | MAY metadata | Looks like ranking truth | Sort hint only |
| `protection_level` | MAY metadata | Looks like security level | SCAR access rule remnant only |
| `tags` | MAY opaque | Free-form | No taxonomy authority |
| `metadata` | **Ambiguous** | Open dict can smuggle claims | **Consume only allowlisted keys** or REJECT unknown claim-like keys (`true`, `admitted`, `verified`, …) |
| Store `integrity_root` | MAY at capture | Snapshot timing | Record `integrity_root` + `captured_at`; not continuous proof |
| M07 validation result | MAY record | One-shot local check | Status at T0 only; not continuous |

### Ambiguity still requiring policy choice before code

1. **`metadata` allowlist** — exact denied key list for claim smuggling.  
2. **`status == suspect|pruned`** — hard REJECT vs accept-as-flagged.  
3. **Empty optional text fields** — accept vs require non-empty `title`+`description`.  
4. **Embeddings** — remain out of first adapter (recommended).  

Until these four are decided in writing, implementation stays blocked.

---

## 3. Conceptual test cases (no code)

| # | Scenario | Expected |
|---|----------|----------|
| T1 | Valid active Scar, hash matches, root provided | MAY accept → evidence_status OBSERVED/CLAIMED only |
| T2 | Description changed, hash not updated | REJECT |
| T3 | `created_by` missing under strict provenance policy | REJECT/HALT |
| T4 | Adapter output sets `admitted=true` | HALT |
| T5 | Sovereign scar | Still no truth/admission inference |
| T6 | `metadata: {"verified": true}` | REJECT or strip per allowlist policy |
| T7 | Embedding present | Ignored or REJECT if policy forbids; never semantic use |
| T8 | M07 reported valid at capture, later store corrupted | Firefly record still only claims “reported valid at T0” |

---

## 4. Implementation gate

- [x] V1 SCAR_STATUS frozen  
- [x] This CONSUME/REFUSE contract written  
- [ ] Resolve four ambiguity items in §2  
- [ ] Adapter contract tests specified against real Scar fields  
- [ ] Still no M11 bypass in API  
- [ ] Firefly code not started  

**Firefly remains DESIGN / DEFERRED.**

---

## 5. Claim language

| Allowed | Forbidden |
|---------|-----------|
| “Consume/refuse seam is designed and field-audited” | “Firefly is implemented” |
| “SCAR fields classified for adapter use” | “Hashed scars are true” |
| “Ambiguities listed for policy freeze” | “Firefly verifies SCAR” |

«SCAR preserves scars. Firefly may relate records. Neither establishes factual truth.»
