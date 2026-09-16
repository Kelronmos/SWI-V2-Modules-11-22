# SWI V2 — Modules 11–22

Upstream: [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10)

```text
Serialized V1 evidence → M11 → AdmittedInput → Kernel
```

**M11:** TESTED + hardened (strict fields, opt-in ReplayGuard) / **NOT SEALED**  
**Tip freeze:** [`docs/M11_TIP_FREEZE.md`](docs/M11_TIP_FREEZE.md)  
**M12–22:** **BLOCKED** until M11 sealed  
**CRTG:** DESIGN PENDING  

Prior `M11_FINAL_AUDIT_REPORT.md` is **historical** for earlier SHAs — re-audit the frozen tip before sealing.

```bash
pip install -r requirements.txt && python -m pytest -q
```
