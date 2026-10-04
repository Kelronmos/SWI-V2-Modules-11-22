"""Test engine — executes repository-declared test commands only."""

from __future__ import annotations

import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any

from runner.evidence import EvidenceLedger

# Prevent pytest from collecting this module (function name test_repositories)
__test__ = False


def _run_command(
    command: str,
    cwd: Path,
    log_path: Path,
    timeout: int = 600,
) -> dict[str, Any]:
    is_windows = platform.system() == "Windows"
    start = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env={**os.environ},
        )
        duration = round(time.monotonic() - start, 2)
        stdout = result.stdout or ""
        stderr = result.stderr or ""

        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as f:
            f.write(f"COMMAND: {command}\n")
            f.write(f"CWD: {cwd}\n")
            f.write(f"EXIT: {result.returncode}\n")
            f.write(f"DURATION: {duration}s\n")
            f.write("\n===== STDOUT =====\n")
            f.write(stdout)
            f.write("\n===== STDERR =====\n")
            f.write(stderr)

        return {
            "exit_code": result.returncode,
            "duration_seconds": duration,
            "stdout_preview": stdout[:2000],
            "stderr_preview": stderr[:2000],
            "log_file": str(log_path),
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        duration = round(time.monotonic() - start, 2)
        return {
            "exit_code": -1,
            "duration_seconds": duration,
            "stdout_preview": "",
            "stderr_preview": f"TIMEOUT after {timeout}s",
            "log_file": str(log_path),
            "timed_out": True,
        }
    except Exception as exc:
        duration = round(time.monotonic() - start, 2)
        return {
            "exit_code": -1,
            "duration_seconds": duration,
            "stdout_preview": "",
            "stderr_preview": str(exc),
            "log_file": str(log_path),
            "timed_out": False,
        }


def _needs_toolchain(spec: dict[str, Any], env: dict[str, Any]) -> str | None:
    toolchains = spec.get("toolchain", [])
    for t in toolchains:
        t_lower = t.lower()
        if "python" in t_lower and not env.get("python"):
            return "python"
        if "node" in t_lower and not env.get("node"):
            return "node"
        if "rust" in t_lower and not env.get("rust"):
            return "rust"
        if "cargo" in t_lower and not env.get("cargo"):
            return "cargo"
    return None


def test_repositories(
    packages: dict[str, Any],
    repo_results: list[dict[str, Any]],
    build_results: list[dict[str, Any]],
    workspace: dict[str, Path],
    env: dict[str, Any],
    ledger: EvidenceLedger,
) -> list[dict[str, Any]]:
    """Run declared test commands for each repository."""
    is_windows = platform.system() == "Windows"
    repos_cfg = packages.get("repositories", {})
    test_results: list[dict[str, Any]] = []
    logs_dir = workspace["logs"]

    special_paths = {
        "v1": workspace["v1"],
        "v2": workspace["v2"],
    }

    build_by_key = {b["key"]: b for b in build_results}

    for repo in repo_results:
        key = repo["key"]
        spec = repos_cfg.get(key, {})
        record: dict[str, Any] = {
            "key": key,
            "role": spec.get("role"),
            "commit_sha": repo.get("commit_sha"),
            "status": "NOT_RUN",
            "command": None,
            "exit_code": None,
            "duration_seconds": None,
            "log_file": None,
            "reason": None,
        }

        if repo.get("status") != "MATERIALIZED":
            record["status"] = "BLOCKED"
            record["reason"] = f"Repository not materialized ({repo.get('status')})"
            test_results.append(record)
            print(f"       [{key}] TEST BLOCKED — {record['reason']}")
            continue

        if spec.get("status") in ("LEGACY_STUB",) or spec.get("test") == "NO_TEST_CLAIM":
            record["status"] = "NOT_APPLICABLE"
            record["reason"] = "Manifest declares NO_TEST_CLAIM / LEGACY_STUB"
            test_results.append(record)
            print(f"       [{key}] TEST NOT_APPLICABLE")
            continue

        missing = _needs_toolchain(spec, env)
        if missing:
            record["status"] = "NOT_RUN"
            record["reason"] = f"Missing toolchain: {missing}"
            test_results.append(record)
            print(f"       [{key}] TEST NOT_RUN — missing {missing}")
            continue

        command = spec.get("test")
        if not command or command == "NO_TEST_CLAIM":
            record["status"] = "NOT_APPLICABLE"
            record["reason"] = "No test command declared"
            test_results.append(record)
            print(f"       [{key}] TEST NOT_APPLICABLE — no command")
            continue

        # Resolve target
        if key in special_paths:
            target = special_paths[key]
        else:
            target = workspace["repos"] / key

        # Prefer venv python if it exists
        if "pytest" in command:
            if is_windows:
                venv_python = target / ".venv" / "Scripts" / "python.exe"
            else:
                venv_python = target / ".venv" / "bin" / "python"
            if venv_python.exists():
                command = f'"{venv_python}" -m pytest -q'
            else:
                # fallback to system python
                py = "python" if is_windows else "python3"
                command = f"{py} -m pytest -q"

        log_path = logs_dir / f"test_{key}.log"
        record["command"] = command

        print(f"       [{key}] Testing... ({command[:60]})")
        result = _run_command(command, target, log_path)

        record["exit_code"] = result["exit_code"]
        record["duration_seconds"] = result["duration_seconds"]
        record["log_file"] = result["log_file"]

        if result["timed_out"]:
            record["status"] = "FAIL"
            record["reason"] = "TIMEOUT"
        elif result["exit_code"] == 0:
            record["status"] = "PASS"
        else:
            record["status"] = "FAIL"
            record["reason"] = f"exit_code={result['exit_code']}"

        test_results.append(record)
        print(f"       [{key}] TEST {record['status']} ({record['duration_seconds']}s)")

        if record["status"] == "FAIL":
            ledger.record_failure("test", f"{key}: {record.get('reason')}")

    return test_results
