# Program Proof Boundary

**Status:** DESIGN / NORMATIVE BOUNDARY  
**Seal:** NOT SEALED  
**Production:** NOT AUTHORIZED  
**Date:** 26 September 2026

SWI can be designed to prove **properties of a program and its execution path** under stated conditions.  
It cannot honestly prove that an arbitrary program is **universally** correct, safe, or truthful.

---

## What SWI can establish (scoped)

For a submitted program, SWI may produce evidence for:

| Concern | Meaning |
|---------|---------|
| **Identity** | Exactly which source/version was examined |
| **Reproducibility** | Same inputs and environment reproduce the same result |
| **Tests** | Specified tests passed, including adversarial tests |
| **Invariants** | Defined safety/security invariants were satisfied |
| **Dependencies** | Required modules and controls were present |
| **Data provenance** | Where inputs came from and how they were transformed |
| **Policy compliance** | Explicitly defined machine-checkable rules were satisfied |
| **Authorization** | A particular human/authority authorized a particular action |
| **Execution trace** | What was permitted, blocked, paused, or executed |
| **Failure behaviour** | Specified failure conditions produced required refusal/containment |
| **Integrity** | Tested artifact corresponds to the artifact later executed |

Honest result form:

> “These properties were tested/proven **under these stated conditions**.”

Not:

> “This program is proven correct.”

---

## Core law

```text
PROGRAM              ≠ PROOF
TEST RESULT          ≠ UNIVERSAL CORRECTNESS
FORMAL PROOF         ≠ AUTHORIZATION
SIGNATURE            ≠ TRUTH
EXECUTION SUCCESS    ≠ SAFETY
SEALED EVIDENCE      ≠ PERMISSION TO ACT
```

---

## Pipeline

```text
PROGRAM → NORMALIZE → INSPECT → STATIC ANALYSIS → TEST
  → ADVERSARIAL TEST → FORMAL / PROPERTY CHECKS → EVIDENCE
  → VERIFICATION → REPRODUCTION → HUMAN AUTHORITY → AUTHORIZED EXECUTION
```

---

## Program Proof / Evidence Ledger (conceptual)

```text
Program / Version / Source Hash / Environment / Dependencies
Properties claimed: P001 …
Evidence: E001 test · E002 invariant · E003 replay · E004 adversarial
Verification: PASS | FAIL | INCOMPLETE
Authority: NONE | IDENTIFIED | AUTHORIZED
Execution: BLOCKED | AWAITING AUTHORITY | AUTHORIZED | COMPLETED
```

S9 / execution gate asks: required evidence, verification, policy, security, human authority, and execution conditions present? If not → **NO ACTION**.

---

## Reflexivity

SWI’s own proof machinery is subject to the same standard: testing, verification, replay, provenance, and authority controls. It cannot claim to prove programs while exempting itself.

**Proof claims must always be scoped to explicitly defined properties and conditions.**
