# SCAR → Firefly Contract Audit

**Status:** DESIGN PENDING — NO IMPLEMENTATION AUTHORIZED  
**Date:** 17 September 2026  
**Against:** V1 `swi_core/scar.py` + `docs/SCAR_STATUS.md`  
**Contract:** `docs/SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md`  
**Scope:** Challenge the consume/refuse seam before any Firefly code  
**Out of scope:** M11 changes · M12 changes · Firefly implementation

---

## Architecture (current)

```text
V1 SCAR          IMPLEMENTED / TESTED  (evidence, not authority)
    ↓
Consume/Refuse   DESIGN PENDING
    ↓
Firefly          must not manufacture authority
    ↓
M11              SEALED (untouched)
    ↓
Replay           NOT SEALED
    ↓
M12              IMPLEMENTATION FROZEN
    ↓
M13–22           BLOCKED
```

---

## Boundary audit (question → answer from real SCAR)

| Boundary | Question | Answer from V1 implementation | Contract implication |
|----------|----------|-------------------------------|----------------------|
| **Identity** | Can Firefly identify exactly which SCAR record it consumed? | Yes — `scar_id` is required primary key (UUID by default) | MUST consume + preserve `scar_id`; REJECT if missing |
| **Content** | Can it preserve original content without silent transform? | Yes — text fields are plain strings; hash covers the canonical concat | MAY preserve opaque; MUST NOT normalize/summarize under this contract |
| **Hash** | Can it verify/record content hash without treating that as truth? | Yes — `compute_content_hash()` is pure over fixed field set; `validate_integrity()` compares stored vs recomputed | MUST verify match on consume; MUST NEVER promote match → truth |
| **Priority** | Is priority retained only as SCAR metadata? | `priority_score`, `scar_class`, `protection_level` are local ordering/access hints | MAY as metadata only; never trust rank or clearance |
| **Integrity root** | Preserve without claiming external anchoring? | `integrity_root()` = SHA-256 over sorted **active** content hashes; in-process or SQLite only | MAY snapshot at capture; MUST NOT claim external/consensus anchor |
| **Provenance** | Can lineage survive transfer? | `created_by`, `created_at`, `source_event_id`, `version`, `previous_scar_hash` exist; not cryptographically bound to actor | MUST preserve as SCAR-reported; MUST NOT invent; no identity proof |
| **M07 status** | Is scar_integrity a bounded validation result? | M07 may attach ScarStore and surface integrity check results | MAY record “reported at T0”; not continuous or sealed truth |
| **Mutation** | What if SCAR content changes after consumption? | Later edits without hash update → `validate_integrity` marks SUSPECT; Firefly holds a **snapshot** | Firefly record is point-in-time; MUST NOT claim it tracks live store |
| **Missing data** | What causes REFUSE/HALT? | Missing `scar_id`/`content_hash`; hash mismatch; open `metadata` smuggling; manufactured admission flags | See consume/refuse REJECT/HALT table |
| **Authority** | Can Firefly interpret SCAR as M11 admission? | No path in SCAR produces `AdmittedInput` | Contract MUST HALT any admission laundering |
| **Replay** | Can Firefly interpret memory as replay evidence? | SCAR has no replay result vocabulary | MUST NEVER set REPLAY_MATCH/etc. from SCAR alone |
| **Truth** | Can any path turn “stored” into “true”? | No SCAR API exposes truth | evidence_status only OBSERVED/CLAIMED at adapt; never TRUE/SEALED from adapter |

---

## Hard findings

1. **SCAR is sufficient as a source of structured evidence fields** for a memory adapter.  
2. **SCAR is insufficient as a trust or admission authority** — by design and by code.  
3. **Main smuggling surface:** `metadata: Dict[str, Any]` — must be allowlisted.  
4. **Main semantic surface:** `embedding` — exclude from v1 adapter.  
5. **Main false-authority surfaces:** `scar_class=sovereign`, `protection_level`, `recommended_response` — metadata/opaque only.  
6. **Mutation model:** consumption is snapshot-based; live store can diverge; Firefly must not pretend to be the live SCAR store.

---

## Adversarial contract tests (must pass before implementation authorization)

These are **contract tests**, not Firefly code. They define required behaviour of any future adapter.

### A. Valid path

| ID | Setup | Required outcome |
|----|--------|------------------|
| A1 | Active Scar, hash matches, integrity_root provided | Accept candidate; `source_system=swi_v1_scar`; evidence_status ∈ {OBSERVED, CLAIMED} |
| A2 | Same Scar twice (same id + same hash) | Deterministic identity linkage; no status upgrade |

### B. Integrity / mutation

| ID | Setup | Required outcome |
|----|--------|------------------|
| B1 | Flip one char in `description`, keep old `content_hash` | **REJECT** |
| B2 | Valid consume at T0; later V1 store corrupts same id | Firefly snapshot unchanged; must not claim live validity |
| B3 | `status=suspect` after V1 `validate_integrity` | Per policy: REJECT or accept-as-flagged only — never clear |

### C. Missing / malformed

| ID | Setup | Required outcome |
|----|--------|------------------|
| C1 | Empty `scar_id` | **REJECT** |
| C2 | Missing `content_hash` | **REJECT** |
| C3 | Null required provenance under strict policy | **REJECT** or **HALT** |
| C4 | Unknown type / non-dict scar payload | **REJECT** |

### D. Authority laundering (most important)

| ID | Setup | Required outcome |
|----|--------|------------------|
| D1 | Output field `admitted=true` or type `AdmittedInput` | **HALT** |
| D2 | Output claims `replay_result=REPLAY_MATCH` | **HALT** |
| D3 | Output `evidence_status=SEALED` or `TRUE` from adapter alone | **HALT** |
| D4 | `scar_class=sovereign` used to set trust=high | **HALT** or forced metadata-only (no trust bit) |
| D5 | `metadata={"m11_admitted": true}` | **REJECT** (deny key) |
| D6 | `recommended_response` treated as authorization grant | **HALT** |

### E. Semantic / AI-memory creep

| ID | Setup | Required outcome |
|----|--------|------------------|
| E1 | Non-empty `embedding` | Ignore or REJECT; no similarity API in v1 adapter |
| E2 | Adapter returns “summary” or “intent” derived from text | **HALT** — out of contract |

### F. Priority / root honesty

| ID | Setup | Required outcome |
|----|--------|------------------|
| F1 | High `priority_score` | Stored as metadata only |
| F2 | `integrity_root` present | Stored as capture-time reference; no “anchored” flag |

**Pass rule:** Any future implementation that fails D1–D6 or E2 is **not** authorized as SCAR→Firefly under this project.

---

## Most important adversarial principle

> The critical test is not whether Firefly can consume a valid SCAR.  
> It is whether Firefly **refuses to infer** something the SCAR record does not establish.

That is where the boundary becomes real rather than merely documented.

---

## Sequence from here

```text
DESIGN PENDING
    → this contract audit (done)
    → resolve 4 policy ambiguities (metadata allowlist, suspect/pruned,
       empty title/description, embeddings)
    → adversarial tests A–F specified as acceptance criteria
    → only then: implementation authorization decision
    → only then: adapter code + tests
```

**No M11 changes. No M12 changes. No Firefly code.**

---

## Related

- `docs/SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md`  
- `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md`  
- `docs/V2_MEMORY_WEB_STATUS.md`  
- V1 `docs/SCAR_STATUS.md`  
- `docs/M11_SEAL_RECORD.md` (immutable intent)
