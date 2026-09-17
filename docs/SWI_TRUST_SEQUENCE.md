# SWI Trust Sequence (revised 2026-09-17)

Advance by validated dependency boundaries — not by adding modules.

```text
PRIORITY FIXES (governance drift, evidence honesty)
        ↓
Foundation Seal 5 — signed V1 FoundationEvidenceEnvelope export
        ↓
CRTG v0 — minimal root + CI-signed run metadata (no HSM claim)
        ↓
Standalone verifier — public artifacts → reconstruct chain
        ↓
Independent verification party / clean-checkout proof
        ↓
Deterministic replay of sealed evidence chains
        ↓
Sparse Merkle — research experiment only
        ↓
Node Access Boundary Stage 2 (after Seal 5)
        ↓
Cross-node M11 admission evidence
        ↓
Firefly reconsideration (evidentiary bar)
        ↓
Controlled Module Manual Schema v1  ← docs/CONTROLLED_MODULE_MANUAL_SCHEMA_v1.md
        ↓
M12 contract (already drafted) → M12 implementation only when trust gates above allow
        ↓
M13…
```

## Immediate freezes

| Item | State |
|------|--------|
| M12 **implementation** | **FROZEN** |
| M12 contract doc | Retained as draft for later; not a green light to code |
| M13–22 capability | **BLOCKED** |
| Network / NAB Stage 2 | **BLOCKED** until Seal 5 |

## Why replay before Firefly / M12 expansion

Signature/hash validity ≠ reconstructible sealed chain. Replay proves reconstruction; expansion without it overclaims.
