#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="$(git rev-parse --show-toplevel)" || exit 2
cd "$ROOT" || exit 2

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="evidence/independent_replay/$STAMP"
mkdir -p "$OUT"

echo "SWI INDEPENDENT REPLAY"
echo "UTC=$STAMP"
echo "BRANCH=$(git branch --show-current)"
echo "BASE_COMMIT=$(git rev-parse HEAD)"

git rev-parse HEAD > "$OUT/base_commit.txt"
git branch --show-current > "$OUT/branch.txt"
git status --short --branch > "$OUT/status_before.txt"
git diff --binary > "$OUT/working_tree.patch"
git diff --cached --binary > "$OUT/index.patch"

python --version > "$OUT/python_version.txt" 2>&1
python -m pytest --version > "$OUT/pytest_version.txt" 2>&1

find test tests -type f \
  \( -name 'test_*.py' -o -name '*_test.py' \) \
  -not -path '*/__pycache__/*' \
  2>/dev/null | sort > "$OUT/test_inventory.txt"

echo "=== FULL REPOSITORY PYTEST RUN ==="
python -m pytest -q > "$OUT/pytest_full.txt" 2>&1
TEST_EXIT=$?
cat "$OUT/pytest_full.txt"
echo "$TEST_EXIT" > "$OUT/pytest_exit_code.txt"

echo "=== PYTHON COMPILE CHECK ==="
python -m compileall -q swi_v2 swi_policy_mapper \
  > "$OUT/compile.txt" 2>&1
COMPILE_EXIT=$?
echo "$COMPILE_EXIT" > "$OUT/compile_exit_code.txt"

echo "=== DIFF CHECK ==="
git diff --check > "$OUT/diff_check.txt" 2>&1
DIFF_EXIT=$?
echo "$DIFF_EXIT" > "$OUT/diff_check_exit_code.txt"

if [ "$TEST_EXIT" -eq 0 ] &&
   [ "$COMPILE_EXIT" -eq 0 ] &&
   [ "$DIFF_EXIT" -eq 0 ]; then
    STATUS="FULL_REPOSITORY_RUN_PASS_NOT_INDEPENDENTLY_REPRODUCED"
else
    STATUS="FAIL_OR_BLOCKED_NOT_SEALED"
fi

{
  echo "SWI INDEPENDENT REPLAY RECORD"
  echo "Timestamp UTC: $STAMP"
  echo "Base commit: $(git rev-parse HEAD)"
  echo "Branch: $(git branch --show-current)"
  echo "Test command: python -m pytest -q"
  echo "Test exit: $TEST_EXIT"
  echo "Compile command: python -m compileall -q swi_v2 swi_policy_mapper"
  echo "Compile exit: $COMPILE_EXIT"
  echo "Diff check exit: $DIFF_EXIT"
  echo "Overall status: $STATUS"
  echo
  echo "CLAIM: Repository tests were invoked and their output recorded."
  echo "LIMITATION: This run is not an independent reproduction."
  echo "LIMITATION: Compile success is not test success."
  echo "LIMITATION: Test success is not proof, seal, compliance or authorization."
  echo "HUMAN AUTHORITY: Not authenticated by this runner."
  echo "PROVEN: NO"
  echo "SEALED: NO"
  echo "PRODUCTION AUTHORIZED: NO"
} > "$OUT/REPLAY_RECORD.txt"

(
  cd "$OUT" || exit 1
  sha256sum \
    base_commit.txt branch.txt status_before.txt \
    working_tree.patch index.patch \
    python_version.txt pytest_version.txt \
    test_inventory.txt pytest_full.txt pytest_exit_code.txt \
    compile.txt compile_exit_code.txt \
    diff_check.txt diff_check_exit_code.txt \
    REPLAY_RECORD.txt > SHA256SUMS
)

echo
echo "=== REPLAY SUMMARY ==="
cat "$OUT/REPLAY_RECORD.txt"
echo
echo "EVIDENCE DIRECTORY: $OUT"
echo "SHA256:"
cat "$OUT/SHA256SUMS"

if [ "$TEST_EXIT" -ne 0 ] ||
   [ "$COMPILE_EXIT" -ne 0 ] ||
   [ "$DIFF_EXIT" -ne 0 ]; then
    exit 1
fi
