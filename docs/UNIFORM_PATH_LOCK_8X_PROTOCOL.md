# SWI — Uniform Path-Lock & 8× Repeatability Protocol

**Date:** 2026-09-22  
**Status:** RESEARCH / EXPERIMENTAL  
**Production:** NOT AUTHORIZED  
**Seal:** NOT AUTHORIZED  
**Scope:** Controlled SWI experimental nodes only  
**M11 seal:** Unchanged / not expanded

---

## 1. Purpose

Establish one simple rule for every controlled journey:

> Only the verified next path is allowed. Everything else is a failure.

The same rule must apply whether the workflow is in a GOOD, BAD, HALTED, COMPLETED, or REPLAY state.

No special interpretation is permitted because a result looks reasonable.

---

## 2. Common-Sense Rule

```
CURRENT STATE
      |
WHAT IS THE EXACT NEXT ALLOWED PATH?
      |
OBSERVE ACTUAL PATH
      |
MATCH?
  +--------+--------+
 YES               NO
  |                 |
ALLOW              FAIL
OBSERVE            HALT
  |                 |
NEXT               LOCKED
STATE              STOP
```

**Fundamental invariant**

```
EXPECTED_NEXT_PATH == OBSERVED_PATH  ->  APPROVED OBSERVATION
EXPECTED_NEXT_PATH != OBSERVED_PATH  ->  FAILURE -> HALT -> NO FURTHER PATH
```

APPROVED OBSERVATION does **not** mean authorization to perform a real-world action.

---

## 3. Canonical Controlled Journey

Fixed reference journey:

```
NODE-A -> NODE-B -> NODE-C -> NODE-D
```

Allowed transitions only:

- A -> B
- B -> C
- C -> D

Anything else is an invalid next transition (A->C, A->D, B->D, C->X, C->B, D->E, ...) -> FAIL -> HALT.

The experiment does not negotiate with an invalid path.

---

## 4. GOOD STATE

Current state known. Expected next transition known. Observed transition matches exactly. Evidence available. Journey not halted.

Example:

```
CURRENT = B
EXPECTED = B -> C
OBSERVED = B -> C
RESULT = APPROVED_OBSERVATION
HALTED = FALSE
```

Journey may continue to the next verified state.

---

## 5. BAD STATE

Any required condition for the next transition is not satisfied (wrong destination, wrong origin, skipped node, repeated/replayed transition, unknown node, malformed transition, expired/missing state, foreign node, unexpected extra leg).

Uniform response:

```
RESULT = FAILURE
HALTED = TRUE
```

Do not repair the path inside the same journey.  
Do not silently skip the failure.  
Do not reinterpret the failure as success.

---

## 6. PATH LOCK

Once a journey begins, its path is locked. Previous approval cannot be reused as permission for a different transition.

```
PAST APPROVAL != NEXT PERMISSION
```

---

## 7. FIRST FAILURE LOCK

The first invalid transition becomes the controlling failure point.

```
FIRST FAILURE -> HALT -> ALL SUBSEQUENT TRANSITIONS -> JOURNEY_ALREADY_HALTED
```

No later event can erase the earlier failure.

---

## 8. REPLAY LOCK

Replay must reproduce the recorded experiment. It must not automatically create new authority.

```
ORIGINAL TRACE -> REPLAY INPUT -> RECONSTRUCTED TRACE -> COMPARE
```

Compare at minimum: journey ID, initial state, expected path, observed path, first failure, halt state, transition order, event IDs, hashes, final result.

```
REPLAY == REPRODUCTION
REPLAY != NEW AUTHORIZATION
```

---

## 9. Eight Identical Experimental Cycles

Each cycle:

```
TRY -> TEST -> TRACE -> RESULT -> REPLAY -> TEST REPLAY -> COMPARE -> RECORD
```

Conditions remain fixed. Rules are not changed because a previous cycle failed.

---

## 10. GOOD CONTROL — 8x

Path: `A -> B -> C -> D`

Expected: all transitions APPROVED_OBSERVATION, HALTED=FALSE, COMPLETED=TRUE.

Purpose: demonstrate that the valid path remains valid under the same conditions.

---

## 11. BAD CONTROL — 8x

Path: `A -> B -> C -> X` then attempt `X -> D`

Expected: C->X = FAILURE, HALTED=TRUE; subsequent = JOURNEY_ALREADY_HALTED.

Purpose: demonstrate consistent first-invalid-path failure and post-halt lock.

---

## 12. Additional Bad-State Families

Same grammar for: wrong door, skipped node, reverse path, duplicate transition, replay transition, unknown node, malformed transition, extra path after completion, foreign node, post-halt transition.

---

## 13. Uniform Evidence Record

Every cycle (success or failure) produces the same minimum record:

CYCLE_ID, TEST_ID, SEED, INITIAL_STATE, EXPECTED_NEXT_PATH, OBSERVED_PATH, PRECONDITION, RESULT, FIRST_FAILURE, HALTED, POST_HALT_RESULT, TRACE, TRACE_HASH, REPLAY_RESULT, REPLAY_MATCH, COMMIT_SHA, ENVIRONMENT, LIMITATION

No special evidence format for successful runs vs failed runs.

---

## 14. Comparison Rule

Do not ask "Did most runs pass?"  
Ask "Did every run obey the defined invariant?"

Divergence is an observation requiring investigation. It is not averaged away.

---

## 15. Common-Sense Locks (fixed before execution)

1. No guessing — UNKNOWN NEXT PATH -> HALT  
2. No skipping — SKIPPED REQUIRED PATH -> HALT  
3. No going backward — INVALID REVERSE -> HALT  
4. No replay-as-new — REPLAYED TRANSITION -> REJECT/HALT  
5. No approval inheritance — PREVIOUS APPROVAL != CURRENT AUTHORIZATION  
6. No silent recovery — HALTED remains HALTED until separately verified recovery exists  
7. No evidence laundering — NEW CLAIM -> NEW TEST -> NEW EVIDENCE  
8. No status inflation — TESTED != SEALED · CI GREEN != PRODUCTION AUTHORIZED · REPLAYED != TRUE

---

## 16. What the Experiment Can Actually Prove (bounded)

> Under the defined controlled conditions, the implemented exact-next-path evaluator consistently distinguishes the expected transition from defined invalid transitions, halts on the first invalid transition, and reproduces the recorded result under the defined replay procedure.

It does **not** prove: universal enforcement, OS/network-wide enforcement, real-world authorization correctness, production security, distributed-node security, M11 expansion, or production readiness.

---

## 17. Gate G2 Eligibility

G2 is eligible for consideration only when evidence demonstrates:

Exact next path + invalid path rejection + first failure halt + post-halt lock + replay + replay comparison + 8x repeatability + trace integrity

And status still distinguishes:

IMPLEMENTED · TESTED · CI-VERIFIED · REPRODUCED · **NOT SEALED** · **NOT PRODUCTION AUTHORIZED**

---

## 18. Final Principle

The experiment should be boring.

Same input. Same conditions. Same allowed path. Same failure rules. Same trace structure. Same replay procedure. Repeated eight times.

If the system behaves differently, the difference becomes the evidence to investigate.

```
LOCK THE PATH
LOCK THE CONDITIONS
LOCK THE FAILURE RULE
LOCK THE EVIDENCE FORMAT
TRY -> TEST -> TRACE -> REPLAY -> TEST AGAIN -> COMPARE -> REPEAT x8
```

No verified next path -> no execution.

All execution remains inside controlled SWI experimental nodes.

---

## Document control

- This protocol is a **research design document**.
- It does not authorize production use.
- It does not expand the historical M11 seal.
- Implementation of the minimal experimental harness is the next controlled step.
- Confidential external proposals are never committed to this repository.
