# ISO Lab Repair Report

## Status

- **EVIDENCE_SCHEMA_VALIDATION** = `PASS` (unit tests)
- **SERIAL_LEDGER_INTEGRITY** = `PASS` (unit tests + active ledger chain)
- **REPLAY_CONSISTENCY** = `PARTIAL` (docs set to NOT_RUN; full kernel replay NOT_RUN)
- **CRYPTOGRAPHIC_VERIFICATION** = `PARTIAL`
- **SWI_KERNEL_TESTS** = `PARTIAL` (boundary probes only)
- **ISO_CLAUSE_COMPATIBILITY** = `NOT_ASSESSED`
- **ISO_COMPLIANCE** = `NOT_ESTABLISHED`
- **INDEPENDENT_REPLAY** = `NOT_RUN`
- **CI_STATUS** = `ADDED`
- **GITHUB_PUBLICATION** = `PARTIAL`
- **PROVEN** = `NO`
- **SEALED** = `NO`
- **AUTHORIZED** = `NO`
- **PRODUCTION_AUTHORIZED** = `NO`

## Repairs

1. Aligned proof-record schema; validate before ledger admit
2. Historical ledger preserved; duplicates marked HISTORICAL_DUPLICATE
3. New SerialAllocator + ACTIVE ledger with hash-chain checks
4. Kernel adapter uses existing governing_permit / admission / replay_guard / canonical
5. Replay documentation: NOT_RUN for kernel/ISO scopes

## Tests

```
python -m pytest SWI_ISO_Evidence_Replay_Lab_Pack/tests/test_schema_and_ledger.py -q
11 passed
```

## Limitations

- Kernel probes are smokes, not full suite
- ISO clause conformity not demonstrated
- Do not treat CI green as authorization
