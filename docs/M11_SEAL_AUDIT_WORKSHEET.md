# M11 Seal Audit Worksheet

**Fill only from CI/test evidence. Use PASS / FAIL / NOT PROVEN only.**

```text
V2 SHA (current tip):          9e13e83753cda46f5a09e45053c3902e678f4657
V2 SHA (last CI-verified tip): 061a47ff23705684179cb48836051c8b097e1b65
V1 producer SHA:               be31dd733e7fba17ceddb0b142a075abcfca890a
Workflow:                      two_checkout_travel.yml
Run ID:                        34987307390
CI status (audited tip):       GREEN
Date:                          15 September 2026
Auditor:                       formal audit per NEXT STAGE EXECUTION INSTRUCTION
```

## A — Contract

| Item | Result |
|------|--------|
| Digest = payload, foundation_version, evidence_schema_version, evidence_id, source_reference | PASS |
| created_at excluded | PASS |
| Version reject unsupported | PASS |
| Status: fixture vs v1_trainer_pipeline_completed documented | PASS |

**Evidence:** `swi_v2/kernel/admission.py` `compute_integrity_reference` and `admit_foundation_input`; tests in `test/test_serialized_v1_travel.py`.

## B — Boundary

| Item | Result |
|------|--------|
| V2-only checkout in admit job | PASS |
| import swi_core fails | PASS |
| No PYTHONPATH/sys.path to V1 | PASS |
| M10 not handoff | PASS |

**Evidence:** Admission accepts only envelope/mapping; raw types raise; no V1 import in V2 path; enforcement requires `AdmittedInput`.

## C — Real producer

| Item | Result |
|------|--------|
| Artifact from V1 export script | NOT PROVEN |
| Not fixture substitution for primary proof | NOT PROVEN |

**Evidence note:** Unit tests use V1-*shaped* fixtures + JSON round-trip. Contracts still label the envelope PROPOSED. Historical two-checkout CI claimed real producer; tip-specific confirmation of live V1 export → artifact → V2 admit on the *current* tip is still required.

## D — Admission matrix

| Case | Expected | Actual |
|------|----------|--------|
| Valid V1 artifact | ACCEPT | PASS |
| Payload altered | REJECT | PASS |
| Integrity altered | REJECT | PASS |
| Status altered | REJECT | PASS |
| Missing field | REJECT | PASS |
| Malformed JSON | REJECT | PASS |
| Bad version | REJECT | PASS |
| Raw non-envelope | REJECT | PASS |

**Evidence:** `test/test_serialized_v1_travel.py` (including `test_malformed_json_rejected_at_boundary`).

## E — Kernel isolation

| Item | Result |
|------|--------|
| Raw dict blocked | PASS |
| Raw string blocked | PASS |
| Reject does not reach Kernel | PASS |

**Evidence:** `require_admitted` + `test_rejection_never_reaches_module12`.

## F — Reproducibility

| Item | Result |
|------|--------|
| Tip-specific CI green | NOT PROVEN (for current tip) |

**Evidence note:** Run 34987307390 GREEN for tip `061a47f` / V1 `be31dd7`. Current tip is documentation-only; historical green does not automatically prove the new commit.

## G — Documentation

| Item | Result |
|------|--------|
| Status files agree; no false SEALED | PASS |

**Evidence:** MODULE_STATUS, evidence manuals, closing manuals consistently show CI_VERIFIED + NOT SEALED. No false SEALED claims.

## Decision

```text
[ ] ALL PASS → SEAL ELIGIBLE (then write M11_SEAL_RECORD.md)
[x] ANY FAIL/NOT PROVEN → M11 remains NOT SEALED; blocker:
    C — real-producer primary path still needs tip-specific confirmation
    F — current tip has not been re-proven by two-checkout CI
```
