# SWI V2 — Modules 11–22

Upstream: [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10)

Closing phase: **prove** the boundary — do not complete 11–22 by claim.

```text
Contract FROZEN · local travel PROVEN · two-checkout CI PENDING
M11 / Kernel TESTED · NOT SEALED · M12–22 BLOCKED · CRTG DESIGN PENDING
```

**Manuals:** [Closing](docs/V2_CLOSING_AND_M11_SEAL_MANUAL.md) · [Execution](docs/V2_CLOSING_EXECUTION_MANUAL.md) · [Two-checkout](docs/TWO_CHECKOUT_CI_TEST_PLAN.md)

```bash
pip install -r requirements.txt && python -m pytest -q
```

CI: `two_checkout_travel.yml` — Job 1 produces V1 evidence; Job 2 admits with V1 **not** importable.
