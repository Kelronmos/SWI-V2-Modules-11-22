# SWI Teaching Guide

## How to Audit a Memory Boundary Before Writing Code

**Example boundary:** V1 SCAR → V2 Firefly  
**Status:** Teaching / Design  
**Firefly implementation:** Not authorized  
**Date:** 17 September 2026

---

## 1. The lesson

When two systems need to communicate, the first question is not:

«How do we connect them?»

The first question is:

«What exactly is allowed to cross the boundary, and what meaning is forbidden from crossing with it?»

A system can transfer data successfully while still creating a dangerous architectural problem. The transfer may accidentally change:

```text
data → evidence → authority → truth
```

Our job is to stop that escalation.

---

## 2. Start with what actually exists

Never design against memory of an old architecture. Inspect the current implementation.

For SCAR, the source defines: Scar, ScarStore, classes, statuses, content hashing, integrity-root, persistence, validation, optional embeddings, metadata, provenance-related fields.

**The source, not an old diagram, is the authority for what currently exists.**

---

## 3. Separate four things

| Layer | Example |
|-------|--------|
| What the **code** does | Scar computes a SHA-256 content hash |
| What the **tests** demonstrate | Mutation of a hash-covered field is detected |
| What the **documentation** claims | SCAR provides bounded integrity information |
| What people might **incorrectly infer** | “The hash proves the memory is true” |

The fourth category is where many architectural failures begin.

---

## 4–5. The hash lesson

Current SCAR `content_hash` covers:

`scar_class | title | description | trigger_context | failure_signature | recommended_response | embedding_model`

It does **not** cover every field on Scar (e.g. `priority_score`, `protection_level`, `tags`, `metadata`, `status`, `created_by`).

Therefore:

```text
content_hash valid  ≠  every Scar field is unchanged
```

**Correct conclusion (narrow):**  
«The recorded hash remains consistent with the fields included in the current hashing function.»

That is evidence. It is not a universal integrity certificate.

**Example:** Change `priority_score` 1.0 → 99.0. Hash can stay valid. So hash-valid must not mean entire-record-unchanged.

---

## 6. Why this matters for Firefly

Careless chain:

```text
hash valid → record trusted → memory trusted → memory authoritative
```

Correct model:

```text
Scar → bounded evidence → contract evaluation → Firefly memory record
```

No automatic authority upgrade.

---

## 7–8. Classify every field

For every field ask:

| Q | Question |
|---|----------|
| A | Can Firefly consume it? |
| B | Must Firefly preserve it? |
| C | Is it covered by the current integrity mechanism? |
| D | What does it actually establish? |
| E | What must Firefly refuse to infer from it? |

| Field | Consume? | Hash-covered? | Meaning |
|-------|----------|---------------|--------|
| scar_id | Yes | No | Record identity |
| title | Yes | Yes | Opaque content |
| description | Yes | Yes | Opaque content |
| trigger_context | Yes | Yes | Opaque context |
| failure_signature | Yes | Yes | Recorded signature |
| recommended_response | Yes | Yes | Opaque recommendation |
| content_hash | Yes | — | Integrity evidence |
| priority_score | Yes | **No** | Metadata |
| protection_level | Yes | **No** | SCAR metadata |
| tags | Yes | **No** | Metadata |
| metadata | Restricted | **No** | Potential smuggling channel |
| created_by | Yes | **No** | SCAR-reported provenance |
| source_event_id | Yes | **No** | Source reference |
| status | Yes | **No** | State |
| embedding | **No** (v1) | No | Out of scope |

The important column people forget: **Hash-covered?**

---

## 9–10. metadata is the smuggling door

```json
{"truth": true, "trusted": true, "m11_admitted": true, "replay_verified": true}
```

Blind copy ⇒ authority without evidence.  
**Unknown metadata must not automatically cross the boundary.** Initial design: allowlist.

Names and values are not automatically evidence. Evidence requires a defined process and provenance.

---

## 11. Four-level thinking exercise

```text
What is stored?
    ↓
What is validated?
    ↓
What is proven?
    ↓
What am I tempted to assume?   ← challenge this leap
```

Example: stored content_hash → validated hash matches covered content → proven bounded content consistency → temptation “memory is true” → **reject the leap**.

---

## 12–15. Status, priority, provenance, recommendation

| Concept | Rule |
|---------|------|
| Status ACTIVE/SUSPECT/… | Describe SCAR record; not universal truth. SUSPECT ≠ FALSE; ACTIVE ≠ TRUE |
| priority_score | Metadata; not permission; not “execute immediately” |
| created_by | SCAR-reported provenance ≠ independently verified identity |
| recommended_response | Opaque recommendation ≠ authorized command |

---

## 16. Embeddings

Optional on SCAR ≠ required on first Firefly adapter. Embeddings open model/version/dim/reproducibility/similarity/authority/drift questions. **Out of scope for adapter v1.**

---

## 17–18. Mutation and silent repair

SCAR can detect mutations of **hash-covered** fields only. Firefly must preserve **snapshot at T0**; T1 source changes must not silently rewrite T0 memory.

```text
content=A, hash=hash(B)  →  INTEGRITY_FAILURE → REJECT/HALT
```

Do **not** recalculate hash(A) and overwrite to ACCEPT. The mismatch is valuable evidence.

---

## 19–22. Critical teaching tests

| Test | Setup | Correct outcome |
|------|--------|-----------------|
| Authority laundering | Valid SCAR + metadata truth/trusted/m11_admitted/replay_verified | AUTHORITY_FAILURE → REJECT/HALT → no memory authority |
| Semantic creep | Text about intent/future | Preserve statement; not established intention; not future fact |
| M11 injection | m11_admitted without admission evidence | REJECT — Firefly cannot manufacture AdmittedInput |
| Replay injection | replay_verified without replay process/result | REJECT — memory of a claim ≠ replay |

---

## 23–24. Good adapter behaviour & negative space

A good adapter is intentionally boring: receive, validate, preserve, classify, reject, report. It does not: guess, upgrade, interpret, authorize, invent, repair.

Boundary tests must include: valid, mutated, missing identity/provenance, hash mismatch, unknown metadata, truth/trust/M11/replay/priority/semantic/embedding injection.

---

## 25. Evidence ladder

```text
CLAIM → IMPLEMENTATION → TEST → CI → AUDIT → SEAL
```

A SCAR record does not jump to the top. hash ≠ audit ≠ seal ≠ truth.

---

## 26. Core architectural law

```text
DATA MAY CROSS
MEANING MUST BE CONTROLLED
AUTHORITY MUST BE EARNED
```

«Never allow a boundary to increase the authority of information merely because another component can store it.»

---

## 27. Practical developer workflow

1. Read the source (actual SCAR model)  
2. Read the tests (demonstrated behaviour)  
3. Build the field matrix (consume / preserve / hash-covered / meaning / forbidden inference)  
4. Identify smuggling channels (metadata, status, priority, provenance, free text, extensions)  
5. Write adversarial tests  
6. Review failures (weak contract signal)  
7. Freeze the contract  
8. Authorize implementation only after acceptance criteria are explicit  

---

## 28. Current SWI position

| Component | Status |
|-----------|--------|
| V1 SCAR | IMPLEMENTED / TESTED |
| SCAR → Firefly contract | AUDITED / DESIGN FROZEN |
| Adapter | NOT IMPLEMENTED |
| Firefly | DESIGN / DEFERRED |
| M11 | SEALED |
| Replay | NOT SEALED |
| M12 | IMPLEMENTATION FROZEN |
| M13–22 | BLOCKED |

Related: `SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md` · `SCAR_FIREFLY_CONTRACT_AUDIT.md` · `SCAR_FIREFLY_ADAPTER_TEST_SPEC.md` · `SCAR_FIREFLY_TEACHING_MANUAL.md` · V1 `SCAR_STATUS.md`

---

## 29. Final exercise

Before approving any Firefly code, ask:

«Show me exactly where this piece of information **gains authority**.»

Insufficient answers: “It was already in SCAR.” · “The adapter copied it.” · “The hash matched.”

The developer must identify the **actual contract and evidence** that establishes authority. If they cannot → **HALT**.

---

## 30. Final doctrine

«Memory is not truth.  
Integrity is not truth.  
Provenance is not automatically identity proof.  
Priority is not authority.  
A signature is not replay.  
M07 is not M11.  
A stored claim is not an established fact.  
And a boundary is not safe merely because the code successfully crosses it.»

When information crosses SCAR → Firefly: evidence stays bounded, provenance stays visible, uncertainty stays visible, and authority does not silently increase.
