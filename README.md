# SWI V2 — Modules 11–22

Upstream: [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10)

**Closing goal:** prove V1→V2 serialized boundary — **not** complete Modules 11–22.

```text
Serialized V1 evidence → M11 → AdmittedInput → Kernel
RAW / invalid → REJECT (no M12+)
```

| Item | State |
|------|--------|
| Contract / local travel | Documented / **locally proven** |
| Two-checkout CI | Scripts + workflow · **PENDING green tip** |
| M11 / Kernel | TESTED / **NOT SEALED** |
| CRTG | DESIGN PENDING |
| M12–22 | **BLOCKED** |

**Manual:** [`docs/V2_CLOSING_AND_M11_SEAL_MANUAL.md`](docs/V2_CLOSING_AND_M11_SEAL_MANUAL.md)

```bash
pip install -r requirements.txt && python -m pytest -q
```

Two-checkout: `docs/TWO_CHECKOUT_CI_TEST_PLAN.md` · workflow `two_checkout_travel.yml`
