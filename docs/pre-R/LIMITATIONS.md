# pre-R Limitations Register (V2)

| ID | Limitation | Status |
|----|------------|--------|
| PR-001 | Experimental slice; not sealed | OPEN |
| PR-002 | Unit suite present; re-verify tip CI after each push | OPEN |
| PR-003 | Semantic truth not in scope | STANDING |
| PR-004 | Production key custody not in scope | STANDING |
| PR-005 | UI adapter contract-only | OPEN |
| PR-006 | Network transport outside experiment | STANDING |
| PR-007 | No independent audit | OPEN |
| PR-008 | No hidden V1 return-path dependency | STANDING |
| PR-009 | **Gate fail-closed ≠ fail-safe enforcement** — caller can ignore REJECT until enforcement layer exists | **STANDING** |
| PR-010 | HALT decision constant unused by ReturnGate path (failures → REJECT) | OPEN |
| PR-011 | No automatic recovery protocol | STANDING |
| PR-012 | V1 ModuleKernel / V2 HaltedWorkflow patterns not composed into pre-R | OPEN |
