# S9 ZKP Research Contract

**Status:** RESEARCH SPECIFICATION  
**Implementation:** NOT IMPLEMENTED  
**Proving system:** NOT SELECTED  

## 1. Purpose

Define the minimal contract that any future zero-knowledge experiment in SWI must satisfy before it is allowed to interact with the S9 authority-chain or ExecutionGate.

## 2. Required elements of any experiment

### 2.1 STATEMENT
Exact predicate being proven.  
Must be written as a public claim, e.g.:

> “The private witness satisfies constraint set C with respect to public inputs P.”

### 2.2 WITNESS
Private data known only to the prover.  
Must be listed explicitly.  
Must never appear in the proof transcript or public inputs.

### 2.3 PUBLIC INPUT
Data the verifier is allowed to see.  
Includes at minimum: statement identifier, public parameters, and any values that the ExecutionGate already treats as public.

### 2.4 CONSTRAINTS
The arithmetic or logical constraints that the witness and public inputs must jointly satisfy.  
Must be fixed before any proof is generated.

### 2.5 PROOF
The object produced by the prover.  
Must be treated as opaque data until a Verifier returns PASS or FAIL.

### 2.6 VERIFIER OUTCOME
- PASS establishes only that the constraints hold for the given public inputs under the assumptions of the selected proving system.
- PASS does **not** establish authority.
- PASS does **not** establish admission.
- PASS does **not** authorize execution.

### 2.7 AUTHORITY (separate)
After a successful verification, an independent AuthorityGrant (or equivalent) is still required.  
A proof cannot manufacture an AuthorityGrant.

### 2.8 EXECUTION (separate)
Even after verification and authority, the existing ExecutionGate (or successor) remains the final control.  
A proof cannot bypass it.

## 3. Invariants that must be preserved

```
ZKVerify = PASS  ⇏  Authorization
Authorization    ⇏  Execution
Escalation       ⇏  Authorization
Execution        ⇒  Verify(Command, Scope, Authority, Evidence, …)
```

## 4. Explicit non-claims at this stage

- No concrete circuit exists.
- No proving system has been selected.
- No soundness, completeness, or zero-knowledge property has been demonstrated.
- No privacy guarantee is claimed.
- No production security is claimed.

## 5. Selection criteria for a future proving system

Any candidate must be evaluated against:

1. Ability to express the exact STATEMENT / CONSTRAINTS needed by SWI.
2. Transparent documentation of setup assumptions (trusted setup vs transparent).
3. Ability to keep the defined WITNESS private under the system’s stated security model.
4. Practical proof size and verification cost for the intended boundary.
5. Compatibility with the “proof ≠ authority ≠ execution” discipline.

Selection happens **after** the contract for a concrete predicate is written, not before.
