# Offline Build and Runner

**Status:** RESEARCH / EXPERIMENTAL  
**Production authorization:** NOT AUTHORIZED

## Purpose

Provide deterministic offline start/build entry points that log results and return explicit exit codes. Missing required controls must fail closed.

## Scripts

| Script | Role |
|--------|------|
| `scripts/start_offline.py` | Canonical offline test runner |
| `scripts/start_offline.sh` / `.bat` / `.cmd` | OS entry points |
| `scripts/build_offline.py` | Vendored-deps install + compile |
| `scripts/build_offline.sh` / `.bat` / `.cmd` | OS entry points |
| `scripts/start_background.bat` | Background start with logs |

## Exit categories

```text
0  SUCCESS
10 TEST_FAILURE
20 BUILD_FAILURE
30 ENVIRONMENT / REQUIRED DEPENDENCY FAILURE
40 INTEGRITY_FAILURE
50 AUTHORITY_FAILURE
60 UNKNOWN / UNVERIFIED
```

These codes are diagnostic/control outcomes. They are not authorization.

## Fail-closed rule

```text
REQUIRED CHECK
    -> unavailable prerequisite
    -> UNKNOWN / NOT VERIFIED
    -> FAIL-CLOSED / HALT
    -> no closure
```

```text
SKIP != VERIFIED
PASS != PROVEN
TESTED != PROVEN
PROVEN != SEALED
SEALED != PRODUCTION AUTHORIZED
```

Until `offline/wheels/` is populated, offline build returns environment failure rather than inventing success.
