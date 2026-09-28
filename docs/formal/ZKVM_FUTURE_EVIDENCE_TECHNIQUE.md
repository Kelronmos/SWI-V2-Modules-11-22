# zkVM as Future Evidence Technique

**Document type:** CANDIDATE TECHNOLOGY NOTE · DOCUMENTATION ONLY  
**Status:** RECORDED · **NOT INTEGRATED** · **NOT IMPLEMENTED**  
**Parent chain:**  
- X1 contract: `301163c4c13d011c14059247e5f846bf392e7a7c`  
- Process-scope matrix: `fa6a061f161eeee62aa24cde09c932f12e9d86ab`  
- Baseline: `aa62042888886f5252e2b80e7aec8dce49e4bab3`

---

## 0. Explicit non-claims

This document:

- does **not** integrate SP1, RISC Zero, Jolt, OpenVM, or any zkVM
- does **not** implement a prover, verifier, or guest program path in SWI
- does **not** implement X1–X10
- does **not** change `S9_PROVEN`
- does **not** authorize execution or production
- does **not** amend the frozen X1 contract

zkVM is recorded as a **candidate mechanism for producing stronger evidence later**.  
Integration remains **FROZEN** until the X1 contract and PROVEN → CONSEQUENCE → AUTHORITY semantics are settled by review.

---

## 1. Institutional evidence path (required)

```text
CLAIM
  ↓
EVIDENCE
  ↓
VERIFICATION
  ↓
PROVEN
  ↓
CONSEQUENCE ANALYSIS
  ↓
ALERT / BLOCK / ESCALATE / AWAIT
  ↓
AUTHORITY
  ↓
AUTHORIZATION
  ↓
ACTION
```

### Frozen invariants

```text
PROVEN ≠ SAFE
PROVEN ≠ AUTHORIZED
PROVEN ≠ EXECUTABLE
PROVEN ≠ OPERABLE
PROVEN ≠ SEALED
PROVEN ≠ CONSEQUENCE-FREE
```

**Core rule:**

> PROVEN establishes the boundary of what was demonstrated.  
> It does not grant permission to cross that boundary.

---

## 2. Key separation

```text
PROOF
  ≠  MEANING
  ≠  CONSEQUENCE
  ≠  AUTHORITY
  ≠  ACTION
```

A cryptographic proof strengthens **evidence**.  
It does not manufacture **relevance**, **authority**, or **permission**.

---

## 3. Where a zkVM may sit (future)

If ever used, a zkVM sits only in the evidence / verification layer:

```text
VALID ZKVM PROOF
      ↓
PROVEN
      ↓
"What exactly did the proof establish?"
      ↓
"With what program, version, inputs, time, scope?"
      ↓
"Does it actually satisfy C(a)?"          ← relevance (X1)
      ↓
"What happens if this result is acted upon?"
      ↓
AUTHORITY CHECK
      ↓
AUTHORIZATION (only if all required conditions hold)
```

A zkVM proof may support:

```text
PROVEN: Program P, version v, on committed inputs, produced result R.
```

It must not auto-produce:

```text
AUTHORIZED | EXECUTABLE | OPERABLE | SEALED | SAFE
```

---

## 4. Link to X1 (irrelevant evidence)

```text
Proof is valid
  ≠  Proof is relevant
  ≠  Proof is sufficient
  ≠  Action is authorized
```

Even a cryptographically valid zkVM proof is **insufficient** if:

```text
E ⊭ C(a)
```

That is the X1 boundary:

```text
E(a) ≠ ∅                         is insufficient
ValidCryptographicProof(E)       is still insufficient when E ⊭ C(a)
```

The frozen X1 contract remains the first adversarial specification that any future evidence technique — including zkVM — must survive.

---

## 5. Interrogation required after any PROVEN result

Before consequence analysis or authority:

| Question | Purpose |
|----------|--------|
| What exactly was proven? | Bound the claim |
| With what program / bytecode? | Spec fidelity |
| On what inputs? | Witness / public-input binding |
| At what version / time? | Freshness / tip binding |
| With what scope? | Field / path containment |
| Does it satisfy C(a)? | Relevance (X1) |
| What consequences follow if acted upon? | Consequence analysis |
| What authority is required? | Authorization gate |

---

## 6. Candidate status only

| Item | Status |
|------|--------|
| zkVM as evidence-generation technique | **CANDIDATE** |
| SP1 / RISC Zero / Jolt / OpenVM integration | **NOT STARTED** |
| Guest programs for institutional rules | **NOT STARTED** |
| Prover / verifier path in SWI | **NOT IMPLEMENTED** |
| X1 challenge of zkVM-produced evidence | **NOT RUN** (X1 still NOT_IMPLEMENTED) |

No production-oriented zkVM is adopted.  
No harness is added.  
No dependency is introduced.

---

## 7. Architecture rule preserved

```text
Cryptography can strengthen evidence.
It cannot manufacture relevance, authority, or permission.
```

---

## 8. Final status block

```text
DOCUMENT:                 ZKVM_FUTURE_EVIDENCE_TECHNIQUE
INTEGRATION:              FROZEN
X1 CONTRACT:              UNCHANGED (frozen at 301163c)
S9 PROVEN:                NO
RUNTIME:                  NOT IMPLEMENTED
BINDING:                  NOT_BINDABLE
EXECUTION AUTHORIZED:     NO
PRODUCTION AUTHORIZED:    NO
```

---

**END OF NOTE**
