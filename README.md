# SWI V2 — Modules 11–22

Upstream: [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10)

**Travel rule:** V1 produces a versioned evidence contract; V2 consumes **serialized** evidence — not a V1 Python import.

```text
RAW → HALT
Serialized V1 evidence → M11 → AdmittedInput → Kernel → M12+
```

| Item | State |
|------|--------|
| Local V1-shaped travel | **PROVEN** |
| Live two-checkout CI | **PENDING** |
| CRTG | DESIGN PENDING |
| M11 / Kernel seal | NOT READY |
| M12–22 bulk | **Not authorized** |

```bash
pip install -r requirements.txt && python -m pytest -q
```

See `docs/CROSS_REPO_TRAVEL.md` · `docs/GOVERNANCE_LOCK.md`.
