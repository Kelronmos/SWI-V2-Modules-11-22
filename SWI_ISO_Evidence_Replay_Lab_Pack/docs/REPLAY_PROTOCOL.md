# Replay Protocol

Scopes (must not be conflated):

- PACKAGE_STRUCTURE
- SCHEMA_VALIDATION
- LEDGER_INTEGRITY
- SWI_KERNEL_TEST
- ISO_CLAUSE_COMPATIBILITY

If no execution occurred for a scope, status is **NOT_RUN**.

`REPLAY_MATCH` is only valid when the same test_id was re-executed against the recorded commit and results match.

Package-structure checks must never be reported as kernel or ISO-clause replay.
