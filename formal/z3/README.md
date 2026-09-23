# Formal Z3 models (experimental)

**STATUS:** RESEARCH / EXPERIMENTAL · NOT SEALED · NOT PRODUCTION AUTHORIZED

## Purpose

Check formalized **transition contracts** beside the SWI kernel.
These modules are **not** authorization engines and do not replace
`experimental/law/authority.py` or `swi_v2.kernel.authority`.

## Law authority model

```bash
pip install z3-solver
python -m formal.z3.law_authority
# or: python formal/z3/law_authority.py
```

Properties F-001…F-006 (see module docstring).

| Layer | What it establishes |
|-------|---------------------|
| pytest | Concrete implementation behavior |
| Z3 | No counterexample in the formalized single-step model |
| CI | Reproducible runs |
| Evidence manifest | SHA + results actually recorded |
| Independent audit | Model ↔ Python correspondence |

**TESTED ≠ FORMALLY CHECKED ≠ SEALED ≠ PRODUCTION AUTHORIZED ≠ LEGAL COMPLIANCE**

Designed against tip `4cb10a0` contract; regenerate evidence after formal runs.
