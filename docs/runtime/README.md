# SWI Runtime documentation package

**Status:** Architecture and gate definitions only.  
**Runtime implementation:** NOT AUTHORIZED until Phase 3 gates G01–G13 (required scope) and Runtime Entry Gate pass.  
**M11:** Historical seal records, if any, are separate from current runtime seal — do not reopen or rewrite seal records as runtime proof.  
**Human authority (H):** UNDER_CONSTRUCTION — see `HUMAN_AUTHORITY.md`.

## Documents

| File | Role |
|------|------|
| **PHASE3_RUNTIME_CLOSURE_CONTINUATION.md** | **Primary Phase 3** — SWI-P3-85000+ (17 macro-gates) |
| RUNTIME_CLOSURE_MANUAL.md | Pre-runtime gates G00–G11 |
| RUNTIME_ENTRY_GATE.md | Explicit checklist before runtime code |
| RUNTIME_PATH.md | Path sketch |
| BINDING_CONTRACT.md | BIND-001…010 |
| DEPENDENCY_GRAPH_MODEL.md | Typed edges |
| MODULE_COMPLETION_CONTRACT.md | Per-module record |
| RUNTIME_STATE_MACHINE.md | State machine + HALT rule |
| CLOSURE_BASELINE_2026-09-24.md | Phase 0 starting envelope |
| SNYDER_COMPATIBILITY_MATRIX.md | Six Snyder rows (OPEN/PARTIAL) |
| DECISION_ENVELOPE.md | Design-only decision context |
| **HUMAN_AUTHORITY.md** | **H under construction — not a closed gate** |

## Master programme

| File | Role |
|------|------|
| `docs/LAW_TRUTH_CEK_GEO_RUNTIME.md` | CEK → Module → Binding → Runtime |
| `docs/CEK_GEOMETRY_CONTRACT.md` | CEK terminology + GEO-001…010 |

## Repository truth

| Component | Status |
|-----------|--------|
| M11 | Historical seal ≠ current runtime seal |
| M12 | **FROZEN** pending Gates A–D |
| M13–22 | **BLOCKED** |
| PR-009 / pre-R | **EXPERIMENTAL** — NOT SEALED |
| Replay | **NOT sealed** |
| PRE-CONSEQUENCES | Separate — **NOT BUILT** |
| Human authority (H) | **UNDER_CONSTRUCTION** |
| Phase 3 runtime (G14) | **NOT STARTED** |

## Standing separations

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORITY ≠ BINDING ≠ EXECUTION ≠ TRUTH ≠ CONTINUITY
TESTED ≠ SEALED
Module seal ≠ Runtime seal ≠ System release
SYSTEM_RESULT ≠ HUMAN_AUTHORIZATION
```
