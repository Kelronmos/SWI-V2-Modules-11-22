#!/usr/bin/env bash
set -euo pipefail

echo "=================================="
echo "SWI LOCAL REBUILD"
echo "=================================="

command -v python3 >/dev/null 2>&1 || {
    echo "ERROR: Python 3 not found."
    exit 1
}

command -v git >/dev/null 2>&1 || {
    echo "ERROR: Git not found."
    exit 1
}

echo "Python:"
python3 --version

echo "Git:"
git --version

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip

if [ -f requirements.txt ]; then
    python -m pip install -r requirements.txt
fi

echo
echo "Running tests..."

python -m pytest

echo
echo "SWI REBUILD/TEST PASSED"
