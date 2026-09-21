# SWI LAW-TRUTH — CEK Geometry → Module Completion → Binding → Runtime

**Document ID:** SWI-LAW-TRUTH-CEK-GEO-RUNTIME-8000  
**Status:** Draft for implementation — architecture & law freeze  
**Discipline:** V1 evidence discipline  
**Primary doctrine:** Claim → Implementation → Test → Result → Limitation → Next iteration  
**Core rule:** TESTED ≠ SEALED  
**Runtime rule:** DATA ≠ AUTHORITY ≠ BINDING ≠ EXECUTION  

## 0. Purpose

Establish one coherent higher-level structure for:

1. CEK geometry  
2. SWI module topology  
3. Authority boundaries  
4. Evidence boundaries  
5. Binding  
6. Runtime state  
7. Execution  
8. Continuity  
9. Replay  
10. Cross-module integration  
11. V1/V2 travel  
12. Adversarial verification  
13. Independent audit  
14. Module seals  
15. Runtime seal  

Every capability must cross the same evidence ladder:

```text
IDEA → CLAIM → DEFINED CONTRACT → IMPLEMENTATION → UNIT → NEGATIVE →
ADVERSARIAL → INTEGRATION → EVIDENCE → REPLAY → AUDIT → SEAL
```

## 1. SWI Law (LAW-001 … LAW-015) — summary

| ID | Rule |
|----|------|
| LAW-001 | No claim without scope |
| LAW-002 | Documentation does not create capability |
| LAW-003 | Test result has a scope |
| LAW-004 | Evidence is not authority |
| LAW-005 | Binding is not execution |
| LAW-006 | Authority is not execution eligibility |
| LAW-007 | REJECT does not become ALLOW through representation |
| LAW-008 | HALT is a state, not an error message |
| LAW-009 | Unknown is not ALLOW |
| LAW-010 | TESTED ≠ SEALED |
| LAW-011 | PRE-CONSEQUENCES remains separate |
| LAW-012 | V1 discipline (claim→…→next) |
| LAW-013 | Replay does not create authority |
| LAW-014 | Hashing ≠ truth / authenticity / authority |
| LAW-015 | Seal claims cannot exceed evidence |

Full expansion: `docs/pre-R/LAW_TRUTH_PHASE.md` and this document’s source programme.

## 2. Evidence ladder (non-negotiable)

```text
CLAIM
  ↓
CONTRACT
  ↓
IMPLEMENTATION
  ↓
TEST
  ↓
ADVERSARIAL TEST
  ↓
INTEGRATION
  ↓
EVIDENCE
  ↓
REPLAY
  ↓
AUDIT
  ↓
SEAL
```

## 3. Runtime path (conceptual)

```text
DATA
  ↓
ADMISSION
  ↓
AUTHORITY
  ↓
BINDING
  ↓
EXECUTION ELIGIBILITY
  ↓
EXECUTION
  ↓
EVIDENCE
  ↓
CONTINUITY
```

Hard separations:

```text
REJECT  ─────────X→ EXECUTION
HALT    ─────────X→ EXECUTION
UNKNOWN ─────────X→ implicit ALLOW
EVIDENCE ────────X→ AUTHORITY
BINDING ─────────X→ automatic EXECUTION
REPLAY  ─────────X→ new AUTHORITY
```

## 4. Related frozen documents

| Document | Role |
|----------|------|
| `docs/CEK_GEOMETRY_CONTRACT.md` | CEK terminology + GEO-001…010 |
| `docs/runtime/BINDING_CONTRACT.md` | BIND-001…010; BIND ≠ EXECUTE |
| `docs/runtime/RUNTIME_ENTRY_GATE.md` | Gate before any runtime code |
| `docs/runtime/RUNTIME_STATE_MACHINE.md` | State machine + HALT rule |
| `docs/runtime/DEPENDENCY_GRAPH_MODEL.md` | Typed edges |
| `docs/runtime/MODULE_COMPLETION_CONTRACT.md` | Per-module common record |
| `docs/pre-R/PRE_CONSEQUENCES_SURFACE_SEPARATION.md` | PRE-CONSEQUENCES outside SWI |
| `docs/pre-R/LAW_TRUTH_*` | Experimental boundary evidence |

## 5. Runtime Entry Gate (recap)

Runtime development is **AUTHORIZED** only when all of the following hold:

- [ ] Module contracts frozen  
- [ ] Dependency graph frozen  
- [ ] Authority semantics frozen  
- [ ] CEK contract frozen (this doc + CEK_GEOMETRY_CONTRACT)  
- [ ] Geometric invariants frozen  
- [ ] Binding contract frozen  
- [ ] State machine frozen  
- [ ] HALT semantics frozen  
- [ ] Evidence contract frozen  
- [ ] V1/V2 travel contract preserved  
- [ ] PRE-CONSEQUENCES separation preserved  
- [ ] M11 status reconciled (own seal criteria)  
- [ ] Existing regression green  
- [ ] Limitations recorded  

**Current status: NOT PASSED.**

## 6. First runtime release (when authorized)

Intentionally small:

1. RuntimeContext  
2. State  
3. Transition  
4. Binding  
5. ExecutionEligibility  
6. ExecutionDispatcher  
7. Evidence  
8. HALT  

Prove those before expanding orchestration.

## 7. Module completion (universal)

Every remaining module uses the same structure:

MODULE · PURPOSE · SCOPE · INPUT · OUTPUT · PRECONDITION · POSTCONDITION ·  
AUTHORITY · DEPENDENCIES · BINDING POINTS · STATE TRANSITIONS ·  
FAILURE STATES · HALT CONDITIONS · EVIDENCE · REPLAY · TESTS ·  
LIMITATIONS · SEAL CRITERIA  

Sequence: Contract → Threat model → … → Audit → Seal (own criteria only).

## 8. What this programme does **not** prove

Even after a future runtime seal, the seal must not claim:

- AI cannot fail / cannot be manipulated / is conscious  
- AI is safe in every environment  
- Bypass is impossible outside tested scope  
- Legal compliance everywhere  
- CEK proves truth  
- Evidence proves truth  
- SWI solves all AI safety  

The seal is about **defined implementation and defined verification scope**.

## 9. Execution map (high level)

| Range | Focus |
|-------|--------|
| 01–400 | Baseline / truth freeze |
| 401–800 | CEK definition |
| 801–1600 | Geometry + invariants |
| 1601–2800 | Topology, authority, evidence geometry |
| 2801–4400 | Binding contract → implementation → adversarial |
| 4401–5600 | Runtime context, state machine, execution boundary |
| 5601–6400 | Evidence, continuity, replay |
| 6401–7200 | Integration, V1/V2 |
| 7201–8000 | Audit, seal, controlled release |

## 10. SWI Law-Truth equation

```text
Nothing becomes true because we designed it.
Nothing becomes proven because it passed once.
Nothing becomes sealed until its evidence, limitations,
replay, and audit support the exact claim being sealed.
```

**Next phase is not “code runtime everywhere.”**  
Next phase is: freeze CEK geometry + freeze binding semantics + freeze runtime state transitions + map every remaining module onto those contracts — then implement the common substrate once and make each module prove its own transition through it.
