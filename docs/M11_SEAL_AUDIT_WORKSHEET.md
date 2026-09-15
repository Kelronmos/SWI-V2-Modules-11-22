# M11 Seal Audit Worksheet

**Fill only from CI/test evidence. Use PASS / FAIL / NOT PROVEN only.**

```text
V2 SHA:
V1 producer SHA:
Workflow: two_checkout_travel
Run ID / URL:
CI status:
Date:
Auditor:
```

## A — Contract

| Item | Result |
|------|--------|
| Digest = payload, foundation_version, evidence_schema_version, evidence_id, source_reference | |
| created_at excluded | |
| Version reject unsupported | |
| Status: fixture vs v1_trainer_pipeline_completed documented | |

## B — Boundary

| Item | Result |
|------|--------|
| V2-only checkout in admit job | |
| import swi_core fails | |
| No PYTHONPATH/sys.path to V1 | |
| M10 not handoff | |

## C — Real producer

| Item | Result |
|------|--------|
| Artifact from V1 export script | |
| Not fixture substitution for primary proof | |

## D — Admission matrix

| Case | Expected | Actual |
|------|----------|--------|
| Valid V1 artifact | ACCEPT | |
| Payload altered | REJECT | |
| Integrity altered | REJECT | |
| Status altered | REJECT | |
| Missing field | REJECT | |
| Malformed JSON | REJECT | |
| Bad version | REJECT | |
| Raw non-envelope | REJECT | |

## E — Kernel isolation

| Item | Result |
|------|--------|
| Raw dict blocked | |
| Raw string blocked | |
| Reject does not reach Kernel | |

## F — Reproducibility

| Item | Result |
|------|--------|
| Tip-specific CI green | |

## G — Documentation

| Item | Result |
|------|--------|
| Status files agree; no false SEALED | |

## Decision

```text
[ ] ALL PASS → SEAL ELIGIBLE (then write M11_SEAL_RECORD.md)
[ ] ANY FAIL/NOT PROVEN → M11 remains NOT SEALED; blocker:
```
