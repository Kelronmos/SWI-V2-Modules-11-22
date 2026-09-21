# PRE-CONSEQUENCES Surface Separation

**Document status:** Architectural separation record  
**Date:** 2026-09-21  
**Scope:** V2 pre-R documentation and experimental boundary  
**Authority:** Documentation only — no implementation authorization

---

## Primary statement

**PRE-CONSEQUENCES is not a renamed SWI gate.**

It is not:

- ReturnGate
- standing
- authorization
- PR-009
- stronger ALLOW/DENY
- an SWI module
- an SWI dependency
- proven interoperable with the existing SWI surface

It represents a **separate architectural surface** that begins from a different computational starting condition.

That architecture is **not implemented** in this repository.

---

## Two independent surfaces

### Surface A — Existing SWI (this repository)

```text
Existing computational substrate
        ↓
Admission
        ↓
Authority
        ↓
Enforcement
        ↓
Execution
        ↓
Evidence
        ↓
Continuity
```

This is the surface currently being rebuilt and tested (ReturnGate, PR-009, M11 path, etc.).

### Surface B — PRE-CONSEQUENCES

```text
Different computational starting condition
        ↓
PRE-CONSEQUENCES
        ↓
Future architecture
```

Status of Surface B:

| Claim | State |
|-------|--------|
| Implemented in this repository | **NO** |
| SWI module | **NO** |
| SWI dependency | **NO** |
| Proven interoperable | **NO** |
| Authorized for implementation | **NO** |

---

## Explicit non-claims

Do **not** write or infer any of the following:

- SWI → PRE-CONSEQUENCES
- ReturnGate → PRE-CONSEQUENCES
- PR-009 implements PRE-CONSEQUENCES
- PRE-CONSEQUENCES is a stronger form of ReturnGate / PR-009
- standing = authorization = corrected computational condition
- any equivalence or interoperability claim between the two surfaces

The separation is **architectural**, not merely semantic.

---

## Relationship to existing experimental work

| Existing item | Classification |
|---------------|----------------|
| ReturnGate | SWI experimental (admission) |
| PR-009 / enforce / privileged_action | SWI experimental (rejection boundary enforcement) |
| docs/pre-R/* (prior to this document) | SWI experimental / docs-only |
| PRE-CONSEQUENCES | Separate architecture — not built |

Existing PR-009 and ReturnGate remain SWI experimental work.  
They are **not** re-labelled as PRE-CONSEQUENCES.

---

## Invariants preserved by this document

```text
TESTED ≠ SEALED
DATA ≠ AUTHORITY
REGISTRY ≠ IMPLEMENTATION
DOCUMENTATION ≠ PROOF OF RUNTIME BEHAVIOUR
ARCHITECTURAL SEPARATION ≠ INTEROPERABILITY
```

---

## Next action

PRE-CONSEQUENCES remains at the documentation / separation phase only.

Any future work on PRE-CONSEQUENCES requires:

1. Its own independent specification
2. Its own independent proof path
3. Explicit implementation authorization

It must not be dragged into the existing SWI ReturnGate / PR-009 / M11–M22 cycle as another gate or module.
