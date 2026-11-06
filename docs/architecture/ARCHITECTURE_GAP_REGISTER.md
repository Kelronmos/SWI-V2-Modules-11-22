# Architecture Gap Register — 2026-11-06 (corrected)

## Open gaps relevant to recovered packages

| ID | Gap | Severity | Status | Notes |
|----|-----|----------|--------|-------|
| GAP-01 | Foundation Seal 5 not ready | High | OPEN | V1 and V2 both record NOT READY |
| GAP-02 | FoundationEvidenceEnvelope is unsigned | High | OPEN | Hash integrity only; no authenticated origin |
| GAP-03 | Firefly has NO IMPLEMENTATION AUTHORIZED in V2 | High | FROZEN | Do not integrate adapter without explicit gate |
| GAP-04 | Durable replay not implemented in V2 | Medium | OPEN | ReplayGuard partial in-memory only |
| GAP-05 | Device package uses string/fingerprint identity, not CRTG | Medium | OPEN | Demonstration only |
| GAP-06 | Possible diagram lag: producer IMPLEMENTED vs diagram PROPOSED | Low | OPEN | Resolve by updating diagram status language; do not rewrite producer history |
| GAP-07 | Educational package vs EDUCATION_ARCHITECTURE_V1 | Low | **CORRECTED** | Document **exists** at `docs/education/EDUCATION_ARCHITECTURE_V1.md` (SPECIFICATION / PROPOSED). Device-bound educational package is a **partial demonstration** of fail-closed checks and recovery-oriented language; it does **not** implement the full Discover→Reflect cycle, Setho/Botho frameworks, subject suites, or lesson record schema. Classification remains: educational demonstration / independent experiment, not a complete education-architecture implementation. |

## Explicit unknowns
- Exact schema of FoundationEvidenceEnvelope JSON fields beyond the integrity-covered set.
- Whether private V1-Canonical adds further normative requirements not in public V1-Module-1-10.
- Full SCAR→Firefly Consume/Refuse contract text beyond MODULE_STATUS freeze.

## Non-gaps (clarified)
- The three recovered packages do **not** create a second authorization engine inside `swi_v2/`.
- SCAR remains in V1; Firefly remains unauthorized for implementation in V2.
- `docs/education/EDUCATION_ARCHITECTURE_V1.md` is present; prior "not found" claim was incorrect.
