# SWI Runtime documentation package

**Status:** Architecture and gate definitions only.  
**Runtime implementation:** NOT AUTHORIZED until Phase 3 / entry gates pass.  
**Evidence freshness doctrine:** **FROZEN** — see `EVIDENCE_FRESHNESS_CONTRACT.md`.  
**Human authority (H):** UNDER_CONSTRUCTION — see `HUMAN_AUTHORITY.md`.

## Core

| File | Role |
|------|------|
| **EVIDENCE_FRESHNESS_CONTRACT.md** | **FROZEN** — TIP_BOUND ≠ HEAD_CURRENT; no tip rewrite |
| COMPLETE_CLOSURE_PROGRAMME.md | WP-01→22 gate index |
| CLOSURE_BASELINE_2026-09-24.md | Phase 0 starting envelope |
| SNYDER_COMPATIBILITY_MATRIX.md | Six Snyder rows (OPEN/PARTIAL) |
| DECISION_ENVELOPE.md | Design-only decision context |
| HUMAN_AUTHORITY.md | H under construction |
| PHASE3_RUNTIME_CLOSURE_CONTINUATION.md | Phase 3 macro-gates |
| RUNTIME_CLOSURE_MANUAL.md | Pre-runtime gates |
| RUNTIME_ENTRY_GATE.md | Checklist before runtime code |
| RUNTIME_PATH.md | Path sketch |
| BINDING_CONTRACT.md | BIND-001… |
| DEPENDENCY_GRAPH_MODEL.md | Typed edges |
| MODULE_COMPLETION_CONTRACT.md | Per-module record |
| RUNTIME_STATE_MACHINE.md | State machine + HALT |

## Standing separations

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORITY ≠ BINDING ≠ EXECUTION ≠ TRUTH ≠ CONTINUITY
TESTED ≠ SEALED ≠ PRODUCTION AUTHORIZED
AncestorPass ≠ HeadCurrent
TIP_BOUND ≠ HEAD_CURRENT
SYSTEM_RESULT ≠ HUMAN_AUTHORIZATION
```
