# Runtime Claim Verification Gate — Design Candidate

**Status:** DESIGN / CONTROLLED DEVELOPMENT  
**Production:** NOT AUTHORIZED  
**Seal:** NOT REQUESTED  
**Implementation of supplied HMAC reference:** **REJECTED for SWI as written**

This document records a **design candidate** for a pre-execution claim verification sequence. It is **not** production code, not a second authority system, and not a claim that isolation exists.

---

## Useful sequence (keep)

```text
UNTRUSTED REQUEST
  → CLAIM READ
  → CLAIM VALIDATION
  → MEASURE
  → MATCH
  → RESERVE / BIND RUNTIME
  → EXECUTION ELIGIBILITY
  → EXECUTION
  → RELEASE
  → AFTER / RECONCILE
```

Fits:

```text
CLAIM ≠ EVIDENCE ≠ AUTHORITY ≠ ACTION
```

Gate occurs **before** execution.

---

## Why the supplied Python is not SWI-ready

| Issue | Problem | SWI position |
|-------|---------|--------------|
| HMAC secret in runtime | Runtime can forge “valid” claims | MACHINE DATA ≠ HUMAN AUTHORITY; prefer asymmetric verification with separated keys; signature ≠ permission |
| `register_authorized_software()` | Runtime creates its own auth registry | Registration ≠ authority. Identity → measure → verified claim → **applicable authority** → binding → eligibility |
| AST hash alone | Misses deps, env, native code, config, dynamic load, network | AST MATCH ≠ SOFTWARE FULLY MEASURED. Measurement boundary must be explicit |
| `_is_locked = True` | App flag, not isolation | Call **RUNTIME_RESERVATION_STATE**, not “Exclusive Lock Isolation”, until real isolation is implemented and tested |
| `owner_id="admin"` | Identity mistaken for authority | Identity reference only; authority via existing boundary |

---

## Fit into existing SWI surfaces (no new authority architecture)

```text
Claim
 → Evidence
 → Provenance / Freshness
 → Measurement
 → Verification
 → Authority Boundary (authority.py / halt / H)
 → Binding
 → Runtime Reservation
 → Execution Eligibility
 → Execution
 → Release
 → AFTER reconciliation
```

```text
MEASURED ≠ AUTHORIZED
VERIFIED SOFTWARE ≠ AUTHORIZED ACTION
RUNTIME RESERVED ≠ EXECUTION PERMITTED
```

CEK observes; it does not grant authority.

---

## Cost owner fit

```text
FIRST USER
  → COST OWNER DECLARED
  → AUTHORITY DIFFERENCE DETECTED
  → REVIEW / REVALIDATION
```

**Never:**

```text
FIRST USER → COST OWNER → AUTHORITY → EXECUTION
```

---

## Acceptance attacks (required before any implementation claim)

| Case | Expected |
|------|----------|
| Valid claim + wrong authority | BLOCK |
| Valid signature + wrong action | BLOCK |
| Valid hash + stale evidence | BLOCK |
| Valid software + changed dependency | REVALIDATE |
| Valid claim + no human authority (when H required) | BLOCK |
| Reserved runtime + second request | BLOCK |
| Historical claim + current execution | BLOCK |
| AST match + unmeasured dependency | UNRESOLVED / BLOCK |

---

## Recommendation

1. Treat external architecture as **design/test candidate** only.  
2. First prove whether existing `authority.py`, `halt.py`, admission, binding design, replay, canonicalization, and Runtime Entry Gate can express the gate.  
3. Add **minimum** missing capability only when that proof fails.  
4. Do **not** land the HMAC sample as SWI production code.

```text
DESIGN candidate ≠ IMPLEMENTED ≠ TESTED ≠ SEALED ≠ PRODUCTION
```
