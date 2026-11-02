#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "=========================================="
echo "SWI UNIVERSAL TEST RUNNER"
echo "=========================================="
echo "ROOT                 : ${ROOT}"
echo "MODE                 : SELF-REPAIR + TEST + EVIDENCE"
echo "PRODUCTION AUTHORIZED: NO"
echo "PROVEN               : NO"
echo "SEALED               : NO"
echo "=========================================="

if [[ ! -f "$ROOT/packages.json" ]]; then
    echo "ERROR: packages.json was not found at ${ROOT}/packages.json"
    echo "This launcher must be run from the repository root or its parent directory."
    echo "PRODUCTION AUTHORIZED: NO"
    echo "PROVEN               : NO"
    echo "SEALED               : NO"
    exit 12
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 was not found."
    echo "Install Python 3.10+ and then restart this terminal before running SWI."
    echo "PRODUCTION AUTHORIZED: NO"
    echo "PROVEN               : NO"
    echo "SEALED               : NO"
    exit 10
else
    echo "[OK] Python detected"
    python3 --version
fi

if ! command -v git >/dev/null 2>&1; then
    echo "ERROR: Git was not found."
    echo "Install Git and then restart this terminal before running SWI."
    echo "PRODUCTION AUTHORIZED: NO"
    echo "PROVEN               : NO"
    echo "SEALED               : NO"
    exit 11
else
    echo "[OK] Git detected"
    git --version
fi

NEEDS_NODE=$(SWI_ROOT="$ROOT" python3 -c 'import json, os; from pathlib import Path; p = Path(os.environ["SWI_ROOT"]) / "packages.json"; d = json.loads(p.read_text(encoding="utf-8")); repos = d.get("repositories", {}); print(1 if any("node" in str(item).lower() for repo in repos.values() for item in repo.get("toolchain", [])) else 0)')

if [[ "$NEEDS_NODE" == "1" ]]; then
    if ! command -v node >/dev/null 2>&1; then
        echo
        echo "Missing tool detected: Node.js is required by the manifest."
        echo "The launcher will not silently install software."
        read -r -p "Install Node.js now? [y/N]: " answer || answer="n"
        case "$answer" in
            y|Y|yes|YES)
                ;;
            *)
                echo "Installation cancelled by user."
                echo "PRODUCTION AUTHORIZED: NO"
                echo "PROVEN               : NO"
                echo "SEALED               : NO"
                exit 23
                ;;
        esac

        echo "Installing Node.js..."
        if command -v brew >/dev/null 2>&1; then
            brew install node
        elif command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update && sudo apt-get install -y nodejs
        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y nodejs
        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -S --noconfirm nodejs
        else
            echo "ERROR: Node.js installation is not supported on this system."
            echo "Install Node.js manually and restart the terminal before running SWI."
            echo "PRODUCTION AUTHORIZED: NO"
            echo "PROVEN               : NO"
            echo "SEALED               : NO"
            exit 23
        fi
    fi
    echo "[OK] Node.js detected"
    node --version
fi

echo
echo "Manifest validation..."
if ! SWI_ROOT="$ROOT" python3 -c '
import json, os, sys
from pathlib import Path
p = Path(os.environ["SWI_ROOT"]) / "packages.json"
data = json.loads(p.read_text(encoding="utf-8"))
schema = data.get("schema", "")
repos = data.get("repositories", {})
if not str(schema).startswith("swi.online.test.rebuild.packages."):
    raise SystemExit(14)
if not isinstance(repos, dict) or not repos:
    raise SystemExit(15)
print(f"Manifest validated: {len(repos)} repositories")
'; then
    echo "ERROR: Manifest validation failed."
    echo "PRODUCTION AUTHORIZED: NO"
    echo "PROVEN               : NO"
    echo "SEALED               : NO"
    exit 15
fi

echo
echo "Launching verified Python runner..."
python3 -m runner.main "$@"
EXITCODE=$?

echo
echo "=========================================="
echo "SWI RUN COMPLETE"
echo "=========================================="
echo "Reports are under: ${ROOT}/swi-test-workspace/reports"
echo
echo "PRODUCTION AUTHORIZED: NO"
echo "PROVEN               : NO"
echo "SEALED               : NO"
echo "=========================================="

echo
exit "$EXITCODE"
