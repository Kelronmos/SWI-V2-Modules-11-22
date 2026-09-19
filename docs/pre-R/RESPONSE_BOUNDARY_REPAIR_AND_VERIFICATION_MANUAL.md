# SWI pre-R Response Boundary — Build, Repair, Verification & Evidence Manual

**Status:** PRE-R / EXPERIMENTAL  
**Authority:** NOT SEALED  
**Production:** NOT AUTHORIZED  
**Primary rule:** Do not convert a passing test into a system-wide security claim.

Order: Claim → Contract → Implementation → Test → Result → Limitation → Next iteration.

## Purpose

Repair and verify the experimental response boundary without weakening V1/V2.

Demonstrate under controlled tests: explicit authority, admission, classification, non-escalation, no implicit authority transfer, fail-closed, evidence continuity, tamper detection, deterministic rejection, separation from sealed foundation.

Not a replacement for M11, CRTG, Foundation Seal 5, or production security.

## Architectural constraints

```text
V1 produces evidence only → V2 admits (M11) → seal → kernel
V2 must not import V1 / execute V1 internals / inherit V1 authority
pre-R is experimental and separate
```

## Failure classification (mandatory before “fixed”)

| Code | Meaning |
|------|--------|
| F1 | Implementation defect |
| F2 | Contract defect |
| F3 | Test defect |
| F4 | Fixture defect |
| F5 | Dependency/environment |
| F6 | Intentional fail-closed |
| F7 | Ambiguous behaviour |

Do **not** change tests merely to obtain a green badge.

## Doctrine

```text
DATA ≠ AUTHORITY · DISCOVERY ≠ ACCESS · MODEL OUTPUT ≠ TRUST
ALLOW / DENY / HALT (do not collapse all failures to False)
UNKNOWN / missing / malformed ⇏ ALLOW
INTEGRITY ≠ TRUTH · TESTED ≠ SEALED · IMPLEMENTED ≠ AUTHORIZED
```

## Decision semantics

| Decision | Meaning |
|----------|--------|
| ALLOW | All required conditions satisfied |
| DENY | Request understood but not permitted |
| HALT | Cannot safely establish required condition |

## Regression gate

Reject a pre-R change if it causes: V1 CI fail, V2 CI fail, M11 regression, two-checkout failure, tamper acceptance, authority escalation, V1 import inside V2, fail-open exceptions.

## Status vocabulary

TESTED · CI-VERIFIED · AUDITED · SEALED · PROPOSED · IMPLEMENTED · NOT IMPLEMENTED · NOT AUTHORIZED — never substitute one for another.

## Limitations (standing)

1. Suite pass ≠ all attacks prevented  
2. Hash ≠ semantic truth  
3. Tamper-evident ≠ tamper-proof  
4. Local test ≠ independent verification  
5. Ed25519 primitive ≠ key-management system  
6. Boundary pass ≠ whole SWI proven  
7. Model output remains untrusted data  
8. Experimental pre-R does not change V1/V2 seal status  

## Final acceptance

CONTRACT → IMPLEMENTATION → UNIT → ADVERSARIAL → FAIL-CLOSED → FULL V2 → TWO-CHECKOUT → CI → DOCS → AUDIT  
Even then PRE-R PASS ≠ SEALED.
