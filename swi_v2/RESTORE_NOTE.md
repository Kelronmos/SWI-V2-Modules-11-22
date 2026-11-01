# Execution integrity restore status

**Branch:** `review/iso-gate-repro-2026-11-01`  
**Restored:** 2026-11-01  

Incomplete base64 payload parts (`_ei_payload_0/1/4.txt`) have been removed.

`swi_v2/execution_integrity.py` is restored as a full tracked module from
`recovery/execution-integrity-restore` (lineage 77ee326 / MATCH ≠ PERMIT).

```text
Status: RESEARCH · NOT SEALED · NOT PRODUCTION_AUTHORIZED
PROVEN = NO
SEALED = NO
PRODUCTION_AUTHORIZED = NO
```

Do not treat this branch as production-authorized until the full CI matrix
(including adversarial execution-integrity tests) is green on a recorded tip.
