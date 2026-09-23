# SWI COMPLETE FIX MANUAL — 23 September 2026

**Status:** RESEARCH / EXPERIMENTAL  
**Production:** NOT AUTHORIZED  
**Execution module:** BLOCKED  
**M11:** NOT SEALED  
**Foundation PASS:** NOT YET CLAIMED

This is the governing controlled procedure for the current milestone.

---

## 0. FREEZE THE BOUNDARY FIRST

**CURRENT MILESTONE:**

```
SWI NON-EXECUTION FOUNDATION PASS
```

**Allowed:**
- BUILD
- TEST
- EVIDENCE
- FRESHNESS
- INTEGRITY
- REPLAY
- CROSS-REPO TRAVEL
- BOUNDARY VERIFICATION
- DOCUMENTATION
- AUDIT

**NOT allowed:**
- PRODUCTION EXECUTION
- BLOCKED EXECUTION MODULE
- M11 SEAL
- PRODUCTION AUTHORIZATION
- FORMAL PRE-R PROMOTION

Do not modify a test simply because it prevents execution.

---

## 1. FIX THE STALE EVIDENCE FAILURE FIRST

### Current failure

```
FAILED tests/law/test_evidence_freshness.py::test_evidence_source_tip_reachable_from_head

source_tip = 8245e3f03d8673c966abf9c63be9d838073159b0
HEAD       = a6b81fb3de23c5d392fa478ede7d814a5030a1f5

Result: stale/orphaned evidence
```

### What this means

The evidence claims it was generated from commit X, but the repository is at commit Y, and X is neither Y nor an ancestor of Y. The evidence cannot honestly be presented as evidence for the current repository state.

### Do NOT do this

```
# BAD
source_tip = CURRENT_HEAD
```

Also do not:

- delete the freshness test
- loosen the ancestor check
- manually replace the SHA
- call historical evidence current
- rewrite old evidence as though it was newly generated

### Correct repair

**Step 1 — identify the evidence artifact**  
Find the JSON/report/receipt that contains `source_tip = 8245e3f…`.

**Step 2 — determine its status**

**Case A — historical evidence**  
If the evidence genuinely belongs to the older commit:

```
STATUS = HISTORICAL
```

Keep it. Do not destroy it. Add explicit metadata:

```json
{
  "status": "HISTORICAL",
  "source_tip": "8245e3f03d8673c966abf9c63be9d838073159b0",
  "current_head": "a6b81fb3de23c5d392fa478ede7d814a5030a1f5",
  "current_proof": false
}
```

The freshness test must not treat deliberately archived historical evidence as current evidence.

**Case B — supposed current evidence**  
Regenerate it:

```
checkout current HEAD
        ↓
run actual test
        ↓
capture result
        ↓
capture current commit SHA
        ↓
generate evidence
        ↓
verify SHA
        ↓
verify replay
        ↓
commit evidence
```

Resulting evidence must contain:

```json
{
  "source_tip": "<actual current HEAD>",
  "test_result": "PASS",
  "replayable": true
}
```

Then re-run:

```
pytest -q
pytest -q tests/law/test_evidence_freshness.py
```

### Required status distinction

The repository must distinguish:

- CURRENT
- HISTORICAL
- REFRESH_REQUIRED
- FAIL
- BLOCKED

rather than converting every stale receipt into FAIL.

---

## 2. ESTABLISH ONE UNIVERSAL SWI EVIDENCE CONTRACT

Every current evidence artifact must answer:

- WHAT was tested?
- WHICH implementation was tested?
- WHICH commit was tested?
- WHICH tests ran?
- WHAT was the result?
- WHEN was it tested?
- WHAT exactly was proven?
- WHAT was NOT proven?
- CAN it be replayed?
- IS source_tip reachable from HEAD?

Minimal structure:

```json
{
  "evidence_id": "...",
  "repository": "...",
  "source_tip": "...",
  "generated_at": "...",
  "test_command": "...",
  "result": "PASS",
  "tests_passed": 0,
  "tests_failed": 0,
  "replayable": true,
  "scope": "...",
  "limitations": [],
  "status": "CURRENT"
}
```

This is the common evidence discipline across V1, V2, Firefly, Mathematical Evidence Engine, API Foundation, Node Access Boundary, and Rust.

---

## 3. FIX THE LEGACY SWI REPOSITORY FAILURE

**Repository:** Structured-Workflow-Intelligence  
**Result:** 22 passed, 1 failed

**Failing test:**
```
tests/admission/test_positive_admission.py::test_execution_gate_allows_on_admit
expected: outcome["executed"] is True
actual:   outcome["executed"] is False
```

### DO NOT immediately change the code

First establish what the test is supposed to prove.

Current test expectation:

```
ADMIT → EXECUTED = TRUE
```

Current SWI doctrine:

```
ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

This old test may be testing an older architecture assumption.

### Controlled steps

1. Inspect the test and document: What does ADMIT mean here? What does EXECUTED mean? Is execution intended at this layer? Is the repository historical/legacy?
2. Trace: test → admission function → gate → outcome → executed. Do not modify yet.
3. Compare against current boundary model (DATA → EVIDENCE → ADMISSION → AUTHORIZATION → ACTION).
4. Classify the repository.

If it is a legacy test expecting execution directly from admission, record:

```
LEGACY CONTRACT CONFLICT
```

rather than weakening the current boundary.

### Two controlled paths

**Path A — preserve historical behaviour**  
Keep the test and mark the repository:

```
LEGACY
NOT CURRENT SWI CONTRACT
```

**Path B — migrate the contract** (only if explicitly authorized)

```
old: ADMIT → EXECUTE
new: ADMIT → AUTHORIZATION CHECK → ACTION
```

Do not implement the action layer now while execution is blocked.

Safe interim test:

```
ADMIT → admitted = TRUE
        execution = NOT_PERFORMED
```

That proves the admission boundary without opening execution.

---

## 4. V1 — KEEP THE GREEN STATE

**Verified result:** SWI-V1-Module-1-10 — 306 tests passed (Python 3.10; CI also 3.11/3.12)

Do not rebuild V1.

Verify only:

```
HEAD → CI run → test result → evidence artifact → source_tip
```

- If ancestor → REFRESH_REQUIRED
- If current → CURRENT / PASS
- If deliberately historical → HISTORICAL

V1 remains a stable foundation.

---

## 5. V2 — PRESERVE THE VERIFIED FOUNDATION

**Verified result:** 152 passed (Python 3.12) + verification summary PASS + two-checkout travel PASS

```
V2 = TESTED
V2 = CI-VERIFIED
V2 ≠ SEALED
```

Do not convert:

```
152 PASS → M11 SEALED
```

Instead:

```
152 PASS → CURRENT TEST EVIDENCE → BOUNDARY REVIEW → INDEPENDENT AUDIT → possible future seal
```

M11 remains **NOT SEALED**.

---

## 6. PRE-R — DO NOT PROMOTE IT

PRE-R boundary tests pass within existing scope. Keep:

```
TESTED
```

Do not convert into:

```
FORMAL PRE-R
AUTHORIZED
PRODUCTION READY
```

Correct chain:

```
implementation → tests → test evidence → boundary review → audit
```

Not:

```
tests passed → authorization
```

---

## 7. LAW INGESTION — FIX FRESHNESS, NOT ARCHITECTURE

Keep the existing separation:

```
LAW DATA ≠ LAW EVIDENCE ≠ LIFECYCLE EVENT ≠ POLICY INTERPRETATION ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

Law lane remains:

```
LAW SOURCE → INGEST → LAW ARTIFACT → CANONICALIZE → HASH → INTEGRITY VERIFY → PASS/REJECT → LIFECYCLE → POLICY MAPPING
```

Future diagnostic layer (above, not inside):

```
NEW LAW / AMENDMENT → INGEST → DIAGNOSE → IDENTIFY AFFECTED BOUNDARIES → TEST → REPORT IMPACT → HUMAN / AUTHORIZED DECISION
```

```
LAW INGESTED ≠ ACTION AUTHORIZED
```

---

## 8. FOUR LAW NEGATIVE-TEST FAMILIES (MUST REMAIN)

A. Missing authority → AuthorityHalt → ZERO WRITE  
B. Wrong authority → AuthorityError → ZERO WRITE  
C. Forged hash → REJECT → ZERO WRITE  
D. Valid operation (correct authority + valid hash + valid artifact) → ACCEPT

Negative tests are more valuable than the happy path alone.

---

## 9–13. UNVERIFIED REPOSITORIES

| Repository | Current | Required action |
|------------|---------|-----------------|
| Mathematical Evidence Engine | ⚪ NO VERIFIED CI | Establish CI workflow → pytest → evidence → freshness |
| API Foundation (SWI_V103_API_Foundation) | ⚪ NOT VERIFIED | Inspect → identify tests → CI → evidence → freshness |
| Node Access Boundary | ⚪ NOT VERIFIED | Same + explicit negative tests (unauthorized/missing/wrong/malformed → reject/halt; valid → accept). REJECT must not become ACTION |
| Rust (structured-workflow-intelligence-rust) | ⚪ NOT VERIFIED | Establish what is implemented/tested; cargo test; record rustc/cargo/SHA/flags/platform. No parity claim until behaviour is tested |
| Firefly Memory | 🟢 PASS | Check HEAD + workflow + freshness + replayability only. Stale evidence → REFRESH_REQUIRED, not SYSTEM FAILURE |

Do not add architecture merely because CI is missing. First determine whether functionality already exists.

---

## 14. UNIVERSAL STATUS MODEL

| Status | Meaning |
|--------|--------|
| 🟢 PASS | Current required tests/evidence pass |
| 🟡 REFRESH_REQUIRED | Historical evidence exists but current evidence must be regenerated |
| 🔵 HISTORICAL | Deliberately preserved old evidence |
| ⚪ NOT_VERIFIED | No trustworthy current execution evidence |
| 🔴 FAIL | Current reproducible test contradicts required behaviour |
| ⛔ BLOCKED | Intentionally outside current execution scope |
| 🔒 NOT_SEALED | Tested but formal sealing requirements not satisfied |
| 🚫 NOT_AUTHORIZED | No production authorization |

This prevents one stale SHA from becoming a false system-wide failure.

---

## 15. MASTER VERIFICATION PIPELINE

```
1. IDENTIFY IMPLEMENTATION
2. IDENTIFY CURRENT HEAD
3. RUN COMPLETE TEST SUITE
4. CAPTURE RAW RESULT
5. GENERATE EVIDENCE
6. VERIFY source_tip == HEAD OR ANCESTOR
7. REPLAY
8. NEGATIVE TESTS
9. BOUNDARY AUDIT
10. CLASSIFY STATUS
```

---

## 16. WHAT “PASS” MEANS AT THIS MILESTONE

Do **not** define PASS as “everything executes”.

**SWI FOUNDATION PASS** means:

- implementation identified
- tests executed
- results reproducible
- evidence tied to source
- freshness verified
- negative paths tested
- boundaries preserved
- cross-repository travel verified
- limitations documented
- blocked execution remains blocked

Then:

```
FOUNDATION PASS ≠ PRODUCTION READY
FOUNDATION PASS ≠ SEALED
FOUNDATION PASS ≠ AUTHORIZED
```

---

## 17. FINAL ORDER OF REPAIR (DO NOT REORDER)

```
01  Fix/classify stale evidence
02  Establish universal evidence contract
03  Refresh current evidence
04  Re-run / confirm V1
05  Re-run / confirm V2
06  Re-run / confirm two-checkout travel
07  Verify PRE-R boundary tests
08  Verify law-ingestion tests
09  Classify legacy execution failure
10  Do NOT open blocked execution
11  Establish CI for Mathematical Evidence Engine
12  Establish CI for API Foundation
13  Establish CI for Node Access Boundary
14  Establish Rust test/evidence pipeline
15  Reconfirm Firefly
16  Cross-repository evidence audit
17  Independent audit
18  FOUNDATION PASS (only if all prior gates hold)
```

---

## GOVERNING RULE

> Don’t make the system green by making the test weaker.  
> Make it green by making the evidence true, current, reproducible and correctly scoped.  
> Where something genuinely fails, preserve the failure until the implementation or contract is corrected.

That is stronger evidence for SWI than every repository reporting PASS.

End of manual.
