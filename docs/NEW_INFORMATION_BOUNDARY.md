# New-information evidence boundary

**Status:** IMPLEMENTED + TESTED on `ExecutionIntegrityGate` supported API  
**Not:** process-wide V2 kernel wiring, production enforcement, universal safety

## Runtime sequence

```
ACTION REQUEST
      ↓
KNOWN EVIDENCE / ADMITTED BINDINGS
      ↓
VALIDATION (check pipe)
      ↓
NEW INFORMATION?
      ↓
YES → affects evidence boundary sufficiency?
      ↓
YES → INVALIDATE prior decision
      ↓
Decision.UNKNOWN / NodeState.PAUSED
      ↓
REQUEST human authority bound to exact workflow + action
      ↓
validate_human_authority → ValidatedAuthority
      ↓
recheck(...)
      ↓
PASS → EXECUTION_ALLOWED (only if all bindings match)
FAIL → HALT
UNKNOWN (missing/invalid authority) → no execution
```

## Rules

- **Human “yes” is not automatic override.** Affirmative text alone does not authorize execution.
- Authority must be **validated**, **bound** to workflow_id + action_id, then **re-evaluated**.
- **Prior PASS does not survive** boundary-changing new information.
- **HASH ≠ AUTHORITY ≠ TRUTH**

## Demonstrated scope

Library/demo gate (`swi_v2/execution_integrity.py`). Real V2 module execution paths are **not** proven to force this gate.
