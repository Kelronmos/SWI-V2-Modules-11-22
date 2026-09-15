#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:-}:$ROOT"

run_check() {
  local name="$1"
  shift
  echo "==> $name"
  "$@"
}

run_check "Compile" python -m compileall -q swi_v2
run_check "Module 11 admission tests" python -m pytest -q test/test_module11_admission.py
run_check "Foundation contract tests" python -m pytest -q test/test_foundation_contract.py
run_check "Full pytest suite" python -m pytest -q
run_check "Documentation present" test -f docs/V1_FOUNDATION_CONTRACT.md -a -f docs/MODULE_STATUS.md -a -f docs/RELEASE_GATE.md
echo "VERIFY: PASS"
