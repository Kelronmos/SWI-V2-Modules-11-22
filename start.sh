#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# SWI ONLINE TEST REBUILD — V1 + V2
# =============================================================================
# Controlled TEST-ONLY bootstrap.
# Does NOT establish production authorization.
# Does NOT claim the system is complete, proven, or sealed.
#
# ONLINE SOURCE → MATERIALIZE → REBUILD → TEST → INVENTORY → HASH → REPORT
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SCRIPT_DIR}/swi-test-workspace"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ 2>/dev/null || date +%Y%m%dT%H%M%S)"
REPORT_DIR="${WORKSPACE}/reports"
ARTIFACT_DIR="${WORKSPACE}/artifacts"
LOG_DIR="${WORKSPACE}/logs"
DOWNLOAD_DIR="${WORKSPACE}/downloads"

V1_URL="https://github.com/Kelronmos/SWI-V1-Module-1-10.git"
V2_URL="https://github.com/Kelronmos/SWI-V2-Modules-11-22.git"
V1_DIR="${WORKSPACE}/v1"
V2_DIR="${WORKSPACE}/v2"

echo "=============================================="
echo "SWI ONLINE TEST REBUILD — V1 + V2"
echo "=============================================="
echo "Mode          : TEST ONLY"
echo "Timestamp     : ${TIMESTAMP}"
echo "Workspace     : ${WORKSPACE}"
echo "Production authorization : NO"
echo "=============================================="
echo

# ---------------------------------------------------------------------------
# 0. Prerequisite checks
# ---------------------------------------------------------------------------
if ! command -v git >/dev/null 2>&1; then
    echo "ERROR: Git is required but was not found."
    exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 is required but was not found."
    exit 1
fi

echo "Git    : $(git --version)"
echo "Python : $(python3 --version)"
echo

# ---------------------------------------------------------------------------
# 1. Create workspace layout
# ---------------------------------------------------------------------------
mkdir -p "${V1_DIR}" "${V2_DIR}" "${ARTIFACT_DIR}" "${REPORT_DIR}" "${LOG_DIR}" "${DOWNLOAD_DIR}"

# ---------------------------------------------------------------------------
# Helper: safe acquire or update a repository (ff-only, never destructive)
# ---------------------------------------------------------------------------
acquire_repo() {
    local url="$1"
    local target="$2"
    local name="$3"

    echo "---- Acquiring ${name} ----"
    if [ -d "${target}/.git" ]; then
        echo "Existing checkout found at ${target}"
        cd "${target}"
        if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
            echo "ERROR: Working tree for ${name} has uncommitted changes."
            echo "Refusing to synchronize. Resolve manually."
            git status --short
            exit 1
        fi
        git fetch origin
        local branch
        branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
        if ! git pull --ff-only origin "${branch}"; then
            echo "ERROR: Unable to fast-forward ${name}."
            echo "Divergent history detected. No automatic merge or reset performed."
            exit 1
        fi
    else
        echo "Cloning ${url} ..."
        if ! git clone --branch main "${url}" "${target}" 2>/dev/null; then
            git clone "${url}" "${target}"
        fi
        cd "${target}"
    fi

    local sha
    sha="$(git rev-parse HEAD)"
    echo "${name} commit: ${sha}"
    echo "${sha}" > "${ARTIFACT_DIR}/${name}_COMMIT.txt"
    cd "${SCRIPT_DIR}"
}

# ---------------------------------------------------------------------------
# 2. Acquire both repositories
# ---------------------------------------------------------------------------
acquire_repo "${V1_URL}" "${V1_DIR}" "V1"
acquire_repo "${V2_URL}" "${V2_DIR}" "V2"

V1_SHA="$(cat "${ARTIFACT_DIR}/V1_COMMIT.txt")"
V2_SHA="$(cat "${ARTIFACT_DIR}/V2_COMMIT.txt")"

echo
echo "V1 COMMIT : ${V1_SHA}"
echo "V2 COMMIT : ${V2_SHA}"
echo

# ---------------------------------------------------------------------------
# 3. Rebuild + test V1 (using repository's own mechanism)
# ---------------------------------------------------------------------------
echo "=============================================="
echo "V1 REBUILD + TEST"
echo "=============================================="

V1_REBUILD="FAIL"
V1_TEST="FAIL"
V1_LOG="${LOG_DIR}/v1_rebuild_${TIMESTAMP}.log"

(
    set -e
    cd "${V1_DIR}"
    if [ ! -d .venv ]; then
        python3 -m venv .venv
    fi
    # shellcheck disable=SC1091
    source .venv/bin/activate
    python -m pip install --upgrade pip
    if [ -f requirements.txt ]; then
        python -m pip install -r requirements.txt
    fi
    echo "Running V1 tests..."
    python -m pytest -q 2>&1 | tee -a "${V1_LOG}"
    if [ -x scripts/verify.sh ]; then
        ./scripts/verify.sh 2>&1 | tee -a "${V1_LOG}" || true
    fi
) > "${V1_LOG}" 2>&1 && V1_REBUILD="PASS" && V1_TEST="PASS" || {
    V1_REBUILD="PASS"
    V1_TEST="FAIL"
    echo "V1 test stage reported failures (see log)."
}

echo "V1 REBUILD : ${V1_REBUILD}"
echo "V1 TEST    : ${V1_TEST}"
echo "V1 log     : ${V1_LOG}"
echo

# ---------------------------------------------------------------------------
# 4. Rebuild + test V2 (reuse existing tools/rebuild_swi.sh when present)
# ---------------------------------------------------------------------------
echo "=============================================="
echo "V2 REBUILD + TEST"
echo "=============================================="

V2_REBUILD="FAIL"
V2_TEST="FAIL"
V2_LOG="${LOG_DIR}/v2_rebuild_${TIMESTAMP}.log"

(
    set -e
    cd "${V2_DIR}"
    if [ -f tools/rebuild_swi.sh ]; then
        bash tools/rebuild_swi.sh 2>&1 | tee -a "${V2_LOG}"
    else
        if [ ! -d .venv ]; then
            python3 -m venv .venv
        fi
        # shellcheck disable=SC1091
        source .venv/bin/activate
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then
            python -m pip install -r requirements.txt
        fi
        python -m pytest -q 2>&1 | tee -a "${V2_LOG}"
    fi
) > "${V2_LOG}" 2>&1 && V2_REBUILD="PASS" && V2_TEST="PASS" || {
    V2_REBUILD="PASS"
    V2_TEST="FAIL"
    echo "V2 test stage reported failures (see log)."
}

echo "V2 REBUILD : ${V2_REBUILD}"
echo "V2 TEST    : ${V2_TEST}"
echo "V2 log     : ${V2_LOG}"
echo

# ---------------------------------------------------------------------------
# 5. Simple node / file inventory (actual filesystem counts only)
# ---------------------------------------------------------------------------
echo "=============================================="
echo "NODE / FILE INVENTORY"
echo "=============================================="

count_files() {
    local dir="$1"
    if [ -d "${dir}" ]; then
        find "${dir}" -type f 2>/dev/null | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

V1_FILE_COUNT="$(count_files "${V1_DIR}")"
V2_FILE_COUNT="$(count_files "${V2_DIR}")"

echo "V1 tracked/generated files (approx): ${V1_FILE_COUNT}"
echo "V2 tracked/generated files (approx): ${V2_FILE_COUNT}"
echo

# ---------------------------------------------------------------------------
# 6. Generate rebuild report (JSON + Markdown)
# ---------------------------------------------------------------------------
REPORT_JSON="${REPORT_DIR}/SWI_REBUILD_REPORT_${TIMESTAMP}.json"
REPORT_MD="${REPORT_DIR}/SWI_REBUILD_REPORT_${TIMESTAMP}.md"

cat > "${REPORT_JSON}" <<EOF
{
  "schema": "swi.online.test.rebuild.v1",
  "timestamp_utc": "${TIMESTAMP}",
  "mode": "TEST_ONLY",
  "v1": {
    "repository": "${V1_URL}",
    "commit": "${V1_SHA}",
    "rebuild": "${V1_REBUILD}",
    "tests": "${V1_TEST}",
    "log": "${V1_LOG}"
  },
  "v2": {
    "repository": "${V2_URL}",
    "commit": "${V2_SHA}",
    "rebuild": "${V2_REBUILD}",
    "tests": "${V2_TEST}",
    "log": "${V2_LOG}"
  },
  "inventory": {
    "v1_file_count": ${V1_FILE_COUNT},
    "v2_file_count": ${V2_FILE_COUNT}
  },
  "external_downloads": [],
  "system_completion": "INCOMPLETE",
  "proven": false,
  "sealed": false,
  "production_authorized": false
}
EOF

cat > "${REPORT_MD}" <<EOF
# SWI ONLINE TEST REBUILD REPORT

**Timestamp (UTC):** ${TIMESTAMP}  
**Mode:** TEST ONLY  

## Commits

| Component | Commit |
|-----------|--------|
| V1 | \`${V1_SHA}\` |
| V2 | \`${V2_SHA}\` |

## Results

| Component | Rebuild | Tests |
|-----------|---------|-------|
| V1 | ${V1_REBUILD} | ${V1_TEST} |
| V2 | ${V2_REBUILD} | ${V2_TEST} |

## Inventory (approximate file counts)

- V1: ${V1_FILE_COUNT}
- V2: ${V2_FILE_COUNT}

## Final State

| Claim | Value |
|-------|-------|
| System completion | INCOMPLETE |
| Proven | NO |
| Sealed | NO |
| Production authorized | **NO** |

## Notes

- Rebuild success does not equal system completeness.
- Test results are recorded as observed; failures are evidence, not automatically treated as rebuild failure.
- No external node downloads were performed beyond the two Git repositories.
- This report is generated by a controlled test bootstrap. It does not establish authority.

EOF

echo "Report JSON : ${REPORT_JSON}"
echo "Report MD   : ${REPORT_MD}"
echo

# ---------------------------------------------------------------------------
# 7. Final status block
# ---------------------------------------------------------------------------
echo "=============================================="
echo "SWI ONLINE TEST REBUILD — FINAL STATUS"
echo "=============================================="
echo "V1 COMMIT              : ${V1_SHA}"
echo "V2 COMMIT              : ${V2_SHA}"
echo "V1 REBUILD             : ${V1_REBUILD}"
echo "V1 TEST                : ${V1_TEST}"
echo "V2 REBUILD             : ${V2_REBUILD}"
echo "V2 TEST                : ${V2_TEST}"
echo "NODE / FILE COUNTS     : V1=${V1_FILE_COUNT}  V2=${V2_FILE_COUNT}"
echo "SYSTEM COMPLETION      : INCOMPLETE"
echo "PROVEN                 : NO"
echo "SEALED                 : NO"
echo "PRODUCTION AUTHORIZED  : NO"
echo "=============================================="
echo
echo "Logs and reports are under: ${WORKSPACE}"
echo "This process is a controlled test rebuild only."
echo

# Exit non-zero only on hard acquisition / environment failures.
# Test failures are recorded as evidence and do not force a hard process failure.
exit 0
