# SWI Evidence Freshness Status — 23 September 2026

**Status:** RESEARCH / EXPERIMENTAL  
**Production:** NOT AUTHORIZED  
**Execution module:** BLOCKED  
**Seal:** NOT AUTHORIZED

---

## 0. PURPOSE

Record the correct interpretation of the evidence freshness failure and the SWI-wide non-execution foundation gate.

This document does **not** weaken any test.
This document does **not** hand-edit any source_tip.
This document does **not** authorize execution.

---

## 1. OBSERVED FAILURE

```
FAILED tests/law/test_evidence_freshness.py::test_evidence_source_tip_reachable_from_head
AssertionError: stale/orphaned evidence:
  source_tip '8245e3f03d8673c966abf9c63be9d838073159b0'
  is not HEAD 'a6b81fb3de23c5d392fa478ede7d814a5030a1f5'
  and not an ancestor of HEAD
```

**Classification of this failure:**

| Label | Meaning |
|-------|--------|
| STALE / ORPHANED EVIDENCE | Evidence artifact claims a source tip that is not reachable from current HEAD |
| NOT a law-ingestion implementation failure | The test is correctly rejecting non-current evidence |
| REFRESH_REQUIRED | Current proof cannot be established from this artifact |

---

## 2. GOVERNING RULE (UNIVERSAL)

Every current evidence package must answer:

- WHAT was tested?
- WHICH implementation?
- WHICH COMMIT?
- WHICH TEST RESULT?
- WHEN?
- WHAT DID IT PROVE?
- WHAT DID IT NOT PROVE?
- CAN IT BE REPLAYED?
- IS THE SOURCE TIP REACHABLE FROM CURRENT HEAD?

Required condition for **current** evidence:

```
source_tip == HEAD
        OR
source_tip ∈ ancestry(HEAD)
```

If neither holds:

```
FAIL — STALE / ORPHANED EVIDENCE
```

**Do not** manually rewrite the SHA to manufacture a PASS.

---

## 3. STATUS VOCABULARY (ENFORCED)

| Status | Meaning |
|--------|--------|
| 🟢 PASS | Current evidence verified against reachable source_tip |
| 🟡 REFRESH_REQUIRED | Evidence is historically valid but cannot establish current state |
| 🔵 HISTORICAL | Deliberately preserved old evidence (must be labelled) |
| 🔴 FAIL | Claimed current property is contradicted or cannot be reproduced |
| ⚫ BLOCKED | Scope intentionally not entered |

**Key distinction:**

- Stale evidence = **evidence freshness FAIL** for that artifact (unless explicitly HISTORICAL).
- Stale evidence ≠ automatic “SWI system failure”.

---

## 4. CORRECT RESPONSE SEQUENCE

```
CURRENT HEAD
     ↓
RE-RUN REQUIRED TESTS
     ↓
GENERATE FRESH EVIDENCE
     ↓
RECORD CURRENT SOURCE TIP
     ↓
VERIFY source_tip ∈ ancestry(HEAD)
     ↓
PASS (or remain REFRESH_REQUIRED)
```

If the evidence is intentionally historical:

```
EVIDENCE_STATUS = HISTORICAL
CURRENT_STATUS  = NOT_CURRENT
```

Preserve it. Do not interpret it as a system failure.

---

## 5. SWI-WIDE NON-EXECUTION FOUNDATION GATE

Milestone target:

> **SWI NON-EXECUTION FOUNDATION PASS**

Only when all of the following hold:

| Area | PASS condition | Freshness applies? |
|------|----------------|--------------------|
| V1 M00–M10 | Full V1 regression | Yes |
| V2 M11–M22 (applicable) | Full applicable regression | Yes |
| Law ingestion | Authority, integrity, policy, registry, lifecycle, replay, freshness | Yes — mandatory |
| PRE-R / boundary | Existing PRE-R tests (incl. T20 where implemented) | Yes |
| Cross-repo travel | Two-checkout / evidence-travel tests | Yes |
| Evidence artifacts | source_tip is HEAD or verified ancestor | Yes |
| Hashes / canonicalisation | Integrity + tamper tests | Yes |
| Replay | Existing replay tests within stated limits | Yes |
| Authority | Missing → HALT; wrong → REJECT; valid → permitted transition | Yes |
| Documentation | Status accurately reflects TESTED / CI-VERIFIED / NOT SEALED | Yes |
| Independent audit | Another review can reproduce evidence and limitations | Yes |
| **Execution module** | **Remains BLOCKED** | **NO** |

**PASS does not mean SEALED.**

Example truthful statement after the gate:

> CURRENT FOUNDATION / NON-EXECUTION LAYERS: PASS — TESTED AND REPRODUCIBLE  
> M11: NOT SEALED (or historical seal preserved)  
> PRE-R: NOT AUTHORIZED  
> EXECUTION: BLOCKED  
> PRODUCTION: NOT AUTHORIZED

---

## 6. IMMEDIATE WORK SEQUENCE (ORDERED)

1. Locate why evidence still points to `8245e3f…`
2. Determine whether it is HISTORICAL or intended as CURRENT
3. If intended CURRENT → regenerate evidence from current HEAD
4. Run the freshness test
5. Run complete relevant regression
6. Verify negative / authority paths
7. Verify cross-repo travel
8. Review evidence artifacts
9. Independent audit
10. Record PASS / FAIL / REFRESH_REQUIRED / HISTORICAL / BLOCKED per gate

Do **not** push into the blocked execution module.

---

## 7. EXPLICIT NON-CLAIMS

This status record does **not**:

- weaken or remove `test_evidence_source_tip_reachable_from_head`
- hand-edit any source_tip SHA
- authorize execution
- reseal any module
- convert REFRESH_REQUIRED into PASS by declaration
- convert TESTED into SEALED
- convert SEALED into PRODUCTION AUTHORIZED

---

## 8. CURRENT DECISION

```
EVIDENCE FRESHNESS          = REFRESH_REQUIRED (for the reported artifact)
LAW LANE                    = cannot claim CURRENT PASS until freshness clears
EXECUTION MODULE            = BLOCKED
PRODUCTION                  = NOT AUTHORIZED
NON-EXECUTION FOUNDATION    = IN PROGRESS (target defined above)
```

The freshness failure is consistent with SWI evidence discipline:

> Evidence freshness is itself a property that must be tested.

End of status record.
