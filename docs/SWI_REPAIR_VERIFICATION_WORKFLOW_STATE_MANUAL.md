# SWI Repair, Verification & Workflow-State Manual

**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Branch:** architecture/kernel-progression-human-authority  
**Status:** RESEARCH / EXPERIMENTAL  
**Production:** NOT AUTHORIZED

## Purpose

Preserve the chain:

```text
CLAIM → IMPLEMENTATION → TEST → RESULT → EVIDENCE → REVIEW → AUTHORITY
```

No layer may silently replace another.

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
TESTED ≠ SEALED
CI_VERIFIED ≠ AUTHORIZED
MODEL_CHECKED ≠ LEGAL VALIDITY
PASSING TEST ≠ ETHICAL TRUTH
SIGNATURE alone ≠ REPLAY COMPLETENESS
```

## Filename reconciliation

Older plans may say `test_protected_humanity_adversarial.py`.  
**Live file:** `tests/architecture/test_ph_adversarial_boundary.py`

Do **not** create a duplicate family for an obsolete name.

## Workflow labels (states, not scores)

| Class | Labels |
|-------|--------|
| Blue | AWAITING_EXECUTION, AWAITING_CI, AWAITING_HUMAN, AWAITING_COMMAND, READY |
| Orange | EXECUTED |
| Yellow | TESTED |
| White | EVIDENCE_RECORDED, CI_VERIFIED, PIPE_SEALED |
| Red | HALTED |
| Black | NOT_AUTHORIZED, NOT_PROVEN |

Machine-readable: `docs/workflow_state_registry.json`

```text
PIPE_SEALED ≠ AUTHORIZED ≠ PRODUCTION
TESTED ↛ SEALED
A seal is a frozen (SHA, run, scope, limitations) contract — it does not travel with a branch.
```

## Cryptographic primitive rule

**Never** repair a governance, authorization, admission, or truth problem by adding a signature.

First identify the missing boundary, then choose the mechanism that actually proves it:

canonicalization · integrity verification · admission · authorization · human review ·
governance · legal/policy binding · execution control · evidence/replay

Use cryptography only for the property it actually proves.

```text
SIGNATURE ≠ TRUTH
SIGNATURE ≠ AUTHORITY
SIGNATURE ≠ ADMISSION
SIGNATURE alone ≠ REPLAY COMPLETENESS
SIGNATURE ≠ PRODUCTION AUTHORIZATION
```

Ed25519 placement: integrity over canonical bytes under a key. See `docs/ED25519_SIGNATURE_PRIMITIVE.md`.

M11 order remains: **admit first, then seal** — never `RAW → Ed25519 → admitted`.

## Repair protocol (summary)

1. Record exact remote, branch, HEAD SHA, status  
2. Locate live implementation (FIND FIRST)  
3. Check claimed problem exists (RepoGrade lesson)  
4. Define problem / invariant / test / limitation  
5. Smallest valid change  
6. Targeted → architecture → pre_r → full pytest  
7. CI on **exact** SHA  
8. Fresh checkout replay  
9. Independent review  
10. Seal only if repository seal contract is satisfied

## Forbidden shortcuts

```text
TESTED → AUTHORIZED | SEALED
CI_VERIFIED → PRODUCTION
MODEL_CHECKED → LEGAL | ETHICAL
COMMON_SENSE → AUTHORITY
SURVIVAL_CLAIM → AUTHORITY
Ed25519 PASS → ADMISSION | AUTHORITY | SEAL OF NEW SHA
```

## PH family (live)

`tests/architecture/test_ph_adversarial_boundary.py` — PH-01…14 per manual contract.

## Formal layers

- L0: `test_ph_formal_properties_l0.py` (P01–P14 executable)  
- L1: `docs/formal/common_sense_fsm.tla` — **TLC_NOT_RUN** until executed  
- Universal Gate: **NOT_PROVEN** while path universe open

## Operational position (update SHA when tip moves)

```text
🟡 L0 / PH — TESTED (local / fresh checkout evidence exists)
⚪ TLA FSM — PRESENT (EXECUTED as file write)
🔵 CI — AWAITING_CI
⚫ TLC — NOT_RUN
⚫ UNIVERSAL_GATE — NOT_PROVEN
🔵 Independent review — AWAITING_HUMAN
⚫ Seal — NOT_CLAIMED
⚫ Production — NOT_AUTHORIZED
```

## Immediate progression

```text
CURRENT TIP
  → AWAITING_CI
  → CI_VERIFIED (exact SHA)
  → FRESH_REPLAY
  → TLC optional
  → INDEPENDENT_REVIEW
  → seal requirements only if met
```

## Constitutional rule

```text
DO NOT REPAIR THE STORY.
REPAIR THE SYSTEM.
TEST THE SYSTEM.
RECORD THE EVIDENCE.
STATE THE LIMITATION.
DECIDE WHAT MAY PROGRESS.

DO NOT SEAL A CLAIM.
SEAL ONLY WHAT THE EVIDENCE ACTUALLY PROVES.
```
