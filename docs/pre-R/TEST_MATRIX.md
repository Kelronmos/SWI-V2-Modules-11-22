# pre-R Test Matrix (V2)

**Status:** Gate-level tests present · fail-safe beyond gate not fully covered  

## Gate (fail-closed) — covered by current unit suite

| Mutation | Expected |
|----------|----------|
| Valid response | ADMIT |
| Change result / destination / integrity | REJECT |
| Wrong request binding | REJECT |
| Expand authority | REJECT |
| Missing evidence | REJECT |
| Expired / revoked | REJECT |
| Policy deny | REJECT |
| Principal/action/resource mismatch | REJECT |
| Transform without new integrity | REJECT |
| NaN in payload | cannot form integrity |
| Certificate out of scope | not permitted |
| Receipt | not authority |
| No execute attribute on response | no self-authorization API |

## Fail-safe / enforcement — not yet established in pre-R slice

| Test | Expected | Status |
|------|----------|--------|
| REJECT → caller cannot execute | blocked | **NOT IMPLEMENTED / NOT TESTED** |
| HALT → may_execute() == False | non-executing | **N/A** (no pre-R may_execute) |
| Sticky halt via require_admitted | blocked | Uses V2 kernel helpers, **not wired to pre-R gate** |
| Automatic recovery after HALT | forbidden unless policy | **NOT IMPLEMENTED** |
| Evidence/receipt → execute | REJECT | receipt test only (no authorize) |

See `docs/pre-R/FAIL_CLOSED_FAIL_SAFE_REBUILD_MANUAL.md`.
