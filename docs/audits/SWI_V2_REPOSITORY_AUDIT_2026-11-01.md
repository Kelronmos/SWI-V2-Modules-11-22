# SWI V2 repository audit — 1 November 2026

## Executive result

**Repository:** `Kelronmos/SWI-V2-Modules-11-22`  
**Default branch:** `main`  
**Audited HEAD:** `b226564b5f9401a1a05703c4befee9f371460437`  
**Latest commit:** `Add the reproduced ISO compatibility claim record and Level 1 status evidence based on the local independent test snapshot.`  
**Latest push:** 2026-11-01 15:02:55 UTC  
**Repository visibility:** Public  
**Branches observed:** 40  

### Verdict

**Overall engineering rating: 3/10 — NOT READY for a clean verification baseline.**

This rating is not a measure of the project's intent or research value. It reflects the current public `main` checkout's reproducibility and test state. The strongest finding is a blocking defect in the dynamically reconstructed execution-integrity source: GitHub Actions fails identically under Python 3.10, 3.11 and 3.12 before the adversarial tests can run.

`PROVEN=NO`, `SEALED=NO`, `PRODUCTION_AUTHORIZED=NO` remain the appropriate status. The ISO compatibility claim is explicitly recorded as not established.

## Clone and local execution status

A local clone was attempted with:

```bash
git clone --no-tags https://github.com/Kelronmos/SWI-V2-Modules-11-22.git repo
```

It did **not** complete in this execution environment: DNS resolution failed (`Could not resolve host: github.com`). Therefore this audit did not produce a complete Git working copy, did not fetch remote refs locally, and did not execute the test suite locally. The branch and CI findings below were retrieved from GitHub's repository/API and workflow records. Do not represent them as local test execution.

## Branch inventory

The repository API returned these 41 branches:

1. `architecture/kernel-progression-human-authority`
2. `audit/governing-permit-stage-2-2026-10-15`
3. `docs/acceptance-and-empty-capability-2026-10-31`
4. `docs/control-freshness-offline-2026-10-02`
5. `docs/m12-controlled-manual-test`
6. `evidence/complete-closure-2026-09-30`
7. `evidence/s9-process-scope-baseline`
8. `evidence/s9-x1-irrelevant-evidence-contract`
9. `evidence/zkvm-future-evidence-technique`
10. `experimental/cek-alignment-monitor`
11. `experimental/institutional-levels-demo`
12. `experimental/law-ingestion-lane`
13. `experimental/privacy-domain`
14. `experimental/s9-adversarial-authority-chain`
15. `experimental/s9-evaluation-harness`
16. `experimental/s9-zkp-research`
17. `feature/execution-boundary-final-closure`
18. `feature/execution-boundary-hardening`
19. `feature/execution-integrity-boundary`
20. `feature/iso-claim-gate`
21. `feature/observation-claim-separation-2026-10-29`
22. `feature/swi-iso-evidence-replay-lab`
23. `feature/universal-halt-error-and-reports`
24. `fix/ci-full-history`
25. `fix/m11-status-reconciliation`
26. `fix/new-information-boundary`
27. `governance/universal-path-claim-benefit-framework`
28. `hardening/m11-independent-verification`
29. `main`
30. `open-016-failure-tests`
31. `recovery/execution-integrity-restore`
32. `recovery/swi-full-implementation`
33. `repair/execution-integrity-2026-10-11`
34. `repair/execution-integrity-2026-10-12`
35. `repair/iso-evidence-replay-integrity`
36. `review/iso-gate-repro-2026-11-01`
37. `review/swi-v2-zip-reconciliation-2026-11-01`
38. `s9/zip-proof-package-harness`
39. `security/empty-capability-never-permit-2026-10-29`
40. `test/gate07-mutation`

**Note:** The branch listing returned 40 distinct names. Confirm completeness with `git ls-remote --heads origin` after network access is restored.

## Latest GitHub Actions result

Workflow: `SWI V2 Modules 11-22 Verification`  
Run: `41319201764` (run number 318)  
Commit: `b226564b5f9401a1a05703c4befee9f371460437`  
Status: **FAILURE**  

| Python | Compile | M11/contract tests | Execution-integrity adversarial | Later steps |
|---|---|---|---|---|
| 3.10 | PASS | 14 passed | Collection ERROR | Skipped |
| 3.11 | PASS | 14 passed | Collection ERROR | Skipped |
| 3.12 | PASS | 14 passed | Collection ERROR | Skipped |

All three jobs stop at `test/adversarial/test_execution_integrity.py`. The full suite, universal halt tests, gate PASS/FAIL matrix, report generation, and `verify.sh` are skipped. Final summary job is skipped.

### Root cause observed in the CI logs and source tree

`swi_v2/execution_integrity.py` reconstructs source code by concatenating `_ei_payload_0.txt`, `_ei_payload_1.txt`, etc. It stops at the first missing sequential payload. The current `main` tree contains `_ei_payload_0.txt`, `_ei_payload_1.txt`, and `_ei_payload_4.txt`, but not `_ei_payload_2.txt` or `_ei_payload_3.txt`.

Because the loader stops at missing part 2, payload 4 is never read. The resulting truncated source fails compilation while importing the adversarial test:

```text
File "swi_v2/execution_integrity_body.py", line 56
    authority.token:
IndentationError: unexpected indent
```

This is a deterministic source packaging/reconstruction defect, not a Python-version-specific failure. The CI workflow does not reach the rest of the test suite, so its result cannot support a green repository claim.

## Additional evidence reviewed

### ISO compatibility claim

`evidence/iso_compatibility_claim_level_1.json` records:

- `claim_proven: false`
- `claim_true: false`
- `claim_false: true`
- `standard_status: NOT_ESTABLISHED`
- `color: red`
- no ISO conformity, certification, sealing, or production authorization
- optional ISO validator and ISO gate test files absent from this checkout

This is appropriately conservative. It is not evidence of ISO conformity.

### Imported local verification snapshot

`Local Independent Tests/current_verification_run.json` describes a source ZIP snapshot without Git metadata. It records:

- full suite: 703 passed, 1 failed, 5 collection errors
- compileall: passed
- three DCRE schemas: valid
- truth: `UNKNOWN`
- state: `PARTIAL`
- level: `L3_TESTED`
- Git checkout: absent
- remote access: DNS failure
- CI: not run for that local ZIP snapshot

`PUBLIC_MAIN_RECONCILIATION_2026-11-01.md` explicitly says the ZIP has no `.git` metadata and is not proven to represent a particular upstream commit. Its local test results must not be attributed to the public `main` commit audited here.

## Strengths

- The repository documents important non-claims and distinguishes tested, proven, sealed and production-authorized states.
- M11 admission/contract test group passes in current CI (14 tests per Python matrix job).
- The ISO compatibility claim is not falsely promoted; it remains `NOT_ESTABLISHED`.
- The repository contains substantial adversarial, kernel, law-boundary, replay, and evidence-oriented test coverage.
- CI checks for full Git history rather than silently accepting a shallow checkout.

## Blocking issues / priorities

1. **P0 — Restore the complete execution-integrity source.** Restore and verify the exact missing payload sequence or replace the fragile base64-fragment loader with a normal tracked Python module. Do not synthesize missing source from assumptions. Verify the reconstructed source hash against a trusted source snapshot.
2. **P0 — Add an explicit payload integrity check.** Require all expected parts, validate their count/order and SHA-256 before decoding/compiling. Missing or altered parts must fail with a clear controlled error before test collection.
3. **P0 — Run the complete CI pipeline.** Re-run Python 3.10/3.11/3.12 after repair. Require the execution-integrity adversarial suite, universal halt contract, gate matrix, full pytest suite, report generation, and `verify.sh` to execute; no skipped verification stage should be mistaken for pass.
4. **P1 — Reconcile branch state.** Fetch all remote heads and compare them with `main`; identify stale, duplicate-purpose, and superseded branches. Do not merge recovery/experimental branches without source and ancestry review.
5. **P1 — Reconcile local ZIP evidence against a genuine Git checkout.** Preserve the ZIP's independent results as snapshot-scoped evidence only. Establish exact commit ancestry and tree hashes before attributing them to public `main`.
6. **P1 — Keep ISO status red/not established.** Do not change the claim color/status until the applicable standard requirements are individually mapped, evidenced, independently verified, reproducible and correctly scoped.

## Rating breakdown

| Area | Rating | Basis |
|---|---:|---|
| Architecture and boundary doctrine | 7/10 | Clear separation of claim/evidence/authority and explicit non-claims in project records. |
| Test design and coverage intent | 7/10 | Broad adversarial and boundary test inventory exists. |
| Current executable integrity | 1/10 | Core execution-integrity import is broken by missing payload parts. |
| CI reliability | 2/10 | All three supported Python jobs fail at the same collection error; remaining checks skipped. |
| Evidence/provenance discipline | 5/10 | Good status discipline, but source ZIP evidence cannot be attributed to a Git commit and snapshot discrepancies remain. |
| Reproducibility of public main | 1/10 | Fresh local clone blocked in this environment; CI itself cannot complete. |

**Overall: 3/10 — research/prototype repository with meaningful governance design, but current `main` is not a passing verification baseline.**

## Reproduction commands after network access is restored

```bash
git clone https://github.com/Kelronmos/SWI-V2-Modules-11-22.git
cd SWI-V2-Modules-11-22
git fetch --all --prune
git branch -a
git log --graph --oneline --decorate --all -n 100
python -m pip install -r requirements.txt
python -m compileall -q swi_v2
python -m pytest -q test/test_module11_admission.py test/test_foundation_contract.py
python -m pytest -q test/adversarial/test_execution_integrity.py
python -m pytest -q test/adversarial/test_universal_halt.py
python -m pytest -q test/adversarial/test_gate_pass_fail_matrix.py
python -m pytest -q
./scripts/verify.sh
```

Do not record the repository as verified until all required commands complete successfully on the exact recorded HEAD and the CI run is green.
