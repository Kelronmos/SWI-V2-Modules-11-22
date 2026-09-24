# Claim-Level Evidence Ledger (WP-02)

**STATUS:** STARTED / ACCOUNTING  
**MACHINE-READABLE:** `evidence/claim-ledger.json`  
**OBSERVED_HEAD_AT_WRITE:** `a10e0c490d2ce4d7fccbbbeec6fb32f5f32b7c02`  
**FRESHNESS DOCTRINE:** `docs/runtime/EVIDENCE_FRESHNESS_CONTRACT.md` (FROZEN)  
**LIMITATIONS:** Manual first population. Not a verifier. Not Foundation PASS. Not seal.  
**NEXT GATE:** Optional machine validator + scoped HEAD_CURRENT runs for REGENERATE rows only; then WP-03.

Execution: **BLOCKED**. Classifications allowed: **INHERIT | REGENERATE | NO_EVIDENCE** only.

---

## Rules

1. One record per claim.  
2. `TIP_BOUND ≠ HEAD_CURRENT`.  
3. Docs identify requirements; they are not implementation proof.  
4. Do not rewrite `source_tip`. New proof → new package.  
5. Do not REGENERATE tests for systems that do not exist yet (use NO_EVIDENCE).  
6. Six partial Snyder rows ≠ Snyder compatible.

---

## Summary table

| claim_id | classification | freshness | next |
|----------|----------------|-----------|------|
| LAW-001 | **INHERIT** | TIP_BOUND | optional scoped HEAD_CURRENT later |
| AUTH-001 | **INHERIT** | TIP_BOUND | keep narrow (two blobs) |
| FRESH-001 | **INHERIT** | TIP_BOUND | CI-bind when claiming CI-VERIFIED |
| TEST-001 | **REGENERATE** | REFRESH_REQUIRED | full suite at controlled HEAD |
| FOUNDATION-001 | **REGENERATE** | REFRESH_REQUIRED | foundation evidence at HEAD |
| TRAVEL-001 | **REGENERATE** | REFRESH_REQUIRED | two-checkout at HEAD |
| INV-001 | **NO_EVIDENCE** | — | build runtime first |
| EXEC-001 | **NO_EVIDENCE** | — | WP-07 after prior WPs |
| H-001 | **NO_EVIDENCE** | — | WP-15 |
| ENV-001 | **NO_EVIDENCE** | — | implement envelope |
| LEDGER-001 | **NO_EVIDENCE** | — | WP-09 |
| SNYDER-01…06 | **NO_EVIDENCE** | — | per-requirement proof |

---

## INHERIT (tip-bound, still valid for named tip)

### LAW-001
Experimental law formal/pytest at **8245e3f**. Artifacts under `evidence/law/`. Blobs match. **Does not prove HEAD.**

### AUTH-001
`authority.py` / `registry.py` blob SHAs unchanged vs manifest. **Not** “authority system proven.”

### FRESH-001
`8245e3f` ancestor of main + local freshness tests pass. **AncestorPass only.**

---

## REGENERATE (need new HEAD-bound run)

### TEST-001 / FOUNDATION-001 / TRAVEL-001
Prior greens are tip-bound or historical relative to current HEAD. Require controlled environment → tests → CI → **new** evidence package. Never overwrite 8245e3f.

---

## NO_EVIDENCE (no implementation to re-run)

### INV-001
Six-way invariant. MATH-002 ≠ this claim.

### EXEC-001
Mandatory corridor / ExecutionCapability. Execution policy-blocked.

### H-001 / ENV-001 / LEDGER-001
Under construction or design-only. Documentation ≠ proof.

### SNYDER-01…06
Matrix is diagnostic. Each requirement needs its own evidence row closed later.

---

## Closure chain (accounting → proof)

```text
CLAIM → IMPLEMENTATION → TEST → EVIDENCE → FRESHNESS → CLASSIFICATION
         INHERIT | REGENERATE | NO_EVIDENCE
              → … later WPs → SEAL (≠ production)
```

«Do not claim what the code cannot demonstrate.»
