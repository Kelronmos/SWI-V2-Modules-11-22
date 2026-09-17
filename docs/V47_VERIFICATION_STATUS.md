# SWI v4.7 — Verification Status

**Status:** HISTORICAL ARCHITECTURE / RESEARCH DOCUMENTATION  
**Date recorded:** 2026-09-17  
**M11 seal:** unchanged (SEALED — do not reopen for v4.7 reconciliation)

---

## Formal statement

The v4.7 document set (`SWI v4.7.zip`: SWI v4.7.pdf, VOLUME 2.pdf, WII Trusts Motion.pdf, SWI v4 1-35.pdf) is treated as:

- historical architecture;
- research documentation;
- a source of recoverable design concepts.

It is **not**, by itself:

- implementation evidence;
- test evidence;
- CI evidence;
- a security seal;
- production certification;
- proof of runtime capability.

Every technical claim extracted from v4.7 must be independently classified and reconciled against the current repositories.

---

## Classification vocabulary

| Class | Meaning |
|-------|---------|
| **DESIGN** | Architecture / algorithm / pseudocode intent only |
| **HISTORICAL** | Older naming, concept, or specification language |
| **IMPLEMENTED** | Current source exists in an active repository |
| **SEALED** | Governance record + frozen tip + CI + explicit limitations |
| **UNPROVEN** | No matching current implementation / tests / CI |

---

## Evidence hierarchy (mandatory)

```
HISTORICAL DOCUMENT
        ↓
CLAIM EXTRACTION
        ↓
CLAIM CLASSIFICATION
        ↓
CURRENT REPOSITORY MATCH
        ↓
TEST EVIDENCE
        ↓
CI EVIDENCE
        ↓
SEAL / GOVERNANCE RECORD
```

**Forbidden shortcut:** PDF → “implemented”.

---

## Current M11 freeze (do not modify for v4.7)

| Field | Value |
|-------|--------|
| Status | **SEALED** |
| V2 tip | `1d6d7dc250df80f39aa60bd8da812c9ae3efebec` |
| V1 tip (seal time) | `e0c6a521d7965c46c18464edc5dc6fbd8f9e254c` |
| CI run | `35253244912` |
| Records | `M11_SEAL_RECORD.md` · `MODULE_STATUS.md` · `M11_AUDIT_SUMMARY.json` |

**Claim limited to:** post-admission cryptographic continuity path.

**Explicit non-claims (retained):**

- CRTG / certificate chain — NOT IMPLEMENTED  
- Production key management / HSM / rotation — NOT IMPLEMENTED  
- Replay policy — NOT established by signature alone  
- Factual truth — NOT established by cryptography  
- Sparse Merkle — RESEARCH ONLY  
- M12–22 automatic completion — NOT claimed  

---

## PDF rule

> PDF code is reference material until independently reconciled.

Matching requires:

1. current repository implementation;
2. identifiable source path;
3. corresponding tests;
4. successful test execution;
5. where applicable, CI evidence;
6. where applicable, a governing seal record.

---

## Related

- `docs/V47_CLAIM_LEDGER.md`
- `docs/V47_MODULE_RECONCILIATION.md`
- `docs/TRUTH_ASSUMPTION_LEDGER.md`
