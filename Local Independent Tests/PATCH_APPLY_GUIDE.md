# Apply guide — SWI public-main reconciliation patch

## Important provenance boundary

This patch was generated against the supplied source archive `SWI-V2-Modules-11-22-main (9).zip`, SHA-256:

`96048f70821ef034e635074bba97a6e0c71aeb3bd831b636cc6f94c2ab75c625`

That archive contains no `.git` metadata. The external reviewer narrative names public `main` as `51a67e4`, but this workspace could not prove that the ZIP is exactly that commit. Do not assume upstream ancestry from this patch.

## Apply to a genuine clone

1. Clone/fetch the repository and confirm the intended base:

   ```bash
   git fetch origin --prune
   git switch main
   git rev-parse HEAD
   git status --short
   ```

2. Create a feature branch from the genuine `main` checkout:

   ```bash
   git switch -c feature/swi-dcre-public-main-reconciliation
   ```

3. Copy `SWI_PUBLIC_MAIN_RECONCILIATION.patch` to the clone and test applicability:

   ```bash
   git apply --check SWI_PUBLIC_MAIN_RECONCILIATION.patch
   ```

   If the check fails, stop. Do not force-apply, overwrite files, or use the synthetic local Git bundle. Reconcile the differing upstream files first.

4. Apply the patch without rewriting upstream history:

   ```bash
   git apply SWI_PUBLIC_MAIN_RECONCILIATION.patch
   ```

5. Install dependencies and reproduce the checks:

   ```bash
   python -m pip install -r requirements.txt
   python -m pytest -q tests/claims
   python tools/validate_claim_schemas.py --summary evidence/claims/current_verification_run.json
   python tools/verify_claim_history.py evidence/claims/claim_history.jsonl
   python -m compileall -q swi_v2 tools tests
   python -m pytest -q --continue-on-collection-errors
   ```

   The supplied source snapshot's full suite is recorded as failing with five collection errors and one additional kernel freshness ancestry failure when no Git metadata is present. A genuine clone may change the ancestry test result, but it must not hide the five collection errors. Update the evidence record with results from the actual commit before making any public-main claim.

6. Review the diff and open a pull request. Do not push directly to `main` or merge until the full required CI checks pass and the review is complete.

## Governance

The README status panel remains `NOT VERIFIED` for the supplied ZIP snapshot. `PROVEN=NO`, `SEALED=NO`, ISO conformity `NOT_ESTABLISHED`, and `PRODUCTION_AUTHORIZED=NO`. This patch adds development claim/evidence reporting only; it does not grant authority or authorize execution.
