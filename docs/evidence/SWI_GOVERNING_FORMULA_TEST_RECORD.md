# SWI Governing Formula — Test Record

**Date (UTC context):** 2026-10-03  
**Base tip inspected:** `7590657dd5670752aae8b9ce7c66b2b2532ec21b`

## Purpose

Implement and test the SWI governing authorization condition as an executable, pure predicate:

```text
Permit(a) ⟺ ∀L,G,S,H: C(a) ⊆ L ∩ G ∩ S ∩ H  ∧  E(a) ≠ ∅
```

## Status language (mandatory)

| Claim | State |
|-------|--------|
| IMPLEMENTED | YES (`swi_v2/kernel/governing_permit.py`) |
| TESTED | YES (11 targeted tests + existing authority non-escalation suite) |
| PROVEN | **NO** |
| SEALED | **NO** |
| PRODUCTION AUTHORIZED | **NO** |

## Distinctions preserved

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
TESTED ≠ PROVEN
PROVEN ≠ SEALED
SEALED ≠ PRODUCTION AUTHORIZED
UNKNOWN ≠ PERMITTED
SIGNATURE ≠ AUTHORIZATION
OBSERVATION ≠ AUTHORITY
```

## Implementation

- Path: `swi_v2/kernel/governing_permit.py`
- Export: `evaluate_governing_permit`, `PermitOutcome`, `GoverningEvaluation`
- Additive only: does not alter M11 seal, admission path, or existing `authority.py` non-escalation helper beyond export.
- Fail-closed: any UNKNOWN required layer → `UNKNOWN` (never `PERMITTED`).
- Empty evidence → `REJECTED`.
- Layer failure → `REJECTED`.

## Tests

Path: `test/test_governing_formula.py`

| # | Case | Expected |
|---|------|----------|
| 1 | All L/G/S/H + evidence | PERMITTED |
| 2 | Law failure | REJECTED |
| 3 | Governance failure | REJECTED |
| 4 | System failure | REJECTED |
| 5 | Human authority failure | REJECTED |
| 6 | No evidence | REJECTED |
| 7 | Unknown layer | UNKNOWN (never PERMITTED) |
| 8 | Observation ≠ authority | UNKNOWN / not permitted |
| 9 | Signature ≠ authorization | UNKNOWN / REJECTED as appropriate |
| 10 | Revalidation after change | prior not auto-reused |

## Commands executed (local)

```text
python -m pytest test/test_governing_formula.py -q
→ 11 passed

python -m pytest test/test_governing_formula.py test/test_authority_non_escalation.py -q
→ 25 passed
```

## Limitations

- Demonstrates that the **tested implementation** behaves according to the listed cases.
- Does **not** establish universal proof of SWI.
- Does **not** replace IAM, legal process, or institutional authorization.
- Does **not** mark any production system authorized.

## Explicit non-claims

`production_authorized = false`  
`proven = false`  
`sealed = false`
