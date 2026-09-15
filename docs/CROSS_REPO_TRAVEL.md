# Cross-Repository Travel (V2)

**Handoff is the evidence envelope, not Module 10 and not `import swi_core`.**

```text
Serialized FoundationEvidenceEnvelope (JSON)
        → parse / field check
        → M11
        → AdmittedInput
        → Kernel
```

## Zero-base

No V1 Python dependency. No shared Trainer memory. No ambient singletons.

## Provenance

Do not mutate admitted V1 evidence in place. Derive **new** V2 records (admission, trust, task state) and keep them distinct.

## Integrity

Same five fields as V1. `created_at` optional metadata, not in digest.

## Status

| `verification_status` | Role |
|----------------------|------|
| `foundation_verified_test_fixture` | Unit fixture only |
| `v1_trainer_pipeline_completed` | V1 producer status after serialize |

## Rejects (must not reach Kernel)

Raw PipelineResult-shaped objects without envelope fields · bad integrity · bad version · bad status · missing fields
