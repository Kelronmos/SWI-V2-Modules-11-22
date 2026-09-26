# Current SWI Position (V2 view) — 26 September 2026

**Label: CURRENT**

**Claim ledger:** `docs/runtime/CLAIM_EVIDENCE_LEDGER.md` + `evidence/claim-ledger.json`  
**Freshness contract (FROZEN):** `docs/runtime/EVIDENCE_FRESHNESS_CONTRACT.md`  
**WP-02 inheritance matrix:** `docs/WP02_EVIDENCE_INHERITANCE_MATRIX_2026-09-24.md`  
**WP-01 classification:** `docs/WP01_CLASSIFICATION_CLOSURE_2026-09-24.md`  
**Programme index:** `docs/runtime/COMPLETE_CLOSURE_PROGRAMME.md`

| Area | Status |
|------|--------|
| Freshness doctrine | 🔒 FROZEN |
| WP-01 | ✅ CLOSED FOR CLASSIFICATION |
| **WP-02 claim ledger** | 🟡 **POPULATED (first pass)** |
| LAW-001 / AUTH-001 / FRESH-001 | INHERIT (TIP_BOUND) |
| TEST / FOUNDATION / TRAVEL | REGENERATE |
| INV / EXEC / H / ENV / LEDGER / SNYDER-* | NO_EVIDENCE |
| Execution | 🚫 BLOCKED |
| Production / seal / Foundation PASS | NOT CLAIMED |

## Normative design (this branch)

| Document | Role |
|----------|------|
| [`docs/SWI_MANIFESTO.md`](SWI_MANIFESTO.md) | Human-capacity doctrine; audience; non-autonomy |
| [`docs/ZERO_TRUST_RELATIONSHIP.md`](ZERO_TRUST_RELATIONSHIP.md) | External ZT reference; SWI boundary |
| [`docs/REPOSITORY_OWNERSHIP_MAP.md`](REPOSITORY_OWNERSHIP_MAP.md) | Rebuild contract ownership map |

**Manifesto status:** NORMATIVE DESIGN / REBUILD CONTRACT · does **not** create or imply a seal · production **BLOCKED** unless separately authorized.

## Experimental rebuild kernel (this branch only)

**Branch:** `experimental/privacy-domain`  
**Status:** RESEARCH / EXPERIMENTAL · **NOT SEALED** · **PRODUCTION BLOCKED**

| Unit | Path | Status |
|------|------|--------|
| Privacy domain gate | `experimental/privacy/` | IMPLEMENTED · tests on branch · NOT SEALED |
| Closed transition engine | `experimental/repair/transition_engine.py` | IMPLEMENTED · P0 adversarial tests · NOT SEALED |

**Invariant (frozen):**

```text
ZT_SIGNAL ≠ EVIDENCE ≠ ADMISSION ≠ VERIFICATION
  ≠ HUMAN_AUTHORITY ≠ AUTHORIZATION ≠ ACTION

CERTIFICATE_VALID / TPM / HSM / CI_GREEN / ZTA_ACCESS_GRANTED
  ↛ HUMAN_AUTHORITY
  ↛ SWI_AUTHORIZATION
```

**CISA-style maturity ratings for SWI:** NOT_ASSESSED (analytical mapping only).

## Next

1. Keep experimental work on this branch; do not merge as seal or production.
2. Capture independent verification evidence for privacy + transition tests before promotion claims.
3. Expand ATM-001 with ZTA domain scenarios (ZTA-A01–A10) as defined scenarios, not sealed results.
4. Execute REGENERATE rows only with new packages; keep INHERIT tip-bound.

«Do not claim what the code cannot demonstrate.»
