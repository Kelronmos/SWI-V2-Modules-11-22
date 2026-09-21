# pre-R Limitations Register (V2)

**Last diagnostic:** 2026-09-21 (V1 export repair + LAW-TRUTH evidence)

| ID | Limitation | Status |
|----|------------|--------|
| PR-001 | Experimental slice; not sealed | OPEN |
| PR-002 | Re-verify tip CI after each push (matrix 3.10–3.12) | OPEN |
| PR-003 | Semantic truth not in scope | STANDING |
| PR-004 | Production key custody not in scope | STANDING |
| PR-005 | UI adapter contract-only | OPEN |
| PR-006 | Network transport outside experiment | STANDING |
| PR-007 | No independent audit | OPEN |
| PR-008 | No hidden V1 return-path dependency | STANDING |
| PR-009 | Enforcement API path tested (Level 3). Process-wide / structural bypass resistance (Level 4–5) **not proven** | **PARTIAL** |
| PR-010 | ReturnGate failures return REJECT (not HALT string); enforce maps to HaltedWorkflow | **ACCEPTED** |
| PR-011 | No automatic recovery protocol | STANDING |
| PR-012 | Full V1 ModuleKernel composition into pre-R not required | OPEN |
| PR-013 | Distributed multi-agent / NATS stack = design only (`docs/design/`) | STANDING |
| PR-014 | PRE-CONSEQUENCES is a separate architecture and is **not implemented** in this repository | **STANDING** |
| PR-015 | V1 `export_travel_evidence.py` required admission= | **RESOLVED** (V1 `c25467c`) |

## Current proof boundary (PR-009)

```text
Proven:
  Within the enforced experimental API path
  (enforce → require_executable / privileged_action)
  a REJECT/HALT state cannot reach privileged execution.

Unproven:
  process-wide bypass resistance
  arbitrary alternate execution paths
  runtime monkey-patching / direct mutation of kernel objects
  complete structural coverage (Level 4 / Level 5)
```

## Two-checkout

Live V1 export → V2 `admit_foundation_input` verified after V1 fix.
CI workflow `.github/workflows/two_checkout_travel.yml` is the authoritative path.
