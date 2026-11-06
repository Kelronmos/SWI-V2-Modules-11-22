# Camera Telemetry Authority Research Harness

Isolated research package for signed sensor telemetry gating under SWI authority rules.

**Scope (hard limits)**
- Simulated protected action only
- No physical hardware or live sensor connected
- Does not modify core SWI V2 execution paths
- Does not claim PROVEN / SEALED / PRODUCTION_AUTHORIZED

**Results (2026-11-04)**
- 7/7 tests PASS
- Cases cover: fresh signed telemetry, camera-only observation, mathematical explanation, stale telemetry, wrong identity, tampered signature, identical replay

See `evidence/test_run.json` and `evidence/TEST_REPORT.md`.

**Import**
See `REPO_IMPORT.md`. Place under `research/camera-telemetry-authority/` on a research branch only.
