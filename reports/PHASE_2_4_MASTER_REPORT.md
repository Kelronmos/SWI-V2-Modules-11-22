# Phase 2–4 Master Report

**Branch:** `repair/iso-evidence-replay-integrity`  
**Baseline remote tip before local commit:** `15312ac425cba5e2c08b8719a2967b5bdd94649c`  
**Local full commit (push blocked):** `9109f373bcfb179e8a818f6d503cce50d5c33cfb`  
**UTC:** 2026-11-01T05:56:32Z

## Matrix

| Category | Status |
|----------|--------|
| Package integrity | PASS (ZIP overlay) |
| Schema validity (pack records) | **FAIL** VALID=0 INVALID=20 |
| Ledger integrity (adversarial) | PASS (executed cases) |
| Cryptographic integrity | PARTIAL (ephemeral) |
| Kernel execution | exit=0 passed=536 failed=0 |
| Independent replay | PARTIAL (same workspace; stdout digests differ) |
| ISO alignment | NOT_ASSESSED |
| ISO conformity | NOT_ESTABLISHED |
| Certification | NOT_ESTABLISHED |

## Commands

```
python3 -m pytest SWI_ISO_Evidence_Replay_Lab_Pack/tests/test_schema_and_ledger.py -q
python3 -m pytest tests/cek_alignment_monitor tests/law tests/pre_r -q
python3 SWI_ISO_Evidence_Replay_Lab_Pack/tools/verify_local_records.py
```

## Evidence

- serial: `SWI-ISO-SWI-KERNEL-SUITE-20261101-000001`
- Active ledger verify: ok

## Phase 3 adversarial (executed)

UNIQUE_SERIAL, MONOTONIC, CONCURRENT, DUPLICATE, BROKEN_HASH, REORDER, MISSING_ENTRY = PASS  
SERIAL_ROLLBACK, MODIFIED_SIGNATURE, WRONG_PUBLIC_KEY, REPLAYED_OLD_RECORD, MODIFIED_PAYLOAD = NOT_RUN

## Governance

```
PROVEN=NO
SEALED=NO
AUTHORIZED=NO
PRODUCTION_AUTHORIZED=NO
GITHUB_PUBLICATION=BLOCKED_AUTHENTICATION (full tree)
CI_GREEN ≠ SWI_AUTHORIZED
```

Historical evidence preserved. Invalid pack records not admitted. No merge to main.
