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
| `reviewer_registry.json` | Machine-readable five-position registry |
| `README.md` | This document |

Immutable review receipts and automatic README registration of admitted reviews are not yet implemented.
