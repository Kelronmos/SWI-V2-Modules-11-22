# LAW INGESTION LANE — STATUS

**Date:** 23 September 2026  
**Branch:** `experimental/law-ingestion-lane`  
**Tip:** `538490a525f2e86c9bd9b37293b82adf302dfc4f`

## Status vocabulary

RESEARCH / EXPERIMENTAL · IMPLEMENTED · **TESTED (this tip)** · NOT SEALED · NOT PRODUCTION AUTHORIZED · LEGAL COMPLIANCE NOT CLAIMED

## Governing invariant

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
LAW ARTIFACT (immutable) ≠ LIFECYCLE EVENT ≠ POLICY MAPPING (interpretive)
```

Artifacts are never rewritten. Supersession is recorded only as a separate immutable `LawLifecycleEvent`.

## Execution evidence (this tip)

| Capability                         | Result                                      |
|------------------------------------|---------------------------------------------|
| Law adversarial suite              | **20/20 PASSED** (local)                    |
| V2 `test/` + law                   | **129/129 PASSED** (local)                  |
| CI pre-R boundary                  | **success** (run 35853865120)               |
| CI SWI V2 Verification             | **success** (run 35853865150)               |
| CI two-checkout-travel             | **success** (run 35853865056)               |
| Evidence package                   | populated under `evidence/law/`             |
| EU source demo                     | **deferred**                                |
| Botswana source demo               | **deferred**                                |
| Independent audit                  | **required next**                           |
| Sealed                             | **NO**                                      |
| Production authorized              | **NO**                                      |
| Legal compliance claim             | **NO**                                      |

## Demonstrated properties (by test + CI)

1. **Authority** — missing → HALT; wrong scope → REJECT; correct admin scope → accepted  
2. **Integrity** — content / metadata / hash tamper → REJECT; forged/empty lifecycle hash → REJECT  
3. **Supersession** — invalid event → zero writes; v001 remains identical; v002 independently addressable; event stored separately  
4. **Replay** — first event accepted; replay → REJECT; **explicitly in-process only, not durable**  
5. **Non-escalation** — ingest does not authorize; policy does not mutate or authorize the artifact; status remains `INGEST_ONLY`

## Defensible claim (only)

> SWI experimentally ingests identified legal-source artefacts and demonstrates controlled versioning, integrity verification, immutable evidence retention, authority-gated registry mutation, and separation between legal-source evidence and executable policy **for the tested scenarios at tip 538490a**.

## Forbidden claims

- “SWI understands the law.”
- “SWI is legally compliant.”
- “SWI automatically enforces EU / Botswana law.”
- “TESTED → SEALED.”

## Next

1. Independent audit of the experimental lane  
2. Only then EU / Botswana source fixtures  
3. PR remains unopened until audit boundary is accepted
