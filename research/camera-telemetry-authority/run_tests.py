#!/usr/bin/env python3
"""Runner for camera telemetry research package."""
import subprocess
import sys

def main():
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/"], check=False)
    print("PRODUCTION_AUTHORIZED=NO")
    return r.returncode

if __name__ == "__main__":
    raise SystemExit(main())
