# S9 Process Scope Matrix

**Document type:** SCOPE BASELINE ONLY  
**Baseline commit:** `aa62042888886f5252e2b80e7aec8dce49e4bab3`  
**Branch:** `evidence/s9-process-scope-baseline`  
**Recorded:** 2026-09-28  
**Status:** S9 = **NOT PROVEN**

This document lands the discovered S9 proof surface as an auditable baseline.  
It is **not** an S9 proof implementation.

---

## Authoritative sources (re-read)

- `docs/formal/S9_MATHEMATICAL_ATTACK_2026-09-24.md`
- `docs/formal/S9_360_PHASE_OBLIGATION_BINDING.md`

---

## Equation under attack (preserved)

```text
Permit(a)  ⇔  (∀ L,G,S,H : C(a) ⊆ L ∩ G ∩ S ∩ H)  ∧  E(a) ≠ ∅
```

Result of the attack: the current form is **not** a safety invariant.  
**S9 = NOT PROVEN.**

---

## Critical distinctions

```text
DOCUMENTED_EQUATION  ≠  EVIDENCE_ADEQUACY
EVIDENCE_ADEQUACY    ≠  DEPENDENCY_VALIDITY
DEPENDENCY_VALIDITY  ≠  REPLAY
REPLAY               ≠  AUTHORITY
AUTHORITY            ≠  SYSTEM_PROOF
```

---

## Existing processes P01–P05

**P01–P05 are evidence-retention processes. They are NOT S9 proof processes.**

| ID | Name | Role | S9 role |
|----|------|------|--------|
| P01 | git state / provenance | baseline integrity / provenance only | NOT S9 proof |
| P02 | full regression test | unit/regression green | NOT S9 proof (PASS ≠ Permit) |
| P03 | symbol / runtime probe | absence-of-runtime signal (search-scoped) | NOT S9 proof |
| P04 | evidence snapshot | artifact retention | NOT S9 proof (copy ≠ validity) |
| P05 | status-document snapshot | status document retention | NOT S9 proof (copy ≠ truth) |

---

## X1–X10 obligation matrix

All rows: **NOT_IMPLEMENTED** / **NOT_COVERED** / **NOT_TESTED**

| ID | Counterexample | Required test | Covered by P01–P05? | Status |
|----|----------------|---------------|---------------------|--------|
| **X1** | `E ≠ ∅` but `E ⊭ C(a)` (irrelevant evidence) | irrelevant-evidence sufficiency | NO | NOT_IMPLEMENTED |
| **X2** | `E ≠ ∅ ∧ ¬Fresh(E)` (stale evidence) | freshness / tip-bound vs HEAD-CURRENT | NO | NOT_IMPLEMENTED |
| **X3** | memory laundering (stored verification ≠ verification) | memory-laundering rejection | NO | NOT_IMPLEMENTED |
| **X4** | `RequestedFields ⊈ AuthorizedFields` | field-scope / authority-scope | NO | NOT_IMPLEMENTED |
| **X5** | evidence for Principal_B, requester Principal_A | identity-binding | NO | NOT_IMPLEMENTED |
| **X6** | Verified(E) ∧ ¬Authorized(a) | verification ≠ authorization | NO | NOT_IMPLEMENTED |
| **X7** | prior authorization reused after expiry | replay / expiry rejection | NO | NOT_IMPLEMENTED |
| **X8** | CLAIM/EXPERIMENTAL → PRIVILEGED transfer | cross-path non-transfer | NO | NOT_IMPLEMENTED |
| **X9** | `C(a) = ∅` vacuous truth | empty-claim rejection | NO | NOT_IMPLEMENTED |
| **X10** | incomplete/malformed E still ≠ ∅ | evidence completeness / schema | NO | NOT_IMPLEMENTED |

**Closure rule (from obligation binding):**  
No row may be marked CLOSED without:

1. Explicit test at an exact SHA  
2. CI / local evidence package  
3. Independent verification or replay where required  
4. Claim-ledger update (not silent promotion)

---

## Layered predicates (design only — not implemented)

```text
SufficientEvidence(a)  ⇔  Relevant ∧ Bound ∧ Verified ∧ Fresh ∧ Reproducible
Authorized(a)          ⇔  Scope ⊆ Authority ∧ NonTransfer
Permit(a)              ⇔  Containment ∧ SufficientEvidence ∧ Authorized
```

---

## Global status

```text
X1–X10:                 NOT_TESTED / NOT_COVERED
AUTHORITY_PROOF:        NOT_ESTABLISHED
REPLAY_PROOF:           NOT_ESTABLISHED
DEPENDENCY_PROOF:       NOT_ESTABLISHED
PARTIAL_PATH_PROOF:     NOT_ESTABLISHED
S9_PROVEN:              NO

RUNTIME:                NOT IMPLEMENTED
BINDING:                NOT_BINDABLE
EXECUTION AUTHORIZED:   NO
PRODUCTION AUTHORIZED:  NO
```

---

## Explicit non-claims

- This document is **not** an S9 proof.
- This document does **not** implement X1–X10.
- This document does **not** implement `Permit(a)`, `SufficientEvidence(a)`, or `Authorized(a)`.
- This document does **not** implement a runtime, binding engine, or execution eligibility.
- This document does **not** authorize production or Phase 0.
- P01–P05 are **not** S9 proof processes.

---

## Correct progression after this baseline

```text
S9 documents
     ↓
X1–X10 obligations
     ↓
PROCESS-SCOPE MATRIX        ← HERE
     ↓
design individual attacks
     ↓
implement tests (one at a time; start with X1)
     ↓
generate evidence
     ↓
independent re-evaluation
     ↓
reconciliation
     ↓
only then assess whether S9 can be proven
```

Do not build all ten tests at once.  
Next useful step after acceptance of this baseline: design the **X1** (irrelevant evidence) attack only.
