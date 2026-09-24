# WP-01 Source-Tip Location Report — 24 September 2026

**STATUS:** LOCATED / CLASSIFIED  
**EVIDENCE:** Live tree at `690f4fd68c30e1a2100dbdf3391d089c682e95c3` + local `pytest tests/law/test_evidence_freshness.py` (2 passed).  
**LIMITATIONS:** Local pytest is not CI-VERIFIED at this SHA. Does not claim Foundation PASS, seal, or production.  
**NEXT GATE:** Optionally re-run law suite + record CI run ID bound to an exact SHA if CURRENT attestation of *later* code is required; otherwise keep package as tip-bound HISTORICAL-capable CURRENT-for-that-tip.

Execution module: **BLOCKED**. No silent SHA rewrite performed.

---

## 1. Artifacts that assert `source_tip = 8245e3f03d8673c966abf9c63be9d838073159b0`

| Path | Role |
|------|------|
| `evidence/law/manifest.json` | Primary freshness gate input (`tests/law/test_evidence_freshness.py`) |
| `evidence/law/formal-results.json` | Z3 F-001…F-006 machine-readable results |
| `evidence/law/test-results.json` | pytest-law + verify.sh results for that tip |

**Not** the same tip:

| Path | Value |
|------|--------|
| `evidence/law/replay-results.json` | `tip`: `538490a525f2e86c9bd9b37293b82adf302dfc4f` |
| `evidence/pre_r/baseline.sha` | `3f87e7c3c21ba7016a8affb5c4c0b3045703055e` |

**Docs only** (narrative references, not gate inputs): `docs/EVIDENCE_FRESHNESS_STATUS_2026-09-23.md`, `docs/SWI_COMPLETE_FIX_MANUAL_2026-09-23.md`, `docs/SWI_NON_EXECUTION_FOUNDATION_STATUS_2026-09-23.md`, `docs/CURRENT_POSITION.md`.

---

## 2. What the package attests

From `evidence/law/manifest.json`:

- **Lane:** `experimental/law`
- **Branch at generation:** `experimental/law-ingestion-lane`
- **source_tip:** `8245e3f03d8673c966abf9c63be9d838073159b0` — commit *formal(z3): bind model to audited contract tip…*
- **declared_contract_tip:** `4cb10a0425b1026d51ef60dae97eda2c42bafc35`
- **status:** RESEARCH / EXPERIMENTAL · `sealed: false` · `production_authorized: false`
- **Formal:** F-001…F-006 PASS (model-level; not Python proof)
- **pytest_law:** 40 passed; **verify_sh** full_pytest: 192 passed (as recorded at generation time)
- **Blob binds:** `authority_py_blob_sha` / `registry_py_blob_sha` to `experimental/law/authority.py` and `registry.py`

Generator pattern: evidence commits `543764b` → `b8fbaae` → `e36c0fe` recorded results **for** tip `8245e3f`, then anti-stale guard `1b1206b`.

---

## 3. Comparison to current HEAD

| Field | Value |
|-------|--------|
| Current HEAD (at classification) | `690f4fd68c30e1a2100dbdf3391d089c682e95c3` |
| `git merge-base --is-ancestor 8245e3f HEAD` | **true** (exit 0) |
| Authority/registry blob SHAs vs working tree | **match** |
| `test_evidence_source_tip_reachable_from_head` | **PASS** (local) |
| `test_evidence_authority_registry_blobs_match_tree` | **PASS** (local) |

### Why docs once reported FAIL

When HEAD was `a6b81fb…` **before** `experimental/law-ingestion-lane` landed on `main`, `8245e3f` was not necessarily an ancestor of **main**. After **PR #2 merge** (`d2997c8`), the tip is on main ancestry. The earlier failure was legitimate for that tip/HEAD pair; it is not the current pair.

Commits after `8245e3f` that touch law evidence/tests are evidence/docs/CI/guard only — not authority.py/registry.py content drift (blobs still match).

---

## 4. Classification (do not manufacture PASS)

| Question | Answer |
|----------|--------|
| Is the JSON package **orphaned** from current main HEAD? | **No** — source_tip is an ancestor |
| Does it attest **current HEAD** as the tested code tip? | **No** — it attests **8245e3f** |
| Are authority/registry blobs still those tested? | **Yes** (match) |
| HISTORICAL vs CURRENT? | **Tip-bound CURRENT for experimental/law at 8245e3f**; **not** a claim that all of HEAD (docs, other modules, runtime docs) was re-proven |
| Hand-edit source_tip to HEAD? | **Forbidden** — would falsify provenance |
| Foundation PASS? | **NOT CLAIMED** |
| Execution / production? | **BLOCKED / NOT AUTHORIZED** |

Honest SWI lag pattern (also noted in the test docstring): source_tip may be an ancestor when newer commits only update evidence/docs.

---

## 5. Regeneration decision

**Not required** solely to satisfy the ancestor check — the check already passes.

Regenerate **only if** the project needs a new package that:

1. Re-runs Z3 + `tests/law` + verify at a **chosen** code tip (e.g. post-merge main), and  
2. Writes a new `source_tip` equal to that tip, and  
3. Records new CI run IDs — without rewriting the old package in place as if it had always been about HEAD.

Until then: keep `8245e3f` evidence as the formal/pytest record for that tip; treat post-tip documentation commits as non-invalidating for this **lane’s** blob-bound claims.

---

## 6. Decision-envelope note (design only)

Expanding `DecisionEnvelope` so every consequential result carries law/policy/ethics/governance/security/human context remains **DESIGNED** (`docs/runtime/DECISION_ENVELOPE.md`). Human authority remains **UNDER_CONSTRUCTION** (`docs/runtime/HUMAN_AUTHORITY.md`). Neither is implemented by this report.

---

## 7. WP-01 outcome

```text
LOCATE     = DONE
CLASSIFY   = TIP-BOUND / ANCESTOR-REACHABLE / BLOBS-MATCH
REWRITE    = NOT DONE (correct)
CI-VERIFY  = NOT YET (local only)
FOUNDATION = NOT CLAIMED
EXECUTION  = BLOCKED
WP-02      = allowed to start only as design/contracts — not as runtime open
```

«Do not claim what the code cannot demonstrate.»
