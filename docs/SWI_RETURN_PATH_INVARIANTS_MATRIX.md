# Bidirectional Return Path — Invariants Matrix

**Date:** 2026-09-19  
**Scope:** pre-R experimental (not formal SWI modules)  
**Implementation:** NOT AUTHORIZED · **Code:** absent  

| Label | Meaning |
|-------|---------|
| **DESIGN** | Specified in build manual |
| **NOT TESTED** | No executable test yet |
| **TESTED** | Automated test exists and passes on a commit |
| **PROVEN** | Tested + CI on frozen tip + recorded evidence |
| **BLOCKED** | Depends on missing prerequisite |

## I-01 … I-15

| ID | Invariant | Status now |
|----|-----------|------------|
| I-01 | A result cannot create authority | **DESIGN / NOT TESTED** |
| I-02 | A UI cannot create authority | **DESIGN / NOT TESTED** |
| I-03 | A backend result is not automatically deliverable | **DESIGN / NOT TESTED** |
| I-04 | Verification state cannot be upgraded without evidence | **DESIGN / NOT TESTED** |
| I-05 | Integrity does not imply semantic truth | **DESIGN / NOT TESTED** |
| I-06 | A certificate is evidence, not unrestricted authority | **DESIGN / NOT TESTED** |
| I-07 | A receipt is evidence of an event, not automatically permission | **DESIGN / NOT TESTED** |
| I-08 | A response cannot silently change recipient | **DESIGN / NOT TESTED** |
| I-09 | An expired response cannot silently regain validity | **DESIGN / NOT TESTED** |
| I-10 | An unverified transformation cannot inherit verification automatically | **DESIGN / NOT TESTED** |
| I-11 | Unknown mandatory verification state cannot silently become ALLOW | **DESIGN / NOT TESTED** |
| I-12 | A new privileged action requires a new authority decision | **DESIGN / NOT TESTED** |
| I-13 | Forward authority does not expand during backward delivery | **DESIGN / NOT TESTED** |
| I-14 | The UI renders an admitted response; it does not establish its authority | **DESIGN / NOT TESTED** |
| I-15 | The response gate is the mandatory boundary between backend result and trusted delivery | **DESIGN / NOT TESTED** |

## pre-R map

pre-R01 Envelope · pre-R02 Binding · pre-R03 Authority · pre-R04 Evidence · pre-R05 Integrity · pre-R06 Provenance · pre-R07 Policy · pre-R08 Destination · pre-R09 Sealer · pre-R10 Delivery — all **DESIGN** only.

```text
DESIGN ≠ TESTED ≠ PROVEN ≠ SEALED
```
