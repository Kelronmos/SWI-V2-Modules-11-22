# SWI Junction Receipt, Frontier & Runtime Audit Manual

**Status:** DESIGN / CONTROLLED DEVELOPMENT  
**Production:** NOT AUTHORIZED  
**Seal:** NOT REQUESTED  
**Kernel `receipt.py`:** **NOT IMPLEMENTED** on main or this branch as production code  
**Schema:** `docs/governance/junction_receipt.schema.json` (`swi.junction_receipt.v1`)

This is an **audit/receipt requirement across existing SWI junctions**, not a new architectural layer and not a second authority system.

---

## Receipt invariant

> Every controlled SWI junction MUST produce or reference an auditable receipt containing the evidence necessary to reconstruct what entered, what was measured, what decision/state was produced, what authority applied, what changed, and what happened afterward.

> A receipt shall not be interpreted as proof beyond the evidence it references.

## Drill-down invariant

> Any SWI-generated observation exposed through the Frontier UI or CEK shall be traceable through its receipt chain to the underlying generated records. Where supporting proof is absent, the system shall expose the absence rather than manufacture or infer it.

---

## Junction chain

```text
INPUT → PROVENANCE → CLAIM → EVIDENCE → ADMISSION → MEASUREMENT
  → VERIFICATION → AUTHORITY → BINDING → RUNTIME_RESERVATION
  → EXECUTION_ELIGIBILITY → EXECUTION → OBSERVATION → RECONCILIATION
```

Failures also receipt:

```text
DRIFT · FAILURE · BLOCK · UNKNOWN · UNRESOLVED
```

At each junction:

```text
STATE → RECEIPT → EVIDENCE → PROVENANCE → HASH/INTEGRITY → REPLAY REFERENCE
```

---

## What a receipt does **not** prove

```text
Receipt exists          ≠  Truth of original observation
Hash chain intact       ≠  Truth
Status VERIFIED         ≠  Authorized
Authority state present ≠  H closed
Runtime RESERVED        ≠  Execution permitted
PDF looks complete      ≠  Case admissible in court
```

---

## Evidence-state indicator (not a score)

Use discrete states — **do not** collapse into a single “rate” or dashboard score that could be mistaken for authorization:

```text
OBSERVED · TESTED · REPRODUCED · FORMALLY_CHECKED · INDEPENDENTLY_VERIFIED
```

Display **separately**:

```text
AUTHORITY STATE · BINDING STATE · RUNTIME STATE · FRONTIER · EQUATION STATE
```

---

## JSON vs PDF

| Form | Role |
|------|------|
| **JSON** | Canonical structured audit record — hash, chain, replay, machine verify |
| **PDF** | **Derived** human presentation of the same recorded JSON/evidence |

```text
JSON is the structured record; PDF is a derived presentation of that record.
```

PDF must not be independently authored by the UI as a parallel truth source.

---

## Frontier UI / CEK

UI and CEK **observe and drill down**. They do not grant authority.

```text
CEK → Receipt → Evidence → Claim → Dependency → Measurement → Authority → Binding
```

Dashboard may show only what generated records substantiate. It cannot promote, authorize, repair, or invent state.

---

## Case audit report (not auto “court evidence”)

```text
CASE
├── identity, scope, inputs, provenance
├── claims, evidence, dependencies
├── tests, formal checks, verification
├── authority records, bindings, runtime events
├── drift, failures, corrections attempted
├── replays, consequences, reconciliation
├── outstanding UNKNOWNs
└── integrity manifest
```

```text
CASE REPORT → JSON MASTER → PDF DERIVED → INTEGRITY MANIFEST → REPLAY REFS
```

SWI does **not** declare legal admissibility. Reviewers assess independently.

**Gaps must remain visible:**

```text
CLAIM ✓  TEST ✓  FORMAL ✓  AUTHORITY ?  REPLAY ✗
OVERALL: INCOMPLETE
```

---

## Receipt integrity (conceptual)

```text
H(Rn) = SHA256(canonical(Rn))
R(n+1).previous_receipt_hash = H(Rn)
```

```text
Hash-chain integrity ≠ truth
```

---

## Cost owner / non-SWI

Unchanged:

```text
Cost Owner ≠ Authority
FIRST USER → COST OWNER → REVIEW   (never → auto authority → execution)
```

---

## Implementation status (honest)

| Component | Status |
|-----------|--------|
| Existing foundation / authority boundary / canonical hash | Present on main |
| Receipt **design** + schema | This document + schema on governance branch |
| `swi_v2/kernel/receipt.py` | **NOT IMPLEMENTED** |
| Receipt tests | **NOT ADDED** |
| Runtime integration | **NOT IMPLEMENTED** |
| Durable replay | **NOT IMPLEMENTED** |
| PDF generation | **NOT IMPLEMENTED** |
| Frontier dashboard | **NOT IMPLEMENTED** |
| Production authorization | **NOT AUTHORIZED** |

```text
DESIGN READY FOR CONTROLLED TEST IMPLEMENTATION
≠ IMPLEMENTED ≠ TESTED ≠ VERIFIED ≠ SEALED ≠ PRODUCTION
```

No generated SWI state → no claim that implementation exists.

M11 untouched. H remains UNDER_CONSTRUCTION.

```text
«Do not claim what the code cannot demonstrate.»
```
