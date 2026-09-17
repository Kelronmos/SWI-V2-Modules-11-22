# SWI Controlled Module Manual Schema v1

**Status:** FROZEN schema (process standard)  
**Date (UTC):** 2026-09-17  
**Applies to:** M12, M13, … and any later controlled module  
**Does not authorize:** implementation of M12+ functionality

---

## Purpose

One evidence-bearing format for every module manual so modules do not invent their own standard.

```text
PRE-NAME
  → PURPOSE
  → BOUNDARY
  → CONTRACT
  → INPUT
  → OUTPUT
  → INVARIANTS
  → REJECTION CONDITIONS
  → IMPLEMENTATION
  → TESTS
  → RESULT
  → LIMITATION
  → CI EVIDENCE
  → AUDIT
  → SEAL
  → DEPENDENCY RELEASE
```

Doctrine: evidence before claim · boundary before expansion · contract before code · never claim what the code cannot demonstrate.

---

## Required sections (conformance checklist)

| # | Section | Required content |
|---|---------|------------------|
| 1 | **PRE-NAME** | Human/architectural name + explicit non-interpretations |
| 2 | **PURPOSE** | One narrow responsibility sentence |
| 3 | **BOUNDARY** | What this module owns vs upstream/downstream |
| 4 | **CONTRACT** | Link to frozen contract doc; status CONTRACT / IMPLEMENTING / SEALED |
| 5 | **INPUT** | Exact types/fields; reject list |
| 6 | **OUTPUT** | Exact types/fields; forbidden outputs |
| 7 | **INVARIANTS** | Determinism, preservation, no invention, immutability, etc. |
| 8 | **REJECTION CONDITIONS** | Fail-closed table |
| 9 | **IMPLEMENTATION** | Paths + symbols; or **NOT STARTED** |
| 10 | **TESTS** | Property → test path → assertion intent |
| 11 | **RESULT** | Observed pass/fail with command (no assumed counts) |
| 12 | **LIMITATION** | Permanent non-claims |
| 13 | **CI EVIDENCE** | Workflow, run ID, head_sha, conclusion — or **UNVERIFIED** |
| 14 | **AUDIT** | Contract ↔ code ↔ tests ↔ CI cross-check |
| 15 | **SEAL** | SEALED only with record + commit + CI; else **NOT SEALED** |
| 16 | **DEPENDENCY RELEASE** | Exact downstream type released (e.g. `NormalizedEvidence`) or **NONE** |

Missing required section → manual **non-conformant** → module must not be sealed.

---

## Status vocabulary (only these)

| Status | Meaning |
|--------|--------|
| `DESIGN` | Narrative only |
| `CONTRACT_FROZEN` | Contract committed; no claim of behaviour |
| `IMPLEMENTING` | Code in progress; not sealed |
| `TESTED` | Local/CI tests recorded; still not sealed |
| `SEALED` | Full chain independently evidenced |
| `BLOCKED` | Dependency or gate not met |

---

## Conformance tests (manual / CI later)

1. Every module under controlled development has a manual with all 16 sections.  
2. `SEALED` appears only if §13 has real run ID + head_sha and §15 points to a seal record.  
3. `IMPLEMENTATION` paths exist in the repo or status is `NOT STARTED`.  
4. Forbidden claims (truth, production keys, CRTG complete, etc.) do not appear as proven.  
5. Downstream modules name the **released type**, not “whatever upstream returned.”

---

## Sequencing relative to trust infrastructure

This schema is required **before** substantive M12+ functionality.

It does **not** replace:

- Foundation Seal 5 (signed V1 export)
- CRTG v0
- Standalone independent verifier
- Deterministic replay of sealed chains

Those remain higher priority than expanding module behaviour.

---

## M12 under this schema

| Item | State |
|------|--------|
| Contract draft | `docs/M12_CONTRACT.md` (field-aligned to `AdmittedInput`) |
| Implementation | **FROZEN / NOT STARTED** |
| Manual status | Pre-filled by contract; full 16-section manual completed at implementation time |
| Scaffold | `accepted_placeholder` only — boundary, not normalization |
