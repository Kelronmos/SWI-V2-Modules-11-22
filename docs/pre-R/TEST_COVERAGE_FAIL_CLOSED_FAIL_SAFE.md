# pre-R: 20 Unit Tests vs Fail-Closed / Fail-Safe

**Date:** 2026-09-19  
**Suite:** `tests/pre_r/test_response_boundary.py`  
**Local result:** 20 passed  
**Status:** EXPERIMENTAL · NOT SEALED · NOT AUTHORIZED FOR PROMOTION  

## Architecture reminder

```text
V1  — foundation / evidence · design-only pre-R docs · NO pre-R runtime
        │ evidence contract
        ▼
V2  — M11 + experimental/response_boundary/
        EXPERIMENTAL → gate-tested → NOT SEALED
```

## What each test asserts

Most tests stop at: `ReturnGate.evaluate(...) == ADMIT | REJECT`  
That is **gate-level fail-closed**, not full **fail-safe enforcement**.

| # | Test | Proves | Fail-closed | Fail-safe |
|---|------|--------|-------------|-----------|
| 1 | `test_valid_response_admitted` | Happy path → ADMIT | ✓ positive | — |
| 2–4 | `test_integrity_mutations_rejected` | Altered result / destination / digest → REJECT | ✓ | — |
| 5 | `test_wrong_request_rejected` | Binding mismatch → REJECT | ✓ | — |
| 6 | `test_authority_expansion_rejected` | Authority expansion → REJECT | ✓ | — |
| 7 | `test_wrong_destination_rejected` | Destination mismatch → REJECT | ✓ | — |
| 8 | `test_missing_evidence_rejected` | No evidence → REJECT | ✓ | — |
| 9 | `test_expired_response_rejected` | Past expiry → REJECT | ✓ | — |
| 10 | `test_revoked_authority_rejected` | Revoked → REJECT | ✓ | — |
| 11 | `test_policy_denial_rejected` | policy_allows=False → REJECT | ✓ | — |
| 12–14 | `test_scope_mismatch_rejected` | Wrong principal / action / resource → REJECT | ✓ | — |
| 15 | `test_certificate_is_scoped` | Certificate cannot widen scope | ✓ (scope object) | — |
| 16 | `test_receipt_is_not_authority` | Receipt has no authorize | Structural | — |
| 17 | `test_response_does_not_create_new_privileged_action` | No execute on envelope | Structural | Weak |
| 18 | `test_transformation_requires_new_integrity` | Mutate without re-seal → REJECT | ✓ | — |
| 19 | `test_nan_is_rejected_by_canonicalization` | NaN cannot form integrity | ✓ construction | — |
| 20 | `test_integrity_is_deterministic` | Digest stable | Integrity property | — |

**Summary:** ~16–17 strong gate fail-closed tests · ~2–3 structural checks · **0** tests that a caller cannot ignore REJECT and still execute.

## Precise claim

> Within the experimental pre-R slice, ReturnGate rejects the listed unauthorized/mutated cases and admits the one valid fixture. That is gate-level fail-closed under those tests. It is **not** proof of fail-safe enforcement beyond the gate.

## Not established by these 20 tests

| Claim | Supported? |
|-------|------------|
| REJECT → non-executing state / no side effects | **No** |
| HALT → may_execute() == False | **No** |
| Sticky halt / require_admitted on pre-R path | **No** |
| T20: caller ignores REJECT → still blocked | **No** |
| SEALED / production / system-wide security | **No** |

See: `FAIL_CLOSED_FAIL_SAFE_REBUILD_MANUAL.md`, `LIMITATIONS.md` (PR-009).
