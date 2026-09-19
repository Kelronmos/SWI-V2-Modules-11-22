# SWI PRE-R Response Boundary — Fail-Closed vs Fail-Safe Rebuild Manual

**Date:** 2026-09-19  
**Status:** EXPERIMENTAL — NOT SEALED — NOT PRODUCTION AUTHORIZED  
**Tip note:** `tests/pre_r/test_response_boundary.py` **exists** on current tip (historical gap was `64bf105` only).

---

## 1. Two separate proofs

### FAIL-CLOSED (admission)

> May this request cross the security gate?

```text
PROVEN     → ADMIT
NOT PROVEN → REJECT / HALT
```

Unknown is not permission.

### FAIL-SAFE (enforcement)

> What happens after the system cannot safely proceed?

```text
FAILURE → STOP → NON-EXECUTING STATE
  → NO privileged side effect
  → NO output release
  → EXPLICIT recovery required
```

**REJECT is a decision. Fail-safe is enforced behaviour after the decision.**

A security decision is incomplete if the system can ignore it.

---

## 2. Current pre-R implementation (honest)

`ReturnGate.evaluate()`:

| Property | State |
|----------|--------|
| Gate-level fail-closed (invalid → REJECT, all pass → ADMIT) | **IMPLEMENTED / unit-tested** |
| `BoundaryDecision.HALT` constant | Present; gate path currently returns REJECT for failures |
| `may_execute()` on response / sticky HALTED workflow in pre-R | **NOT IMPLEMENTED** in experimental slice |
| Caller forced to honor REJECT | **Dependent on caller** until an enforcement layer is added and tested |
| Automatic recovery | **NOT IMPLEMENTED** |

**Precise claim:**

> Gate-level fail-closed is implemented and testable.  
> Fail-safe enforcement beyond the gate remains dependent on the caller/enforcement layer until explicitly implemented and tested.

Do **not** invent `may_execute()` merely so tests can pass. Match real APIs (or add enforcement under contract first).

Related proven patterns elsewhere in SWI (not automatic pre-R proof):

- V1 `ModuleKernel` — pre-check fail → no operation; post-check fail → no output release  
- V2 `HaltedWorkflow` / `require_admitted` — sticky non-execution  
- Authority HALT vs out-of-scope REJECT  

---

## 3. Doctrine invariants

```text
DATA ≠ AUTHORITY
EVIDENCE ≠ AUTHORITY
MODEL OUTPUT ≠ AUTHORITY
INTEGRITY ≠ TRUTH
record_halt() ≠ clear_halt() ≠ authorize_execution()
TESTED ≠ SEALED
CI GREEN ≠ PRODUCTION AUTHORIZATION
```

---

## 4. Test matrix extension (T20)

| Test | Proves |
|------|--------|
| Failure → REJECT | Gate fail-closed |
| Failure → HALT (when contract requires) | Terminal decision vocabulary |
| HALT → non-executing state | Fail-safe (only if API exists) |
| REJECT → no output release | Fail-safe release boundary |
| Pre-check exception → no operation | Fail-safe |
| Post-check exception → no release | Fail-safe |
| Evidence/receipt → execute | Rejected as authority |
| **T20: caller ignores REJECT → still blocked** | Full fail-safe; **not yet proven in pre-R** |

Current suite focuses on gate decisions (A1–style). Expanding T20 requires an explicit enforcement primitive under contract.

---

## 5. Classification before “fixed”

F1 implementation · F2 contract · F3 test · F4 fixture · F5 environment · F6 intentional fail-closed · F7 ambiguous REJECT vs HALT

Never weaken a security assertion to obtain green CI.

---

## 6. Order of work

```text
CONTRACT → BOUNDARY → IMPLEMENTATION → UNIT → ADVERSARIAL
  → FAIL-SAFE ENFORCEMENT (if adding API) → REGRESSION → CI → DOCS
```

Historical missing-file CI error ≠ behavioral security failure.

---

## 7. Promotion language

Until fail-safe enforcement is implemented and tested for pre-R:

| Term | Allowed? |
|------|----------|
| EXPERIMENTAL / IMPLEMENTED / TESTED (gate) | Yes, with scope |
| CI-VERIFIED | Only with tip run evidence |
| SEALED / PRODUCTION READY / SECURE | **No** |

---

## 8. One-line summary

```text
FAIL-CLOSED = do not admit without proof
FAIL-SAFE   = do not continue unsafely after failure
```

Together: NOT PROVEN → NO ADMIT → REJECT/HALT → NON-EXECUTING (when enforced) → NO PRIVILEGED CONTINUATION → NO UNVALIDATED RELEASE.

Anything beyond gate-level REJECT in pre-R remains a **documented limitation** until independently implemented and tested.
