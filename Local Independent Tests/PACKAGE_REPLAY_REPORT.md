# Reproducibility check of the delivered ZIP

The delivered repository ZIP was extracted to a fresh directory without Git metadata and checked again.

| Check | Result | Exit |
|---|---|---:|
| `python -m pytest -q tests/claims --tb=short` | 48 passed | 0 |
| `python -m compileall -q swi_v2 tools tests` | Passed | 0 |
| `python tools/validate_claim_schemas.py --summary evidence/claims/current_verification_run.json` | 3 schemas valid; aggregate record valid | 0 |
| `python tools/verify_claim_history.py evidence/claims/claim_history.jsonl` | 18 records; hash chain valid | 0 |
| `python -m pytest -q --continue-on-collection-errors --tb=short` | 703 passed, 1 failed, 5 collection errors, 1 warning | 1 |
| `python -m pytest -q --tb=short` | 5 collection errors | 2 |

The additional kernel freshness failure is caused by the absence of `.git` metadata in the source archive and is recorded separately in the repository run evidence. The full-suite collection blockers remain unresolved. This replay does not establish upstream ancestry, GitHub CI, proof, sealing, ISO conformity, or production readiness.
