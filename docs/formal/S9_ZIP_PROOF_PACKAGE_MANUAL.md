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

`UNKNOWN` never becomes `PASS`.  
`Harness PASS` does not imply S9 proof.

## Build

```bash
python scripts/s9_build_package.py --commit aa62042888886f5252e2b80e7aec8dce49e4bab3 --out /tmp/s9_out
```

Default system action is expected **BLOCKED** (H missing).

«Do not claim what the code cannot demonstrate.»
