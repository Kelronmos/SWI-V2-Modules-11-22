#!/usr/bin/env python3
"""Canonical non-interactive SWI offline test runner.

No network access is attempted. Required failures remain failures/unknown;
this runner never converts an unavailable required control into success.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import subprocess
import sys

EXIT_SUCCESS = 0
EXIT_TEST_FAILURE = 10
EXIT_BUILD_FAILURE = 20
EXIT_ENVIRONMENT = 30
EXIT_INTEGRITY = 40
EXIT_AUTHORITY = 50
EXIT_UNKNOWN = 60


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compile-only", action="store_true")
    parser.add_argument("--pytest-args", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    log_dir = root / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "offline-start.log"

    def log(message: str) -> None:
        line = f"{dt.datetime.now(dt.timezone.utc).isoformat()} {message}\n"
        print(line, end="")
        with log_file.open("a", encoding="utf-8") as fh:
            fh.write(line)

    log("SWI OFFLINE START")
    log(f"ROOT={root}")
    log(f"PYTHON={sys.executable}")

    if os.environ.get("SWI_ALLOW_NETWORK") == "1":
        log("ERROR: SWI_ALLOW_NETWORK=1 is forbidden for offline runner")
        return EXIT_ENVIRONMENT

    if not (root / "requirements.txt").exists():
        log("ERROR: requirements.txt missing")
        return EXIT_ENVIRONMENT

    compile_cmd = [sys.executable, "-m", "compileall", "-q", "swi_v2", "tests", "test"]
    log("RUN: " + " ".join(compile_cmd))
    result = subprocess.run(compile_cmd, cwd=root)
    if result.returncode != 0:
        log(f"COMPILE FAILED rc={result.returncode}")
        return EXIT_BUILD_FAILURE

    if args.compile_only:
        log("SUCCESS: compile-only completed")
        return EXIT_SUCCESS

    pytest_cmd = [sys.executable, "-m", "pytest", "-q"]
    if args.pytest_args:
        pytest_cmd.extend(args.pytest_args)
    log("RUN: " + " ".join(pytest_cmd))
    result = subprocess.run(pytest_cmd, cwd=root)
    if result.returncode != 0:
        log(f"TEST FAILURE rc={result.returncode}")
        return EXIT_TEST_FAILURE

    log("SUCCESS: offline test run completed")
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
