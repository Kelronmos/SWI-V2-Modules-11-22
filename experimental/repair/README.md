# Experimental: Closed transition engine

**Status:** RESEARCH / EXPERIMENTAL  
**Implemented:** StateRegistry / TransitionRegistry / GateRegistry / attempt_transition  
**Seal:** NOT SEALED  
**Production:** NOT AUTHORIZED  
**Branch:** `experimental/privacy-domain`

## Decision semantics

```text
UNKNOWN TRANSITION              → REJECT
KNOWN TRANSITION + FAILED GATE  → BLOCK
INTEGRITY FAILURE               → QUARANTINE
KNOWN TRANSITION + ALL GATES PASS → ALLOW
```

REJECT / BLOCK / QUARANTINE → **no state mutation**.

## Hard separations

```text
STATE EXISTS ≠ TRANSITION EXISTS ≠ GATES PASS
≠ AUTHORITY EXISTS ≠ AUTHORIZATION ≠ ACTION
```

Forbidden shortcuts (must remain blocked in tests):

- TAMPERED → VERIFIED / SEALED / AUTHORIZED / ACTION
- CI_GREEN / SIGNATURE_VALID → AUTHORIZED
- TECHNICAL_VERIFICATION → HUMAN_AUTHORITY

## Privacy integration

Privacy is evaluated as a **gate** when required by the transition rule.  
It does not invent transitions.

## Primary API

See `transition_engine.py` — `attempt_transition(current, requested, context)`.

## Tests

P0 adversarial suite under `tests/experimental/` (on this branch).  
Independent evidence capture required before any promotion claim.
