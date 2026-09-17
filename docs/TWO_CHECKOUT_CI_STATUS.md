# Two-Checkout CI Status

**Date:** 2026-09-17  
**M11 status:** CRYPTO SEAL IMPLEMENTED + TESTED / **NOT SEALED**

## Workflows

| Workflow | File | What it proves |
|----------|------|----------------|
| `two-checkout-travel` | `.github/workflows/two_checkout_travel.yml` | V1 produce → artifact → V2 admit (no V1 import) → tamper reject → post-admission seal → V2 pytest on 3.10/3.11/3.12 |
| `SWI V2 Modules 11-22 Verification` | `.github/workflows/swi_v2_ci.yml` | V2-only compile + pytest matrix 3.10/3.11/3.12 |

## What two-checkout proves (when green on tip SHA)

```text
V1 checkout (only)
  → export real foundation evidence
  → upload artifact
V2 checkout (only; no V1 tree)
  → download artifact
  → assert swi_core not importable
  → admit valid evidence
  → reject tampered payload
  → reject bad integrity
  → post-admission seal + verify + tamper reject (scripts/seal_travel_evidence.py)
  → pytest
```

## Historical note

Older green travel runs (e.g. on `0af60d3`) proved **admission isolation** only.
Seal steps exist on tip after the commit that adds `seal_travel_evidence.py`.
Always match Actions run ID to the **exact** main SHA under audit.

## Status line

| Layer | Status |
|-------|--------|
| Admission two-checkout design | IMPLEMENTED |
| Seal travel script | IMPLEMENTED |
| Tip CI green for current main | CHECK Actions after push |
| M11 SEALED | NO |
| `M11_SEAL_RECORD.md` | ABSENT |

## How to re-verify

1. https://github.com/Kelronmos/SWI-V2-Modules-11-22/actions
2. Open `two-checkout-travel` for the exact main SHA
3. Confirm produce + admit matrix (3.10/3.11/3.12) + seal step green
4. Record run URL + SHAs only then in any future seal record

Do not mark M11 SEALED from this document alone.
