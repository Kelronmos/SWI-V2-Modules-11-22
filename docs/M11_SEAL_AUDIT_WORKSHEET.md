# M11 Seal Audit Worksheet

Status: **AUDIT IN PROGRESS — NOT SEALED**

This worksheet is the evidence inventory for the M11 seal decision. It must be
understandable without relying on memory: every row needs a concrete
artifact, file path, test name, or CI run reference — not a restated claim.

Do not write `PASS` alone. Write `PASS — supported by <specific evidence>`.
Leave a row `PENDING` until the evidence exists.

---

## A — Contract Freeze

| Requirement | Evidence | Test / file / CI reference | Result | Reviewer note |
|---|---|---|---|---|
| V1 Foundation Evidence Contract is frozen (schema, field set, versioning) | | | PENDING | |
| No contract-breaking change has landed since freeze | | | PENDING | |

## B — Architectural Boundary

| Requirement | Evidence | Test / file / CI reference | Result | Reviewer note |
|---|---|---|---|---|
| V2 does not import V1 code at runtime | | | PENDING | |
| M11 consumes only serialized evidence, never a live V1 object | | | PENDING | |

## C — Real Producer

| Requirement | Evidence | Test / file / CI reference | Result | Reviewer note |
|---|---|---|---|---|
| `export_foundation_evidence()` (or equivalent) runs against real V1 | | | PENDING | |
| Output artifact filename recorded | e.g. `foundation_evidence.json` | | PENDING | |
| SHA-256 of artifact recorded (generated, not hand-typed) | | | PENDING | |

## D — Admission Behaviour

| Requirement | Evidence | Test / file / CI reference | Result | Reviewer note |
|---|---|---|---|---|
| Positive test: real serialized evidence → ACCEPT → `AdmittedInput` | | | PENDING | |
| Payload-tampered artifact (integrity ref unchanged) → REJECT | | | PENDING | |
| Integrity-reference-tampered artifact (payload unchanged) → REJECT | | | PENDING | |
| Malformed JSON → REJECT | | | PENDING | |
| Missing `payload` → REJECT | | | PENDING | |
| Missing `foundation_version` → REJECT | | | PENDING | |
| Missing `evidence_schema_version` → REJECT | | | PENDING | |
| Missing `evidence_id` → REJECT | | | PENDING | |
| Missing `source_reference` → REJECT | | | PENDING | |
| Unsupported foundation version → REJECT | | | PENDING | |
| Unsupported evidence schema version → REJECT | | | PENDING | |
| Unsupported verification status → REJECT | | | PENDING | |
| Raw dict (not envelope) → REJECT | | | PENDING | |
| `PipelineResult`-shaped object → REJECT | | | PENDING | |

## E — Kernel Isolation

| Requirement | Evidence | Test / file / CI reference | Result | Reviewer note |
|---|---|---|---|---|
| `AdmittedInput` → Kernel succeeds | | | PENDING | |
| Raw dict → Kernel fails | | | PENDING | |
| Rejected M11 input → Kernel fails | | | PENDING | |
| V1 import unavailable inside V2 admission environment (no `PYTHONPATH`/`sys.path` manipulation) | `import swi_core` fails naturally | | PENDING | |

## F — Reproducibility

| Requirement | Evidence | Test / file / CI reference | Result | Reviewer note |
|---|---|---|---|---|
| Two-checkout CI (`two_checkout_travel.yml`) green: Job 1 produces V1 evidence, Job 2 admits with V1 not importable | | | PENDING | |
| Passes on Python 3.10 | | | PENDING | |
| Passes on Python 3.11 | | | PENDING | |
| Passes on Python 3.12 | | | PENDING | |
| Exact V1 commit SHA recorded | | | PENDING | |
| Exact V2 commit SHA recorded | | | PENDING | |

## G — Documentation Honesty

| Requirement | Evidence | Test / file / CI reference | Result | Reviewer note |
|---|---|---|---|---|
| All Markdown claims containing "complete / secure / verified / sealed / production-ready / universal / safe / identity / truth / CRTG / Foundation Seal 5 / V2 complete / Modules 11–22 complete" classified as PROVEN / PARTIALLY PROVEN / DESIGN / STALE / UNSUPPORTED / CONTRADICTED | | | PENDING | |
| No claim in README or docs exceeds what this worksheet demonstrates | | | PENDING | |

---

## Seal Gate

M11 may move to `SEALED` only when **all** of A–G above read `PASS` with
cited evidence, and:

- [ ] Exact V2 SHA identified
- [ ] Exact V1 SHA identified
- [ ] Real producer demonstrated
- [ ] Serialized artifact identified (filename + SHA-256)
- [ ] Tamper rejection demonstrated (both payload and integrity-reference paths)
- [ ] Kernel isolation demonstrated
- [ ] Two-checkout CI green across the full Python matrix
- [ ] Documentation reconciled against evidence

Until every box is checked with a cited row above, status remains
`AUDIT_PENDING`. Do not set `SEALED` in `M11_AUDIT_SUMMARY.json` or in this
worksheet as a shortcut to unblock M12.
