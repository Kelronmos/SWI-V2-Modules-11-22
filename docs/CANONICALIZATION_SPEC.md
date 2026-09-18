# Canonicalization Specification (Lane B) — V2

**Contract id:** `canonicalization_v0`  
**Status:** IMPLEMENTED → TESTED (not SEALED)  
**Paired with:** V1 `swi_core.canonical`

```text
reject non-finite floats
json.dumps(..., sort_keys=True, separators=(",", ":"), default=str, allow_nan=False)
→ UTF-8 → SHA-256 hex
```

Covered fields exclude `created_at`. Does not establish truth or authorization.

Golden vectors: `test/fixtures/canonical_vectors.json` (shared digests with V1).

Implementation: `swi_v2.kernel.canonical`
