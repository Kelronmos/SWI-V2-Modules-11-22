# SWI TEST REPORT

**Commit:** `6e5fdf11d8c65bcd802911fec0d8735482e09529`
**Branch:** `feature/universal-halt-error-and-reports`
**Report hash (time-stable):** `7a1565fa5c2d2ac881d4eba9e0137ff6814db5e04f61344ee6bdb3ee2da75b6f`

## Summary
- Adversarial suite: 50 passed
- Report generator checks: 10/10 PASS
- Report SHA-256 is time-stable (excludes generated_at / test timestamps / volatile evidence_hash)

## Results
- valid_bindings_execute: PASS decision=EXECUTION_ALLOWED exec=True
- Admission/Node/Identity/Route/Input/Policy FAIL: PASS decision=HALT exec=False
- direct_protected_operation_blocked: PASS
- retry_without_revalidation_no_execution: PASS
- persistent_failure_escalates: PASS

## Reproduce
```
git checkout 6e5fdf11d8c65bcd802911fec0d8735482e09529
python3 -m pytest -q test/adversarial/
python3 scripts/generate_execution_integrity_report.py
# REPORT_HASH must equal 7a1565fa5c2d2ac881d4eba9e0137ff6814db5e04f61344ee6bdb3ee2da75b6f
```

HASH != AUTHORITY != TRUTH
