# BUILD_BASELINE — SWI Device Binding Demonstrator

**Date:** 2026-11-09  
**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Branch:** feature/device-binding-demonstrator-2026-11-09  
**Baseline main HEAD:** `245ec74c4943b93a1710cf1621aafdce3dac9cba`

## Existing reusable components

- `swi_v2/kernel/governing_permit.py` — authoritative permit evaluator (do not replace)
- `swi_v2/kernel/replay_guard.py`, `seal.py`, `ed25519_sig.py`, `canonical.py`
- Research: `research/camera-telemetry-authority/` (fail-closed telemetry demo)

## Integration policy

- Package under `research/device-binding-demonstrator/`
- Does **not** modify `governing_permit.py` or M11 contracts
- Capability PASS does **not** issue execution permits

```
PROVEN=NO
SEALED=NO
PRODUCTION_AUTHORIZED=NO
```
