# evidence/pre_r — LAW-TRUTH-BOUNDARY-01 artifacts

All artifacts under this tree are **evidence**, not authority (LAW-005).

## Contents

| Path | Purpose |
|------|---------|
| baseline.* | Frozen environment at start of phase |
| test-results/ | pytest / compileall stdout |
| hashes/ | SHA-256 of result artifacts |
| replay/ | Reserved for full two-checkout packages |
| manifest.json | Machine-readable claim + scope + artifact list |

## Claim recorded in manifest

REJECT/HALT blocks privileged execution through the enforced experimental API path.

## Explicit non-claims

- process-wide enforcement  
- Level 4 / Level 5  
- M11 seal  
- PRE-CONSEQUENCES runtime  

## Two-checkout note (2026-09-21)

- Local V2 serialized-travel tests: **10 passed** (`test/test_serialized_v1_travel.py`).
- Live V1 export via `SWI-V1-Module-1-10/scripts/export_travel_evidence.py` currently fails:
  `Trainer.process()` now requires keyword-only `admission=…`; the export script has not been updated.
- This is recorded as an open diagnostic gap (PR-015), not silently worked around.
- CI workflow `.github/workflows/two_checkout_travel.yml` remains the authoritative cross-repo path once the V1 export is repaired.
