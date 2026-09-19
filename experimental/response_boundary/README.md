# Experimental response boundary (pre-R)

**Status:** EXPERIMENTAL · **NOT** a formal SWI module · **NOT SEALED** · **NOT production-authorized**

## Components

| Piece | Module | Role |
|-------|--------|------|
| RequestBinding, AuthorityScope, EvidenceCarrier | `core.py` | Contracts |
| ReturnGate | `core.py` | Fail-closed **admission** (ADMIT/REJECT) |
| enforce / AdmittedResponse / privileged_action | `enforcement.py` | **PR-009** fail-safe binding |
| HaltedWorkflow | `swi_v2.kernel.halt` | `may_execute() == False` |

## Flow

```text
envelope → ReturnGate.evaluate → ADMIT|REJECT
                ↓
            enforce()
         ┌──────┴──────┐
      ADMIT          REJECT
         ↓               ↓
 AdmittedResponse   HaltedWorkflow
 may_execute True   may_execute False
         ↓
 privileged_action / require_executable
```

## Tests

```bash
PYTHONPATH=. python -m pytest -q tests/pre_r/
```

Gate suite + PR-009/T20. See `docs/pre-R/PR009_ENFORCEMENT.md`.
