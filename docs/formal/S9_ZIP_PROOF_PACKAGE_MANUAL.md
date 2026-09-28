# S9 ZIP Proof Package Manual

**Status:** CONTROLLED DEVELOPMENT / EXPERIMENTAL  
**S9:** NOT PROVEN by this harness alone  
**Production:** NOT AUTHORIZED  
**Tip binding required:** yes  

## Purpose

Record evidence and evaluation state for an S9 evaluation at a **specific repository tip**.

The harness makes results **recalculable, falsifiable, tip-bound, and auditable**.  
It does **not** authorize production, issue human authority, or seal modules.

## Equation

```text
Permit(a)  ⇔  (∀ L,G,S,H : C(a) ⊆ L ∩ G ∩ S ∩ H) ∧ E(a) ≠ ∅
```

## Important limitation

```text
E(a) ≠ ∅  is reported separately from evidence adequacy
(relevant ∧ fresh ∧ scoped ∧ provenance ∧ integrity)
```

Counterexamples X1–X10 remain design obligations.  
`UNKNOWN` never becomes `PASS`.

## Module layout

```text
swi_v2/s9/   inventory · constraints · evidence · evaluator · reconciliation
             replay · manifest · package · diagnostics
tests/s9/
scripts/s9_build_package.py
```

## Reproduction

1. Verify package zip SHA-256.  
2. Verify `source_commit` matches intended tip.  
3. Validate `00_MANIFEST.json`.  
4. Load evaluation JSON.  
5. Recalculate constraint mapping and evidence adequacy.  
6. Run negative cases (`pytest tests/s9`).  
7. Replay pure evaluation; compare.  
8. Produce independent conclusion — do not trust SWI’s label alone.

## Build

```bash
python scripts/s9_build_package.py --commit aa62042888886f5252e2b80e7aec8dce49e4bab3 --out /tmp/s9_out
```

Default system action is expected **BLOCKED** (H missing).

## Final gate

```text
SATISFIED ≠ SEALED ≠ PRODUCTION ≠ LEGAL ADMISSIBILITY
s9_proven remains False at package level until closed programme says otherwise
```

«Do not claim what the code cannot demonstrate.»
