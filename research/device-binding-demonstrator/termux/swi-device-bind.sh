#!/data/data/com.termux/files/usr/bin/bash
# SWI Device Binding Demonstrator — Termux entry
set -euo pipefail
echo "WELCOME TO SWI"
echo "Device Binding Demonstrator (research only)"
echo "PROVEN=NO SEALED=NO PRODUCTION_AUTHORIZED=NO"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT:${PYTHONPATH:-}"

if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: Python not available in Termux"
  exit 1
fi
PY=$(command -v python3 || command -v python)

OUT_BASE="${HOME}/storage/shared/SWI-Security-Audits/SWI-DEVICE-BIND"
if [ ! -d "${HOME}/storage/shared" ]; then
  echo "BLOCKED: shared storage not mounted. Run: termux-setup-storage"
  echo "Falling back to $HOME/SWI-DEVICE-BIND"
  OUT_BASE="${HOME}/SWI-DEVICE-BIND"
fi
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="${OUT_BASE}/${STAMP}"
mkdir -p "$OUT"

if command -v termux-battery-status >/dev/null 2>&1; then
  echo "Termux:API: available"
else
  echo "Termux:API: NOT available — hardware adapters will be BLOCKED/NOT_IMPLEMENTED"
fi

"$PY" - << PY
from pathlib import Path
from swi_device_bind.runner import run_offline_demo
r = run_offline_demo(Path("$OUT"))
print("Report:", r.get("report_path"))
print("Status counts:", r.get("status_counts"))
print("PROVEN=NO PRODUCTION_AUTHORIZED=NO")
PY

if command -v sha256sum >/dev/null 2>&1; then
  (cd "$OUT" && sha256sum * > SHA256SUMS 2>/dev/null || true)
  echo "SHA256SUMS written under $OUT"
fi
echo "Done. Physical camera/biometric/mic tests require permissions and Termux:API."
