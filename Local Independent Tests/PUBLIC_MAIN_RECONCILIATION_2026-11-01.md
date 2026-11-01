# Public-main DCRE reconciliation report — 1 November 2026

## Decision

The supplied public-repository source archive was integrated locally with the DCRE claim engine and evidence-bound status tooling. The package is **not pushed to GitHub**. The archive has no `.git` metadata and a fresh remote fetch failed because `github.com` DNS could not be resolved. No upstream ancestry, commit, branch, PR, or merge is claimed.

## Base snapshot

- Input: `SWI-V2-Modules-11-22-main (9).zip`
- Entries: 505
- SHA-256: `96048f70821ef034e635074bba97a6e0c71aeb3bd831b636cc6f94c2ab75c625`
- `.git`: absent
- External narrative says public `main` is `51a67e4`, but this archive cannot be proven to represent that commit without Git metadata.

## Imported and updated

- Added `swi_v2/claims/` with claim engine, fingerprints, history and SWI report adapter.
- Added `tests/claims/` (48 focused tests), three JSON schemas, and DCRE CLI/report/history tools.
- Added operator, development, verification, recovery-doctrine and ISO reference/boundary documentation.
- Imported the live append-only claim history (18 records; valid hash chain). The historical 17-record snapshot remains separately labelled as a snapshot, not the current ledger.
- Imported the external reviewer evidence ZIP without promoting it to local verification. All four external manifest checksums match.
- Replaced the stale hard-coded CI reference to an earlier local run with direct DCRE test, schema and history checks.
- Hardened README publication: exact main/HEAD binding, clean checkout, passing tests/build/schema, CI PASS, non-empty hash-valid evidence references, and rejection of path traversal.
- Hardened the local runner so a source ZIP with no Git metadata is not treated as a clean checkout. It records missing optional ISO gate files as `ABSENT`.

Generated caches and `.pyc` files were excluded. Historical run directories with inconsistent test counts were not copied as current evidence. Earlier conflicting reports are not included as current reports.

## Local verification

| Check | Result | Exit |
|---|---|---:|
| DCRE claim tests | 48 passed | 0 |
| Governing formula tests | 11 passed | 0 |
| Kernel subset | 535 passed, 1 failed because the ZIP has no Git metadata for the freshness ancestry check | 1 |
| Python compileall (`swi_v2 tools tests`) | Passed | 0 |
| DCRE schemas | 3 valid | 0 |
| Aggregate DCRE verification JSON | Valid | 0 |
| Append-only claim history | 18 records; hash chain valid | 0 |
| Full suite with collection continuation | 703 passed, 1 failed, 5 collection errors, 1 warning | 1 |
| Full suite in CI command form | 5 collection errors | 2 |
| External reviewer evidence manifest | 4/4 checksums valid | 0 |

The five collection errors remain associated with the malformed dynamically reconstructed execution-integrity payload and the unresolved trusted-source inspector placeholder. No source payload was invented to repair them. The kernel freshness test additionally requires Git metadata absent from the source ZIP.

## External reviewer evidence discrepancy

The supplied reviewer narrative names public `main` as `51a67e4`. Its attached `verification_run.json` records `9d1576e8af81a79f54409cd3cd9b4d1a78f957ad`. The discrepancy is preserved in `evidence/external/2026-11-01/reviewer-main-run/IMPORT_NOTE.md`. The reported 11 formula tests, 536 kernel tests, and 704 passed/5 errors are reviewer observations, not attributed to `51a67e4` and not independently reproduced on a genuine clone here.

The ISO claim-gate validator, its 13 tests, and `iso_claim_status.json` were absent from the supplied main snapshot. They are recorded as absent, not fabricated or counted as passing. The three-entry DCRE reference register and five-entry research register remain separate; all ISO standards remain unassessed/unmapped and conformity is not established.

## Current claim status

- Truth: `UNKNOWN`
- State: `PARTIAL`
- Development level: `L3_TESTED`
- Public main verified: `NO`
- Proven: `NO`
- Sealed: `NO`
- ISO conformity: `NOT_ESTABLISHED`
- Production authorized: `NO`

The README panel is generated from `evidence/claims/current_verification_run.json` and correctly displays `NOT VERIFIED` for this source-only, no-Git snapshot.
