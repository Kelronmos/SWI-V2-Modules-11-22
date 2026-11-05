# ISO Claim Governance

This document governs **allowed ISO-related wording** for SWI. It is not a certification procedure.

## Status

- ISO claim-gate: register + validator + tests + CI
- ISO conformity: **NOT ESTABLISHED**
- Production authorization: **NO**

## Commands

```bash
python tools/validate_iso_claim_status.py evidence/iso_claim_status.json
python -m pytest tests/test_iso_claim_gate.py -q
```

## Non-claims

```
JSON VALID ≠ ISO CONFORMITY
CI GREEN ≠ SWI AUTHORIZED
GATE GREEN ≠ PRODUCTION AUTHORIZED
```
