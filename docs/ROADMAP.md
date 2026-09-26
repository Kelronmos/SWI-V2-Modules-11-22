# V2 Roadmap — CURRENT status (26 September 2026)

```text
M11 SEAL                 — SEALED (historical tip 1d6d7dc… · CI 35253244912)
CROSS-REPO TRAVEL        — BOUNDARY PROVEN LOCALLY / two-checkout path exists
FOUNDATION SEAL 5 (V1)   — NOT READY
REPLAY                   — NOT SEALED (ReplayGuard = partial in-memory only)
FIREFLY                  — DESIGN / DEFERRED — NO IMPLEMENTATION AUTHORIZED
SCAR→FIREFLY DOCS        — DESIGN FROZEN (see docs/SCAR_FIREFLY_INDEX.md)
M12 IMPLEMENTATION       — FROZEN until trust gates + contract
M13–22                   — BLOCKED
CRTG                     — DESIGN PENDING
DISTRIBUTED FIREFLY      — BLOCKED
```

## Experimental rebuild lane (`experimental/privacy-domain`)

```text
PRIVACY DOMAIN GATE      — EXPERIMENTAL / IMPLEMENTED / NOT SEALED
TRANSITION ENGINE        — EXPERIMENTAL / IMPLEMENTED / NOT SEALED
  StateRegistry → TransitionRegistry → GateRegistry → attempt_transition()
  REJECT | BLOCK | QUARANTINE | ALLOW
ZTA EXTERNAL REFERENCE   — DESIGN DOC (NIST → CISA → DoD/NSA)
ATM ZTA DOMAIN           — DEFINED scenarios (ZTA-A01–A10); not yet full suite evidence
REBUILD / OWNERSHIP MAP  — DESIGN DOC (docs/REPOSITORY_OWNERSHIP_MAP.md)
PRODUCTION               — BLOCKED
```

**Priority (controlled):**

1. Independent verification evidence for privacy + transition (do not claim seal).
2. ATM expansion: privacy + transition + ZTA substitution domains.
3. Keep M11 historical seal tip-bound; do not re-seal HEAD without gates.
4. M12 remains FROZEN until trust gates + contract.
5. **STOP** before production authorization.

Historical “M11 SEAL — NOT READY” notes are **SUPERSEDED** by `docs/M11_SEAL_RECORD.md`.

See: `docs/MODULE_STATUS.md` · `docs/CURRENT_POSITION.md` · `docs/ZERO_TRUST_RELATIONSHIP.md` · `docs/REPOSITORY_OWNERSHIP_MAP.md` · `docs/M11_SEAL_RECORD.md`
