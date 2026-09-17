# SWI V2 — SCAR → Firefly Consume/Refuse Design & Teaching Manual

**Status:** DESIGN-ONLY  
**Implementation:** NOT AUTHORIZED  
**Firefly adapter:** NOT IMPLEMENTED  
**M11:** SEALED — HISTORICAL SEAL MUST NOT BE MODIFIED  
**M12:** IMPLEMENTATION FROZEN  
**Scope:** V1 SCAR → future Firefly memory boundary  
**Date:** 17 September 2026

---

## 1. Purpose

This manual teaches how to design a controlled boundary between the existing V1 SCAR implementation and the future Firefly memory architecture.

The objective is **not** to build Firefly.

The objective is to establish exactly:

1. what Firefly may consume from SCAR;
2. what Firefly must preserve;
3. what Firefly must reject;
4. what Firefly must never infer;
5. how the boundary can later be tested independently.

«Do not build the connection until the meaning of the connection is controlled.»

---

## 2. Current evidence

SCAR in V1: **IMPLEMENTED / TESTED** — Scar, ScarStore, content hashing, priority/integrity-root, optional SQLite, M07 scar_integrity, behavioural tests.

Does **not** establish: tamper-proof storage, external anchoring, factual truth, semantic scars, general AI memory, M11 equivalence.

Firefly must consume the **bounded evidence SCAR actually provides**, not a stronger interpretation.

---

## 3. Architecture

```text
V1 SCAR (implemented / tested)
        │ controlled contract
        ▼
SCAR → FIREFLY SEAM
  MAY CONSUME | MUST PRESERVE | MUST REJECT | MUST NEVER INFER
        │ future adapter (not authorized)
        ▼
Firefly (memory only)
```

Firefly is not a replacement for SCAR. SCAR is not automatically an authority for Firefly.

---

## 4–5. Four questions & never-infer

See also: `docs/SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md`

| Rule | Meaning |
|------|--------|
| MAY CONSUME ≠ TRUST | Receiving a field does not grant trust |
| MUST PRESERVE status | SUSPECT stays SUSPECT; never silent upgrade to VERIFIED |
| MUST REJECT | Missing id/hash, mismatch, authority metadata, manufactured admission/replay/truth |
| MUST NEVER INFER | Hash≠truth · Storage≠trust · M07≠M11 · Memory≠replay · Text≠intent · Class≠authority · Similarity≠fact |

Canonical failure path:

```text
SCAR → adapter → contract violation → REJECT/HALT → NO MEMORY AUTHORITY CREATED
```

---

## 6–19. Field principles (summary)

| Topic | Rule |
|-------|------|
| Identity | Reference, not authority |
| Content | Opaque; receiving ≠ understanding; no silent rewrite |
| Content hash | Supports INTEGRITY CONSISTENT, not TRUTH CONFIRMED |
| Integrity root | ≠ external anchor |
| Class / priority | Metadata only; not permission |
| M07 scar_integrity | Reported status at T0; not truth/admission/replay |
| **metadata** | Allow known only; reject unknown by default — primary smuggling risk |
| suspect / pruned | Preserve status; never SUSPECT→VERIFIED or PRUNED→FALSE silently |
| Empty title/description | Not automatic reject if id/hash/provenance valid (unless policy requires fields) |
| Embeddings | **Out of adapter v1** |
| Provenance | Answer origin/scar/validation/contract version; missing → REJECT/HALT; no guessing |
| Mutation | new_hash ≠ recorded_hash → INTEGRITY_FAILURE → REJECT; do not overwrite hash to pass |

---

## 20. Failure vocabulary

`INVALID_INPUT` · `CONTRACT_FAILURE` · `INTEGRITY_FAILURE` · `PROVENANCE_FAILURE` · `AUTHORITY_FAILURE` · `OUTPUT_FAILURE` · `HALT`

---

## 21–24. Boundaries

- **M11:** Only M11 establishes AdmittedInput. SCAR→Firefly must not create admission.
- **Replay:** Memory ≠ reconstructed execution. Firefly may reference replay evidence; must not invent it.
- **M12:** No Firefly shortcut around M11 → AdmittedInput → M12.
- **Firefly may:** preserve, relate, expose evidence refs, retain historical status.  
  **Firefly must not independently establish:** truth, authorization, replay, M11 admission, security, semantic correctness.

«Firefly can remember. Firefly can expose memory evidence. Firefly cannot turn memory into truth by itself.»

---

## 25–31. Teaching exercises (expected behaviour)

| # | Input | Expected |
|---|--------|----------|
| 1 Valid record | Valid SCAR | Accept; established = SCAR record + local integrity conditions — **not** “true” |
| 2 Hash mismatch | content A, hash(B) | INTEGRITY_FAILURE REJECT; **do not** recalculate and overwrite |
| 3 Authority smuggling | metadata truth/m11_admitted/trusted | AUTHORITY_FAILURE REJECT; **do not** copy into atom as authority |
| 4 Suspect | status=SUSPECT | Accept **as** SUSPECT; not erase; not upgrade |
| 5 Missing provenance | id+hash ok, provenance missing (if mandatory) | CONTRACT_FAILURE REJECT/HALT; no invention |
| 6 M11 injection | m11_admitted without admission ref | REJECT |
| 7 Replay injection | replay_verified without replay evidence | REJECT |

---

## 32–33. Acceptance & negative space

Acceptance: valid SCAR; identity/content/hash/provenance/status/contract version preserved.  
Rejection: missing id/hash, mismatch, bad provenance, forbidden metadata, manufactured authority, malformed, embeddings in v1.  
Non-inference tests: hash→truth, status→authority, M07→M11, memory→replay, text→intent, priority→permission must **fail**.

Strongest tests: what Firefly **refuses to believe**.

---

## 34–36. Versioning, gate, must-not

Contract version explicit (e.g. 0.x). Old evidence stays historical under old contract.

**Implementation gate:** metadata allowlist, forbidden categories, suspect/pruned policy, empty-field policy, embeddings excluded, provenance requirements, failure semantics, adversarial vectors, field audit, contract version — all frozen in writing first.

Do not implement Firefly first; do not blindly copy metadata; do not treat hashes as truth; do not modify M11 seal for Firefly.

---

## 37. Current state

| Component | Status |
|-----------|--------|
| SCAR | IMPLEMENTED / TESTED |
| SCAR STATUS | FROZEN |
| SCAR→Firefly contract | DESIGN FROZEN |
| Firefly adapter | NOT IMPLEMENTED |
| Replay | NOT SEALED |
| M11 | SEALED |
| M12 | IMPLEMENTATION FROZEN |
| M13–22 | BLOCKED |

---

## 38. Final teaching principle

A developer should answer for any SCAR field: Can Firefly consume it? Must it preserve it? Must it reject it? What is it forbidden from concluding?

If unclear → seam not ready for implementation.

«Connect everything that needs to communicate, but do not allow everything to become everything.»

**Next gate:** `docs/SCAR_FIREFLY_ADAPTER_TEST_SPEC.md` — design only.
