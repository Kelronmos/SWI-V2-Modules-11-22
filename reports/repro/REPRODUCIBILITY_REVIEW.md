# Reproducibility Review — ISO Claim Gate

**Branch:** `review/iso-gate-repro-2026-11-01`  
**Commit under test:** `4f8685181d8c8af2166277262ecae30182c90cce`

## Status of this package

This package publishes **execution records from a controlled run** so another reviewer can inspect commands, environment and hashes.

```text
REPORTED ≠ INDEPENDENTLY VERIFIED
BACKUP HASH MATCH ≠ FULL-TREE BACKUP COMPLETENESS
TEST PASS ≠ ISO CONFORMITY
```

## Backup / restore (critical paths only)

| Artifact | Path |
|----------|------|
| BEFORE manifest | `evidence/backup_restoration/BEFORE_manifest.json` |
| BEFORE SHA list | `evidence/backup_restoration/BEFORE_manifest.sha256` |
| Archive digest | `evidence/backup_restoration/archive.sha256` |
| Restore verification | `evidence/backup_restoration/restore_verification.json` |
| AFTER SHA list | `evidence/backup_restoration/AFTER_manifest.sha256` |

Restore check recorded for **7 critical paths**.  
Limitation: **not** a full-repository archive. Local full-tree comparisons are not republished as a complete source archive.

## Test execution records

See `reports/repro/test_results.json` and `reports/repro/command_log.txt`.

Environment: `reports/repro/environment.json`

## Governance

```text
ISO CONFORMITY = NOT ESTABLISHED
CONFORMITY_CLAIM = SEALED
PROVEN = NO
AUTHORIZED = NO
PRODUCTION_AUTHORIZED = NO
```

Open: DEF-ISO-002 (licensed mapping), DEF-ISO-003 (durable replay), DEF-ISO-004 (jsonschema in CI).

Do **not** merge this review branch as proof of ISO conformity.
