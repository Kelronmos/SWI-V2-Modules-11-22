# SWI V2 — Modules 11–22

**Volume 2** of Structured Workflow Intelligence.  
**Governance:** [`docs/GOVERNANCE_LOCK.md`](docs/GOVERNANCE_LOCK.md)

| Volume | Repo | Scope |
|--------|------|--------|
| 1 | [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10) | Foundation 00–10 |
| 2 | This repo | Continuation 11–22 |

## Rules

- Never convert unverified data into verified data.  
- Never claim V1 verified what V1 did not.  
- Advance by **dependency boundaries**, not module-count symmetry.  
- Readiness % **never** overrides a failed critical gate.

```text
RAW → HALT
V1 evidence → M11 → AdmittedInput → Kernel → M12+
```

## Status

| Component | State |
|-----------|--------|
| Kernel | IMPLEMENTED / TESTED / NOT SEALED |
| M11 | Tested (fixture + `v1_trainer_pipeline_completed`) / NOT SEALED |
| Ed25519 | Primitive only · not CRTG |
| CRTG | Design track |
| M12–22 | Sequential only · **not bulk-built** |

## Verify

```bash
pip install -r requirements.txt
python -m pytest -q
```

Next: **prove admission/kernel boundary**, not another layer.
