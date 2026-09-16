# SWI M11 Closure Checklist

**Rule:** Exact SHAs only. NOT PROVEN ≠ PASS. No M12 until SEALED + seal record.

```text
[ ] Freeze V1 SHA
[ ] Freeze V2 SHA
[ ] Clean V1 environment
[ ] Clean V2 environment
[ ] Confirm no V1 import in V2
[ ] Run V1 tests
[ ] Generate real V1 evidence
[ ] Record artifact SHA-256
[ ] Admit valid evidence
[ ] Tamper payload / integrity / evidence_id / source_reference
[ ] Unsupported foundation / schema version
[ ] Invalid verification status
[ ] Remove required fields
[ ] Malform JSON
[ ] Unexpected fields (UnexpectedFieldError)
[ ] Raw dict / PipelineResult bypass
[ ] Kernel isolation
[ ] ReplayGuard (separate; in-memory only)
[ ] Python 3.10
[ ] Python 3.11
[ ] Python 3.12
[ ] Current-tip two-checkout CI + run ID
[ ] A–G worksheet
[ ] Documentation honesty
IF ALL PASS:
[ ] M11_SEAL_RECORD.md
[ ] Mark M11 SEALED
ONLY THEN:
[ ] M12 contract (minimal)
```
