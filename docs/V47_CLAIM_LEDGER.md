# SWI v4.7 — Claim Ledger

**Purpose:** Prevent historical claims from becoming false implementation evidence.  
**Rule:** Promote only via the evidence hierarchy in `V47_VERIFICATION_STATUS.md`.  
**M11:** remains SEALED; this ledger does not alter the seal.

| ID | v4.7 claim | Classification | Current repo | Evidence | Status |
|----|------------|----------------|--------------|----------|--------|
| V47-001 | 46-module architecture | HISTORICAL / DESIGN | V1/V2 + architecture map | PDF only | Not implementation proof |
| V47-002 | M11 Continuity Lock (name/concept) | HISTORICAL | V2 M11 | Current M11 seal | Name/concept reconciled; implementation differs |
| V47-003 | M11 context-pinning / state-tag mechanism | HISTORICAL / DESIGN | No current equivalent established as the M11 seal | PDF code | Not current M11 specification |
| V47-004 | Ed25519 sealing | IMPLEMENTED → CI / SEAL path | V2 | Code + tests + CI 35253244912 | Verified under current M11 |
| V47-005 | Merkle verification / reconstruction | IMPLEMENTED → CI | V2 | Code + adversarial tests + CI | Verified under current M11 |
| V47-006 | CRTG | DESIGN | V2 | M11 limitations | Unimplemented |
| V47-007 | HSM / production key custody | DESIGN | V2 | M11 limitations | Unimplemented |
| V47-008 | Module 46 Lockdown | HISTORICAL / DESIGN | No current implementation match | PDF | Unproven |
| V47-009 | Project Alpha claims | UNPROVEN | Requires independent evidence | Historical docs | Do not promote |
| V47-010 | Multi-Agent Swarm / Witness Protocol | DESIGN | No production mesh in V1/V2 | PDF narrative / illustrations | Unproven as runtime |
| V47-011 | Sovereign Mesh / edge Botswana agent | DESIGN / HISTORICAL | Product prototypes ≠ architecture seal | PDF | Unproven as SWI kernel |
| V47-012 | Cryptographic integrity establishes factual truth | FALSE if claimed | — | Explicit M11 non-claim | Reject as doctrine |

### Promotion path (per claim)

```
CLAIM
 → locate current implementation?
     NO  → UNPROVEN
     YES → tests?
            NO  → IMPLEMENTED (untested)
            YES → CI?
                   NO  → TESTED
                   YES → formal seal?
                          NO  → CI VERIFIED
                          YES → SEALED
```

### Contradiction rule

If historical text and current implementation differ, record:

`HISTORICAL SPECIFICATION ≠ CURRENT SPECIFICATION`

Do not silently overwrite either side. Explain reconciliation in the module reconciliation file.
