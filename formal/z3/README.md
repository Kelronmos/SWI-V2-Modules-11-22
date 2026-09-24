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
| CI | Reproducible runs (see law_adversarial.yml) |
| Evidence manifest | SHA + results actually recorded |
| Independent audit | Model ↔ Python correspondence |

**TESTED ≠ FORMALLY CHECKED ≠ SEALED ≠ PRODUCTION AUTHORIZED ≠ LEGAL COMPLIANCE**

**SOURCE_CONTRACT_TIP** = `4cb10a0` — the git tip of the *Python*
authority/registry semantics this model was audited against.

HEAD may be newer when only `formal/` or `evidence/` changed. The model
refuses results if `authority.py` / `registry.py` **blob SHAs** drift.
Do not set SOURCE_CONTRACT_TIP = HEAD; that would hide stale models.

Historical M11 seal (e.g. V2 `1d6d7dc…`) is a separate record and is not
rewritten by this experimental law-authority lane.
