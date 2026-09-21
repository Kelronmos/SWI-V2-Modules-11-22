# SWI RUNTIME-CLOSURE MANUAL

**Claim → Contract → Implementation → Test → Evidence → Replay → Audit → Seal → Runtime**

**Status:** Programme definition — architecture & gates only  
**Date:** 2026-09-21  
**Doctrine:** V1 evidence discipline  

## Governing law

```text
NO CLAIM WITHOUT IMPLEMENTATION
NO BEHAVIOURAL CLAIM WITHOUT TEST
NO SECURITY CLAIM WITHOUT ADVERSARIAL TEST
NO REPRODUCIBILITY CLAIM WITHOUT REPLAY
NO CROSS-BOUNDARY CLAIM WITHOUT CROSS-BOUNDARY TEST
NO SEAL WITHOUT A DEFINED SEAL CONTRACT
NO RUNTIME AUTHORITY FROM DOCUMENTATION ALONE
```

**Permanent geometry:**

```text
DATA ≠ EVIDENCE
EVIDENCE ≠ ADMISSION
ADMISSION ≠ AUTHORITY
AUTHORITY ≠ BINDING
BINDING ≠ EXECUTION
EXECUTION ≠ TRUTH
TRUTH ≠ CONTINUITY
```

---

## 1. Current starting position (repository truth)

| Surface | Current state |
|---------|----------------|
| **M11** | **SEALED** (historical) — tip `1d6d7dc…` · CI `35253244912` |
| M11 seal record | Historical / frozen — does **not** claim CRTG, production keys, factual truth, or M12 complete |
| V1→V2 travel | Boundary proven under seal conditions |
| ReturnGate | Tested (experimental pre-R) |
| PR-009 | Implemented / tested experimentally — **NOT SEALED** |
| Replay | **NOT sealed** (ReplayGuard = partial in-memory only) |
| CRTG | **NOT implemented** |
| Production key management | **NOT implemented** |
| Firefly | Design / deferred — **NO IMPLEMENTATION AUTHORIZED** |
| **M12** | **FROZEN** pending Gates A–D |
| **M13–22** | **BLOCKED** |
| PRE-CONSEQUENCES | Separate architecture — **NOT BUILT** |

### Rule

> **Do not reopen M11 to solve problems that belong after M11.**

M11 is the sealed foundation. Remaining work closes the runtime architecture **around** it.

---

## 2. The complete closure stack (12 gates)

```text
G00  TRUTH / BASELINE
 ↓
G01  TERMINOLOGY
 ↓
G02  GEOMETRY
 ↓
G03  CONTRACTS
 ↓
G04  ADMISSION
 ↓
G05  AUTHORITY
 ↓
G06  BINDING
 ↓
G07  EXECUTION
 ↓
G08  EVIDENCE
 ↓
G09  CONTINUITY / REPLAY
 ↓
G10  CROSS-MODULE RUNTIME
 ↓
G11  AUDIT / RELEASE
 ↓
RUNTIME DEVELOPMENT
```

Only after **G11** does the programme move from module development to runtime development.

---

## G00 — Truth / baseline freeze

Prevent the runtime architecture from being built on an incorrect description of the repository.

Record: HEAD, branch, working tree, Python, pytest, dependencies, V1 SHA, V2 SHA, M11 seal SHA, M11 CI run, module status, blocked modules, experimental surfaces, design-only surfaces, tests, CI, scripts, limitations.

**Closure:** G00 = CLOSED only if the repository can be reconstructed from the recorded baseline.

---

## G01 — Terminology lock

Canonical vocabulary (must not remain mere names):

Evidence · Admission · Context · Constraint · Authority · Permission ·  
DecisionCandidate · EnforcedDecision · ExecutionEligibility · Execution ·  
Outcome · Receipt · Continuity · Recovery · Closure · HALT · REJECT  

For every term record: definition, input, output, authority relationship, may execute?, may mutate?, may bind?, may authorize?, may create evidence?, seal status.

| Object | Can execute? | Can authorize? |
|--------|--------------|----------------|
| Evidence | No | No |
| Admission | No | No |
| Authority | No | Yes, within defined scope |
| Binding | No | No |
| EnforcedDecision | No* | No |
| Execution eligibility | No | No |
| Execution capability | Yes | No |
| Receipt | No | No |
| Continuity state | No | No |

\* Distinction must be explicit in the implementation contract.

---

## G02 — SWI geometry

Constrained directed graph: nodes + permitted transitions. An edge is not valid merely because code can call it.

Every edge requires a predicate (source_state, destination_state, required_evidence, required_authority, required_context, required_constraints, expiration, revocation, transformation_rule).

**Central invariants:**

```text
NO VALID EDGE WITHOUT VALID PRECONDITIONS
REJECTED STATE  ──X──> EXECUTION
HALTED STATE    ──X──> EXECUTION
EXPIRED STATE   ──X──> EXECUTION
REVOKED STATE   ──X──> EXECUTION
UNRESOLVED AUTHORITY ──X──> EXECUTION
```

See also: `docs/CEK_GEOMETRY_CONTRACT.md`, `docs/runtime/DEPENDENCY_GRAPH_MODEL.md`.

---

## G03 — Contracts before code

For each remaining module: Claim → Input/Output schema → Allowed/Forbidden transitions → Authority/Evidence requirements → Failure behaviour → Replay requirements → Seal criteria.

**Progression:**

```text
M12 CONTRACT → IMPLEMENTATION → TEST → AUDIT → SEAL → M13 CONTRACT
```

Not: M12–22 coding sprint.

Repository rule: M12 implementation frozen pending Gates A–D; M13–22 blocked.

---

## G04 — Admission closure

M11 already provides the admission foundation (AdmittedInput only; envelope/dict rejected).

Required matrix includes: valid → ADMIT; missing/wrong schema, bad integrity, tampered field, missing verification, expired, unknown version, extra dangerous field, wrong producer/destination, malformed encoding, NaN, infinity, wrong type → REJECT.

**Invariant:** REJECT → no executable object.

---

## G05 — Authority closure

Authority must be explicit (principal, actions, resources, destinations, time bounds, authority_id). Containment: requested ⊆ granted.

**Most important:** Evidence, receipt, binding, and execution **cannot enlarge authority**.

---

## G06 — Binding closure

Binding answers what request, for whom, against what resource, at what destination, under what authority/policy/period, with what evidence.

Binding is **pure validation** → BindingDecision. It must **not execute**.

**Invariant:** BINDING ≠ EXECUTION.

See: `docs/runtime/BINDING_CONTRACT.md` (BIND-001…010).

---

## G07 — Execution closure

Execution requires a specific executable capability. Never allow execute(raw_request | raw_envelope | evidence | receipt | binding_request).

PR-009 experimental enforcement is a useful predecessor; it is **not** automatically promoted to production because T20 passes. Repository records PR-009 as tested but **not sealed**.

---

## G08 — Evidence closure

Every material transition needs a structured evidence record.  
HASH ≠ TRUTH · HASH ≠ AUTHORITY · HASH ≠ AUTHENTICITY.  
M11 seal explicitly preserves this limitation.

---

## G09 — Continuity / replay closure

Replay is **not sealed**. ReplayGuard is partial/in-memory only.

Required direction: same inputs + version + configuration + declared conditions → same decision; mutations → differ or reject.

State machine: RECEIVED → ADMITTED → AUTHORIZED → BOUND → EXECUTION_READY → EXECUTING → COMPLETED → EVIDENCED → CONTINUING, with explicit failure branches. **No silent jumps** (e.g. RECEIVED → EXECUTING, REJECTED → EXECUTING, EVIDENCE → AUTHORIZED).

---

## G10 — Cross-module runtime

Process M12–M22 using the **same lifecycle**, one module at a time:

| Module | Focus |
|--------|--------|
| M12 | Evidence normalization, canonicalization, determinism |
| M13 | Context binding |
| M14 | Constraint resolution (never → execution) |
| M15 | Authority & permission (UNRESOLVED ≠ ALLOW) |
| M16 | Decision preparation (DecisionCandidate ≠ EnforcedDecision) |
| M17 | Decision enforcement |
| M18 | Execution control (hard boundary) |
| M19 | Outcome verification (INCONCLUSIVE ≠ success) |
| M20 | Evidence & receipt (Receipt ≠ Authority) |
| M21 | Continuity & recovery (no automatic authority inheritance) |
| M22 | V2 closure record from full evidence chain |

---

## G11 — Audit / release

Independent audit of contracts, code, tests, evidence, replay, limitations. Seal only where a defined seal contract exists and is fully satisfied.

---

## 3. Universal test matrix (every module)

T01–T30: happy path, missing/malformed/wrong type/identity/authority, expansion, expiry, revocation, destination/resource/action, policy denial/unresolved, evidence missing/mutation, integrity, replay, serialization, raw-object, mutation, state-transition bypass, exception, timeout, unexpected field, NaN/infinity, nondeterminism, cross-module misuse.

Execution-control modules additionally T31–T40: rejected/halted/expired/revoked/wrong/stale/mutated capability → execution; alternate API; direct callback; serialization laundering → execution. **All must fail.**

---

## 4. Final runtime gate (before genuine runtime development)

All must be green:

- [ ] Baseline frozen  
- [ ] Terminology frozen  
- [ ] SWI geometry frozen  
- [ ] Module contracts frozen  
- [ ] Admission proven  
- [ ] Authority boundaries proven  
- [ ] Binding proven  
- [ ] Execution boundary proven  
- [ ] Evidence model proven  
- [ ] Replay implemented/proven to required scope  
- [ ] Continuity transitions proven  
- [ ] Recovery rules proven  
- [ ] Cross-module transitions proven  
- [ ] Cross-repository travel proven  
- [ ] Python matrix green  
- [ ] Adversarial matrix green  
- [ ] Static execution-path review complete  
- [ ] Evidence manifests complete  
- [ ] Reproduction scripts complete  
- [ ] Limitations recorded  
- [ ] Independent audit complete  
- [ ] Each required module has its own seal criteria  
- [ ] Required seals recorded  
- [ ] Runtime authority explicitly defined  
- [ ] Production key/CRTG decision explicitly documented  
- [ ] No experimental surface silently promoted  

Then—and only then:

```text
CONTROLLED MODULE DEVELOPMENT
              ↓
        RUNTIME DEVELOPMENT
```

---

## 5. Final closure order

1. Freeze truth  
2. Freeze terminology  
3. Freeze geometry  
4. Freeze contracts  
5. Close M12 … M22 (one lifecycle each)  
6. Close replay  
7. Close cross-module runtime  
8. Close cross-repository boundary  
9. Close adversarial execution paths  
10. Close evidence/replay package  
11. Independent audit  
12. Record required seals  
13. Runtime-development gate  
14. Begin controlled runtime implementation  

**Key distinction:** M11 is already sealed; the runtime stack above it is not. Experimental pre-R/PR-009 must not be mistaken for production runtime authority.

```text
CLOSE THE CONTRACTS
→ PROVE THE TRANSITIONS
→ PROVE THE FAIL-CLOSED BOUNDARIES
→ PROVE REPLAY
→ PROVE THE MODULE GRAPH
→ AUDIT
→ SEAL WHAT HAS A SEAL CONTRACT
→ THEN START RUNTIME
```
