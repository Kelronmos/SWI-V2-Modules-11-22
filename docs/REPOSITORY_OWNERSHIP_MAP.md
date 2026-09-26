# Repository, Ownership & Authority Map

**Document status:** NORMATIVE — rebuild contract §54  
**Seal status:** NOT SEALED  
**Production status:** BLOCKED  
**Date:** 26 September 2026

**Rule:** Code location ≠ ownership ≠ authority ≠ seal ≠ production authorization.

---

## 1. Required fields per controlled unit

| Field | Meaning |
|-------|---------|
| Module / Unit | Structural concern |
| Owner | Accountable human or role (not a bot, not “the repo”) |
| Repository | Code and docs location |
| Branch / lane | Development or evidence lane |
| Responsibility | What it may decide or enforce |
| Dependencies | What must already be true |
| Evidence scope | Tests / records that support claims |
| Authority boundary | What it may never manufacture |

---

## 2. Repository inventory

| Repository | Role | Seal / production posture |
|------------|------|---------------------------|
| `Kelronmos/SWI-V1-Module-1-10` | Foundation pipeline (M00–10) | Partial seals; Foundation Seal 5 NOT READY; production BLOCKED |
| `Kelronmos/SWI-V2-Modules-11-22` | Continuation (M11–22) | M11 SEALED (historical tip); M12+ controlled/blocked; production BLOCKED |
| Branch `experimental/privacy-domain` | Rebuild kernel (privacy, transition) | EXPERIMENTAL · NOT SEALED · PRODUCTION BLOCKED |

**Contract:** V2 depends on V1 **Foundation Evidence Contract** (serialized evidence), not on importing V1 runtime as trust.

---

## 3. Module / unit map (summary)

| Unit | Repo | Path | Responsibility | Must not |
|------|------|------|----------------|----------|
| V2 M11 Continuity Lock | V2 | `swi_v2/module11`, `kernel` | Admit foundation evidence | Claim truth, sender auth, or action safety |
| V2 M12–M22 | V2 | `swi_v2/module12`… | Controlled development after prior seal | Auto-complete; inherit M11 authority |
| Kernel admission | V2 | `swi_v2/kernel/admission.py` | Schema + integrity + status → ADMIT/REJECT | Manufacture human authority |
| Privacy gate | V2 experimental | `experimental/privacy/` | Domain / purpose / scope decisions | Become transition permission alone |
| Transition engine | V2 experimental | `experimental/repair/` | REJECT/BLOCK/QUARANTINE/ALLOW | Implicit transition discovery; mutate on non-ALLOW |
| ATM / adversarial | V2 + experimental | `tests/` | Prove bypass and substitution | PASS → SEALED |
| Docs / doctrine | V1 + V2 `docs/` | manuals, contracts | Normative meaning | Override code invariants by prose alone |

---

## 4. Branch discipline

| Lane | May produce | Must not produce |
|------|-------------|------------------|
| `main` | CI evidence; tip-bound seal records where declared | Silent experimental promotion |
| `experimental/privacy-domain` | Test evidence; design status | Seal claims; production authorization |
| Historical / scar | Regression, replay inputs | New trust without re-admission |

---

## 5. Dependency direction

```text
V1 foundation evidence (serialized)
        → admit
V2 M11 (historical SEALED admission)
        → controlled unlock
V2 M12…M22 (each gated by prior seal)
        → optional
Experimental rebuild kernel
        → evidence only
ATM-001
        → seal review (separate human governance)
        → production authorization (separate; BLOCKED)
```

Forbidden: V2 imports V1 package as trust; experimental writes module seal records without review; old sealed state as new verified; ZTA/PKI/CI as SWI authorization.

---

## 6. Change record template

```text
module_or_unit:
repository:
branch:
owner:
reviewer:
responsibility_delta:
dependencies_touched:
evidence_invalidated:
evidence_required:
authority_impact: none | scoped | requires_human_authority
privacy_impact: none | domain_list
security_context_only: true | false
seal_impact: none | review_required | blocked
production_impact: BLOCKED
```

Missing owner or authority_impact → **BLOCK PROMOTION**.

---

## 7. Rebuild contract clause

A future maintainer must locate every module in a repository and branch, name its owner, state its responsibility, list dependencies, cite evidence, and state its authority boundary **without inferring authority from path or CI status**.

If path and authority are confused: DOCUMENTATION_GAP → REVIEW → CLARIFY → TEST → REVERIFY.
