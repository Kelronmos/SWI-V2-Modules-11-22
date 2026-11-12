#!/data/data/com.termux/files/usr/bin/bash
# SWI Termux local runtime startup helper
# STATUS: PROTOTYPE
# PROVEN=NO SEALED=NO PRODUCTION_AUTHORIZED=NO
#
# Does not authorize actions. Does not start Firefly (unauthorized).
# Records identity and writes a checkpoint only.

set -euo pipefail

SWI_HOME="${SWI_HOME:-$HOME/swi_local}"
mkdir -p "$SWI_HOME"/{checkpoints,logs,quarantine}

TS=$(date -u +%Y%m%dT%H%M%SZ)
LOG="$SWI_HOME/logs/start_$TS.log"

{
  echo "SWI Termux start — $TS"
  echo "pid=$$"
  echo "SWI_HOME=$SWI_HOME"
  echo "python=$(command -v python3 || true)"
  echo "PROVEN=NO"
  echo "SEALED=NO"
  echo "PRODUCTION_AUTHORIZED=NO"
} | tee "$LOG"

# Optional: activate venv if present
if [[ -f "$SWI_HOME/venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$SWI_HOME/venv/bin/activate"
fi

# Write a minimal checkpoint via Python if available
if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY' || true
import json, os, time
from pathlib import Path
home = Path(os.environ.get("SWI_HOME", Path.home() / "swi_local"))
cp = home / "checkpoints" / f"termux_start_{int(time.time())}.json"
cp.write_text(json.dumps({
    "event": "termux_start",
    "pid": os.getpid(),
    "ts": time.time(),
    "proven": False,
    "sealed": False,
    "production_authorized": False,
}, indent=2))
print(f"checkpoint={cp}")
PY
fi

echo "Startup helper finished. Runtime services must be started explicitly."
echo "Log: $LOG"
