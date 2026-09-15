# V2 Kernel Specification

**STATUS:** IMPLEMENTED (minimal) · TESTED · not production-sealed

Enforcement boundary beneath Modules 11–22. Not a numbered module.

| Responsibility | Status |
|----------------|--------|
| Foundation admission API | IMPLEMENTED |
| AdmittedInput type | IMPLEMENTED |
| Fail-closed raw rejection | IMPLEMENTED |
| require_admitted | IMPLEMENTED |
| HaltRecord / HaltedWorkflow | IMPLEMENTED (minimal) |
| Full state machine | PROPOSED |
| Per-module kernel wrap | DESIGN PENDING |

HALTED → execution attempt → MUST FAIL. No trust-by-flag.
