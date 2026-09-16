# SWI V2 — Controlled Closing, M11 Seal, M12 Implementation & Next-Stage Execution Manual

**Status:** CONTROLLED EXECUTION  
**Date:** 15 September 2026  
**Rule:** «DO NOT CLAIM WHAT THE CODE CANNOT DEMONSTRATE.»

## Sequence (hard order)

```text
GitHub write OK → two-checkout CI tip-green → A–G audit → M11_SEAL_RECORD
  → M11 SEALED → M12 contract → M12 implement → tests → CI → M12 audit
  → next module (not bulk 13–22)
```

## States (never collapse)

| State | Meaning |
|-------|---------|
| TESTED | Tests ran and passed |
| CI_VERIFIED | Exact tip workflow SUCCESS + observable logs |
| SEALED | A–G (or M12 audit) passed + seal record exists |

## Current position (update only with evidence)

```text
Contract FROZEN · Local travel PROVEN
Two-checkout CI: NOT CI_VERIFIED until tip run SUCCESS proven
M11 / Kernel: TESTED / NOT SEALED
M12–22: BLOCKED · CRTG DESIGN PENDING · Seal 5 = V1 decision
```

## M11 seal requires

A–G all PASS **and** tip-specific `two_checkout_travel` GREEN.  
Then write `docs/M11_SEAL_RECORD.md` **before** changing MODULE_STATUS to SEALED.

Scope of seal: admission of **serialized foundation evidence** only.  
Not: truth, origin beyond fields, CRTG, Seal 5, V2 complete, M12–22.

## M12 hard gate

M12 code **forbidden** until `M11_SEAL_RECORD.md` exists and status is SEALED.

M12: contract-first · `AdmittedInput` only · positive/negative/bypass tests · no CRTG rename.

## Stop conditions

Missing seal record · CI unknown/red · V1 import works in admit job · raw bypasses M11 · docs contradict code · bulk M13–22 · silent CRTG/Seal 5 claims
