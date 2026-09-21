# SWI CEK GOD'S-EYE FLOW OBSERVABILITY MANUAL

**Document ID:** SWI-CEK-GODSEYE-FLOW-OBSERVABILITY-01  
**Status:** DRAFT — ARCHITECTURE FREEZE  
**Runtime:** NOT AUTHORIZED  
**Seal:** NONE  
**M11:** SEALED / CLOSED / UNCHANGED  
**PR-009:** EXPERIMENTAL / TESTED / NOT SEALED  
**PRE-CONSEQUENCES:** SEPARATE / NOT BUILT  

## 0. Purpose

CEK provides continuous **structural observability** of a flow from origin through every node and transition to the boundary where an action could affect the real world.

> If a consequential flow cannot be observed, characterized, and traced sufficiently through CEK, that missing visibility cannot itself become authority to continue the flow.

CEK is an **observational layer**. It is **not**:

- an authorization engine  
- a replacement for ReturnGate  
- a replacement for PR-009  
- a source of authority  
- an execution engine  
- a truth oracle  
- a surveillance mechanism  
- an automatic seal mechanism  

## 1. Permanent SWI separation

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORITY ≠ BINDING ≠ EXECUTION ≠ TRUTH ≠ CONTINUITY
```

CEK sits **across** this geometry as observability — it does not own the structure.

```text
CEK: Context | Evidence | Knowledge/Constraints | Flow/Transition | Change | Trace
         │
ORIGIN → DATA → EVIDENCE → ADMISSION → AUTHORITY → BINDING
      → EXECUTION → OUTCOME → CONTINUITY → REAL-WORLD DOOR
```

## 2. “God's Eye” definition

**Metaphor only.** Not omniscience.

> CEK God's Eye = the requirement that SWI maintain structured observability of consequential flow paths wherever the architecture claims those paths are observable.

```text
God's Eye = whole-flow observability + traceability + transition awareness
          + boundary awareness + unknown detection
```

Valid outputs: VISIBLE | PARTIALLY VISIBLE | UNKNOWN | UNTRACEABLE | INVALID | HALTED  
— not invented certainty.

## 3. C / E / K freeze

| Symbol | Meaning |
|--------|---------|
| **C — Context** | Circumstances: request, state, module, source, destination, time, dependencies, transition, environment. *Where are we?* |
| **E — Evidence** | What can support a claim: integrity, receipts, hashes, tests, provenance, transition records. *What can we demonstrate?* **EVIDENCE ──X→ AUTHORITY** |
| **K — Knowledge / Constraints** | Established structure: module relationships, contracts, permitted transitions, invariants, limitations, unknowns. *What does the architecture establish?* Not a license to execute. |

## 4. Primary questions (every consequential transition)

Where did it start? What entered? What changed? Who/what touched it? Which node received it? Which edge carried it? What transformed? What evidence travelled? What authority existed/changed? What bound? What executed? What resulted? Where did it end? Did it cross the real-world door?

If a required answer is missing → **record the gap**.

## 5. Graph model

Nodes + edges + transitions. CEK observes **transitions between states**, not only isolated nodes.

Conceptual path: REQUEST → INGRESS → DATA → EVIDENCE → ADMISSION → AUTHORITY → BINDING → EXECUTION ELIGIBILITY → EXECUTION → OUTCOME → EVIDENCE → CONTINUITY → EXTERNAL EFFECT.

## 6. Vibration (technical term)

> A **vibration** is an observable change, signal, deviation, transition, propagation event, or state movement through the architecture.

Lifecycle: ORIGIN → DETECTION → CLASSIFICATION → PROPAGATION → TRANSFORMATION → DESTINATION → OUTCOME.  
Broken chain → **TRACE GAP** (explicit).

## 7. Central safety law

```text
UNOBSERVED ≠ AUTHORIZED
UNTRACED   ≠ TRUSTED
UNKNOWN    ≠ PERMITTED
```

Agent claims, node “pulling,” and representation changes do not manufacture authority.

## 8. CEK does not grant authority

```text
CEK → OBSERVATION → SWI AUTHORITY CONTRACT → DECISION
```

Forbidden: CEK creates authority.

## 9. Relation to existing surfaces

| Surface | Relation |
|---------|----------|
| ReturnGate | Admission only; CEK observes, does not replace |
| PR-009 | Enforcement path; CEK may observe; does not promote |
| M11 | Historical seal **unchanged** |
| PRE-CONSEQUENCES | Separate / not built |

**REJECT / HALT ──X→ EXECUTION** remains hard.

## 10. Unknown & frontier

UNKNOWN must not become TRUE / VALID / AUTHORIZED / SAFE / EXECUTABLE.

**Visibility frontier:** KNOWN → OBSERVABLE → TRACEABLE → CORRELATABLE → FRONTIER → UNKNOWN.  
**Frontier Sense:** identify LAST KNOWN STATE, LAST VERIFIED EDGE, FIRST UNKNOWN TRANSITION, missing evidence/authority/observation — without pretending beyond the boundary.

## 11. Interpretive layers (not authority)

```text
CEK
 ├─ COMMON SENSE → consistency / anomaly / ambiguity
 ├─ SCAR / MAGIC  → experimental pattern inspection → UNEXPLAINED (not MAGIC=TRUE)
 └─ FRONTIER SENSE → visibility boundary
        ↓
 STRUCTURED FINDING → SWI CONTRACTS (not automatic authority)
```

SCAR/MAGIC remains experimental until terminology and contract are frozen.

## 12. Real-world door

Boundary where software can produce external consequence. **No invisible door:** unmapped consequential surface → UNKNOWN EXECUTION SURFACE → block release / review architecture.

## 13. Observability ≠ surveillance

Observe structure and consequential transitions; minimize data (prefer identifiers, digests, state, transition, provenance, timestamp, scope, result). Define retention, access, privacy boundaries in later contract.

## 14. Laundering & replay

Authority/evidence laundering across nodes/agents/serialization must be detectable as attack categories.  
**REPLAY ──X→ NEW AUTHORITY.** Transformation requires revalidation of integrity.

## 15. GEO-CEK laws (001–015)

| ID | Law |
|----|-----|
| GEO-CEK-001 | Every declared consequential flow has a defined observability path |
| GEO-CEK-002 | Observable flow identifies origin |
| GEO-CEK-003 | Consequential transition has a declared edge |
| GEO-CEK-004 | Material transformations observable or marked outside boundary |
| GEO-CEK-005 | Authority has independently defined provenance |
| GEO-CEK-006 | CEK observation does not create authority |
| GEO-CEK-007 | Unknown transition is not authorized by being unknown |
| GEO-CEK-008 | No silent authority propagation through unobserved edge |
| GEO-CEK-009 | Evidence cannot become authority via representation/propagation |
| GEO-CEK-010 | Replay cannot create new authority |
| GEO-CEK-011 | No consequential external boundary outside declared architecture |
| GEO-CEK-012 | Explicitly represent visibility frontier |
| GEO-CEK-013 | Observing execution does not authorize another execution |
| GEO-CEK-014 | Findings scoped to what was observed |
| GEO-CEK-015 | CEK evidence does not automatically seal module/runtime/system |

## 16. Future adversarial categories (not yet tests)

T01–T25: hidden node/edge, forged origin, altered destination, authority/evidence/agent/node laundering, serialization, mutation, stale/expired/revoked, transform without revalidation, unknown/HALT/REJECT → execution, hidden door, direct bypass, graph drift, missing evidence/provenance, inconsistent state, false continuity.

Positive controls required for legitimate full path. Negative controls: UNKNOWN/REJECT/HALT/bad evidence/bad destination/expired/revoked/untraced → no automatic authority/execution.

## 17. Evidence classes

P0 Documented → P1 Implemented → P2 Tested → P3 Reproducible → P4 Structurally verified → P5 Independently audited.  
Do not present P0 as P2 or P2 as P5.

## 18. Architecture freeze gates (before any CEK implementation)

| Gate | Freeze |
|------|--------|
| A Terminology | C, E, K, CEK, vibration, observability, frontier, common sense, SCAR, MAGIC, frontier sense, real-world door |
| B Geometry | Node, edge, transition, state, flow, authority path, observability path |
| C Authority | CEK observes; SWI contracts authorize; binding binds; enforcement enforces; execution executes |
| D Runtime | State transitions |
| E Modules | Map every module to common substrate |

Only then: implementation order (data contract → observation → node/edge/transition/vibration → trace → provenance → frontier → interfaces → real-world mapping → module integration → adversarial → replay → audit → seal evaluation).

## 19. Common substrate

One CEK substrate; modules M12…M22 prove their own transitions through it — not separate incompatible CEK systems per module.

## 20. Final rule

> CEK is SWI's whole-flow observability geometry: it follows the detectable movement of a consequential flow from origin through nodes, edges, transformations, authority boundaries, execution boundaries and the real-world door; where that visibility breaks, SWI must not treat the missing path as authority.

```text
CEK → OBSERVE → UNDERSTAND STRUCTURE → IDENTIFY UNKNOWN → REPORT FRONTIER
                    X
                    └──→ AUTOMATIC AUTHORITY  NOT PERMITTED
```

**Programme law:** OBSERVE → TRACE → CHARACTERIZE → IDENTIFY CHANGE → AUTHORITY PROVENANCE → UNKNOWN → TEST BOUNDARY → REPLAY → AUDIT → ONLY THEN CONSIDER SEAL.

No runtime code in this document. No CEK authority. No automatic execution. No automatic seal. No reopening M11. No merging PRE-CONSEQUENCES into SWI.

**Next engineering gate:** freeze what God's Eye means → what it must see → what it must report → what it must never authorize → map every SWI node + edge → **then** implement the common substrate.
