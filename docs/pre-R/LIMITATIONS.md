# pre-R Limitations Register (V2)

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
| PR-009 | Enforcement API tested; **bypass of API** still possible for undisciplined callers | **PARTIAL** |
| PR-010 | ReturnGate failures return REJECT (not HALT string); enforce maps to HaltedWorkflow | **ACCEPTED** |
| PR-011 | No automatic recovery protocol | STANDING |
| PR-012 | Full V1 ModuleKernel composition into pre-R not required | OPEN |
| PR-013 | Distributed multi-agent / NATS stack = design only (`docs/design/`) | STANDING |
