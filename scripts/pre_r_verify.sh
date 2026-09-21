#!/usr/bin/env bash
# SWI LAW-TRUTH pre-R verification — fail-closed
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
EVID="evidence/pre_r"
mkdir -p "$EVID/test-results" "$EVID/hashes" "$EVID/replay"

echo "=== SWI PRE-R VERIFICATION (LAW-TRUTH-BOUNDARY-01) ==="
echo "UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

SHA=$(git rev-parse HEAD)
echo "HEAD: $SHA"
echo "$SHA" > "$EVID/run.sha"
git status --short > "$EVID/run.status" || true

echo "=== PRE-R TESTS ==="
PYTHONPATH=. python -m pytest -q tests/pre_r/ --tb=line 2>&1 | tee "$EVID/test-results/pre_r.out"
echo "pre_r: PASS" > "$EVID/test-results/pre_r.status"

echo "=== FULL V2 TESTS ==="
PYTHONPATH=. python -m pytest -q test/ tests/ --tb=line 2>&1 | tee "$EVID/test-results/v2_full.out"
echo "v2_full: PASS" > "$EVID/test-results/v2_full.status"

echo "=== COMPILEALL ==="
python -m compileall -q experimental/ swi_v2/ tests/ test/ 2>&1 | tee "$EVID/test-results/compileall.out" || true

echo "=== HASH ARTIFACTS ==="
(
  cd "$EVID"
  find test-results -type f -print0 | sort -z | xargs -0 sha256sum
) > "$EVID/hashes/test-results.sha256" 2>/dev/null || true
sha256sum "$EVID/baseline.sha" "$EVID/run.sha" 2>/dev/null >> "$EVID/hashes/test-results.sha256" || true

echo "=== COMPLETE ==="
echo "Evidence under $EVID"
exit 0
