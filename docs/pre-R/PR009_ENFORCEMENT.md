# PR-009 — Response Rejection Enforcement

**Status:** IMPLEMENTED (experimental) · TESTED (T20 unit) · **NOT SEALED** · **NOT PRODUCTION AUTHORIZED**  
**Module id:** `pre_r_pr009`  
**Code:** `experimental/response_boundary/enforcement.py`  
**Tests:** `tests/pre_r/test_pr009_enforcement.py`

## Purpose

Prove that a `REJECT` (or non-admit) decision cannot be ignored on a privileged path.

```text
Response → ReturnGate → REJECT/HALT → HaltedWorkflow (may_execute=False)
                      → ADMIT      → AdmittedResponse (may_execute=True)
Privileged work requires AdmittedResponse via require_executable / privileged_action.
```

## Separation of duties

| Component | Responsibility |
|-----------|----------------|
| `ReturnGate` | Admission only (unchanged) |
| `enforce()` | Bind decision to token or halt |
| `HaltedWorkflow` | V2 kernel: `may_execute() == False` |
| `require_executable` | Fail-safe type/state check |
| `privileged_action` | Runs callback only after require_executable |

## T20 coverage

| Test | Result |
|------|--------|
| Valid → AdmittedResponse, may_execute True | PASS (local) |
| REJECT → privileged_action blocked | PASS |
| Halted may_execute False | PASS |
| require_executable rejects HaltedWorkflow | PASS |
| require_executable rejects raw envelope | PASS |
| attempt_recovery does not clear halt | PASS |
| REJECT → no output via privileged path | PASS |
| ADMIT → privileged read allowed | PASS |

## Limitations

- Experimental pre-R only; not a formal M-module.
- Does not wire UI/network transport.
- Does not implement authorized recovery protocol.
- Does not replace M11 seal path.
- Callers that bypass `privileged_action` / `require_executable` are out of scope.

```text
TESTED ≠ SEALED · gate REJECT alone ≠ enforcement without this layer
```
