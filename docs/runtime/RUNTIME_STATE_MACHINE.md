# Runtime State Machine (specification only)

**Status:** Conceptual — **NOT IMPLEMENTED**

## Happy path

```text
RECEIVED
   ↓
ADMITTED
   ↓
AUTHORIZED
   ↓
BOUND
   ↓
EXECUTION_READY
   ↓
EXECUTING
   ↓
COMPLETED
   ↓
EVIDENCED
   ↓
CONTINUING
```

## Failure / termination paths

```text
RECEIVED   ──→ REJECTED
ADMITTED   ──→ HALTED
AUTHORIZED ──→ HALTED
BOUND      ──→ INVALIDATED
EXECUTING  ──→ FAILED
CONTINUING ──→ HALTED
```

## Hard rule

```text
HALTED
  ✗
  ↓
EXECUTING
```

unless a **new, explicitly authorized** transition exists.  
Representation change alone must never restore executability (aligned with LAW-006 / LAW-007 / BIND-005 / BIND-006).

## Transition evidence (future)

Each material transition should eventually emit structured evidence:

- request_id, workflow_id, module  
- previous_state, new_state  
- authority_reference, binding_reference  
- input_digest, output_digest  
- timestamp, runtime_revision  

Replay reproduces a historical context; it does **not** automatically authorize a new execution (LAW-014).
