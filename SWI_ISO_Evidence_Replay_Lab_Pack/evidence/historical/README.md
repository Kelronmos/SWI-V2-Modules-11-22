# Historical serial ledger

Pre-repair ledger entries contained **duplicate serial numbers**.

Those entries are preserved for audit and marked:

- `HISTORICAL_DUPLICATE`
- `NOT_VALID_FOR_NEW_ADMISSION`

They must not be used for new evidence admission.

Active ledger (post-repair): `../serial-ledger/SERIAL_LEDGER_ACTIVE.jsonl` (created by allocator/ledger runtime).
