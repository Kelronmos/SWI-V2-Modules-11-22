# Two-Checkout CI Status

**Last reconciled:** 2026-09-25  
**Current main tip (at reconciliation):** `4bd78434ce8147d30de89069d9598c8283a2a47f`

## M11 status (honest, tip-bound)

| Layer | Status |
|-------|--------|
| Post-admission seal **implementation** | IMPLEMENTED + TESTED |
| Historical seal record | **PRESENT** — [`docs/M11_SEAL_RECORD.md`](M11_SEAL_RECORD.md) |
| Audit summary | **PRESENT** — [`docs/M11_AUDIT_SUMMARY.json`](M11_AUDIT_SUMMARY.json) |
| M11 **SEALED at tip** | **YES** — V2 `1d6d7dc250df80f39aa60bd8da812c9ae3efebec` · CI run `35253244912` (2026-09-17) |
| M11 re-sealed at **current HEAD** | **NOT CLAIMED** — later commits (including CI history fix) did not rewrite the seal record |
| Production authorization | **NOT AUTHORIZED** |
| CRTG / prod keys / factual truth | **NOT ESTABLISHED** by the M11 seal |

> **Correction (2026-09-25):** An earlier version of this file stated `M11 SEALED: NO` and `M11_SEAL_RECORD.md: ABSENT`. That was **stale**. The seal record exists and documents a tip-bound continuity seal. A historical tip seal is not automatically a seal of every subsequent HEAD.

## Workflows

| Workflow | File | What it proves |
|----------|------|----------------|
| `two-checkout-travel` | `.github/workflows/two_checkout_travel.yml` | V1 produce → artifact → V2 admit (no V1 import) → tamper reject → post-admission seal → V2 pytest on 3.10/3.11/3.12 |
| `SWI V2 Modules 11-22 Verification` | `.github/workflows/swi_v2_ci.yml` | V2-only compile + pytest matrix 3.10/3.11/3.12 · **full Git history** (`fetch-depth: 0`) as of 2026-09-25 |

## What two-checkout proves (when green on tip SHA)

```text
V1 checkout (only)
  → export real foundation evidence
  → upload artifact
V2 checkout (only; no V1 tree; full history)
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
Seal steps exist after the commit that adds `seal_travel_evidence.py`.  
Always match Actions run ID to the **exact** main SHA under audit.

The sealed tip for M11 continuity is:

```text
V2  1d6d7dc250df80f39aa60bd8da812c9ae3efebec
V1  e0c6a521d7965c46c18464edc5dc6fbd8f9e254c
Run 35253244912
```

## Status line

| Layer | Status |
|-------|--------|
| Admission two-checkout design | IMPLEMENTED |
| Seal travel script | IMPLEMENTED |
| Historical M11 seal record | PRESENT (tip `1d6d7dc`) |
| Tip CI green for **current** main | CHECK Actions after each push |
| M11 SEALED (historical tip) | YES — see `M11_SEAL_RECORD.md` |
| M11 re-sealed at current HEAD | NOT CLAIMED |
| Production | NOT AUTHORIZED |

## How to re-verify

1. https://github.com/Kelronmos/SWI-V2-Modules-11-22/actions  
2. Open `two-checkout-travel` for the **exact** main SHA under audit  
3. Confirm produce + admit matrix (3.10/3.11/3.12) + seal step green  
4. Compare run SHA to the frozen tip in `M11_SEAL_RECORD.md`  
5. Do not treat a later green CI run as an automatic extension of the historical seal without a new seal record

Do not mark production authorized from this document.  
Do not collapse tip-bound seal into HEAD-wide authorization.
