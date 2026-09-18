# Authority Boundary Model

**Status:** DESIGNED → IMPLEMENTED → TESTED (not SEALED)  
**Date:** 18 September 2026  
**Contract id:** `authority_boundary_v0`  
**Rule:** Information may cross a boundary without authority crossing that boundary.

**Paired implementation:** V1 `swi_core.authority` + `docs/AUTHORITY_BOUNDARY_MODEL.md`  
Repository: `Kelronmos/SWI-V1-Module-1-10`

---

## 1. Invariant

```text
DATA  ≠  EVIDENCE  ≠  ADMISSION  ≠  AUTHORIZATION  ≠  ACTION
```

| Layer | May do | Must not imply |
|-------|--------|----------------|
| **Data** | Carry information | Truth or authority |
| **Evidence** | Record an observed/tested result under a contract | Universal truth; permission to act |
| **Admission** | Accept data under a declared schema/integrity contract (e.g. M11) | Authorization or unrestricted execution |
| **Authorization** | Grant **explicit, scoped** permission | Unrestricted authority; truth of content |
| **Action** | Execute **only** within declared authorization | Authority beyond scope |

---

## 2. Core rule

```text
INFORMATION MAY CROSS A BOUNDARY
WITHOUT AUTHORITY CROSSING THAT BOUNDARY.
```

Transfer is not trust. Hash valid is not true. Signature valid is not true.  
Admitted is not authorized. Authorized is not unlimited action.

---

## 3. Non-escalation

| From | Does not grant |
|------|----------------|
| Data present | Evidence status |
| Evidence valid | Admission |
| Admission (e.g. `AdmittedInput`) | Authorization to act |
| Authorization | Action outside declared scope |
| Action success | Broader authority |

---

## 4. Undeclared authority fields

Smuggling via undeclared fields is rejected, not stripped:

`verified`, `trusted`, `truth`, `authority`, `m11_admitted`, `replay_verified`,
`security_level`, `system_authority`, `admin_authority`, `policy_authorized`,
`human_approved`, `authorized`, `permission`, `privilege`

```text
UNDECLARED AUTHORITY FIELD → REJECT
```

Contract-declared exceptions must be listed in `allowed_fields`.

---

## 5. Missing / out-of-scope authorization

```text
ACTION + authorization absent → HALT
ACTION + scope/action outside declared set → REJECT
```

---

## 6. Evidence of rejection

`AuthorityDecision` records: entered keys, rejected fields, reason, contract id, next_state.

Implementation: `swi_v2.kernel.authority`.

---

## 7. Relationship to M11

M11 admission = schema + integrity + status. **Not** authorization or action rights.

---

## 8. Status vocabulary

`HYPOTHESIZED` → `DESIGNED` → `IMPLEMENTED` → `TESTED` → `CI-VERIFIED` → `AUDITED` → `SEALED`

Forbidden: TESTED→SEALED automatically; SEALED→AUTHORIZED; AUTHORIZED→UNRESTRICTED.

**This boundary: TESTED after suite green; not SEALED in this series.**

---

## 9. Limitations (v0)

- Top-level field scan only
- Not a full policy engine / CRTG / production IAM
- Does not implement M12–22
- Does not establish factual truth

## 10. Next

CI-VERIFIED on tip → optional nested scan → module wiring → audit → seal of **this helper only** (independent of M11 seal history).
