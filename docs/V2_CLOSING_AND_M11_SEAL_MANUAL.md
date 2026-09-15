# SWI V2 — Closing & M11 Seal Manual

**Date:** 15 September 2026  
**Status:** OPERATIONAL  
**Does NOT authorize bulk M12–22 or auto-seal M11**

## Purpose

Close the **V2 foundation** and decide whether M11 + Kernel may earn a seal.

Target chain only:

```text
V1 → serialized evidence → M11 → AdmittedInput → Kernel → (later controlled M12)
```

## Constitutional rules (locked)

1. **Serialization is the boundary** — no `import` of SWI-V1 into V2 runtime.  
2. **M10 is not the handoff.**  
3. **Do not mutate V1 evidence in place** — derive V2 state separately.  
4. **Readiness % never overrides** a critical failure.  
5. **No bulk M12–22** until M11 is sealed against real V1 evidence.

## Four closing gates

| Gate | Required |
|------|----------|
| **A Contract** | Frozen fields + digest (excludes `created_at`) |
| **B Two-checkout** | Real V1 producer → JSON → V2 admit; CI preferred |
| **C M11** | Valid accept; tamper/status/schema/parse reject |
| **D Kernel** | Only `AdmittedInput`; rejects cannot reach M12+ |

## Seal criteria checklist

M11 may change **NOT SEALED → SEALED** only if **all** are true:

**Contract**  
- [ ] Evidence contract frozen  
- [ ] Digest fields frozen  
- [ ] `created_at` treatment verified  
- [ ] Version semantics documented  

**Boundary**  
- [ ] No V1 import  
- [ ] M10 not handoff  
- [ ] Serialized evidence is the only cross-repo input  

**Real producer**  
- [ ] Real V1 producer generates evidence  
- [ ] V2 consumes that artifact  
- [ ] Primary proof is not fixture-only  

**Admission**  
- [ ] Valid admitted  
- [ ] Tampered / bad status / missing / malformed rejected  

**Isolation**  
- [ ] Rejected evidence cannot reach Kernel / M12  
- [ ] Raw input cannot bypass M11  

**Reproducibility**  
- [ ] Two-checkout test passes  
- [ ] CI passes on tip  
- [ ] Clean environment  

**Documentation**  
- [ ] README / governance / module status match reality  

Until then: **M11 = NOT SEALED**.

## Ed25519 ≠ CRTG

Cryptographic primitives may exist; **CRTG remains DESIGN PENDING**.

## After M11 seal only

```text
M11 SEALED → M12 design → implement → test → verify → freeze → M13…
```

M13–22 stay **BLOCKED** until their prior boundary is frozen.

## Forbidden

Bulk M12–22 · seal because unit tests pass · import V1 · M10 handoff · fixture as sole final proof · claim CRTG complete · change digest without contract decision · mutate V1 evidence · bypass M11 · drop NOT READY for cosmetics

## Target closing state

```text
Contract              FROZEN (document)
V1 → V2 boundary      LOCAL PROVEN
Two-checkout CI       CI_VERIFIED (tip run 34987307390 · V2 061a47f · V1 be31dd7)
M11 admission         TESTED / NOT SEALED
Kernel isolation      TESTED / NOT SEALED
CRTG                  DESIGN PENDING
M12                   NEXT after M11 seal only
M13–22                BLOCKED
```
