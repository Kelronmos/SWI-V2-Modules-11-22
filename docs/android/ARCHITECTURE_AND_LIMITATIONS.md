# SWI Android Local Prototype — Architecture & Limitations

**Branch:** `prototype/android-local-runtime-2026-11-12`  
**Base:** `9f2a2b1baf8f24e7122b970464e2a975f6186618`  
**Status:** PROTOTYPE  
**PROVEN = NO · SEALED = NO · PRODUCTION_AUTHORIZED = NO**

## Purpose

Provide a diagnosable, recoverable local runtime skeleton that can host SWI Python components under Termux on Android 13 (ARM64), while strictly preserving the SWI governing spine and authority boundaries.

## Component inventory (this branch)

| Path | Role | Status |
|------|------|--------|
| `swi_v2/android/status.py` | Truthful service states | Implemented + unit tests |
| `swi_v2/android/runtime.py` | Supervisor skeleton | Implemented + unit tests |
| `swi_v2/android/recovery.py` | Identity retention / quarantine | Implemented + unit tests |
| `scripts/android/termux_swi_start.sh` | Termux start helper | Implemented (script) |
| `docs/android/*` | Inventory & architecture | Documentation |
| Firefly storage / encryption | — | **NOT AUTHORIZED** (see SCAR_FIREFLY_INDEX) |
| Local model / Codex handover | — | Not yet implemented on this branch |
| Dashboard UI | — | Not yet implemented on this branch |
| Full supervised service lifecycle | — | Partial (bookkeeping only) |

## Governing spine preservation

All new code:

- Calls or respects `evaluate_governing_permit` when authorization questions arise.
- Never treats biometric proof, observation, or signature as authorization.
- Emits explicit `proven=False`, `sealed=False`, `production_authorized=False` on records.
- Uses status values `UNKNOWN` / `STALE` / `FAILED` instead of inventing green results.

## What Termux can and cannot provide

| Capability | Realistic Termux level |
|------------|------------------------|
| Process supervision | Best-effort; not systemd |
| Network isolation | Application-level only |
| Encryption at rest | Possible with care; key storage in private Termux files |
| OS sandbox | Not equivalent to full Android app sandbox or hypervisor |
| 24/7 uptime | Not claimed without extended measurement |

## Firefly gate

Per `docs/SCAR_FIREFLY_INDEX.md` and `SCAR_FIREFLY_IMPLEMENTATION_AUTHORIZATION.md`:

> NO IMPLEMENTATION AUTHORIZED

Any storage layer built on this branch is labeled **prototype cache / recovery workspace** and must not be named or documented as production Firefly.

## Link to SWI-Android-Prototype

The Kotlin companion (`Kelronmos/SWI-Android-Prototype`) produces a biometric-bound signature. Integration path (future work on a separate PR):

1. Export signature + public key + payload.
2. Feed into a verification helper that produces an **observation**.
3. Human authority layer (H) must still be supplied explicitly to `evaluate_governing_permit`.
4. Signature alone never satisfies H.

## Known gaps (honest)

1. No extended runtime evidence (app open / screen-off / reboot cycles).
2. No measured resource / latency baselines yet.
3. No local AI model verification pipeline.
4. No dashboard.
5. Firefly encryption / 500 MB vault not implemented (and not authorized).
6. Sandbox is bookkeeping + quarantine only; not OS isolation.
7. Tests run in CI / local Python; not yet on device.

## Defaults

```
PROVEN=NO
SEALED=NO
PRODUCTION_AUTHORIZED=NO
```

Prototype readiness is earned by test evidence, not declared by the build process.
