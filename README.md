# SWI V2 — Modules 11–22

Upstream: [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10)

```text
Serialized V1 evidence → M11 → AdmittedInput → Kernel → (M12 after M11 seal only)
```

| State | Value |
|-------|--------|
| M11 / Kernel | TESTED / **NOT SEALED** |
| Two-checkout CI | **NOT CI_VERIFIED** until tip SUCCESS proven |
| M12–22 | **BLOCKED** |
| CRTG | DESIGN PENDING |

**Execution order:** write access → tip CI → A–G audit → seal record → M11 SEALED → M12  
See `docs/CONTROLLED_CLOSING_M11_SEAL_M12_EXECUTION_MANUAL.md`

```bash
pip install -r requirements.txt && python -m pytest -q
```

«DO NOT CLAIM WHAT THE CODE CANNOT DEMONSTRATE.»
