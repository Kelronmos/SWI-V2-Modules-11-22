# Canonicalization Specification (Lane B) — V2

**Contract id:** `canonicalization_v0`  
**Status:** IMPLEMENTED → TESTED (not SEALED)  
**Paired with:** V1 `swi_core.canonical`

```text
json.dumps(..., sort_keys=True, separators=(",", ":"), default=str)
→ UTF-8 → SHA-256 hex
```

Covered fields exclude `created_at`. Does not establish truth or authorization.

Implementation: `swi_v2.kernel.canonical`  
Tests: `test/test_canonicalization.py`
