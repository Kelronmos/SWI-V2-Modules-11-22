# V2 Module Status

| Component | Status |
|-----------|--------|
| **M11** | **SEALED** (historical) — tip `1d6d7dc…` · CI `35253244912` |
| Verifier Pass 1 | **LIVE CI path** — `scripts/v47_live_m11_verify.py` + `scripts/v47_ci_resolver.py` |
| Property map | `docs/V47_M11_PROPERTY_MAP.json` · ledger `docs/CLAIM_LEDGER_M11.md` |
| **M12 implementation** | **FROZEN** until Gates A–D |
| M12 contract draft | `docs/M12_CONTRACT.md` |
| Standalone verifier repo | **NOT CREATED** (next gate) |
| Replay | **NOT IMPLEMENTED** (ReplayGuard = partial in-memory only) |
| Foundation Seal 5 (V1) | **NOT READY** |
| **Firefly** | **DESIGN / DEFERRED** — **NO IMPLEMENTATION AUTHORIZED** |
| SCAR → Firefly docs | **DESIGN FROZEN** — see `docs/SCAR_FIREFLY_INDEX.md` |
| SCAR (V1) | **IMPLEMENTED / TESTED** — V1 `docs/SCAR_STATUS.md` |
| M13–22 | **BLOCKED** |
| **pre-R / PR-009** | **EXPERIMENTAL** — gate + enforce API **TESTED**; **NOT SEALED**; API bypass out of scope |
| PRE module registry | `docs/pre-R/PRE_MODULE_REGISTRY.md` (docs only) |
| Lifecycle manual | `docs/SWI_MODULE_LIFECYCLE_MANUAL.md` |
| Latest local regression | `docs/REGRESSION_RECORD_2026-09-19.md` |

## Experimental rebuild kernel (`experimental/privacy-domain` branch)

| Component | Path | Status |
|-----------|------|--------|
| Privacy domain boundary | `experimental/privacy/` | **EXPERIMENTAL** · implemented · **NOT SEALED** · **PRODUCTION BLOCKED** |
| Transition engine (State/Transition/Gate) | `experimental/repair/transition_engine.py` | **EXPERIMENTAL** · implemented · **NOT SEALED** · **PRODUCTION BLOCKED** |
| Privacy adversarial tests | `tests/law/test_privacy_domain.py` (on branch) | Reported on branch; independent capture required before promotion claims |
| Transition adversarial tests | `tests/experimental/test_transition_engine_adversarial.py` (on branch) | Reported on branch; independent capture required before promotion claims |
| ZTA relationship | `docs/ZERO_TRUST_RELATIONSHIP.md` | DESIGN reference only |
| Ownership / rebuild map | `docs/REPOSITORY_OWNERSHIP_MAP.md` | DESIGN / rebuild contract |

**Rules:**

- Experimental code does **not** alter M11 seal.
- Green experimental tests ≠ SEALED ≠ production authorization.
- Privacy is a **gate**, not a state-transition permission by itself.
- Technical signals (cert, TPM, HSM, CI, ZTA grant) never become human authority.

Canonical memory-web freeze: `docs/V2_MEMORY_WEB_STATUS.md`  
SCAR→Firefly entry point: `docs/SCAR_FIREFLY_INDEX.md`
