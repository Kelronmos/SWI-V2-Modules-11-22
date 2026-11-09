# Snyder Runtime v1.0 Integrated Critical Audit

Target baseline:
44a6af93328691b6aff4c5ee35d3790f3c9ac2aa

Purpose:
Run critical tests against actual SWI source and selected existing
regression tests. Record failures, limitations and evidence.

This package does not modify SWI runtime source, authorize execution,
seal a module, or authorize production.

Result vocabulary:
PASS / FAIL / BLOCKED / NOT_RUN

TESTED != PROVEN != SEALED != PRODUCTION_AUTHORIZED

The runner records the exact tested HEAD and worktree status.
