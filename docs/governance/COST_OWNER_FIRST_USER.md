# Cost Owner / First User under Different Authority

**Status:** DESIGN / CONTROLLED DEVELOPMENT  
**Production:** NOT AUTHORIZED  
**Seal:** NOT REQUESTED  
**Tip binding (branch base):** `aa62042888886f5252e2b80e7aec8dce49e4bab3`  
**Schema:** `docs/governance/cost_owner.schema.json` (`swi.cost_owner.v1`)

This document defines a **measurement structure** for cost ownership and first-user authority divergence. It does **not** implement a second authority system.

---

## Hard separations

```text
COST OWNER           ≠  DECISION AUTHORITY
FIRST USER           ≠  UNIVERSAL AUTHORITY
DIFFERENT AUTHORITY  ≠  SYSTEM PERMISSION
COST DECLARATION     ≠  AUTHORIZATION
authority_level      ≠  CAPABILITY
```

| May do | Must not do |
|--------|-------------|
| Record who bears cost | Grant permission from this record |
| Record that first user acts under a different authority | Inherit system authority from first user |
| Flag CONFLICT when path required authority diverges | Auto-merge divergent authorities |
| Attach cost categories for audit | Treat BENEFIT_ALLOCATION as payment order |
| Require divergence_reason when not system default | Treat observational flags as privileges |

---

## Authority boundary reuse

**Actual authority checks remain on existing surfaces:**

- `swi_v2/kernel/authority.py` — denylist, missing-auth → HALT  
- `swi_v2/kernel/halt.py`  
- `docs/runtime/HUMAN_AUTHORITY.md` — **H = UNDER_CONSTRUCTION**  
- INV-08 — still open  

`authority_level` in the cost-owner schema is **descriptive metadata only**. Loaders and verifiers **must not** interpret it as a runtime capability. Issuing or verifying human capability is the H programme, not this schema.

```text
recorded authority ≠ actual authority
```

Forbidden fields (`authorized`, `human_approved`, `permission`, …) remain subject to the kernel denylist if presented as untrusted input.

---

## When first user authority differs

1. Set `same_as_system_default: false`.  
2. Provide `divergence_reason`.  
3. Set `first_user.differs_from_path_required_authority: true` when applicable.  
4. Set `authority_status` to `DECLARED_ONLY`, `INSTRUMENT_REFERENCED`, `CONFLICT`, or `UNRESOLVED` — not silent PASS.  
5. Elevate review depth for authority_review / human_safety_review until resolved.  
6. Do **not** promote path status to authorized or production-ready from this record alone.

---

## Cost vs authority

Who **pays** is not who may **authorize** a consequential transition.

`cost.borne_by` and `cost_owner.identity` support accounting and audit. They do not satisfy `H` in the multi-way permission condition.

`BENEFIT_ALLOCATION` as a cost category is only meaningful when an **optional** Future Generations Benefit term has been **voluntarily adopted** under a separate legal instrument. It still does not execute payment.

---

## Intake questions (first user)

1. Who is the cost owner (identity / organization)?  
2. Under what authority source and instrument do they act?  
3. Does that match the path’s required authority?  
4. What cost categories are accepted?  
5. Is recharge allowed, under which rules?  
6. What remains UNRESOLVED?

Unanswered → `MISSING` / `UNRESOLVED`, not silent defaults that look like approval.

---

## Non-claims

```text
Schema exists                 ≠ Implemented capability
Cost owner declared           ≠ H closed
First user recorded           ≠ Universal authority
Different authority declared  ≠ System permission
authority_level set           ≠ Runtime capability
Review PASS on this record    ≠ Production authorized
```

**M11 untouched. Production not authorized. Seal not requested. H remains UNDER_CONSTRUCTION.**

```text
«Do not claim what the code cannot demonstrate.»
```
