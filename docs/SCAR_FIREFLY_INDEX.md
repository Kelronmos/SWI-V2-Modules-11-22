# SCAR → Firefly Documentation Index

**Status:** DESIGN / DEFERRED — **NO IMPLEMENTATION AUTHORIZED**  
**Date:** 2026-09-19  
**M11:** SEALED · **M12:** FROZEN · **Firefly code:** not present  
**Policy:** FROZEN — `SCAR_FIREFLY_POLICY_RESOLUTION.md`

## Read order

| Order | Document | Role |
|-------|----------|------|
| 1 | V1 `docs/SCAR_STATUS.md` | What SCAR is |
| 2 | `SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md` | MAY / REJECT / NEVER INFER |
| 3 | `SCAR_FIREFLY_ADAPTER_CONTRACT.md` | Adapter I/O |
| 4 | `SCAR_FIREFLY_CONTRACT_AUDIT.md` | Audit vs scar.py |
| 5 | `SCAR_FIREFLY_ADAPTER_TEST_SPEC.md` | Test vectors |
| 6 | `SCAR_FIREFLY_TEACHING_MANUAL.md` | Teaching |
| 7 | `SWI_TEACHING_GUIDE_MEMORY_BOUNDARY_AUDIT.md` | Boundary audit |
| 8 | `SCAR_FIREFLY_BUILD_MANUAL.md` | Build path |
| 8a | `SCAR_FIREFLY_POLICY_RESOLUTION.md` | Policies A–F FROZEN |
| 8b | `SCAR_FIREFLY_FIELD_CONTRACT.md` | Fields aligned to policy |
| 8c | `SCAR_FIREFLY_IMPLEMENTATION_AUTHORIZATION.md` | **NOT AUTHORIZED** |
| 9 | `V2_MEMORY_WEB_STATUS.md` | Status table |

## Implementation gate (closed)

Code requires AUTHORIZED decision + frozen SHAs. No `swi_v2/firefly/` until then.
