#!/usr/bin/env python3
"""Install only vendored dependencies and validate an offline SWI build."""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import subprocess
import sys

EXIT_SUCCESS = 0
EXIT_BUILD_FAILURE = 20
EXIT_ENVIRONMENT = 30


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="run compileall after install")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    log_dir = root / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "offline-build.log"

    def log(message: str) -> None:
        line = f"{dt.datetime.now(dt.timezone.utc).isoformat()} {message}\n"
        print(line, end="")
        with log_file.open("a", encoding="utf-8") as fh:
            fh.write(line)

    log("SWI OFFLINE BUILD")
    req = root / "offline" / "requirements-offline.txt"
    wheels = root / "offline" / "wheels"
    if not req.is_file():
        log("ERROR: offline/requirements-offline.txt missing")
        return EXIT_ENVIRONMENT
    if not wheels.is_dir():
        log("ERROR: offline/wheels missing")
        return EXIT_ENVIRONMENT
    # Placeholder: no wheels yet is environment failure, not success
    wheel_files = [p for p in wheels.iterdir() if p.suffix in {".whl", ".tar.gz", ".zip"}]
    if not wheel_files:
        log("ERROR: offline/wheels empty — offline build not available until wheels are vendored")
        return EXIT_ENVIRONMENT

    cmd = [
        sys.executable, "-m", "pip", "install",
        "--no-index", "--find-links", str(wheels),
        "-r", str(req),
    ]
    log("RUN: " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=root)
    if result.returncode != 0:
        log(f"pip install failed rc={result.returncode}")
        return EXIT_BUILD_FAILURE

    if args.test:
        ccmd = [sys.executable, "-m", "compileall", "-q", "swi_v2", "tests", "test"]
        log("RUN: " + " ".join(ccmd))
        result = subprocess.run(ccmd, cwd=root)
        if result.returncode != 0:
            log(f"compileall failed rc={result.returncode}")
            return EXIT_BUILD_FAILURE

    log("SUCCESS: offline build completed")
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
