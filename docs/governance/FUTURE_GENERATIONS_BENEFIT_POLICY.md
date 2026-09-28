# Future Generations Benefit Policy

**Status:** DESIGN  
**Adoption model:** **OPTIONAL** production-governance term  
**Human / legal review:** REQUIRED before any adopted term becomes binding  
**Automatically contractual:** NO  
**Automatic payment mechanism:** NO  
**Forced on all projects:** NO  
**Production authorization:** NOT AUTHORIZED by this document alone  
**Seal:** NOT REQUESTED  

---

## Purpose

SWI provides an **optional mechanism** for projects, contributors, institutions, or rights-holders who want their production value to include a transparent, auditable future-generations commitment.

This is **not**:

- an automatic claim against all SWI work  
- a mandatory tax on contributors  
- a replacement for intellectual-property rights, contracts, or law  
- a grant of authority or payment order by SWI itself  

---

## Optional production-governance term

**Future Generations Benefit Term — Optional**

Projects, contributors, institutions, or rights-holders may **voluntarily adopt** a benefit-allocation term as part of their applicable terms and conditions.

Where adopted, the following must be **explicitly recorded before production authorization**:

| Record | Meaning |
|--------|--------|
| Agreed percentage | e.g. reference 75% of the *defined* benefit/royalty pool |
| Beneficiaries / qualifying programs | Who or what categories may receive allocation |
| Qualifying uses | What counts as future-generations benefit |
| Governance mechanism | Who decides, how disputes are handled |
| Audit requirements | How allocation and expenditure are evidenced |
| Legal instrument reference | Contract, license addendum, or policy that makes the term binding |

```text
ADOPTED TERM  ≠  automatic entitlement
RECORDED %    ≠  payment executed
SWI PASS      ≠  legal authority to disburse
```

The term does **not** override intellectual-property rights, contracts, law, contributor entitlements, or human authority.

---

## Proposed reference allocation (when the term is adopted)

**Reference target:** 75% of the *defined* benefit/royalty pool toward verified future-generations benefit, **subject to the applicable agreement and legal review**.

Other percentages may be agreed in the adopting instrument. SWI does not invent a percentage in the absence of an adopted term.

---

## Progression (clean ladder)

```text
DESIGN
  → EXPERIMENTAL
  → TESTED
  → VERIFIED
  → PRODUCTION-READY
  → OPTIONAL TERMS (including Future Generations Benefit Term, if chosen)
  → AUTHORIZED PRODUCTION
```

Reaching production readiness does **not** force adoption of the 75% model.  
Adoption is a deliberate choice under applicable terms.  
Once adopted, SWI can require the allocation to be **represented transparently and auditable** as part of path/claim evidence — it still does not execute payment by itself.

---

## Ledger concept (when term is in force)

```text
CONTRIBUTION
  ↓ CLAIM
  ↓ VALUE EVENT
  ↓ ROYALTY / BENEFIT CALCULATION (per adopted instrument)
  ↓ ALLOCATION
  ↓ FUTURE-GENERATIONS SHARE (agreed %)
  ↓ PROGRAM
  ↓ ACTUAL EXPENDITURE
  ↓ BENEFICIARY EVIDENCE
  ↓ AUDIT
```

```text
X% ALLOCATED  ≠  X% BENEFIT PROVEN
```

---

## Hard rules

1. Royalty/benefit fields on claim or path records are **measurement only** unless a separate legal instrument says otherwise.  
2. Without an **adopted** term, royalty status remains `NOT_APPLICABLE` or `UNRESOLVED` — never auto-`ALLOCATED`.  
3. Eligibility and allocation status remain unresolved until human/legal process under the adopted instrument completes.  
4. No JSON field creates entitlement, payment order, or authority.  
5. Beneficiary claims require evidence; unverified statements are `UNTRUSTED` / `UNRESOLVED`.  
6. False or unverifiable “75%” (or other %) claims without an adopted term are adversarial failure conditions.  
7. This policy does not modify M11, production execution defaults, or INV-08 / H.  

---

## Audit questions (when term is adopted)

- Was the term voluntarily adopted, and under which instrument?  
- What value event was recorded?  
- How was the calculation derived under that instrument?  
- What was allocated vs expended?  
- Which programs received funds or equivalent benefit?  
- What beneficiary evidence exists and at what tip/hash?  
- Can an independent auditor reproduce the trail without trusting a single boolean?

---

## Non-claims

```text
Policy document              ≠ contract
Optional term offered        ≠ term adopted
Adopted term                 ≠ payment executed
Allocation target            ≠ benefit proven
Claim royalty.eligible=true  ≠ entitlement
SWI PASS                     ≠ legal authority to disburse
Production-ready             ≠ forced 75% adoption
```

---

## Relation to Universal Path framework

Claim and path schemas may record royalty measurement fields. Those fields support **transparency when a term is adopted**. They do not create the term, force adoption, or authorize production.

```text
«Do not claim what the code cannot demonstrate.»
```
