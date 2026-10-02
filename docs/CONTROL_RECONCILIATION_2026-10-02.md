# Control reconciliation — 2026-10-02

## Changes in this branch

1. **Evidence freshness** — fail-closed when Git metadata is unavailable (UNKNOWN/HALT, not skip).
2. **Offline runners** — scripts + docs; wheels placeholder (environment failure until vendored).
3. **README** — defers control status to CURRENT_POSITION; historical M11 seal marked historical.
4. **Court evidence boundary** — doctrine only; no legal/production claim.

## Explicit non-upgrades

| Item | Status |
|------|--------|
| M11 current production authorization | NOT AUTHORIZED |
| Execution | BLOCKED |
| Foundation PASS | NOT CLAIMED |
| Evidence closure | NOT claimed solely by this docs/script commit |
| S9 / CRTG | NOT PROVEN / NOT IMPLEMENTED |

## Note on ZIP snapshots

A ZIP without `.git` cannot verify evidence ancestry. That condition is UNKNOWN → fail-closed, not PASS via skip.
