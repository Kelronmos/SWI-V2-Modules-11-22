# SAMH Institutional Authority Visibility

**Status:** DRAFT — DESIGN SPEC  
**Seal:** NOT SEALED  
**Production:** BLOCKED  
**Date:** 26 September 2026

Implements the governance communication idea: not only control access, but **explain** who may see what, at what detail, for what purpose, under which authority.

Related: `docs/INSTITUTIONAL_GOVERNANCE_VISIBILITY.md` · `docs/SAMH_STUDENT_MONITOR_ARCHITECTURE.md`

---

## Actors (registry targets)

Student · Parent · Teacher · School Admin · Counselling · Community · District · Ministry · Government

Each access evaluation must bind:

```text
WHO · WHAT · WHY · RELATIONSHIP · DATA SCOPE · DETAIL LEVEL
POLICY · AUTHORITY · TIME · ACTION · AUDIT
```

If incomplete → **BLOCK**.

---

## Upstream / downstream

```text
UPSTREAM ≠ AUTHORITY ESCALATION
DOWNSTREAM ≠ AUTOMATIC EXECUTION
```

Student record moving up does not authorize ministry action.  
Government policy moving down does not authorize teacher or AI to act on a student without the defined workflow.

---

## Schema pointer

Machine-readable stub: `config/samh_authority_registry.schema.json` (design).  
Tests: when implemented, `tests/` adversarial suite for role/relationship/purpose/detail spoofing.

```text
AI EXPLAINS AUTHORITY ≠ AI CREATES AUTHORITY
```

**Implementation order:** actor → relationship → resource → detail → purpose → policy → authority → evaluator → explain → flows → audit → adversarial → replay → review → scoped seal. **Dashboards last.**

**Non-claims:** No live registry enforcement claimed; no real student data.
