# LAW INGESTION LANE — STATUS

**Date:** 23 September 2026  
**Branch:** `experimental/law-ingestion-lane`  
**Tip:** `93e166733039bfd1e65b25e1b56eb776a79c5625`

## Status vocabulary

RESEARCH / EXPERIMENTAL · IMPLEMENTED · **TESTED (this tip)** · NOT SEALED · NOT PRODUCTION AUTHORIZED · LEGAL COMPLIANCE NOT CLAIMED

## Governing invariant

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
LAW ARTIFACT (immutable) ≠ LIFECYCLE EVENT ≠ POLICY MAPPING (interpretive)
```

Artifacts are never rewritten. Supersession is recorded only as a separate immutable `LawLifecycleEvent`.

## Tip lineage (evidence chain)

| Commit | Role |
|--------|------|
| `538490a` | Authority binding fix, atomic supersession, event-hash verification |
| `8945662` | First evidence package (20/20 law + 129/129 combined) |
| `93e1667` | **Current tip** — expanded adversarial surface + dedicated CI gate |

## Execution evidence (tip 93e1667)

| Capability | Result |
|------------|--------|
| Law adversarial suite (expanded) | **35/35 PASSED** (local) |
| V2 `test/` + law (combined, prior tip) | **129/129 PASSED** (local) |
| CI LAW INGESTION ADVERSARIAL | **success** |
| CI SWI V2 Verification (3.10–3.12) | **success** |
| CI pre-R boundary | **success** |
| CI two-checkout-travel | **success** |
| Evidence package | `evidence/law/` |
| EU source demo | **deferred** |
| Botswana source demo | **deferred** |
| Independent audit | **required next** |
| Sealed | **NO** |
| Production authorized | **NO** |
| Legal compliance claim | **NO** |

## Demonstrated properties

1. **Authority** — missing → HALT; wrong scope → REJECT; correct `LAW_REGISTRY_ADMIN` → accepted  
2. **Integrity** — content / metadata / hash tamper → REJECT; forged/empty lifecycle hash → REJECT  
3. **Supersession** — invalid event → zero writes; v001 remains identical; v002 independently addressable  
4. **Replay** — first event accepted; replay → REJECT; **in-process only, not durable**  
5. **Non-escalation** — ingest does not authorize; policy does not mutate or authorize; status remains `INGEST_ONLY`

## Safe claim (only)

> On tip `93e1667`, the dedicated law adversarial suite executed 35 tests and all 35 passed; the full V2 verification CI and the dedicated LAW INGESTION ADVERSARIAL CI both concluded success. The lane demonstrates controlled versioning, integrity verification, immutable evidence retention, authority-gated mutation, and separation of legal-source evidence from executable policy **for the tested scenarios**.

## Forbidden claims

- “SWI understands the law.”
- “SWI is legally compliant.”
- “SWI automatically enforces EU / Botswana law.”
- “TESTED → SEALED.”
- Durable / distributed replay protection.

## Next

1. Independent audit of the experimental lane at tip `93e1667`  
2. Only then EU / Botswana fixtures (URI + timestamp → hash → `INGEST_ONLY` → verify)  
3. PR remains unopened until audit boundary is accepted
