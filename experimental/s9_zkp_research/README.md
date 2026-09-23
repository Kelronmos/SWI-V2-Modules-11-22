# S9 ZKP Research — Experimental Contract

**Status:** RESEARCH ONLY  
**Implementation:** NOT IMPLEMENTED  
**Cryptographic proof system:** NOT SELECTED / NOT IMPLEMENTED  
**Production authorization:** NOT AUTHORIZED  
**Formal module seal:** NOT CLAIMED  

This lane is deliberately separate from:

- `experimental/s9_authority_chain/` (structural binding + deterministic integrity)
- PR-009 response-boundary enforcement
- Any production or seal decision

---

## Research objective

Determine whether a formally specified zero-knowledge proof construction can establish a defined predicate while limiting disclosure of the witness, **subject to the security properties and implementation assumptions of a selected proving system**, without the proof itself becoming authority or execution permission.

Privacy is **not** an unconditional claim. Any future implementation must state the exact statement, witness, public inputs, constraints, and residual disclosure assumptions of the chosen system.

---

## Hard boundaries (frozen)

\[
ZKVerify(statement, proof) = PASS
\;\not\Rightarrow\;
Authorization
\]

\[
Authorization
\;\not\Rightarrow\;
Execution
\]

\[
Escalation
\;\not\Rightarrow\;
Authorization
\]

\[
Execution
\;\Rightarrow\;
Verify(Command, Scope, Authority, Evidence, \ldots)
\]

A valid proof may establish that certain constraints were satisfied.  
It must never be treated as:

- an AuthorityGrant
- an Admission token
- an ExecutionProceedToken
- a substitute for the existing S9 structural binding

---

## Required research distinctions

Any future experiment in this lane must explicitly define:

| Concept | Question |
|---------|----------|
| **STATEMENT** | What exact predicate is being proven? |
| **WITNESS** | What remains private? |
| **PUBLIC INPUT** | What may the verifier see? |
| **CIRCUIT / CONSTRAINTS** | What arithmetic / logical constraints must hold? |
| **PROOF** | What does the prover produce? |
| **VERIFIER** | What does PASS actually establish? |
| **AUTHORITY** | What remains separately required after verification? |
| **EXECUTION** | What remains separately gated after authorization? |

---

## Proposed research tests (stubs only)

| ID | Intent |
|----|--------|
| ZK-001 | Valid constraint proof (contract) |
| ZK-002 | Invalid constraint proof must fail |
| ZK-003 | Private evidence remains undisclosed (specification) |
| ZK-004 | Wrong scope cannot satisfy the defined predicate |
| ZK-005 | Altered command invalidates the proof relation |
| ZK-006 | Altered public input invalidates the proof relation |
| ZK-007 | Valid proof cannot create an AuthorityGrant |
| ZK-008 | Valid proof cannot bypass the ExecutionGate |

Every stub currently reports:

```
STATUS: RESEARCH STUB
IMPLEMENTATION: NOT IMPLEMENTED
CRYPTOGRAPHIC PROOF: NOT IMPLEMENTED
```

---

## Relation to existing S9 authority-chain

```
S9 AUTHORITY CHAIN (current)
  structural binding
  deterministic integrity (SHA-256)
  A01–A12 tested
        │
        ▼
  future real cryptographic authentication
        │
        ▼
  independent audit

SEPARATE LANE ↓

S9 ZKP RESEARCH (this directory)
  research contracts
  threat-model notes
  public/private input definitions
  ZK-001 … ZK-008 stubs
  NO real proving system yet
```

Do not collapse these lanes.  
Do not interpret a hash commitment as a zero-knowledge proof.  
Do not interpret a research stub as cryptographic evidence.

---

## Non-claims

This directory does **not**:

- implement any SNARK, STARK, or other proving system
- select Circom, Noir, Cairo, a zkVM, or any concrete toolchain
- claim soundness, completeness, or zero-knowledge for any construction
- seal M11 or any module
- authorize production execution
- refresh evidence freshness
- weaken or replace the existing S9 ExecutionGate

---

## Doctrine

CLAIM → IMPLEMENTATION → TEST → RESULT → LIMITATION → NEXT ITERATION

Current position on that chain for this lane:

CLAIM (research objective) → **IMPLEMENTATION: NOT STARTED**

---

## Next iteration (when ready)

1. Write precise STATEMENT / WITNESS / PUBLIC INPUT definitions for one narrow SWI predicate.
2. Select a proving system against that contract (not before).
3. Implement the minimal circuit/constraint system.
4. Reify ZK-001 … ZK-008 as real tests against that system.
5. Demonstrate that a valid proof still cannot manufacture AuthorityGrant or bypass ExecutionGate.
6. Independent audit of both the proof system usage and the SWI boundary.
