# SWI V2 — M11 Evidence Collection & Seal Verification Manual

**Date:** 15 September 2026  
**Phase:** Evidence collection — **not** implementation, **not** auto-seal

## Locked position

```text
Contract              FROZEN
Local V1 → V2 travel  PROVEN
Two-checkout CI       CI_VERIFIED
M11                   TESTED / NOT SEALED
Kernel                TESTED / NOT SEALED
CRTG                  DESIGN PENDING
M12–22                BLOCKED
```

## Principle

> A seal is a governance conclusion from reproducible evidence — not a percentage, milestone, or documentation state.

Do not change the frozen contract to make a failing test pass.

## Tip-specific CI

Two-checkout CI is currently CI_VERIFIED for the audited tip.

V2 SHA: `061a47ff23705684179cb48836051c8b097e1b65`
V1 producer SHA: `be31dd733e7fba17ceddb0b142a075abcfca890a`
Workflow run: `34987307390`
Workflow: `two_checkout_travel.yml`
Status: GREEN

This evidence does not by itself seal M11. A–G audit completion is still required.

Evaluate any *future* tip the same way: earlier green runs do **not** prove a new tip.  
Record: V2 SHA · V1 producer SHA · workflow run ID · status for every seal candidate.

## A–G audit (only PASS / FAIL / NOT PROVEN)

| Gate | Meaning |
|------|---------|
| **A Contract** | Docs = code = tests; digest = 5 fields; `created_at` excluded |
| **B Boundary** | Independent V2; no V1 install/path; `import swi_core` fails; no M10 handoff |
| **C Real producer** | V1 `export_travel_evidence` / foundation export → artifact; not fixture-only primary path |
| **D Admission** | Valid ACCEPT; tamper/hash/status/missing/malformed/version REJECT |
| **E Isolation** | Raw dict/string blocked; reject does not reach Kernel; AdmittedInput required |
| **F Reproducibility** | Two-job CI green on tip; clean env |
| **G Documentation** | README / MODULE_STATUS / RELEASE_GATE / manuals consistent |

**ALL PASS → SEAL ELIGIBLE**  
**ANY critical FAIL/NOT PROVEN → NOT SEALED**

## `import swi_core` failure

Proves: V2 admit job does not need `swi_core` importable on that path.  
Does **not** prove mathematical impossibility of all leakage.

## Fixture vs real producer

Fixtures OK for unit/negative tests.  
Primary closing proof must use **real V1 producer** artifact.

## After ALL PASS only

1. Write `docs/M11_SEAL_RECORD.md` with SHAs, run ID, A–G, **limitations**  
2. Then set MODULE_STATUS M11 → SEALED  
3. Authorize **M12 only** — not bulk 13–22  
4. Do not claim CRTG or Seal 5

## If CI red

```text
CLOSING BLOCKER
V2 SHA / job / step / error / criterion / minimal fix
Seal: NOT ELIGIBLE
```

## What M11 seal means (when earned)

Documented admission of **serialized foundation evidence**.  
Does **not** mean: truth, authenticated origin beyond documented fields, CRTG, Seal 5, V2 “secure,” M12–22 done.
