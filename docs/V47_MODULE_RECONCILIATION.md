# SWI v4.7 — Module Reconciliation

**Rule:** Module numbers are identifiers, not proof.  
**Do not force a current match.** Valid result: HISTORICAL/DESIGN → NO CURRENT IMPLEMENTATION MATCH.

---

## Evidence levels

| Level | Name | Requirement |
|-------|------|-------------|
| 0 | Narrative | Mentioned in documentation only |
| 1 | Design | Architecture / algorithm / pseudocode |
| 2 | Implemented | Current source path exists |
| 3 | Tested | Automated tests exercise the implementation |
| 4 | CI verified | Controlled CI reproduces tests |
| 5 | Sealed | Governance record + frozen tip + CI + limitations |
| 6 | Production governance | Key custody, rotation, ops, independent review — **not claimed by M11** |

---

## M11

| Field | Value |
|-------|--------|
| Historical name (v4.7) | Continuity Lock / state-tag / context-pinning (as described in older material) |
| Historical purpose | Continuity / state preservation concepts |
| Current candidate | M11 Foundation Admission + post-admission cryptographic continuity/seal |
| Current repository | SWI-V2-Modules-11-22 |
| Source path | `swi_v2/module11/` (admission + seal path as of sealed tip) |
| Tests | Unit + adversarial (proof substitution, canonicalization, domain substitution, reconstructed proof) |
| CI | `two_checkout_travel.yml` run **35253244912** (Python 3.10 / 3.11 / 3.12) |
| Seal | **SEALED** — `docs/M11_SEAL_RECORD.md`; tip `1d6d7dc250df80f39aa60bd8da812c9ae3efebec` |
| Classification | HISTORICAL name/concept reconciled; **CURRENT SPEC ≠ HISTORICAL SPEC** (context-pinning narrative ≠ current post-admission seal path) |
| Difference | Old material emphasizes state-tag/context-pinning; current M11 is admission + Ed25519/Merkle post-admission seal on `AdmittedInput` only |
| Limitation | CRTG, production keys, factual truth, replay-by-signature, sparse Merkle as product — not part of seal |

**Reconciliation statement:**  
Historical M11 (concept/name) → current M11 (independent implementation evidence). Do not use v4.7 M11 text as the current technical specification.

---

## M00–M10 (Volume 1)

| Range | Current repository | Classification guidance |
|-------|--------------------|-------------------------|
| M00–M10 | SWI-V1-Module-1-10 | Reconcile per module against V1 source + tests; bounded seals where documented; not auto-SEALED by M11 |

Detailed per-module rows: expand as recovered (do not invent).

---

## M12–M22

| Status | UNBLOCKED for controlled development (MODULE_STATUS); **not implemented by M11 seal** |
|--------|----------------------------------------------------------------------------------------|
| Start | New contract → threat model → implementation → tests → CI → limitations → governance decision |

---

## M23–M45

| Status | Architecture allocation / historical design candidates only |
|--------|---------------------------------------------------------------|
| Classification until recovered | HISTORICAL / DESIGN / UNPROVEN |
| Rule | No current implementation match is a valid audit result |

---

## Public technical statement (defensible)

> SWI v4.7 documents a 46-module architecture. Current implementation status is established independently through the active V1/V2 repositories and associated tests and CI.

**Not defensible without per-module evidence:** “SWI has 46 implemented modules.”
