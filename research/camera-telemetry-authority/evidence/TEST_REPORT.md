# Camera Telemetry Authority — Test Report

**Scope:** isolated research harness; simulated protected action only; no physical hardware.

**Local rerun (2026-11-06 recovery):** 7 passed.

| ID | Case | Expected |
|----|------|----------|
| T01 | fresh signed sensor telemetry | PASS |
| T02 | camera-only observation | UNKNOWN / no execution |
| T03 | mathematical explanation only | UNKNOWN / no execution |
| T04 | stale sensor telemetry | HALT |
| T05 | wrong sensor identity / key | HALT |
| T06 | tampered telemetry signature | HALT |
| T07 | identical input replay | same decision and evidence hash |

Observation ≠ authorization. PRODUCTION_AUTHORIZED=NO.
