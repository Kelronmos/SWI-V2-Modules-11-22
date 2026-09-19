# pre-R Test Matrix (V2)

**Status:** Gate + PR-009 enforcement unit-tested · **NOT SEALED**

## Gate (fail-closed) — `test_response_boundary.py`

| Mutation | Expected | Status |
|----------|----------|--------|
| Valid response | ADMIT | TESTED |
| Integrity / destination / result mutation | REJECT | TESTED |
| Wrong request binding | REJECT | TESTED |
| Authority expansion | REJECT | TESTED |
| Missing evidence / expired / revoked / policy deny | REJECT | TESTED |
| Scope mismatch | REJECT | TESTED |
| Certificate scoped / receipt ≠ authority | structural | TESTED |
| Transform without new integrity | REJECT | TESTED |
| NaN / deterministic integrity | construction | TESTED |

## Fail-safe (PR-009) — `test_pr009_enforcement.py`

| Test | Expected | Status |
|------|----------|--------|
| REJECT → privileged_action blocked | StateTransitionError; side effect not run | **TESTED** |
| HaltedWorkflow.may_execute() == False | True | **TESTED** |
| require_executable(HaltedWorkflow) | fails | **TESTED** |
| require_executable(raw envelope) | ModuleKernelError | **TESTED** |
| attempt_recovery does not clear halt | still blocked | **TESTED** |
| REJECT → no output via privileged path | blocked | **TESTED** |
| ADMIT → privileged read | allowed | **TESTED** |

## Still out of scope

| Item | Status |
|------|--------|
| Authorized recovery protocol | NOT IMPLEMENTED |
| Callers that bypass privileged_action API | OUT OF SCOPE |
| ReturnGate returning HALT string (vs REJECT) | DEFERRED (PR-010) |
| Network/UI transport | OUT OF SCOPE |
