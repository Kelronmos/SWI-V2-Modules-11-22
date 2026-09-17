# SWI Trust Sequence

**Authority:** `docs/SWI_CONTROLLED_SEQUENCE_MANUAL.md`

```text
PRIORITY FIXES
  → Foundation Seal 5 (V1 signed export)
  → CRTG v0
  → Standalone independent verifier + live CI
  → Deterministic replay
  → Sparse Merkle (research only)
  → NAB Stage 2 (after Seal 5)
  → Cross-node M11 admission
  → Firefly reconsideration
  → Controlled Module Manual Schema
  → M12 contract → implementation → seal
  → M13…
```

## Freezes

| Item | State |
|------|--------|
| M12 implementation | **FROZEN** until Gates A–D |
| M13–22 | **BLOCKED** |
| NAB Stage 2 | **BLOCKED** until Seal 5 |
| M11 seal | **Historical — do not rewrite** |

## One-line rule

SIGN → VERIFY INDEPENDENTLY → REPLAY → DISTRIBUTE → STANDARDIZE → BUILD NEXT MODULE
