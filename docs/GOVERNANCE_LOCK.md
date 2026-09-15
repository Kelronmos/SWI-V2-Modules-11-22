# SWI Governance Lock (V2)

**Date:** 15 September 2026  
**Aligned with V1** `docs/GOVERNANCE_LOCK.md`

## Rules

1. Advance when the required **dependency boundary** is validated — not when module numbers match V1.  
2. A readiness **percentage never overrides** a failed critical dependency or integrity gate.

## Architecture (frozen this phase)

```text
Foundation Evidence → M11 → AdmittedInput → Kernel
                          ├── M12+ sequential only
                          └── CRTG design (parallel)
```

Engines/adapters: **their** contracts — do not impersonate V1 00–10.

## Priorities

| # | Focus |
|---|--------|
| 1 | Upstream V1 Seal 5 path (blocker for M11 **seal**) |
| 2 | **M11 + Kernel:** invalid → HALT; valid → AdmittedInput; no downstream on failed admission; then **freeze** |
| 3 | CRTG **design** freeze — no implementation rush |

## Non-goals

Bulk M13–M22 · architecture redesign · claiming CRTG or M11 sealed without evidence

**Next: prove the foundation and admission boundary, don't add another layer.**
