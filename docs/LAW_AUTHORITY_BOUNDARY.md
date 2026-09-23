# LAW AUTHORITY BOUNDARY

**Status:** RESEARCH / EXPERIMENTAL · NOT SEALED  
**Date:** 23 September 2026

## Scope required for any law-registry mutation

```
LAW_REGISTRY_ADMIN
```

## Mutations

| Mutation     | Authority required          |
|--------------|-----------------------------|
| INGEST       | LAW_REGISTRY_ADMIN          |
| SUPERSEDE    | LAW_REGISTRY_ADMIN          |
| QUARANTINE   | LAW_REGISTRY_ADMIN          |
| REVOKE       | LAW_REGISTRY_ADMIN          |

Missing authority → `AuthorityHalt` (HALT)  
Wrong / missing scope → `AuthorityError` (REJECT)

Re-uses `swi_v2.kernel.authority.require_authorization_for_action`.
Does not introduce a parallel authority model.
