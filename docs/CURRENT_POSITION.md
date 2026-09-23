# Current SWI Position (V2 view) — 23 September 2026

**Label: CURRENT**

| Area | Status |
|------|--------|
| V1 foundation evidence | Export path exists; **Foundation Seal 5 NOT READY** |
| **V2 M11** | **SEALED** (historical record preserved) |
| Evidence freshness (reported artifact) | **REFRESH_REQUIRED** — see `docs/EVIDENCE_FRESHNESS_STATUS_2026-09-23.md` |
| Replay | **NOT SEALED** — `ReplayGuard` is opt-in in-memory only |
| Firefly | **DESIGN / DEFERRED** — not implemented; no privileged M11 bypass |
| SCAR | Lives in **V1** — IMPLEMENTED/TESTED |
| M12 | Contract draft; **implementation FROZEN** |
| M13–22 | **BLOCKED** |
| Execution module | **BLOCKED** |
| Production | **NOT AUTHORIZED** |
| CRTG / prod keys | **NOT IMPLEMENTED** |

## Evidence freshness rule (universal)

Current evidence requires:

```
source_tip == HEAD
        OR
source_tip ∈ ancestry(HEAD)
```

Otherwise: **REFRESH_REQUIRED** (or explicitly labelled **HISTORICAL**).

Do not hand-edit source_tip. Do not weaken the freshness test.

## Next controlled actions (ordered)

1. Locate why the reported evidence still points to `8245e3f…`
2. Classify: HISTORICAL vs intended CURRENT
3. If CURRENT → regenerate evidence from actual HEAD → re-run freshness + regression
4. Independent audit of non-execution foundation
5. Only after foundation gate: consider further promotion (execution remains BLOCKED)

«Do not claim what the code cannot demonstrate.»
«Do not seal on stale evidence.»
