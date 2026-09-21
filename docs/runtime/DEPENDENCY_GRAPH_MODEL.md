# Dependency / Authority Graph Model

**Status:** Model definition — **NOT A FROZEN GRAPH**  
**Law:** A data dependency must never silently become an authority dependency.

## Typed edges

Every edge A → B must declare one or more explicit types:

| Type | Meaning |
|------|---------|
| DATA | Payload / result flow |
| CONTROL | Sequencing / orchestration |
| AUTHORITY | Permission / scope |
| EVIDENCE | Integrity / provenance artifacts |
| IDENTITY | Principal / identity binding |
| CONTINUITY | State-continuation proof |
| EXECUTION | Right to invoke operation |

An edge that is only DATA must not be treated as AUTHORITY or EXECUTION.

## Illustrative skeleton (not authoritative)

```text
M11 ──→ M12
 │       │
 ↓       ↓
M13 ──→ M14
 …
```

Actual edges must be filled from frozen module contracts, not from registry names alone.

## Construction rules

1. Enumerate modules with completed Module Completion Contract records.  
2. For each declared dependency, assign typed edges.  
3. Reject any edge that expands authority without an explicit AUTHORITY-typed contract.  
4. Reject cycles that would manufacture authority or continuity.  
5. Freeze the graph only after independent review of types.

## Relation to binding

The dependency graph constrains **what may be requested**.  
The binding layer decides **whether a concrete connection is permitted under current authority and evidence**.  
Neither layer executes.
