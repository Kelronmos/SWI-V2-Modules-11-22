# Common Sense / Protected Humanity — Formal Property Freeze (L0→L1)

**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Branch:** architecture/kernel-progression-human-authority  
**Layer:** Parallel evidence (not a seal)

```text
L0 EXECUTABLE INVARIANTS (PH-01…14 + property tests)
        ↓
L1 FINITE-STATE MODEL (TLA+ / Alloy style)
        ↓
L2 SMT (later)
        ↓
SEAL GATES (separate)
```

## Claim boundary

```text
TEST PASS ≠ MODEL CHECK PASS ≠ SMT RESULT
≠ LEGAL VALIDITY ≠ ETHICAL TRUTH ≠ AUTHORIZATION ≠ PRODUCTION
```

Universal Gate remains **NOT_PROVEN** until path universe is closed.

## Frozen properties (map to live API)

| ID | Property |
|----|----------|
| P01 | ∀ action: `request_action(action)` → PermissionError |
| P02 | ∀ case: `may_cross_downstream_pipe(case) = False` |
| P03 | revoked → HALT |
| P04 | expired / not-yet-valid → HALT |
| P05 | scope_mismatch → HALT |
| P06 | condition_mismatch → HALT |
| P07 | equation_mismatch → HALT |
| P08 | privacy_boundary_violation → HALT |
| P09 | security_boundary_violation → HALT |
| P10 | survival/emergency framing ≠ authorization |
| P11 | authority_drift (+ high pattern) → RECHECK |
| P12 | repeated_failure does not PROMOTE |
| P13 | abnormal_sequence does not open pipe |
| P14 | inspect cannot produce EXECUTE/AUTHORIZE/PROMOTE/SEAL authority |

## Critical FSM safety

```text
∀ reachable diagnostic states:
  CommonSense → EXECUTE   = impossible
  CommonSense → AUTHORIZE = impossible
  CommonSense → PROMOTE   = impossible
  CommonSense → SEAL      = impossible
```

Diagnostic states only: CONTINUE | RECHECK | ESCALATE | HALT.

## M11 (separate model — do not merge with PH)

```text
RAW → REJECTED | ADMITTED
ADMITTED ⇒ schema ∧ status ∧ integrity
¬(schema ∧ status ∧ integrity) ⇒ REJECTED
```

## Status

| Item | Status |
|------|--------|
| L0 PH tests | TESTED (see branch tip) |
| L1 model text | PRESENT (`common_sense_fsm.tla`) |
| TLC run in CI | NOT REQUIRED YET |
| Seal | NOT CLAIMED |
