# SWI New Information Regression Package

Candidate:
37e76b93978351025ef7a32fa4154126fa2ee1aa

Scope:
- Non-boundary information invalidation.
- Proposed policy hash reconciliation.
- Proposed route hash reconciliation.
- Proposed input hash reconciliation.

Observed diagnostic results:
- Non-boundary invalidation followed by execution: reproduced.
- Proposed policy change followed by execution under old admission: reproduced.

These are regression tests, not a repair.

Acceptance:
- All regression tests must pass.
- Existing suite must be rerun.
- No execution after unresolved invalidation.
- No reuse of old admission after changed route, input or policy.
- Authority authentication must be independently established.

Status: NOT_PROVEN
Production authorization: NO
Merge authorization: NO
