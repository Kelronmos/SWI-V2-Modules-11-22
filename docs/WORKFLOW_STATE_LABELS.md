# SWI Workflow-State Labels

**Purpose:** Evidence-first workflow states — **not** scores, priorities, or security grades.

```text
Blue   = waiting (do not pretend this happened yet)
Orange/Yellow/White = demonstrated or recorded
Red/Black = boundary blocks progression
```

## Labels

| Label | Meaning |
|-------|---------|
| `AWAITING_EXECUTION` | Defined and ready; execution has not started |
| `AWAITING_HUMAN` | Human decision/authority required |
| `AWAITING_COMMAND` | Prerequisites ready; waiting for authorized command |
| `READY` | Prerequisites verified; may begin when authorized |
| `EXECUTED` | Requested operation was performed |
| `TESTED` | Tests run and results recorded |
| `EVIDENCE_RECORDED` | Evidence artifact linked to exact state/SHA |
| `CI_VERIFIED` | CI independently verified relevant commit/workflow |
| `PIPE_SEALED` | Workflow boundary sealed under documented seal contract only |
| `HALTED` | Intentionally stopped (boundary/condition/authority) |
| `NOT_AUTHORIZED` | Explicitly outside current authority |
| `NOT_PROVEN` | Claim/property not sufficiently demonstrated |

## Progression (example)

```text
AWAITING_EXECUTION
  → (human / authorized command)
EXECUTED
  → tests
TESTED
  → evidence capture
EVIDENCE_RECORDED
  → independent CI / replay
CI_VERIFIED
  → documented seal authority
PIPE_SEALED
```

## Hard inequalities

```text
PIPE_SEALED  ≠  AUTHORIZED
PIPE_SEALED  ≠  PRODUCTION
TESTED       ≠  CI_VERIFIED
CI_VERIFIED  ≠  PIPE_SEALED
NOT_PROVEN   must not be upgraded by inference
```

## Machine-readable

See `docs/workflow_state_registry.json`.

Status vocabulary is closed: only labels defined above (and explicit `NOT_APPLICABLE` where needed).
