# SWI Upgrade & Progressive Repository Integration Manual

**Status:** PROPOSED — Upgrade Governance  
**Shared with V1.** Full policy: same principles as V1 `docs/UPGRADE_AND_PROGRESSIVE_INTEGRATION_MANUAL.md`.

## Rule

«Proven contracts, not module-count symmetry.»

V2 does not wait for every Class C/D repo to implement 00–10.  
V2 does not implement M13–22 as a batch.

## Readiness (governance %)

75% ≈ prepare integration · 85% ≈ boundary integration · 95% ≈ seal candidate  
**Critical blockers override percentage.**

## V2 gates

| Gate | Need |
|------|------|
| M11 | Reject raw/malformed; accept valid V1 evidence; distinct AdmittedInput |
| Kernel | Raw → HALT; Admitted → continue |
| M12+ | Previous boundary Integration/Boundary Ready first |

## Tracks

1. Foundation evidence → M11 → Kernel  
2. Trust (CRTG) — parallel design, not a blocker excuse for freezing foundation work forever  

Unsigned `FoundationEvidenceEnvelope` ≠ authenticated sender.

## Current

M11 tested · not sealed · CRTG proposed · M12–22 not bulk-built
