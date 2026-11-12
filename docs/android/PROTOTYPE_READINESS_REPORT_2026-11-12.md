# SWI Android Local Prototype — Readiness Report

**Date:** 2026-11-12  
**Branch:** `prototype/android-local-runtime-2026-11-12`  
**Base SHA:** `9f2a2b1baf8f24e7122b970464e2a975f6186618`  
**Report commit:** (this file’s commit)

## Executive summary

A bounded local-runtime foundation has been added on an isolated branch:

- Truthful status model (no green-from-missing-evidence)
- Supervisor skeleton with identity and checkpoints
- Recovery suite that retains object identity when content is missing
- Termux startup helper
- Unit tests for the above
- Architecture and limitation documentation

**This is not a complete prototype readiness claim.** Extended device tests, Firefly, dashboard, local model handover, and full supervised lifecycle remain open.

## Implemented vs required (mission mapping)

| Mission area | Status on this branch |
|--------------|----------------------|
| A. Preserve baseline | Done (inventory + isolated branch) |
| B. Preserve governing spine | Preserved; no competing engine |
| C. Persistent Android runtime | Partial (supervisor + Termux start) |
| D. Codex / local AI handover | Not implemented |
| E. Firefly Memory Vault | **NOT AUTHORIZED** — not implemented |
| F. Firefly Sandbox | Bookkeeping / quarantine only |
| G. Recovery suite | Skeleton implemented + tests |
| H. Resource / performance | Not measured |
| I. Dashboard | Not implemented |
| J. Testing | Unit tests added; device tests pending |
| K. Evidence & delivery | This report + architecture docs |

## Test evidence

Unit tests: `test/test_android_status.py`

- missing evidence → UNKNOWN
- RUNNING without evidence → not OK
- STALE conversion only for RUNNING
- recovery retains identity on MISSING
- hash mismatch → CORRUPT + quarantine attempt
- supervisor checkpoint + identity non-claims

**CI / device execution of these tests is not yet recorded in this report.** Treat as IMPLEMENTATION + LOCAL UNIT TEST CANDIDATE until CI evidence is attached.

## Explicit non-claims

```
TESTED (unit, local) ≠ PROVEN
PROVEN ≠ SEALED
SEALED ≠ PRODUCTION_AUTHORIZED
CI_GREEN ≠ SWI_AUTHORIZED
BIOMETRIC_AUTHENTICATED ≠ SWI_AUTHORIZED
SIGNATURE ≠ AUTHORIZATION
OBSERVATION ≠ AUTHORITY
```

Defaults remain:

```
PROVEN=NO
SEALED=NO
PRODUCTION_AUTHORIZED=NO
```

## Blockers requiring human / external steps

1. Firefly implementation authorization decision (currently closed).
2. On-device Termux test run with evidence capture (app open, screen off, reboot).
3. Resource and latency measurements on target hardware.
4. Integration of SWI-Android-Prototype signatures into an observation path that still requires explicit H layer.
5. Independent review before any merge to main.

## Resume checkpoint for next session

- Branch: `prototype/android-local-runtime-2026-11-12`
- Next safe work: (1) wire CI job for `test/test_android_status.py`, (2) Termux install notes, (3) observation bridge from Android Keystore signature → status record, (4) resource probe module.
- Do not implement `sw` package until authorization record exists.

## Provenance

All changes on this branch descend from main `9f2a2b1baf8f24e7122b970464e2a975f6186618`.
No force-push. No main modification.
