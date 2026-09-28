# S9 X1 — Irrelevant Evidence Test Contract

**Document type:** TEST CONTRACT · SPECIFICATION ONLY  
**Obligation:** X1  
**Baseline commit (scope matrix):** `fa6a061f161eeee62aa24cde09c932f12e9d86ab`  
**Source attack:** `docs/formal/S9_MATHEMATICAL_ATTACK_2026-09-24.md` §3 X1  
**Source obligation:** `docs/formal/S9_360_PHASE_OBLIGATION_BINDING.md` X1 row  
**Source matrix:** `docs/formal/S9_PROCESS_SCOPE_MATRIX.json`  
**Status:** CONTRACT FROZEN · **NOT IMPLEMENTED** · **NOT RUN** · **S9 = NOT PROVEN**

---

## 0. Explicit non-claims

This document:

- does **not** implement X1
- does **not** implement `Permit(a)`, `SufficientEvidence(a)`, or `Authorized(a)`
- does **not** implement a runtime, binding engine, or execution eligibility path
- does **not** authorize Phase 0 or any later phase
- does **not** close the X1 obligation
- does **not** change `S9_PROVEN`
- does **not** authorize execution or production

If a later test exposes a weakness, the weakness is **recorded**, not immediately patched.

---

## 1. Attack statement

The equation under examination includes:

```text
Permit(a)  ⇔  (∀ L,G,S,H : C(a) ⊆ L ∩ G ∩ S ∩ H)  ∧  E(a) ≠ ∅
```

**X1 counterexample:**

```text
C(a) ≠ ∅
E(a) ≠ ∅
E(a) ⊭ C(a)          # evidence exists but does not support the claim for a
```

Under the weak form, `E(a) ≠ ∅` alone can still yield `Permit(a) = True`.

**Mathematical attack:**

```text
E ≠ ∅  ⇏  E ⊨ C(a)
```

Evidence existence is not evidence sufficiency.

---

## 2. Required system behaviour

Given a candidate action `a` where:

1. `C(a)` is non-empty, and  
2. some evidence object `E` is present (`E ≠ ∅`), and  
3. `E` does **not** support / entail / satisfy `C(a)` (`E ⊭ C(a)`),

the system **MUST NOT** treat the mere presence of `E` as sufficient for permission.

**Allowed outcomes:**

```text
BLOCK
UNRESOLVED
REJECT
HALT
```

**Forbidden outcomes:**

```text
PERMIT
AUTHORIZED
EXECUTABLE
OPERABLE
SEALED
```

A result of `PERMIT` / `AUTHORIZED` / `EXECUTABLE` under these conditions is a **FAIL** of the X1 obligation.

---

## 3. Minimal scenario definition

### 3.1 Action under test

Define a concrete action `a` such that:

- `C(a)` is a non-empty, well-formed claim set (e.g. a required field set, a required fact set, or a required constraint set).
- `C(a)` is fixed for the duration of the test case.

### 3.2 Irrelevant evidence object

Provide an evidence object `E` such that:

- `E` is non-empty and structurally recognizable as evidence (passes any schema that only checks existence / well-formedness of *an* evidence object).
- `E` is bound to a **different** claim, action, or subject `b` where `b ≠ a`.
- Or `E` is otherwise demonstrably irrelevant to `C(a)` (e.g. supports a disjoint fact set).

### 3.3 Control conditions

To isolate the X1 failure mode:

- Keep `L, G, S, H` in a state that would otherwise pass containment **if** evidence were sufficient, **or** document that the test is focused solely on the `E ≠ ∅` weakness.
- Do not rely on missing authority, missing identity, or staleness to produce the block (those are X2–X6 territory).
- The sole intended defect under test is: evidence exists but does not support the claim.

---

## 4. Expected failure receipt

When the attack succeeds (system correctly refuses), the test evidence package must record at least:

| Field | Requirement |
|-------|-------------|
| `test_id` | `S9-X1-IRRELEVANT-EVIDENCE` |
| `baseline_sha` | Exact commit under test |
| `action_id` | Identifier of `a` |
| `claim_summary` | Non-secret summary of `C(a)` |
| `evidence_id` | Identifier of `E` |
| `relevance_verdict` | `IRRELEVANT` / `DOES_NOT_SUPPORT_CLAIM` |
| `system_outcome` | `BLOCK` / `UNRESOLVED` / `REJECT` / `HALT` |
| `forbidden_outcome_observed` | `false` |
| `timestamp_utc` | ISO-8601 |
| `runner` | Who/what executed the case |
| `notes` | Any residual ambiguity |

When the attack **fails** (system incorrectly permits), the receipt must record:

| Field | Requirement |
|-------|-------------|
| `system_outcome` | actual outcome (`PERMIT` / `AUTHORIZED` / …) |
| `forbidden_outcome_observed` | `true` |
| `weakness_recorded` | `true` |
| `weakness_summary` | Short description of the observed incorrect promotion |

**Do not patch the system inside the same change that records the weakness.**

---

## 5. Evidence package requirements

To demonstrate the attack (whether the system blocks or incorrectly permits):

1. **Provenance** — baseline SHA, branch, working-tree state.  
2. **Inputs** — canonical representation of `a`, `C(a)`, and `E` (or redacted forms where secrets apply).  
3. **Relevance argument** — why `E ⊭ C(a)` (human-readable +, if available, machine check).  
4. **Outcome** — exact system response.  
5. **Non-promotion proof** — confirmation that no `AUTHORIZED` / `EXECUTABLE` / `SEALED` side-effect occurred.  
6. **Environment** — Python / pytest / dependency versions as applicable.

Copying an evidence file is **not** sufficient (see process-scope matrix: P04 ≠ validity).

---

## 6. Dependency / freshness / authority constraints for this contract

| Concern | X1 contract requirement |
|---------|-------------------------|
| Dependency | Test must not silently assume an unimplemented dependency is valid |
| Freshness | Prefer fresh `E`; if `E` is also stale, document that X2 is co-present and do not attribute the block solely to X1 |
| Authority | Do not use missing authority as the blocking reason; that is X6 |
| Identity | Do not use wrong principal as the blocking reason; that is X5 |
| Scope | Do not use field-scope overflow as the blocking reason; that is X4 |
| Replay | Prior authorization must not be required for this case |

X1 is the **narrow** attack: existence without relevance.

---

## 7. Independent replay procedure (when a run exists)

1. Check out the exact baseline SHA recorded in the failure/success receipt.  
2. Restore the recorded inputs (`a`, `C(a)`, `E`).  
3. Re-execute the same test entry point.  
4. Compare outcome to the original receipt.  
5. Record match / mismatch.  

Mismatch → **REPLAY_FAIL** (do not silently update the original receipt).

Until a first run exists, replay status remains **NOT_ESTABLISHED**.

---

## 8. Pass / Fail / Not-run vocabulary

| Result | Meaning |
|--------|--------|
| **PASS** | System returned BLOCK/UNRESOLVED/REJECT/HALT; no forbidden outcome; receipt complete |
| **FAIL** | System returned PERMIT/AUTHORIZED/EXECUTABLE/OPERABLE/SEALED under X1 conditions |
| **NOT_RUN** | Contract exists; no execution performed |
| **NOT_IMPLEMENTED** | No harness / no code path capable of evaluating the case |
| **BLOCKED** | External precondition prevents running the case |
| **INCONCLUSIVE** | Outcome cannot be classified (must be explained) |

Current status of this obligation: **NOT_IMPLEMENTED** / **NOT_RUN**.

---

## 9. Relationship to later work

```text
X1 CONTRACT (this document)     ← HERE
        ↓
smallest harness capable of the scenario
        ↓
first adversarial run at exact SHA
        ↓
receipt + evidence package
        ↓
independent replay
        ↓
record weakness OR record survival
        ↓
claim-ledger update (never silent)
```

Do **not** expand this contract into an implementation of `SufficientEvidence` in the same step.

---

## 10. Final status block

```text
OBLIGATION:                 X1
CONTRACT STATUS:            FROZEN (specification only)
IMPLEMENTATION:             NOT_IMPLEMENTED
TEST RUN:                   NOT_RUN
X1 CLOSED:                  NO
S9 PROVEN:                  NO
RUNTIME:                    NOT IMPLEMENTED
BINDING:                    NOT_BINDABLE
EXECUTION AUTHORIZED:       NO
PRODUCTION AUTHORIZED:      NO
```

---

**END OF X1 TEST CONTRACT**
