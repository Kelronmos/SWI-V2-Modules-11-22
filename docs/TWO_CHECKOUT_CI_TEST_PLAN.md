# Two-Checkout CI Travel Test Plan (V2)

**Status:** PLAN + admit script + workflow · CI_VERIFIED only after Actions green  
Aligned with V1 `docs/TWO_CHECKOUT_CI_TEST_PLAN.md`

## Goal

Separate V1 clone produces JSON → this V2 clone admits via M11. No V1 package import.

## Scripts

| Side | Script |
|------|--------|
| V1 | `scripts/export_travel_evidence.py` |
| V2 | `scripts/admit_travel_evidence.py` |

## CI workflow

`.github/workflows/two_checkout_travel.yml` checks out V1 + V2, exports, admits, then rejects tamper.

## Pass language

| Result | Label |
|--------|--------|
| Scripts exist, local pass | LOCAL |
| Workflow green on tip | **CI_VERIFIED** |
| Not yet | **LIVE TWO-CHECKOUT — PENDING** |

## Seal 5

Necessary for bridge strength; not sufficient alone for Foundation Seal 5.
