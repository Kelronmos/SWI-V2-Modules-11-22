# LAW INTEGRITY MODEL

**Status:** RESEARCH / EXPERIMENTAL · NOT SEALED  
**Date:** 23 September 2026

## Rule

```
content change  OR  metadata change  → hash mismatch  → REJECT / HALT
```

Never:

```
hash mismatch → silent repair → continue
```

## Material hashed

- law_id, jurisdiction, title, issuing_authority, source_uri
- publication_date, effective_date, version
- content_hash (of raw content)
- ingestion_event_id

Canonicalization re-uses `swi_v2.kernel.canonical`.
