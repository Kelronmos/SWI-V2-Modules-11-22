# SCAR → Firefly — Policy Resolution

**Status:** FROZEN (policy only)  
**Date:** 2026-09-18  
**Implementation:** **NOT AUTHORIZED**  
**Code package:** `swi_v2/firefly/` must not exist until an explicit implementation-authorization document is committed  

**Do not modify:** M11 seal · M12 freeze · V1 SCAR implementation  

---

## Freeze inputs (pre-build)

| Item | Value |
|------|--------|
| V2 tip (this doc authored against) | `2e65cf1d10c5e3611eae352df620fc63700d7115` |
| V1 tip (SCAR source inspected) | `f1f6e266d4ac49698369752e4653b9c11e9a2d73` |
| SCAR module | `swi_core/scar.py` |
| Build manual | `docs/SCAR_FIREFLY_BUILD_MANUAL.md` |
| Adapter contract (design) | `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md` |
| Test specification (design) | `docs/SCAR_FIREFLY_ADAPTER_TEST_SPEC.md` |
| Contract version (when implemented) | `scar-firefly-adapter-1` |

---

## Sequence (unchanged)

```text
BUILD MANUAL          (present)
    ↓
POLICY RESOLUTION     ← this document
    ↓
FIELD CONTRACT        (refine from frozen policies)
    ↓
ADVERSARIAL ACCEPTANCE CRITERIA
    ↓
EXPLICIT IMPLEMENTATION AUTHORIZATION
    ↓
swi_v2/firefly/       (only after authorization)
    ↓
TEST → CI → AUDIT → STOP
```

---

## Content-hash honesty (from real SCAR)

V1 `Scar.compute_content_hash()` covers **only**:

```text
scar_class | title | description | trigger_context
| failure_signature | recommended_response | embedding_model
```

**Valid content_hash ≠ entire Scar record unchanged.**

Not covered by content_hash (examples):  
`status`, `priority_score`, `tags`, `metadata`, `created_by`, `source_event_id`, `protection_level`, `embedding` payload, `embedding_dim`, `previous_scar_hash`.

The adapter must state this limitation in every audit and API surface. It must not claim whole-record cryptographic immutability from content_hash alone.

---

## Policy A — Metadata allowlist

**Decision:** SCAR `metadata` is **not** copied blindly.

### Allowlist (exact)

| Key | Rule |
|-----|------|
| `note` | Optional string only |
| `adapter_comment` | Optional string only (Firefly-side annotation; never authority) |

Any other key → **REJECT** (no silent strip).

### Forbidden keys (always REJECT if present)

```text
truth, true, trusted, verified, verification,
m11_admitted, m11_seal, admitted, admitted_input,
replay_verified, replay_ok, replay,
authority, authorized, authorization,
security_level, trust_level, seal, sealed,
independently_verified, production_certified
```

Comparison is **case-insensitive** on the key name after lowercasing and replacing `-`/` ` with `_`.

Structural rule: `metadata` must be a `dict` with **string** keys; non-dict → REJECT.

---

## Policy B — SUSPECT / PRUNED

**Decision:** Preserve source status. Never upgrade. Never silently discard.

| SCAR status | Adapter behaviour |
|-------------|-------------------|
| `active` | Copy as `active` |
| `archived` | Copy as `archived` |
| `suspect` | Copy as `suspect` |
| `pruned` | Copy as `pruned` |
| unknown / malformed | **REJECT** |

Forbidden transitions in the adapter:

```text
SUSPECT → ACTIVE
PRUNED  → ACTIVE
SUSPECT → VERIFIED / TRUSTED / SEALED
```

Downstream consumers may **refuse use** of SUSPECT/PRUNED under separate policy; the adapter must not falsify the source status.

---

## Policy C — Empty title / description

**Decision:** Empty strings are **allowed**.

```text
title = ""
description = ""
```

are valid input and must be preserved as empty.

**Forbidden:** inventing filler such as `"No description available"`.

Absence remains absence.

---

## Policy D — Embeddings

**Decision:** Adapter v1 **excludes** all of:

```text
embedding
embedding_model
embedding_dim
```

- Do not copy embedding vectors into MemoryAtom content.
- Do not run similarity / vector search.
- Do not require embedding fields for acceptance.
- Note: `embedding_model` is part of SCAR **content_hash** input; integrity checks still recompute hash with the SCAR implementation’s formula, but Firefly storage of embeddings is out of scope for v1.

---

## Policy E — Provenance

**Decision:** Preserve SCAR-reported provenance; do not independently authenticate it.

```text
created_by = SCAR-reported string
```

means only:

```text
created_by = value as stored on the SCAR
```

It does **not** mean independently authenticated actor identity.

API/docs must keep that distinction visible.

---

## Policy F — Failure semantics

**Decision:** Only three outcomes:

| Outcome | Meaning |
|---------|---------|
| **ACCEPTED** | MemoryAtom produced under contract `scar-firefly-adapter-1` |
| **REJECTED** | Input failed validation; reason required |
| **HALTED** | Request attempted a forbidden boundary (e.g. manufacture M11/M12/replay authority) |

Examples:

- REJECTED: missing `scar_id`
- REJECTED: content_hash mismatch
- REJECTED: forbidden metadata key
- HALTED: requested `m11_admitted` / sealed evidence status / M12 input manufacture

No silent repair. No “best effort” accept.

---

## Evidence status on accept

On **ACCEPTED** only:

```text
evidence_status ∈ { OBSERVED, CLAIMED }
```

**Never** set by this adapter:

```text
SEALED, INDEPENDENTLY_VERIFIED, TRUE, TRUSTED, AUTHORIZED
```

---

## MemoryAtom identity rules (policy preview)

| Rule | Decision |
|------|----------|
| Source identity | `scar_id` **required**; missing → REJECT (no UUID invention) |
| `source_type` | `"swi_v1_scar"` |
| `source_reference` | equals `scar_id` |
| `source_version` | SCAR `version` preserved |
| `created_at` | SCAR event time preserved |
| `captured_at` | Adapter capture time; **must not** overwrite `created_at` |
| `recommended_response` | Opaque text only — never executable |
| `scar_class` SOVEREIGN | Classification only — never TRUE/TRUSTED/AUTHORIZED |
| `priority_score` | Metadata only — never authorization |

---

## Explicit non-coupling

| Strand | Relation to Firefly adapter |
|--------|----------------------------|
| M11 SEALED | **Untouched**; Firefly must not modify seal record or manufacture `AdmittedInput` |
| M12 | **Frozen**; no SCAR→Firefly→M12 path |
| Replay | Separate; adapter must not claim `replay_verified` |
| CRTG / prod keys | Not in scope |

---

## Implementation gate (still closed)

This document **does not** authorize:

- creating `swi_v2/firefly/`
- writing adapter code
- CI jobs for Firefly
- any Firefly seal

Required before code:

1. Field contract updated to match these frozen policies  
2. Adversarial acceptance criteria signed off against this resolution  
3. Document titled **SCAR_FIREFLY_IMPLEMENTATION_AUTHORIZATION.md** with explicit “AUTHORIZED” and frozen SHAs  

Until then:

```text
SCAR → Firefly adapter = DESIGN + POLICY FROZEN / NOT IMPLEMENTED
```

---

## Final doctrine (repeated)

```text
MEMORY ≠ TRUTH
HASH ≠ TRUTH
INTEGRITY ≠ AUTHORITY
STATUS ≠ AUTHORIZATION
PRIORITY ≠ PERMISSION
PROVENANCE ≠ IDENTITY PROOF
M11 ≠ FIREFLY
FIREFLY ≠ M12
TESTED ≠ UNIVERSALLY SECURE
```

Build only after authorization. Stop at the boundary.
