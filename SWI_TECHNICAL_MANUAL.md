# STRUCTURED WORKFLOW INTELLIGENCE (SWI)

## TECHNICAL ENGINEERING, REPAIR & EVIDENCE GOVERNANCE

**Complete Educational and Practical Engineering Manual**

| Field | Value |
|-------|--------|
| Version | 1.0 |
| Date | 1 November 2026 |
| Project | Structured Workflow Intelligence (SWI) |
| Organization | Trusts Motion |
| Audience | Beginners, students, developers, engineers, researchers, auditors, independent reviewers and technical leaders |

---

## DOCUMENT STATUS

**Classification:** Educational technical manual.

This document describes engineering principles, proposed architecture, reproducible procedures and governance requirements.

It does **not** establish that any particular SWI repository implements these controls. Implementation must be inspected and tested independently.

It does **not** establish ISO conformity, certification, production readiness or authorization.

---

# PART I — FOUNDATIONS

## CHAPTER 1. INTRODUCTION

### 1.1 Purpose

SWI is intended to structure how information, evidence, validation, authorization and execution interact within technical workflows.

The objective is to prevent a system from confusing information with evidence, evidence with proof, proof with permission, permission with execution, or successful testing with production authorization.

### 1.2 Learning objectives

Inspect repositories; establish reproducible environments; create and verify backups; build and review code; validate JSON/schemas; identify and repair defects without destroying historical evidence; create reproducible tests; map ISO requirements individually; generate evidence-based claims; keep unproven claims sealed; separate observation from authorization; protect people, infrastructure and ecosystems from unauthorized consequential actions.

### 1.3 Core principle

Observe before acting. Preserve before changing. Validate before claiming. Prove before unsealing. Authorize before consequential execution.

---

## CHAPTER 2. THE SWI GOVERNING PRINCIPLES

### 2.1 Fundamental distinctions

```text
DATA ≠ EVIDENCE ≠ PROOF ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
MATCH ≠ PERMIT ≠ EXECUTE
CAPABILITY ≠ PERMISSION
INSTRUCTION ≠ AUTHORIZATION
UNKNOWN ≠ FALSE
CI_GREEN ≠ SWI_AUTHORIZED
```

### 2.2 Illustrative workflow

```text
INPUT → OBSERVATION → CONTEXT BINDING → VALIDATION → EVIDENCE COLLECTION
→ EVIDENCE EVALUATION → GOVERNING AUTHORIZATION GATE
  → NOT AUTHORIZED → REFUSE / HOLD / SEAL
  → BOUNDED EXECUTION → MONITORING → POST-EXECUTION EVIDENCE → REVIEW
```

Teaching model only — not proof of an existing implementation.

### 2.3 Authorization formula

```text
Permit(a) ⟺ ∀L,G,S,H: C(a) ⊆ L ∩ G ∩ S ∩ H  ∧  E(a) ≠ ∅
```

Evidence must be relevant, valid, current and sufficient for the exact action. Existence of evidence alone does not establish permission.

---

# PART II — BACKUP AND RECOVERY

## CHAPTER 3. BEFORE, DURING AND AFTER BACKUPS

Preserve recoverability before every repair. Record repository, branch, commit, working tree and environment. Create BEFORE archives with SHA-256 verification. Maintain DURING checkpoints. Create AFTER backups. Rehearse restore in a disposable directory — never by overwriting the working tree.

Example:

```bash
DATE="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="$HOME/swi-backups"
mkdir -p "$BACKUP"
tar -czf "$BACKUP/swi-before-$DATE.tar.gz" -C "$(dirname "$PWD")" "$(basename "$PWD")"
sha256sum "$BACKUP/swi-before-$DATE.tar.gz" > "$BACKUP/swi-before-$DATE.sha256"
sha256sum -c "$BACKUP/swi-before-$DATE.sha256"
```

---

# PART III — MANUAL BUILD AND CODE REPAIR

## CHAPTERS 4–5

Inspect structure and dependencies; compileall for syntax only; follow project build instructions. Review workflows end-to-end. Repair: preserve → reproduce → root cause → minimal patch → tests → evidence. Automatic repair may assist formatting and derived artifacts; must not invent evidence, change proof status, approve ISO conformity, weaken security, or execute consequential external actions.

**Automatic repair ≠ automatic authorization.**

---

# PART IV — JSON AND STRUCTURAL VALIDATION

## CHAPTER 6

Levels: syntax, structural, schema (prefer Draft 2020-12), semantic, referential. Never convert UNKNOWN→FALSE/TRUE or MISSING→PASS. PROVEN requires evidence; PRODUCTION_AUTHORIZED requires separate authorization; ISO_CONFORMITY=ESTABLISHED must not come from incomplete mappings.

---

# PART V — ISO CLAIM GOVERNANCE

## CHAPTER 7

Every allocated standard remains visible. Every applicable requirement is mapped individually. Claims are generated from evidence criteria, not manual status edits. Missing/invalid/stale evidence, failed tests/replay, missing review, or undefined scope → **SEALED**. SWI claims are not ISO certification.

Proposed claim stages (not official ISO ratings): 0 Allocated → 1 Mapped → 2 Implemented/tested → 3 Evidence within scope → 4 Independently assessed → 5 Certified under an applicable scheme.

---

# PART VI — EVIDENCE AND REPRODUCIBILITY

## CHAPTER 8

Evidence records: ID, type, source, producer, timestamp, workflow, scope, commit, artifact, hash, test ref, result, replay instructions, reproducibility, limitations, review. Hash = byte integrity, not truth. Preserve failed and successful records.

---

# PART VII — AUTHORIZATION AND SAFETY

## CHAPTERS 9–10

Observation is not authorization. Consequence classes C0–C3; C2/C3 require human authority. Environmental stop conditions (missing baseline, unknown severe impact, missing permit, no monitoring, unresolved irreversible risk) → SEALED. AI assessments do not replace qualified professionals, communities or regulators.

---

# PART VIII — TESTING

## CHAPTER 11

Unit, integration, E2E, negative, adversarial, recovery, replay, reproducibility, safety. Example commands (adapt; execution is not implied by this text):

```bash
python3 -m compileall -q src tests tools
python3 tools/validate_iso_claim_status.py evidence/iso_claim_status.json
python3 -m pytest tests/test_iso_claim_gate.py -v --tb=short
python3 -m pytest -q
```

---

# PART IX — OPERATIONAL PROCEDURES

## CHAPTERS 12–14

Defect response, evidence discrepancies, unauthorized action attempts: preserve evidence, reproduce, seal claims where needed, repair, test, update evidence, record residual risk.

---

# PART X — REPORTING AND ACCEPTANCE

## CHAPTER 15

Required outputs: repository audit, backup manifest, defect/repair registers, changed-file inventory, JSON/test/ISO/evidence/replay/review/safety reports, final report with limitations. Production authorization remains a separate decision.

---

# PART XI — EDUCATIONAL LEARNING PATH

## CHAPTER 16

Beginner through expert exercises: from backups and JSON to adversarial bypass tests and scope-limited independent review reports.

---

# APPENDIX A — ILLUSTRATIVE PROJECT STRUCTURE

Inspect the actual repository before restructuring. One governing authorization spine must remain authoritative.

# APPENDIX B — ISO CLAIM JSON EXAMPLE

Illustrative sealed/unproven record only. Verify requirement references against the authoritative edition. See repository `evidence/iso_claim_status.json` for the live register format used by the claim-gate.

# APPENDIX C — EVIDENCE JSON EXAMPLE

Do not invent timestamps, results, hashes or review outcomes.

# APPENDIX D — REPRODUCIBLE REVIEW CHECKLIST

Repository identity, BEFORE/DURING/AFTER backups, validation, adversarial/regression tests, evidence/ISO updates, sealed unproven claims, separate production authorization, final report.

# APPENDIX E — FINAL GOVERNANCE STATEMENT

Never confuse components with proof, tests with authorization, allocation with conformity, hashes with truth, or observation with permission. Unproven requirements remain sealed. Consequential workflows must consider people, communities, infrastructure and ecosystems.

---

## FURTHER READING

- https://www.iso.org/
- https://json-schema.org/
- https://docs.python.org/3/
- https://git-scm.com/doc
- https://docs.pytest.org/

---

**END OF SWI TECHNICAL ENGINEERING, REPAIR & EVIDENCE GOVERNANCE MANUAL**

Trusts Motion · Structured Workflow Intelligence · Educational Edition 1.0 · 1 November 2026

This manual is a specification and educational reference. Compare each requirement against the actual repository and record IMPLEMENTED, TESTED, PROVEN, SEALED and AUTHORIZED separately. Retain previous editions; do not silently replace historical versions.
