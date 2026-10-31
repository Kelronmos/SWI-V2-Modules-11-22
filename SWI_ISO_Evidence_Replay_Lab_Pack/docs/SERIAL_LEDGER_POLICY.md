# Serial Ledger Policy (repaired)

- Format: `SWI-ISO-<STANDARD-ID>-<YYYYMMDD>-<SEQ6>`
- Central SerialAllocator — monotonic global sequence
- Active ledger: evidence/serial-ledger/SERIAL_LEDGER_ACTIVE.jsonl
- Historical pre-repair ledger preserved and marked; not valid for new admission
- Append-only; previous_hash chain required
- Duplicate active serial → REJECT
