# SWI Runtime documentation package

**Status:** Architecture and gate definitions only.  
**Runtime implementation:** NOT AUTHORIZED until RUNTIME-ENTRY GATE passes.

## Documents in this directory

| File | Role |
|------|------|
| RUNTIME_PATH.md | End-to-end path from tested modules to runtime seal |
| RUNTIME_ENTRY_GATE.md | Explicit gate before any runtime code |
| BINDING_CONTRACT.md | Binding semantics + BIND-001…010 |
| DEPENDENCY_GRAPH_MODEL.md | Typed dependency edges |
| MODULE_COMPLETION_CONTRACT.md | Common per-module record template |
| RUNTIME_STATE_MACHINE.md | State machine + hard HALT rule |

## Master programme (repo root docs)

| File | Role |
|------|------|
| `docs/LAW_TRUTH_CEK_GEO_RUNTIME.md` | Master CEK → Module → Binding → Runtime programme |
| `docs/CEK_GEOMETRY_CONTRACT.md` | CEK terminology freeze + GEO-001…010 |

## Parallel tracks (after gate)

- **A** Architecture (contracts, graph, state machine)  
- **B** Binding (types, registry, validation, tests)  
- **C** Runtime (context, transitions, dispatcher)  
- **D** Evidence (receipts, chain, replay)  
- **E** Security (laundering, mutation, bypass)  
- **F** Verification (unit → cross-repo → audit)  

Tracks may develop in parallel **only after** their contracts are frozen.

## Standing separations

- PRE-CONSEQUENCES = separate architecture, not built  
- Experimental pre-R (ReturnGate / PR-009) = admission + rejection enforcement, **not** the binding layer  
- TESTED ≠ SEALED  
- Binding ≠ Execution  
- DATA ≠ AUTHORITY ≠ BINDING ≠ EXECUTION  
