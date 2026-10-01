# SWI Execution Integrity Boundary

**Status (this component only)**

| Property | Classification |
|----------|----------------|
| Implementation | IMPLEMENTED |
| Adversarial tests | TESTED |
| Local replay | REPLAYABLE |
| Independent remote verification | NOT_YET_VERIFIED |
| Production enforcement | NOT_PROVEN |
| Universal / regulatory safety | NOT CLAIMED |

**Does not modify:** M11 seal, foundation admission kernel, Security Maze, B1 Merkle batch contract, CRTG, or any production authorization status.

---

## Objective

Protect an execution boundary so that:

> An arriving node may communicate with SWI, but it remains quarantined until SWI verifies that its execution request is still bound to the admitted workflow, approved node, expected route, relevant policy, admission identity, and last verified execution state.

If verification fails:

```
HALT → RECORD → REVALIDATE / RETRY → ESCALATE (if persistent)
```

Retry does **not** grant authority. A failed integrity check must prevent the protected execution function from being reached.

---

## Architecture

```
incoming node/request
         │
         ▼
   ┌─────────────┐
   │ QUARANTINE  │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │ CHECK PIPE  │
   └──────┬──────┘
          │
  identity / workflow / route / input / policy / admission
  + last-execution continuity (+ optional time tolerance)
          │
   ┌──────┴──────┐
   │             │
 PASS          FAIL
   │             │
   ▼             ▼
EXECUTE        HALT
   │             │
   │          RECORD
   │             │
   │       REVALIDATE
   │             │
   │           RETRY
   │             │
   │      ┌──────┴──────┐
   │      │             │
   │     PASS          FAIL
   │      │             │
   │      ▼             ▼
   │   EXECUTE       ESCALATE
   ▼
evidence
```

Critical invariant:

> Decision layer ≠ execution enforcement.  
> `decision == HALT` is insufficient alone; the protected operation must remain unexecuted (`execution_counter == 0`).

---

## Objects

### AdmittedRoute (immutable)

```python
@dataclass(frozen=True)
class AdmittedRoute:
    workflow_id: str
    route_hash: str
    node_id: str
    input_hash: str
    policy_hash: str
    admission_hash: str
```

Incoming data is a **candidate**. It must not mutate the admitted object.

### ExecutionRecord

```python
@dataclass(frozen=True)
class ExecutionRecord:
    execution_id: str
    workflow_id: str
    node_id: str
    route_hash: str
    input_hash: str
    timestamp: float
```

### Decisions / reasons

- Decisions: `EXECUTION_ALLOWED`, `HALT`, `ESCALATE`
- Reasons: `NODE_MISMATCH`, `WORKFLOW_MISMATCH`, `ROUTE_CHANGED`, `INPUT_CHANGED`, `POLICY_CHANGED`, `ADMISSION_MISMATCH`, `NOT_ADMITTED`, `LAST_EXECUTION_MISMATCH`, `TIME_CONTINUITY_EXCEEDED`, `RETRY_LIMIT_EXCEEDED`

---

## Time tolerance (0.0008)

Configured as:

```python
time_tolerance = 0.0008
```

**Classification:** EXPERIMENTAL CONFIGURATION only.

Until the unit and semantic meaning (seconds, simulation units, permitted drift, etc.) are defined and evidenced:

- not a universal SWI standard
- not a production safety constant
- not a compliance claim

---

## Evidence object

Failures and passes produce structured evidence including expected vs received bindings, decision, `execution_allowed`, `execution_occurred`, reasons, retry/escalation state, and a SHA-256 of the canonical evidence payload.

SWI rule retained:

> HASH ≠ AUTHORITY ≠ TRUTH

---

## Demonstrated property (bounded)

A workflow admitted under a defined set of bindings cannot proceed through the **protected** execution boundary when those bindings are subsequently violated, **provided** execution is required to pass through this gate.

Library-level direct calls to the underlying operation (bypassing the gate) are outside this component’s enforcement scope. That limitation is explicit.

---

## Tests

File: `test/adversarial/test_execution_integrity.py`

Required suite (16):

1. `test_matching_route_reaches_execution_boundary`
2. `test_unapproved_node_halts`
3. `test_node_identity_mismatch_halts`
4. `test_workflow_mismatch_halts`
5. `test_route_change_halts`
6. `test_input_change_halts`
7. `test_policy_change_halts`
8. `test_admission_change_halts`
9. `test_not_admitted_halts`
10. `test_last_execution_mismatch_halts`
11. `test_time_continuity_failure_halts`
12. `test_new_information_cannot_silently_change_admitted_route`
13. `test_retry_does_not_grant_authority`
14. `test_persistent_failure_escalates`
15. `test_evidence_is_replayable_and_hashed`
16. `test_admitted_route_immutable_under_poison`

Replay (clean checkout):

```bash
git checkout <exact-sha>
python3 -m pytest -q test/adversarial/test_execution_integrity.py
```

---

## Centrepiece acceptance scenario

```
ADMITTED (W-104 / R-abc / I-1 / N-7 / P-22 / A-9)
        ↓
NEW INFORMATION (R-NEW / I-NEW)
        ↓
CHECK PIPE → HALT (ROUTE_CHANGED, INPUT_CHANGED)
        ↓
execution_counter == 0
        ↓
EVIDENCE HASH RECORDED
        ↓
REVALIDATE → FAIL → RETRY → FAIL → ESCALATE
```

Positive control:

```
ALL BINDINGS MATCH → EXECUTION_ALLOWED → execution_counter == 1
```

(Harmless demo action only.)

---

## Non-claims

This component does **not** establish:

- universal authority
- production trust
- regulatory compliance
- universal safety
- M11 / CRTG / Security Maze / B1 changes

Statuses of those artefacts remain unchanged by this addition.
