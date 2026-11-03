# Public Review Registry

**Capacity:** 5 positions  
**Current verified:** 0  
**Current admitted:** 0

## State machine (not interchangeable)

```
EMPTY
  → REVIEW_SUBMITTED
    → SOURCE_VERIFIED
      → VERSION_MATCHED
        → EVIDENCE_VALIDATED
          → REPRODUCED
            → REVIEW_ADMITTED
```

Any stage may move to `REJECTED` or `WITHDRAWN`. Failed stages remain visible.

## Non-elevation rules

Admission of a review **never** sets:

- `PROVEN = YES`
- `SEALED = YES`
- `PRODUCTION_AUTHORIZED = YES`

Those values remain under the existing SWI governing spine only.

## Author restriction

The author of the implementation cannot occupy a reviewer position for their own work.

## Files

| File | Purpose |
|------|--------|
| `reviewer_registry.json` | Machine-readable five-position registry (all EMPTY) |
| `receipt_generator.py` | Stub that builds/writes receipt JSON; never invents reviewers |
| `../schemas/review_receipt.schema.json` | JSON Schema for receipts |
| `README.md` | This document |

## Receipt generation (stub)

```bash
cd public_evidence_lab
python3 review/receipt_generator.py --position 1 --state REVIEW_SUBMITTED --out-dir receipts
```

Output is a structured receipt with all claim fields locked false and stage results marked `NOT_RUN` unless supplied. This does **not** admit a review or update the registry.

Automatic README registration of admitted reviews is not yet implemented.
