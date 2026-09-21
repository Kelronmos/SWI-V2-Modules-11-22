# SWI Runtime documentation package

**Status:** Architecture and gate definitions only.  
**Runtime implementation:** NOT AUTHORIZED until Runtime-Closure G11 + Runtime Entry Gate pass.  
**M11:** SEALED (historical) — do not reopen.

## Documents

| File | Role |
|------|------|
| **RUNTIME_CLOSURE_MANUAL.md** | **Primary** — 12 closure gates G00–G11; starting position; module path M12–M22 |
| RUNTIME_PATH.md | End-to-end path sketch |
| RUNTIME_ENTRY_GATE.md | Explicit gate checklist |
| BINDING_CONTRACT.md | BIND-001…010; BIND ≠ EXECUTE |
| DEPENDENCY_GRAPH_MODEL.md | Typed edges |
| MODULE_COMPLETION_CONTRACT.md | Per-module common record |
| RUNTIME_STATE_MACHINE.md | State machine + HALT rule |

## Master programme (repo docs)

| File | Role |
|------|------|
| `docs/LAW_TRUTH_CEK_GEO_RUNTIME.md` | CEK → Module → Binding → Runtime programme |
| `docs/CEK_GEOMETRY_CONTRACT.md` | CEK terminology + GEO-001…010 |

## Repository truth (from MODULE_STATUS)

| Component | Status |
|-----------|--------|
| M11 | **SEALED** (historical) |
| M12 | **FROZEN** pending Gates A–D |
| M13–22 | **BLOCKED** |
| PR-009 / pre-R | **EXPERIMENTAL** — TESTED; **NOT SEALED** |
| Replay | **NOT sealed** |
| PRE-CONSEQUENCES | Separate — **NOT BUILT** |

## Standing separations

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORITY ≠ BINDING ≠ EXECUTION ≠ TRUTH ≠ CONTINUITY
TESTED ≠ SEALED
BINDING ≠ EXECUTION
```
