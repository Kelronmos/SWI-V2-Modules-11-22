# V2 Roadmap (dependency-driven)

See `docs/UPGRADE_AND_PROGRESSIVE_INTEGRATION_MANUAL.md`.

## Constitutional rule

> A readiness percentage may authorize investigation or integration preparation, but it can **never** override a failed critical dependency or integrity gate.

Advance when the required **dependency boundary** is validated — not when every repo shares the same module numbers.

## Locked direction

```text
V1 Foundation Evidence → M11 → Kernel → M12+ (sequential)
                              ↘ CRTG design (parallel)
```

Engines/adapters: their contracts only.

## Priority 2 — M11 + Kernel boundary

- invalid evidence → HALT  
- valid evidence → AdmittedInput  
- failed admission cannot reach downstream  
- then **freeze**

## Priority 3 — CRTG design (no rush)

TaskEnvelope · canonical serialization · cert profile · trust policy · key lifecycle · revocation · replay/expiry · failure codes · adversarial test plan.

## Not doing

Bulk M13–M22 · claiming authentication without CRTG · percentage overrides integrity
