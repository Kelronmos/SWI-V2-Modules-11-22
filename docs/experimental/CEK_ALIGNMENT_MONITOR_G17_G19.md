# G17 + G19 evidence (2026-09-27)

## G17 — Clean-checkout regression

| Field | Value |
|-------|-------|
| Branch | experimental/cek-alignment-monitor |
| Python | 3.12.3 |
| pytest | 9.0.3 |
| Platform | Linux x86_64 glibc 2.39 |

### CEK suite (after basename rename)
428 passed

### Full SWI suite (clean checkout + Stage 3/4 sources)
621 passed, 1 failed

### Pre-existing failure (also fails on main)
`tests/law/test_evidence_freshness.py::test_evidence_source_tip_reachable_from_head`
Stale source_tip not related to CEK experimental track.

### G17 findings fixed
- pytest basename collision: `tests/experimental/.../test_replay.py` vs `tests/law/test_replay.py`
- Resolution: rename experimental tests to `test_cek_*.py`

### Isolation checks
- M11 / swi_v2/module11: not modified by CEK track
- No `cek_alignment_monitor` imports under `swi_v2/`

## G19 — CI

PR #5 draft: https://github.com/Kelronmos/SWI-V2-Modules-11-22/pull/5
Combined status at tip before Stage 3/4 source commit: pending, total_count 0
(Workflows may not run on draft PRs or experimental branch — verify after full source is on branch.)

CI PASS ≠ SEAL ≠ PRODUCTION AUTHORIZATION

## Classification
RESEARCH / EXPERIMENTAL
Production: NOT AUTHORIZED
Seal: NO
M11: UNTOUCHED
Runtime: NOT INTEGRATED
