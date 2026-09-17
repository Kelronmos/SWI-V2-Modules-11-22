# V4.7 Verifier Hardening Status

## Problem (v1 score_module)
E4 could promote on seal_record_ok + (ci_verified OR audit_summary_ok).

## Fix (v2-strict-e4)
E4 requires ALL of:
- seal record parses SEALED
- seal binds V2 SHA + CI run ID
- audited commit matches seal SHA (prefix)
- CI run matches seal run
- ci_verified with --ci-independent (not self-attested alone)
- implementation surface + test paths

## Backtests local
- fake seal (SEALED text only) → NOT E4 — PASS
- audit JSON alone → NOT E4 — PASS
- demo M11 regression → E4_SEALED — PASS
- M12 stub → E0 — PASS

## Still required for full independence
- GitHub Actions API resolution of run head_sha/status/conclusion
- Property-level test mapping (function → assertion)
- Full adversarial suite in CI

## Gate before M12
Verifier hardening + M11 independent rediscovery — not M12 implementation.

## Incident
Commit c49d527 briefly wrote placeholder content; this commit restores the full strict-E4 verifier.
