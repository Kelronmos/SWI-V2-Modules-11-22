#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# SWI UNIVERSAL TEST / DEMONSTRATION RUNNER (macOS / Linux)
# ============================================================
# TEST ONLY — does not establish production authorization
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo
echo "============================================================"
echo "SWI UNIVERSAL TEST / DEMONSTRATION RUNNER"
echo "============================================================"
echo "MODE                  : TEST + SIMULATION + EVIDENCE"
echo "REAL-WORLD ACTION     : NONE"
echo "PRODUCTION AUTHORIZED : NO"
echo "============================================================"
echo

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found"
    echo "PRODUCTION AUTHORIZED: NO"
    echo "PROVEN               : NO"
    echo "SEALED               : NO"
    exit 1
fi

echo "Python: $(python3 --version)"
echo
echo "Launching runner..."
echo

python3 -m runner.main "$@"
EXITCODE=$?

echo
echo "============================================================"
echo "SWI RUN COMPLETE"
echo "============================================================"
echo "Reports are under: swi-test-workspace/reports"
echo
echo "PRODUCTION AUTHORIZED: NO"
echo "PROVEN               : NO"
echo "SEALED               : NO"
echo "============================================================"
echo

exit "${EXITCODE}"
