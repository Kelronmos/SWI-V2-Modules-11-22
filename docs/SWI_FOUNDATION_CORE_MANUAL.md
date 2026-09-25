# SWI Foundation Core, SCAR, Seeder, Gate Reflex & Full-System Verification Manual

**System:** Structured Workflow Intelligence (SWI)  
**Date:** 2026-09-25  
**Operating mode:** RESEARCH / CONTROLLED DEVELOPMENT  
**Production authorization:** NOT AUTHORIZED  

---

## PART I — Evidence boundary

### 1. Purpose of this separation

This manual has two layers that **must not be merged**:

| Plane | Answers | Is not |
|-------|---------|--------|
| **NORMATIVE** | What SWI is required to do | Proof of implementation |
| **IMPLEMENTED PROOF** | What has been demonstrated with source, test, result, scope | Expansion of the rule |

### 2. Four-state model

```
DESIGNED ≠ IMPLEMENTED ≠ TESTED ≠ PROVEN-WITHIN-SCOPE
PROVEN ≠ SEALED ≠ AUTHORIZED
```

### 3. Classification labels

Every substantive claim uses one of:

`[NORMATIVE]` · `[IMPLEMENTED]` · `[TESTED]` · `[PROVEN-WITHIN-SCOPE]` · `[HISTORICAL-EVIDENCE]` · `[DESIGN]` · `[UNKNOWN]` · `[NOT-IMPLEMENTED]` · `[NOT-PROVEN]`

If classification cannot be established: **UNKNOWN**.

---

## PART II — Normative rules (requirements, not proof)

### 4. Foundation Core

**Classification:** [NORMATIVE]

```
SWI FOUNDATION CORE
        |
   +----+----+
   |    |    |
STRUCTURE  SCAR STORE  SWI-ZERO
   |    |    |
   +----+----+
        |
   SCAR-MISTIC
        |
     SEEDER
        |
  CONTROLLED FLOW
```

**Root invariant**

```
FOUNDATION VERIFIED → FLOW MAY PROCEED
FOUNDATION UNVERIFIED → FLOW MUST FREEZE
```

No M-module, agent, dashboard, API caller, or recovery routine may override foundation freeze.

### 5. SCAR Store

**Classification:** [NORMATIVE]

SCAR records structural failure. It is **not** repair, authorization, or cleanliness.

Minimum fields: `scar_id`, `task_id`, `continuity_id`, `foundation_id`, `failure_class`, `failure_reason`, `previous_state`, `failed_transition`, `affected_dependencies`, `evidence_refs`, `integrity_reference`, `recovery_state`.

A failure must not disappear merely because a runtime instance was reset.

### 6. SWI-Zero

**Classification:** [NORMATIVE]

```
AFFECTED → HALT → SCAR → NEW ZERO (new identity)
NEW_ZERO ≠ VERIFIED
RESET ≠ CLEAN
```

New-zero is a baseline **requiring verification**.

### 7. Seeder

**Classification:** [NORMATIVE]

```
SCAR → NEW ZERO → SEED → BUILD → CHECK → VERIFY
```

`SEED ≠ TRUST`. Seeder output is a **candidate** until checked. Seeder must not bypass integrity, authority, dependency, continuity, runtime, or execution controls.

### 8. Failure reflex

**Classification:** [NORMATIVE]

```
DETECT → HALT → RECORD → ISOLATE → SCAR → NEW ZERO → SEEDER → REBUILD → RECHECK → VERIFY
```

**Forbidden:** `FAIL → RETRY → PASS → CONTINUE` and `HALT → ACTIVE`.

### 9. Continuity

**Classification:** [NORMATIVE]

Affected continuity **must not** continue. Old instance → HALT → SCAR; only a **new** identity may become the continuation candidate after verification.

### 10. Authority chain

**Classification:** [NORMATIVE]

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

Authority must not be inferred from data, signatures, admission, dashboard state, SCAR, successful build, or test result alone.

### 11. UNKNOWN

**Classification:** [NORMATIVE]

`UNKNOWN` must not silently become true. No authorization from UNKNOWN. Where the safety contract requires: `UNKNOWN → HALT`.

### 12. Forbidden transitions

**Classification:** [NORMATIVE]

| Forbidden |
|-----------|
| REJECT → ACTION |
| HALT → ACTION |
| UNKNOWN → ACTION |
| SCAR → ACTION |
| RAW DATA → ACTION |
| DASHBOARD → ACTION |
| HALT → ACTIVE (direct) |
| RESTORE → VERIFIED (without recheck) |
| OLD CONTINUITY → ACTIVE (after halt) |

### 13. Dashboard

**Classification:** [NORMATIVE]

Dashboard is **read-only observation**. It must not authorize, clear HALT, create seals, alter evidence, change continuity, or convert TESTED → SEALED.

### 14. Seal vs authorization

**Classification:** [NORMATIVE]

```
TESTED → VERIFICATION → SEAL REVIEW → SEALED → SEPARATE AUTHORIZATION
```

Test result does not create a seal. Seal does not create production authorization.

### 15. Dependency and concurrency

**Classification:** [NORMATIVE]

Failure propagation follows **proven** dependency relationships only. Concurrent execution must not produce: duplicate continuity, double recovery, lost update, cross-task leak, unauthorized merge, accepted hash-chain fork. Shared writes require a defined serialization contract.

**Concurrency implementation proof:** [NOT-PROVEN]

### 16. Bypass

**Classification:** [NORMATIVE]

```
REJECT → caller ignores → direct execution → MUST FAIL
HALT → caller clears halt → ACTION → MUST FAIL
```

**Process-wide / structural bypass resistance:** [NOT-PROVEN] (repository documents this limitation for PR-009-class enforcement).

---

## PART III — Gate model (normative structure)

**Classification:** [NORMATIVE] for structure; proof status per gate is separate.

| Gate | Name |
|------|------|
| G00 | SOURCE / TIP |
| G01 | EVIDENCE FRESHNESS |
| G02 | SCHEMA / TYPE |
| G03 | IDENTITY / ORIGIN |
| G04 | AUTHORITY / SCOPE |
| G05 | ADMISSION |
| G06 | INTEGRITY / TAMPER |
| G07 | BINDING / MUTATION |
| G08 | RETURN / RESPONSE |
| G09 | DEPENDENCY / GRAPH |
| G10 | CONTINUITY |
| G11 | REPLAY |
| G12 | CONCURRENCY / RACE |
| G13 | RUNTIME STATE |
| G14 | HALT |
| G15 | SCAR / INCIDENT |
| G16 | NEW-ZERO / RECOVERY |
| G17 | RECHECK |
| G18 | EXECUTION BOUNDARY |
| G19 | DASHBOARD / OBSERVABILITY |
| G20 | SEAL / AUTHORIZATION |

Each gate must be tested in at least: **NORMAL**, **BREAK**, **BREAK+BYPASS**, **BREAK+RECOVERY ATTEMPT**.

Master attack row fields: ATTACK ID, GATE, INPUT MUTATION, EXPECTED STATE, FORBIDDEN STATE, EXPECTED WRITE, EXPECTED EXECUTION, EXPECTED SCAR, EXPECTED RECOVERY, EVIDENCE, RESULT, LIMITATION.

---

## PART IV — Implemented-proof plane

### 17. Proof record rule

**Classification:** [NORMATIVE for format]

Every implemented claim must identify: CLAIM, SOURCE, COMMIT, IMPLEMENTATION PATH, TEST PATH, CI RUN (if any), RESULT, SCOPE, LIMITATION, DATE.

### 18. Contract-level model — 1,000,000 iterations

**Classification:** [TESTED] within **CONTRACT_LEVEL_MODEL** only

| Field | Value |
|-------|--------|
| Test | Deterministic streaming state-machine model |
| Requested | 1,000,000 |
| Executed | 1,000,000 |
| Failures (invariant) | 0 |
| Deterministic | YES |
| Rolling digest | `fa2f4f1ecb7201b8aec0c1cbe0e9249d5d2b66c38855a6af00ce0307f350e8c3` |
| Scope | CONTRACT_LEVEL_MODEL |
| Implementation proof | **NO** |
| Repository Python modules exercised | **NO** |
| Process-wide bypass proven | **NO** |
| Distributed concurrency proven | **NO** |
| M11 resealed | **NO** |

Limitations: does not execute repository module code; does not prove caller-bypass resistance; does not prove distributed races; does not alter historical M11 seal.

### 19. Local continuity prototype (research)

**Classification:** [IMPLEMENTED] + [TESTED] within **LOCAL RESEARCH PROTOTYPE** scope

| Claim | Path (local artifacts) | Result | Scope | Limitation |
|-------|------------------------|--------|-------|------------|
| SCAR cannot CONTINUE | `swi_backend/server/continuity/model.py` + tests | PASS (local) | prototype | not in V2 tip CI |
| New-zero new identity | same | PASS (local) | prototype | not remote-committed |
| Unrelated task isolation | same | PASS (local) | prototype | no dependency graph proof |
| HALT reason_code on SCAR | same | PASS (local) | prototype | not repo-integrated |

**Remote repository commit of this prototype:** NOT ESTABLISHED for code; this manual document is separate.

### 20. Billion-iteration implementation test

**Classification:** [NOT-IMPLEMENTED] / **NOT EXECUTED**

Do not record PASS.

### 21. M11

**Classification:** [HISTORICAL-EVIDENCE]

```
M11 SEALED — HISTORICAL RECORD
```

Current development tip must **not** inherit that seal merely by ancestry. Current tip sealed ≠ historical M11 sealed unless independently sealed.

### 22. Repository position (from inspected module status / current position)

**Classification:** [HISTORICAL-EVIDENCE] / [UNKNOWN] where not re-verified this session

| Area | Recorded posture |
|------|------------------|
| M11 | SEALED — historical |
| M12 | FROZEN |
| M13–22 | BLOCKED |
| Replay | PARTIAL / NOT COMPLETE |
| PR-009 / pre-R | EXPERIMENTAL / TESTED / NOT SEALED |
| Process-wide bypass | NOT PROVEN |
| Automatic recovery | NOT IMPLEMENTED |
| Firefly | DESIGN / DEFERRED |
| Production | NOT AUTHORIZED |

### 23. Normative register (sample)

| ID | Requirement | Mandatory |
|----|-------------|-----------|
| N-001 | Foundation failure freezes flow | YES |
| N-002 | SCAR survives failure recording | YES |
| N-003 | Affected continuity cannot continue | YES |
| N-004 | New-zero receives new identity | YES |
| N-005 | Seeder output requires verification | YES |
| N-006 | UNKNOWN cannot authorize action | YES |
| N-007 | HALT cannot directly become ACTIVE | YES |
| N-008 | Dashboard cannot authorize | YES |
| N-009 | TESTED does not automatically mean SEALED | YES |
| N-010 | Recovery requires recheck | YES |

### 24. Gap register (sample)

| Rule | Implementation | Test | Status |
|------|----------------|------|--------|
| N-001 Foundation freeze | REQUIRED | REQUIRED | NOT-PROVEN (repo-wide) |
| N-003 Affected continuity | local prototype | local PASS | PROVEN-WITHIN-SCOPE (local only) |
| N-007 HALT↛ACTIVE | local model + continuity | local PASS | PROVEN-WITHIN-SCOPE (local only) |
| Bypass after REJECT | REQUIRED | REQUIRED | NOT-PROVEN (process-wide) |
| Concurrency invariants | REQUIRED | REQUIRED | NOT-PROVEN |

### 25. Proof register (honest)

| ID | Requirement | Implementation | Test | Result | Scope | Limitation | Status |
|----|-------------|----------------|------|--------|-------|------------|--------|
| P-MODEL-1M | Forbidden transitions in model | stream_runner | 1M run | 0 inv failures | CONTRACT_LEVEL_MODEL | not repo modules | PROVEN-WITHIN-SCOPE |
| P-CONT-SCAR | SCAR cannot CONTINUE | continuity/model.py | pytest | PASS | local prototype | not in V2 tip | PROVEN-WITHIN-SCOPE |
| P-BYPASS | Caller ignores REJECT | — | — | UNKNOWN | — | not demonstrated process-wide | NOT-PROVEN |
| P-CONC | Concurrent recovery/write | — | — | UNKNOWN | — | not demonstrated | NOT-PROVEN |

---

## PART V — Operating principles

### 26. What must never happen

UNKNOWN → silently PASS · REJECT → ACTION · HALT → ACTION · SCAR → AUTHORIZATION · RESTORE → VERIFIED · SIGNATURE → TRUTH · ADMISSION → AUTHORIZATION · DASHBOARD → AUTHORIZATION · TEST → SEAL · SEAL → PRODUCTION · OLD CONTINUITY → NEW ACTIVE · HASH MISMATCH → silent rewrite · FAILED RECOVERY → same instance continues · MISSING EVIDENCE → invented evidence

### 27. Status language

Use only: DESIGNED, IMPLEMENTED, TESTED, CI-VERIFIED, EVIDENCE-BACKED, INDEPENDENTLY VERIFIED, SEALED, AUTHORIZED — each with scope.

Avoid unqualified: SAFE, SECURE, PROVEN, PRODUCTION-READY, TAMPER-PROOF, UNBREAKABLE.

### 28. Final principle

```
RULE ≠ CODE ≠ TEST ≠ RESULT ≠ PROOF SCOPE ≠ SEAL ≠ AUTHORIZATION
```

A requirement is not proof. Code is not proof. A passing test is not universal proof. A historical seal is not a current seal. A model test is not an implementation test. Recovery is not verified merely because reconstruction succeeded.

**Claim only what the evidence actually demonstrates.**

---

*End of manual. This document is normative + local proof registration. It does not authorize production or reseal M11.*
