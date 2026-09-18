# Bidirectional Verified Return Path — Status

**Date:** 2026-09-18  
**Status:** DESIGN / BUILD SPEC ONLY  
**Implementation:** NOT AUTHORIZED  
**Code:** absent  

| Item | State |
|------|--------|
| Build manual | `docs/SWI_BIDIRECTIONAL_VERIFIED_RETURN_PATH_BUILD_MANUAL.md` |
| Formal SWI modules | None (use **pre-R01…pre-R10** if later authorized) |
| M11 | SEALED — independent strand |
| M12 | FROZEN — no bypass via return path |
| SCAR → Firefly | Separate design strand; not this path |
| Response gate code | Not present |

## Central research question

> Can the same evidence, integrity and authority contract survive the return journey without authority laundering, verification loss, UI injection, or backend reinterpretation?

## Next (still design)

1. Review envelope fields before freeze  
2. Write adversarial acceptance criteria document aligned with the manual  
3. Only then: `*_IMPLEMENTATION_AUTHORIZATION.md`  

Do not implement until authorization is explicit.
