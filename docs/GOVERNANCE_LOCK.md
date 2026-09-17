# Governance Lock (V2)

**Updated:** 17 September 2026

1. Dependency boundaries over module counts.
2. % never overrides critical failure.
3. Serialized contract only — **no V1 package import**.
4. M10 is not the handoff.
5. M11 continuity seal is recorded in `docs/M11_SEAL_RECORD.md` (V2 tip `1d6d7dc…`, CI run `35253244912`).
6. **M12–22 BLOCKED** until independent V4.7 rediscovery / controlled module manuals — not because documentation says “go.”
7. Ed25519 ≠ CRTG. Seal ≠ factual truth. Seal ≠ production keys.
8. **Foundation Seal 5** remains **NOT READY** on V1 (unsigned envelope at origin). M11 does not replace Seal 5.

## Live two-checkout CI

| Item | Value |
|------|--------|
| Status | **Recorded success** (not PENDING) |
| Run | #50 / ID `35253244912` |
| Authority | `docs/M11_SEAL_RECORD.md` + Actions API |

If this lock and the seal record disagree, **fail closed** and reconcile — do not invent a third status.

See also: `docs/V47_GATE_FREEZE.md`, `docs/M11_AUDIT_SUMMARY.json`.
