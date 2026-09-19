# Regression Record — 2026-09-19

**Purpose:** Full local regression after PR-009 / pre-R doc sync.  
Does **not** alter M11 seal by itself.

## Commits checked out

| Repo | Tip SHA (short) |
|------|-----------------|
| V2 | `cca2669` (run start) |
| V1 | `32edfb5` |

## Results

| Suite | Command | Result |
|-------|---------|--------|
| V2 + pre-R | `PYTHONPATH=. python3 -m pytest -q tests/pre_r/ test/` | **134 passed** |
| V1 | `PYTHONPATH=. python3 -m pytest -q` | **190 passed** |

## PRE-R / PR-009

| Area | State |
|------|--------|
| ReturnGate fail-closed | TESTED |
| PR-009 enforce / T20 | TESTED (API) |
| Caller bypass outside API | OUT OF SCOPE |
| Automatic recovery | NOT IMPLEMENTED |
| PRE-R sealed | **NO** |

## M11

| Area | State |
|------|--------|
| Seal record | **SEALED** — `docs/M11_SEAL_RECORD.md` |
| Frozen V2 / V1 | `1d6d7dc…` / `e0c6a521…` |
| CI run | `35253244912` (#50) success |
| Tip pre-R work | Does not unseal M11 without new audit |

## Two-checkout

Authoritative travel proof remains the GitHub Actions run cited in `M11_SEAL_RECORD.md`.

## Next

```text
Registry ✓ · PR-009 ✓ · local V1/V2 regression ✓
  → M11 remains SEALED (existing record)
  → M12 only under Gates A–D
```
