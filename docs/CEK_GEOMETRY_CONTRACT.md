# CEK Geometry Contract

**Document ID:** CEK-GEO-001  
**Status:** Terminology / model freeze — **NOT IMPLEMENTED**  
**Date:** 2026-09-21  
**Cross-ref:** `docs/CEK_GODSEYE_FLOW_OBSERVABILITY.md` (God's-Eye flow observability)  

## 1. Terminology freeze

| Symbol | Meaning |
|--------|---------|
| **C** | *Context* — circumstances of a flow (request, state, module, source, destination, time, dependencies) |
| **E** | *Evidence* — what can support a claim (integrity, receipts, hashes, tests, provenance). **Not authority.** |
| **K** | *Knowledge / Constraints* — established structure (contracts, permitted transitions, invariants, limitations, unknowns) |
| **CEK** | Joint observability geometry of (C, E, K) over consequential flows |
| **geometry** | Nodes, typed edges, states, invariants — not a security percentage |
| **God's Eye** | Whole-flow observability requirement where claimed — **not omniscience** |
| **vibration** | Observable change / transition / propagation through the architecture |
| **frontier** | Boundary between demonstrated visibility and unknown |
| **real-world door** | Boundary where software can produce external consequence |

If any term remains ambiguous in a claim, that claim is **out of scope** until clarified.

## 2. Architectural placement

```text
CEK observes (does not own):

AUTHORITY ▲
          │
    ┌─────┴─────┐
    │  BINDING  │
    └─────┬─────┘
REQUEST → ADMISSION → EXECUTION → EVIDENCE → CONTINUITY → REAL-WORLD DOOR
              │            │
             HALT ←──── FAILURE
```

## 3. Geometric objects

**Node:** id, version, contract, authority_scope, state, observability_status  
**Edge:** source, destination, transition_type (DATA|CONTROL|AUTHORITY|EVIDENCE|IDENTITY|CONTINUITY|EXECUTION), constraints, authority_requirement, evidence_requirement  
**State:** identity, lifecycle, authority_context, binding_context, evidence_context  

DATA edge ≠ AUTHORITY or EXECUTION.

## 4. Invariants

### GEO-001 … GEO-010 (structure)

| ID | Invariant |
|----|-----------|
| GEO-001 | Every runtime node has an identified contract |
| GEO-002 | Every permitted transition has source and destination |
| GEO-003 | Undefined transitions are not implicitly permitted |
| GEO-004 | Transition cannot expand authority without explicit contract |
| GEO-005 | Evidence cannot manufacture authority |
| GEO-006 | Binding cannot silently execute |
| GEO-007 | REJECT cannot reach execution through enforced path |
| GEO-008 | HALT cannot reach execution without explicit transition |
| GEO-009 | Material transition mutation invalidates applicable evidence |
| GEO-010 | Runtime state consistent with transition history |

### GEO-CEK-001 … GEO-CEK-015 (observability)

See full list in `CEK_GODSEYE_FLOW_OBSERVABILITY.md` §15. Core:

- Observation does not create authority  
- Unknown ≠ authorized  
- No silent propagation through unobserved edge  
- No evidence/replay laundering into authority  
- Explicit visibility frontier  
- Observation does not seal  

## 5. CEK position

```text
SWI LAW → runtime conditions → CEK measurement (if implemented) → defined interpretation only
```

Default: measurement informs diagnostics; does **not** grant AUTHORITY or EXECUTION.

## 6. Explicit non-claims

- CEK is **not implemented**  
- This document does **not** authorize runtime development  
- PRE-CONSEQUENCES is **not** part of CEK  
- GEO / GEO-CEK invariants are **requirements**, not proven properties, until tested  
- God's Eye ≠ omniscience  
