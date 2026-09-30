# SWI Universal HALT Error Contract

**Status:** IMPLEMENTED (common record) · TESTED (adversarial mapping) · process-wide coverage NOT_PROVEN

## Inventory (discovered sources)

| Source | Condition | Current result | Should halt? | Evidence | Execution blocked |
|--------|-----------|----------------|--------------|----------|-------------------|
| `kernel/halt.HaltRecord` | explicit halt() | HaltedWorkflow | yes | optional | yes (`may_execute=False`) |
| `kernel/enforcement.require_admitted` | HaltedWorkflow input | StateTransitionError | yes | via record | yes |
| `kernel/authority.AuthorityHalt` | missing ACTION auth | exception | yes | message | caller-dependent |
| `execution_integrity` FailureReason.* | binding mismatch | HALT/ESCALATE | yes | IntegrityEvidence | yes (supported API) |
| Module11 / FoundationAdmissionError | admit failure | exception | yes | module-specific | admit path |

## Common record

`swi_v2.kernel.halt.HaltRecord` — extended optional identity/binding fields; `execution_allowed=False` by default; `with_evidence_hash()`.

## Mapping

`ExecutionIntegrityGate.to_halt_record(CheckResult)` maps integrity HALT/ESCALATE to `HaltRecord`.

## Non-claims

- Process-wide kernel wiring of all modules: NOT_PROVEN
- Production / regulatory: NOT_CLAIMED
- HASH != AUTHORITY != TRUTH retained
