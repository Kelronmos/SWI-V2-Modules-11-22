# SWI TEST REPORT

**Repository:** Kelronmos/SWI-V2-Modules-11-22
**Commit:** `28961cb3d51e88eb279c0989f7fa5f49ec7a16e0`
**Branch:** `feature/universal-halt-error-and-reports`
**Report type:** execution_integrity
**Report hash:** `7a0fe39f41628e3a7ee1c7c83ad03e2a9ac2aff41e799f760b698cb7f9f6ed65`

## Test command
`python3 scripts/generate_execution_integrity_report.py ; pytest -q test/adversarial/...`

## Test summary
- total: 10
- passed: 10
- failed: 0
- errors: 0
- skipped: 0

## Results (abbreviated)
- valid_bindings_execute: PASS (EXECUTION_ALLOWED, counter=1)
- Admission/Node/Identity/Route/Input/Policy FAIL: PASS (HALT, counter=0)
- direct_protected_operation_blocked: PASS
- retry_without_revalidation_no_execution: PASS
- persistent_failure_escalates: PASS

## Limitations
- Library/gate scope; V2 kernel paths not fully wired to ExecutionIntegrityGate.
- time_tolerance=0.0008 is experimental configuration only.

## NOT_PROVEN
- Process-wide / production enforcement
- Universal / regulatory safety

## Notes
- HASH != AUTHORITY != TRUTH
- TEST PASS = expected behavior demonstrated (including correct HALT).
