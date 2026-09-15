# V2 — Cross-Repository Trust Integration

**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Canonical design:** `docs/CROSS_REPOSITORY_TRUST_SPECIFICATION.md`  
**Status:** **PROPOSED / DESIGN PENDING**

## Primary integration point

```text
Cross-Repo Envelope
        → CRTG          (PROPOSED — not coded)
        → M11           (fixture-tested / NOT SEALED)
        → AdmittedInput
        → V2 Kernel
        → M12–M22       (PROPOSED)
```

## Rules

1. **CRTG before M11** for external cross-repo ingress (when implemented).  
2. **M11 still required** — authentication ≠ foundation admission.  
3. **M12+ never accept raw** input; only `AdmittedInput` via kernel.  
4. **No synthetic evidence** to satisfy M11.  
5. **Do not mark CRTG IMPLEMENTED** until code + negative tests + CI on exact tip.

## Repository identity (planned)

| Field | Value |
|-------|--------|
| Repository | `Kelronmos/SWI-V2-Modules-11-22` |
| Pipeline example | `foundation-admission` |
| Certificate / keys | DESIGN PENDING |
| Private keys in repo | **Forbidden** |

## Blockers before CRTG coding

- Freeze certificate profile  
- Freeze envelope + canonical serialization  
- Freeze key lifecycle + rotation/revocation/replay  
- V1 Foundation Seal 5 + real Foundation Evidence Contract (for M11 seal path)

## Claim discipline

README must not say certificates or CRTG are live. Correct line: **PROPOSED / DESIGN PENDING**.
