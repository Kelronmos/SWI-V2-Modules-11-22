# pre-R: Test coverage — fail-closed vs fail-safe

**Suites:** `test_response_boundary.py` + `test_pr009_enforcement.py`  
**Status:** EXPERIMENTAL · NOT SEALED

## Precise claim

> Within the experimental API (`enforce` / `privileged_action` / `require_executable`), REJECT cannot be used to run privileged work.  
> Callers that never use this API are out of scope. Not sealed.

## Not established

| Claim | Status |
|-------|--------|
| Process-wide / OS enforcement | No |
| SEALED / production | No |
| Authorized recovery | No |
| Multi-agent distributed SWI | Design only |
