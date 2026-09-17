# Truth / Assumption Ledger (V2 docs)

**Last updated:** 2026-09-17  
**Scope:** Protect current implementation from historical overclaim.

| ID | Statement | Type | Evidence | Last verified |
|----|-----------|------|----------|---------------|
| T-001 | V1 produces serialized foundation evidence | TRUE / VERIFIED | V1 producer path / CI | 2026-09-17 |
| T-002 | V2 consumes evidence without V1 tree present | TRUE / VERIFIED | two_checkout_travel CI #50 / 35253244912 | 2026-09-17 |
| T-003 | M11 post-admission seal verifies | TRUE / VERIFIED | CI 35253244912; M11_SEAL_RECORD | 2026-09-17 |
| T-004 | M11 is CRTG | FALSE / NOT IMPLEMENTED | M11_SEAL_RECORD limitations | 2026-09-17 |
| T-005 | Production HSM key governance exists | FALSE / NOT IMPLEMENTED | M11_SEAL_RECORD | 2026-09-17 |
| T-006 | M11 establishes factual truth of payloads | FALSE | M11 limitations; doctrine integrity ≠ truth | 2026-09-17 |
| T-007 | M11 seal auto-completes M12–22 | FALSE | MODULE_STATUS controlled unblock only | 2026-09-17 |
| T-008 | Replay protection is established by signature alone | FALSE | M11 limitations | 2026-09-17 |
| A-001 | v4.7 Module 46 is implemented today | ASSUMPTION (reject) | No current evidence | — |
| A-002 | Historical M11 code is current M11 | FALSE ASSUMPTION | Reconciliation: concept ≠ seal implementation | 2026-09-17 |
| A-003 | All 46 documented modules are implemented | FALSE ASSUMPTION | Repo audit V1/V2 | 2026-09-17 |
| A-004 | PDF Python listings are live V1/V2 source | ASSUMPTION (unproven) | Requires path + test + CI match | — |

### Doctrine

- Cryptographic integrity ≠ factual truth  
- Signature ≠ replay protection  
- SEALED ≠ production key custody (Level 6)  
- Narrative (Level 0) never substitutes for CI (Level 4) or seal (Level 5)  
