# CEK Geometry Contract

**Document ID:** CEK-GEO-001  
**Status:** Terminology / model freeze — **NOT IMPLEMENTED**  
**Date:** 2026-09-21  
**Doctrine:** Claim → Implementation → Test → Result → Limitation → Next  

## 1. Terminology freeze (no ambiguous abbreviations)

Until each term is defined below and accepted, **CEK must not appear in runtime claims**.

| Symbol | Provisional meaning (must be confirmed before implementation) |
|--------|----------------------------------------------------------------|
| **C** | *Constraint / Condition space* — the set of declared constraints under which a transition is evaluated |
| **E** | *Evidence / Event space* — structured records of what occurred (integrity-bound, not authority) |
| **K** | *Kernel / Kontrol state* — controlled runtime state subject to explicit transitions |
| **CEK** | The joint geometry of (C, E, K): constrained state-space in which SWI evaluates transitions |
| **geometry** | Formal structure of nodes, typed edges, states, and invariants — not a security percentage |
| **input** | Declared inputs to a geometric evaluation |
| **output** | Declared outputs of a geometric evaluation |
| **measurement** | Explicit function over defined inputs; must name baseline, metric, units |
| **threshold** | Named boundary on a measurement; must name action on cross |
| **decision** | BIND / REJECT / HALT / other contractually defined outcome — not implicit ALLOW |
| **authority relationship** | How (if at all) CEK output is permitted to influence AUTHORITY — default: **none** |

If any row remains ambiguous in a claim, that claim is **out of scope** until clarified.

## 2. Architectural model (not yet an engineering claim)

```text
                    AUTHORITY
                        ▲
                        │
                  ┌─────┴─────┐
                  │  BINDING  │
                  └─────┬─────┘
                        │
REQUEST → ADMISSION → EXECUTION
              │         │
              ▼         ▼
             HALT ←── FAILURE
                    │
                    ▼
                 EVIDENCE
                    │
                    ▼
                CONTINUITY
```

This becomes an engineering claim only after: formal definition + implementation + tests.

## 3. Geometric objects

### Node

```text
Node {
  id
  version
  contract
  authority_scope
  state
}
```

### Edge

```text
Edge {
  source
  destination
  transition_type   # DATA | CONTROL | AUTHORITY | EVIDENCE | IDENTITY | CONTINUITY | EXECUTION
  constraints
  authority_requirement
  evidence_requirement
}
```

### State

```text
State {
  identity
  lifecycle
  authority_context
  binding_context
  evidence_context
}
```

## 4. Edge types (mandatory)

| Type | Meaning |
|------|---------|
| DATA | Payload / result flow |
| CONTROL | Sequencing / orchestration |
| AUTHORITY | Permission / scope |
| EVIDENCE | Integrity / provenance artifacts |
| IDENTITY | Principal / identity binding |
| CONTINUITY | State-continuation proof |
| EXECUTION | Right to invoke operation |

**A DATA edge does not imply AUTHORITY or EXECUTION.**

## 5. Geometric invariants (GEO-001 … GEO-010)

| ID | Invariant |
|----|-----------|
| GEO-001 | Every runtime node has an identified contract. |
| GEO-002 | Every permitted transition has a source and destination. |
| GEO-003 | Undefined transitions are not implicitly permitted. |
| GEO-004 | A transition cannot expand authority without an explicit contract. |
| GEO-005 | Evidence cannot manufacture authority. |
| GEO-006 | Binding cannot silently execute. |
| GEO-007 | REJECT cannot reach execution through the enforced path. |
| GEO-008 | HALT cannot reach execution without an explicitly defined transition. |
| GEO-009 | Material transition mutation invalidates applicable evidence. |
| GEO-010 | Runtime state must remain consistent with its transition history. |

## 6. CEK position relative to SWI law

```text
SWI LAW
  ↓
runtime conditions
  ↓
CEK measurement (if implemented)
  ↓
defined interpretation only
```

CEK output has **only** the authority explicitly assigned by contract.  
Default: measurement informs diagnostics; it does **not** grant AUTHORITY or EXECUTION.

## 7. Thresholds (if used later)

For every threshold, freeze before use:

- name, value, unit  
- input, calculation, boundary  
- meaning, action, evidence, limitation  

Never convert a numeric threshold into an unexplained “security percentage.”

## 8. Explicit non-claims

- CEK is **not implemented** in this repository.  
- This document does **not** authorize runtime development.  
- PRE-CONSEQUENCES is **not** part of CEK geometry.  
- GEO invariants are **requirements**, not proven properties, until tested.  
