#!/usr/bin/env bash
# SWI law/authority boundary closure runner
#
# STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED · NOT PRODUCTION AUTHORIZED
#
# Establishes EXECUTION evidence only.
# Does NOT replace independent correspondence audit.
# Does NOT mark the boundary SEALED.
# Does NOT rewrite historical M11 seal records.
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUT="${SWI_LAW_CLOSURE_OUT:-/tmp/swi-law-closure}"
mkdir -p "$OUT"

echo "========================================"
echo "SWI LAW / AUTHORITY CLOSURE"
echo "========================================"

echo
echo "== BRANCH =="
BRANCH="$(git branch --show-current)"
echo "$BRANCH"
if [ "$BRANCH" != "experimental/law-ingestion-lane" ]; then
  echo "ERROR: expected experimental/law-ingestion-lane, got $BRANCH"
  exit 1
fi

echo
echo "== TIP =="
TIP="$(git rev-parse HEAD)"
echo "$TIP"

echo
echo "== WORKTREE =="
if [ -n "$(git status --short)" ]; then
  git status --short
  echo "ERROR: working tree is not clean"
  exit 1
fi
echo "(clean)"

echo
echo "== SOURCE SHAs =="
AUTH_SHA="$(git hash-object experimental/law/authority.py)"
REG_SHA="$(git hash-object experimental/law/registry.py)"
MODEL_SHA="$(git hash-object formal/z3/law_authority.py)"
echo "authority: $AUTH_SHA"
echo "registry:  $REG_SHA"
echo "formal:    $MODEL_SHA"

echo
echo "== PYTHON =="
python --version | tee "$OUT/python-version.txt"

echo
echo "== Z3 DEPENDENCY =="
python -m pip install -q -r formal/requirements.txt

echo
echo "== FORMAL MODEL =="
python formal/z3/law_authority.py | tee "$OUT/z3.txt"

# Machine-check expected formal contract (do not rely on visual PASS)
grep -E "F-001[[:space:]].*UNSAT" "$OUT/z3.txt" >/dev/null
grep -E "F-002[[:space:]].*UNSAT" "$OUT/z3.txt" >/dev/null
grep -E "F-003[[:space:]].*UNSAT" "$OUT/z3.txt" >/dev/null
grep -E "F-004[[:space:]].*UNSAT" "$OUT/z3.txt" >/dev/null
grep -E "F-005[[:space:]].*SAT" "$OUT/z3.txt" >/dev/null
grep -E "F-006[[:space:]].*UNSAT" "$OUT/z3.txt" >/dev/null
grep -F "MODEL RESULT: PASS" "$OUT/z3.txt" >/dev/null
echo "Z3 contract gates: OK"

echo
echo "== LAW TESTS =="
python -m pytest -q tests/law/ | tee "$OUT/law-pytest.txt"

echo
echo "== FULL V2 TESTS =="
python -m pytest -q | tee "$OUT/v2-pytest.txt"

echo
echo "== VERIFY =="
chmod +x scripts/verify.sh
./scripts/verify.sh | tee "$OUT/verify.txt"
grep -F "VERIFY: PASS" "$OUT/verify.txt" >/dev/null

echo
echo "== FINAL TIP =="
git rev-parse HEAD

echo
echo "========================================"
echo "EXECUTION COMPLETE"
echo "Artifacts under: $OUT"
echo "========================================"
echo
echo "IMPORTANT:"
echo "  Execution evidence is NOT an independent audit."
echo "  Do NOT mark SEALED until correspondence audit passes."
echo "  Historical M11 seal is a separate record — do not rewrite it."
echo "  EU/Botswana fixtures remain HOLD."
echo "  Production authorization remains separate."
