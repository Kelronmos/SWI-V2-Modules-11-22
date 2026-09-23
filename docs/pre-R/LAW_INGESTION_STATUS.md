# LAW INGESTION LANE — STATUS

**Date:** 23 September 2026  
**Branch:** `experimental/law-ingestion-lane`  
**Status vocabulary:** RESEARCH / EXPERIMENTAL · IMPLEMENTED · NOT SEALED · NOT PRODUCTION AUTHORIZED · LEGAL COMPLIANCE NOT CLAIMED

## Governing invariant

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
LAW ARTIFACT (immutable) ≠ LIFECYCLE EVENT ≠ POLICY MAPPING (interpretive)
```

Artifacts are never rewritten. Supersession is recorded only as a separate immutable `LawLifecycleEvent`.

## Current status

| Capability                        | Status                          |
|-----------------------------------|---------------------------------|
| LAW INGESTION LANE                | RESEARCH / EXPERIMENTAL         |
| IMPLEMENTED (skeleton)            | ✓                               |
| ADVERSARIAL TESTED                | required next                   |
| REPLAY TESTED                     | required next                   |
| EU SOURCE DEMO                    | after adversarial suite         |
| BOTSWANA SOURCE DEMO              | after adversarial suite         |
| INDEPENDENT AUDIT                 | required                        |
| SEALED                            | ✗                               |
| PRODUCTION AUTHORIZED             | ✗                               |
| LEGAL COMPLIANCE CLAIM            | ✗                               |

## Defensible claim (only)

> SWI experimentally ingests identified legal-source artefacts and demonstrates controlled versioning, integrity verification, immutable evidence retention, authority-gated registry mutation, and separation between legal-source evidence and executable policy.

## Forbidden claims

- “SWI understands the law.”
- “SWI is legally compliant.”
- “SWI automatically enforces EU / Botswana law.”

## Next concrete step

1. Implement / expand the adversarial test suite under `tests/law/`.
2. Run full existing V2 suite + new law suite.
3. Generate reproducible test / replay evidence package under `evidence/law/`.
4. Independent audit of the experimental lane before any broader integration claim.
