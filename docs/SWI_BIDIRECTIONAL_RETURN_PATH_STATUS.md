# Bidirectional Verified Return Path — Status

**Date:** 2026-09-19  
**Status:** DESIGN complete for pre-R experiment · **NOT IMPLEMENTED**  
**Implementation:** NOT AUTHORIZED  
**Code:** absent  

| Item | State |
|------|--------|
| Build manual | `docs/SWI_BIDIRECTIONAL_VERIFIED_RETURN_PATH_BUILD_MANUAL.md` |
| Envelope field review | `docs/SWI_RESPONSE_ENVELOPE_FIELD_REVIEW.md` |
| Adversarial acceptance | `docs/SWI_BIDIRECTIONAL_RETURN_ADVERSARIAL_ACCEPTANCE.md` |
| Invariants matrix I-01…I-15 | `docs/SWI_RETURN_PATH_INVARIANTS_MATRIX.md` — all **NOT TESTED** |
| Implementation gate | `docs/SWI_RETURN_PATH_IMPLEMENTATION_AUTHORIZATION.md` (**NOT AUTHORIZED**) |
| Formal modules | None — **pre-R01…pre-R10** only after authorization |
| M11 | SEALED — independent |
| M12 | FROZEN — no bypass |

## Central rule

> Information may travel backwards; authority does not.

## Claim discipline

```text
DESIGN ≠ TESTED ≠ PROVEN ≠ SEALED
```

## Next

1. Human sign-off on envelope + adversarial matrix  
2. **AUTHORIZED** + frozen SHAs  
3. Implement under pre-R / `response_path/` only  
4. Executable tests for I-01…I-15 and N01–N28  
5. CI → audit → seal decision only if gates pass  
