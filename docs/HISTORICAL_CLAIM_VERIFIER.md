# SWI Historical Claim Verifier — Formal Design

**Purpose:** Reconcile historical documentation (e.g. SWI v4.7) with live proof surfaces **without** promoting PDF text to implementation evidence.

**Doctrine:** Fail closed. Filename ≠ implementation. Test path ≠ passing test. Audit filename ≠ module seal.

**M11 regression:** The verifier must rediscover M11 E4 from source + tests + seal record + CI identity — **without** hard-coding `"M11": "SEALED"`.

---

## Pipeline

```
PDF / historical claim
        ↓
Package integrity (COMPLETE_ZIP | STANDALONE | INCOMPLETE)
        ↓
Claim extraction (page, heading, text, claim_type)
        ↓
Normalize → module id (M00–M46 only) + claim type
        ↓
Live proof-surface snapshot (repo + commit SHA + timestamp)
        ↓
Classify paths: SOURCE | TEST | DOCUMENTATION | WORKFLOW | ARTIFACT
        ↓
Evidence matcher (content-aware for seal/audit)
        ↓
Fail-closed classifier → E0…E4 + flags (HISTORICAL, UNPROVEN, CONFLICT)
        ↓
Audit report (JSON + Markdown)
```

---

## Path classes (mandatory)

| Class | Path heuristics (examples) | Does **not** imply |
|-------|----------------------------|--------------------|
| SOURCE | `swi_v2/kernel/*.py`, `swi_v2/moduleNN/*.py` excluding pure stubs | Correctness |
| TEST | `test/test_*.py` | Tests passed |
| DOCUMENTATION | `docs/**` | Implementation |
| WORKFLOW | `.github/workflows/*` | Run succeeded |
| ARTIFACT | `*.json` evidence exports | Seal status |

A path containing `m11` in the name is **not** automatically SOURCE.

---

## Evidence ladder

| Level | Name | Requirement |
|-------|------|-------------|
| E0 | DOCUMENTED | Historical/PDF claim only |
| E1 | IMPLEMENTED | Non-stub SOURCE paths exist for the module |
| E2 | TESTED | TEST paths exist that exercise the module (**existence only**; not pass) |
| E3 | CI_VERIFIED | Identified CI run succeeds for relevant jobs (must be recorded, not assumed) |
| E4 | SEALED | Seal record **content** asserts this module SEALED + tip SHAs + limitations; aligned audit summary optional |

**Separate flags:** `HISTORICAL`, `UNPROVEN`, `CONFLICT`, `CI_UNVERIFIED`, `SEAL_UNVERIFIED`

---

## Fail-closed rules

| Condition | Result |
|-----------|--------|
| GitHub unreachable | `UNVERIFIED` (not DESIGN) |
| CI run not confirmed | not E3/E4 |
| Seal record missing or unparsable | `SEAL_UNVERIFIED` (not SEALED) |
| Audit JSON lacks matching `"module"` / wrong module | does not count for that module |
| ZIP missing in COMPLETE_ZIP mode | `PACKAGE_STATUS=INCOMPLETE` → audit aborts |
| Module id M47+ | reject (unless registry explicitly extends) |
| Only `__init__.py` stub for moduleNN | not E1 |

---

## Seal / audit content rules

- `docs/M11_SEAL_RECORD.md` counts for **M11 only** after content confirms SEALED.
- `docs/M11_AUDIT_SUMMARY.json` counts only if JSON `module == "M11"` and `status == "SEALED"`.
- Generic `AUDIT_SUMMARY.json` never seals M12+.

---

## Proof-surface freeze

Every report must include repository, branch, commit SHA, and retrieval timestamp.
Prefer sealed tip SHAs when evaluating M11 seal scope rather than floating `main` alone.

---

## Two conclusions (never collapse)

1. **PACKAGE** — COMPLETE / INCOMPLETE / NOT_VERIFIED / STANDALONE_DOCUMENTS
2. **PROOF SURFACE** — per-module E0–E4 + conflicts

---

## Package modes

| Mode | Requirement |
|------|-------------|
| `COMPLETE_ZIP` | `SWI v4.7.zip` present + expected PDF members + SHA256 recorded |
| `STANDALONE_DOCUMENTS` | Explicit flag; PDFs only; package conclusion ≠ COMPLETE_ZIP |
| Missing zip without standalone flag | **Error / INCOMPLETE** |

Never silently treat missing package as a successful COMPLETE_ZIP audit.

---

## Implementation

See `scripts/historical_claim_verifier.py`.

```bash
python scripts/historical_claim_verifier.py --demo-m11-regression
```

Expected: M11 → E4_SEALED (from evidence objects, not a hardcoded status map); M12 stub → E0 / not E4.
