# SWI Android Local Prototype — Baseline Inventory

**Date:** 2026-11-12  
**Branch:** `prototype/android-local-runtime-2026-11-12`  
**Base commit (main):** `9f2a2b1baf8f24e7122b970464e2a975f6186618`  
**Owner:** Trusts Motion / Kelronmos  
**Environment target:** Android 13, Termux, Python, ARM64

## A. Preserve the baseline

### Repository freeze

| Repository | Default branch | HEAD SHA | Tags | Notes |
|------------|----------------|----------|------|-------|
| Kelronmos/SWI-V2-Modules-11-22 | main | `9f2a2b1baf8f24e7122b970464e2a975f6186618` | none | Primary integration target |
| Kelronmos/SWI-Android-Prototype | main | `8d7fd46ab13a6e433fbb46f73965ba5187dd5146` | none | Biometric Keystore companion only |
| Kelronmos/SWI-V1-Module-1-10 | main | (see separate inventory) | — | Foundation evidence source |
| Kelronmos/Structured-Workflow-Intelligence | main | (see separate inventory) | — | Research / architecture |
| Kelronmos/Cek | main | `a83e91f883f97a911427405624f604e1529ccc1b` | none | CEK Alignment Monitor (TypeScript) |

### Working-tree discipline

- Work exclusively on isolated branch `prototype/android-local-runtime-2026-11-12`.
- Never write directly to `main`.
- Never force-push, clean, or overwrite without review.
- Preserve every existing change and recovery artifact.

### Key status from MODULE_STATUS.md (main)

| Component | Status |
|-----------|--------|
| M11 | SEALED (historical) |
| M12 | FROZEN until Gates A–D |
| M13–22 | BLOCKED |
| Firefly | DESIGN / DEFERRED — **NO IMPLEMENTATION AUTHORIZED** |
| Replay | NOT IMPLEMENTED (ReplayGuard = partial in-memory only) |
| S9 | NOT PROVEN |
| production_authorized | false |

### Android companion status (SWI-Android-Prototype)

- BiometricPrompt + Android Keystore EC signing key (secp256r1).
- Signature payload bound to workflow, action, nonce, timestamp.
- Explicit boundary: `BIOMETRIC_AUTHENTICATED` is **not** `SWI_AUTHORIZED`.
- Does **not** yet connect signed proof to the SWI Python governing spine.
- Does **not** authorize or execute device actions.

### Firefly policy (binding)

From `docs/SCAR_FIREFLY_INDEX.md`:

> **Status:** DESIGN / DEFERRED — **NO IMPLEMENTATION AUTHORIZED**  
> Code requires AUTHORIZED decision + frozen SHAs. No `swi_v2/firefly/` until then.

Any Android/Termux storage work must respect this gate. Prototype storage layers are labeled **PROTOTYPE / NOT AUTHORIZED** and must not claim to be Firefly production implementation.

### Governing spine (must be preserved)

Required distinctions (from `swi_v2/kernel/governing_permit.py` and project rules):

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
MATCH ≠ PERMIT ≠ EXECUTE
Capability ≠ Permission
Instruction ≠ Authorization
TESTED ≠ PROVEN
PROVEN ≠ SEALED
SEALED ≠ PRODUCTION_AUTHORIZED
CI_GREEN ≠ SWI_AUTHORIZED
```

Defaults for this prototype branch:

```
PROVEN=NO
SEALED=NO
PRODUCTION_AUTHORIZED=NO
```

### Placeholders / incomplete items identified

1. No Termux startup/shutdown scripts in V2 main.
2. No supervised local service manager.
3. No Android-friendly dashboard in V2.
4. Firefly implementation explicitly unauthorized.
5. SWI-Android-Prototype does not yet feed proofs into `evaluate_governing_permit`.
6. No local model / Codex handover layer in V2.
7. No resource monitoring or recovery suite for mobile.

### Integrity note

This inventory is an observation record. It is not evidence of completeness, not a seal, and not production authorization.

---

**Next phase:** Implement bounded Python local-runtime adapters, Termux helper scripts, truthful status model, and tests on this branch only. Firefly remains design-only until separate authorization.
