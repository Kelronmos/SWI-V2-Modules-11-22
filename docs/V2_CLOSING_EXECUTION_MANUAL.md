# SWI V2 — Expanded Closing & M11 Seal Execution Manual

**Date:** 15 September 2026  
**Phase:** CLOSING — verification, not redesign

## Current state

```text
Contract              FROZEN
V1 → V2 local travel  PROVEN
Two-checkout CI       CI_VERIFIED (tip run 34987307390 · V2 061a47f · V1 be31dd7)
M11                   TESTED / NOT SEALED
Kernel                TESTED / NOT SEALED
CRTG                  DESIGN PENDING
M12–22                BLOCKED
Seal 5                NOT CLAIMED
```

## Rule

If a test fails, fix implementation or tests to match the **frozen** contract.  
Do **not** silently shrink the contract so the test passes.

## CI shape (two jobs)

```text
JOB produce (V1 checkout)
  → export_travel_evidence.py → evidence.json artifact
JOB admit (V2 only)
  → download artifact
  → V1 must not be importable
  → admit_travel_evidence.py
  → tamper → must fail
```

Workflow: `.github/workflows/two_checkout_travel.yml`

## Seal eligibility

Only after CI_VERIFIED two-checkout + full checklist in `V2_CLOSING_AND_M11_SEAL_MANUAL.md`.  
**Do not** change MODULE_STATUS to SEALED in this phase until that evidence exists.

## Forbidden

Bulk M12–22 · fixture as sole primary proof · import V1 · claim CRTG/Seal 5 · cosmetic NOT SEALED removal
