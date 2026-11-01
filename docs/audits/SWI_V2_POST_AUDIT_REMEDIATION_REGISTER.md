# SWI V2 Post-Audit Remediation Register — 1 November 2026

**Historical audit:** `docs/audits/SWI_V2_REPOSITORY_AUDIT_2026-11-01.md`  
**Historical audit commit:** `d3bef7caceeada82043704660e3b7053bb6372df`  
**Historical audited HEAD:** `b226564b5f9401a1a05703c4befee9f371460437`  

Governance retained: `PROVEN=NO` · `SEALED=NO` · `PRODUCTION_AUTHORIZED=NO` · `ISO_CONFORMITY=NOT_ESTABLISHED` · `CONFORMITY_CLAIM=SEALED`

## Findings

### FINDING-P0-001 — Execution-integrity payload reconstruction broken

| Field | Value |
|-------|-------|
| Severity | P0 |
| Component | `swi_v2/execution_integrity.py`, `_ei_payload_*.txt` |
| Historical revision | `b226564…` (still on `main` at register creation) |
| Defect | Loader stops at first missing sequential payload; parts 2/3 absent; IndentationError; adversarial suite never runs |
| Current status | **FIXED_PENDING_TEST** on repair branches; **OPEN** on `main` |
| Repair branch | `repair/post-audit-execution-integrity`; also applied on `review/iso-gate-repro-2026-11-01` |
| Repair | Full tracked module from recovery lineage; payload parts deleted |
| Regression tests | `test/adversarial/test_execution_integrity.py` — **NOT_RUN** on repair tip in agent session |
| Limitations | Main still broken until PR merges after green CI |

### FINDING-P0-002 — Payload integrity validation insufficient

| Field | Value |
|-------|-------|
| Severity | P0 |
| Status | **FIXED_PENDING_TEST** (loader removed; no fragment path remains) |

### FINDING-P0-003 — Full CI verification blocked

| Field | Value |
|-------|-------|
| Severity | P0 |
| Status | **OPEN** on `main`; depends on CI after EI repair |
| Historical CI | run `41319201764` failed collection on 3.10/3.11/3.12 |

### FINDING-P1-001 — Branch ancestry / stale branches

| Field | Value |
|-------|-------|
| Severity | P1 |
| Status | **OPEN** |
| Notes | ~40 branches; no mass-delete; PR #13/#14 overlap |

### FINDING-P1-002 — Independent ZIP evidence attribution

| Field | Value |
|-------|-------|
| Severity | P1 |
| Status | **OPEN** |
| Notes | ZIP snapshots lack `.git` metadata; do not attribute to public main without tree-hash match |

### FINDING-P1-003 — ISO claim-gate PROVEN eligibility too weak

| Field | Value |
|-------|-------|
| Severity | P1 |
| Component | `tools/validate_iso_claim_status.py` |
| Defect | Accepted PARTIAL replay/reproducibility; hash length-only check |
| Status | **FIXED_PENDING_TEST** on `review/iso-gate-repro-2026-11-01` |
| Repair | Exact PASS only; `^[0-9a-fA-F]{64}$` |

### FINDING-P1-004 — ISO claim colour / true-false semantics

| Field | Value |
|-------|-------|
| Severity | P1 |
| Status | **FIXED_PENDING_TEST** on PR #14 |
| Repair | `claim_true`/`claim_false` → null; colour black; UNKNOWN ≠ FALSE |

## Open PRs (do not merge without human approval)

- Post-audit EI repair (new) — `repair/post-audit-execution-integrity` → main
- [#14](https://github.com/Kelronmos/SWI-V2-Modules-11-22/pull/14) — ISO gate + EI
- [#13](https://github.com/Kelronmos/SWI-V2-Modules-11-22/pull/13) — Feature ISO claim gate

## Verification status (this session)

| Stage | Result |
|-------|--------|
| Live API inspection | OBSERVED |
| EI module restore on repair branch | COMMITTED |
| Payload deletion on repair branch | COMMITTED |
| ISO eligibility harden on PR #14 | COMMITTED (full validator restored) |
| pytest / compileall on repair tip | **NOT_RUN** |
| GitHub Actions full matrix on repair tip | **NOT_RUN** |
| Independent review | **NOT_RUN** |
