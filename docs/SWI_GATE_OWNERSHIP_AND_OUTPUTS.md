# SWI Gate Ownership & Outputs

**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Architecture branch:** architecture/kernel-progression-human-authority  
**Baseline HEAD (at protocol freeze):** `063487bc8b678c9cfb0b67848f5c662293b5d1f0`

Machine-readable status: `docs/gate_register.json`

## Ownership classes

| Owner | May | Must not |
|-------|-----|----------|
| **AI / Engineering** | inspect, implement, test, evidence, request CI, prepare review | authorize production, grant legal authority, issue final seal, extend historical seals |
| **CI** | run workflows, report build/test results | legal/ethical validity, production, seal authority |
| **Independent human reviewer** | review, accept/reject evidence scope | — |
| **Human / org authority** | seal decision, production authorization | — |

```text
GATE → OUTPUT → EVIDENCE → STATE
GATE ↛ AUTHORITY
```

## Required gate record fields

GATE_ID, GATE_NAME, OWNER, INPUTS, PRECONDITIONS, ACTION, EXPECTED_OUTPUT, ACTUAL_OUTPUT, STATUS, EVIDENCE, EXACT_SHA, CI_RUN, LIMITATIONS, FAILURE, NEXT_GATE, STOP_CONDITION, AUTHORITY_REQUIRED

## State progression

```text
AWAITING_EXECUTION → EXECUTED → TESTED → EVIDENCE_RECORDED
  → CI_VERIFIED → FRESH_REPLAY → AWAITING_HUMAN
  → INDEPENDENTLY_REVIEWED → PIPE_SEALED
```

Blocked / other: HALTED, NOT_PROVEN, NOT_AUTHORIZED, TLC_NOT_RUN, UNIVERSAL_GATE_NOT_PROVEN, AWAITING_CI

Forbidden: TESTED→SEALED, CI→PRODUCTION, SIGNATURE→AUTHORITY

## Immediate next gate

**G05 — Exact-SHA CI** for architecture HEAD (or successor tip if HEAD moved).

Acceptance: `workflow_run.head_sha == target SHA` exactly.

## Historical M11

Sealed only at `1d6d7dc…` + run `35253244912`. Does not cover architecture tip.

## Production

**G33: NOT_AUTHORIZED** until separate authority decision.
