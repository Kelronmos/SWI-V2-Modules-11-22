# LAW INGESTION ARCHITECTURE

**Status:** RESEARCH / EXPERIMENTAL · NOT SEALED · NOT PRODUCTION AUTHORIZED  
**Date:** 23 September 2026  
**Branch:** `experimental/law-ingestion-lane`

## Core separation

```
LAW DATA
  ≠
LAW EVIDENCE (LawArtifact — immutable)
  ≠
LIFECYCLE EVENT (LawLifecycleEvent — immutable)
  ≠
POLICY INTERPRETATION (PolicyMapping — interpretive only)
  ≠
ADMISSION
  ≠
AUTHORIZATION
  ≠
ACTION
```

## Path

```
EXTERNAL WORLD
       │
       ▼
  LAW SOURCE
       │
    INGEST
       │
       ▼
 LAW ARTIFACT          (immutable evidence)
       │
  CANONICALIZE
       │
     HASH
       │
 INTEGRITY VERIFY
    │         │
  PASS      REJECT → HALT
    │
 REGISTRY (append-only)
    │
 LIFECYCLE EVENT
  (SUPERSEDE / QUARANTINE / REVOKE)
    │
 POLICY MAPPING (interpretive only)
    │
 ADMISSION → AUTHORIZATION → ACTION
```

## Non-negotiable rules

1. A law being present never authorises an action.
2. Artifacts are never rewritten. Supersession is recorded only as a new event.
3. Integrity failure → REJECT / HALT (no silent repair).
4. Any registry mutation requires explicit `LAW_REGISTRY_ADMIN` authority.
5. Policy mappings are interpretive and cannot mutate LawArtifacts.
6. Replay protection is currently in-process only (honest limitation).

## Implementation location

`experimental/law/` — additive to the existing kernel; does not patch kernel boundaries.
