# M12 Implementation Manual — THE MASTERY ARCHIVE

**Contract draft:** `docs/M12_CONTRACT.md`  
**Status:** Implementation **FROZEN** (2026-09-17)

## Sequencing correction

Under `docs/SWI_TRUST_SEQUENCE.md`, substantive M12 code is **not** the immediate next step.

Order is:

```text
Trust infrastructure (Seal 5 → CRTG v0 → standalone verifier → replay)
  → Controlled Module Manual Schema v1
  → then M12 contract enforcement in code
  → then M12 tests / CI / seal
```

The scaffold (`accepted_placeholder`) remains a **type boundary only**.

Do not remove the placeholder in favor of partial normalization until the trust sequence authorizes Pass 2.

## When implementation is authorized

Follow `docs/M12_CONTRACT.md` and the 16-section schema in `docs/CONTROLLED_MODULE_MANUAL_SCHEMA_v1.md`.

Until then: **no** NormalizedEvidence claim, **no** M12 seal, **no** M13 unlock.
