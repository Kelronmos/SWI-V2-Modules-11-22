# Architecture Gap Register — 2026-11-06

## Open gaps relevant to recovered packages

| ID | Gap | Severity | Status | Notes |
|----|-----|----------|--------|-------|
| GAP-01 | Foundation Seal 5 not ready | High | OPEN | V1 and V2 both record NOT READY |
| GAP-02 | FoundationEvidenceEnvelope is unsigned | High | OPEN | Hash integrity only; no authenticated origin |
| GAP-03 | Firefly has NO IMPLEMENTATION AUTHORIZED in V2 | High | FROZEN | Do not integrate adapter without explicit gate |
| GAP-04 | Durable replay not implemented in V2 | Medium | OPEN | ReplayGuard partial in-memory only |
| GAP-05 | Device package uses string/fingerprint identity, not CRTG | Medium | OPEN | Demonstration only |
| GAP-06 | Possible diagram lag: producer IMPLEMENTED vs diagram PROPOSED | Low | OPEN | Resolve by updating diagram status language; do not rewrite producer history |
| GAP-07 | Educational package not linked to docs/education/EDUCATION_ARCHITECTURE_V1.md | Low | OPEN | Document not found in V2 search; treat educational ZIP as standalone demo until V1 education architecture is located and compared |

## Explicit unknowns
- Exact schema of FoundationEvidenceEnvelope JSON fields beyond the integrity-covered set (not fully expanded in the producer one-pager).
- Whether a private V1-Canonical document adds further normative requirements not present in the public V1-Module-1-10 tree.
- Full content of V2 `docs/SCAR_FIREFLY_INDEX.md` and any Consume/Refuse contract text (referenced but not re-fetched in this turn).

## Non-gaps (clarified)
- The three recovered packages do **not** create a second authorization engine inside `swi_v2/`.
- SCAR remains in V1; Firefly remains unauthorized for implementation in V2.
