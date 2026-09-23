# LAW POLICY MAPPING

**Status:** RESEARCH / EXPERIMENTAL · NOT SEALED  
**Date:** 23 September 2026

## Separation

```
LAW ARTIFACT          = source evidence (immutable)
POLICY MAPPING        = interpretive statement only
```

A `PolicyMapping`:

- references a specific `law_id` + `law_version`
- carries its own `mapping_hash`
- is marked `status = "INTERPRETIVE_MAPPING"`
- **cannot** mutate or replace any `LawArtifact`

Presence of a law artifact without a policy mapping yields **no automatic authorization**.
