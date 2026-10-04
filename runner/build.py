"""Build engine — executes repository-declared build/rebuild commands only."""

from __future__ import annotations

import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any

from runner.evidence import EvidenceLedger


def _run_command(
    command: str,
    cwd: Path,
    log_path: Path,
    timeout: int = 600,
) -> dict[str, Any]:
    """Run a shell command, capture output, return structured result."""
    is_windows = platform.system() == "Windows"
    shell = True

    start = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
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


def _select_command(spec: dict[str, Any], is_windows: bool) -> str | None:
    """Choose the appropriate build/rebuild command from the manifest."""
    # Prefer explicit rebuild, then build
    for key in ("rebuild", "build"):
        cmd = spec.get(key)
        if not cmd or cmd in ("NO_BUILD_CLAIM", None):
            continue
        if " or " in cmd:
            # e.g. "tools/rebuild_swi.sh or tools/rebuild_swi.bat"
            parts = [p.strip() for p in cmd.split(" or ")]
            if is_windows:
                for p in parts:
                    if p.endswith(".bat") or "bat" in p.lower():
                        return p
                return parts[-1]  # fallback
            else:
                for p in parts:
                    if p.endswith(".sh") or "sh" in p.lower():
                        return p
                return parts[0]
        return cmd
    return None


def _needs_toolchain(spec: dict[str, Any], env: dict[str, Any]) -> str | None:
    """Return a missing toolchain name, or None if all present."""
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
        if t_lower == "git" and not env.get("git"):
            return "git"
    return None


def build_repositories(
    packages: dict[str, Any],
    repo_results: list[dict[str, Any]],
    workspace: dict[str, Path],
    env: dict[str, Any],
    ledger: EvidenceLedger,
) -> list[dict[str, Any]]:
    """Attempt to build every materialized repository using its declared command."""
    is_windows = platform.system() == "Windows"
    repos_cfg = packages.get("repositories", {})
    build_results: list[dict[str, Any]] = []
    logs_dir = workspace["logs"]

    special_paths = {
        "v1": workspace["v1"],
        "v2": workspace["v2"],
    }

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
            build_results.append(record)
            print(f"       [{key}] BUILD BLOCKED — {record['reason']}")
            continue

        if spec.get("status") in ("LEGACY_STUB",) or spec.get("build") == "NO_BUILD_CLAIM":
            record["status"] = "NOT_APPLICABLE"
            record["reason"] = "Manifest declares NO_BUILD_CLAIM / LEGACY_STUB"
            build_results.append(record)
            print(f"       [{key}] BUILD NOT_APPLICABLE")
            continue

        missing = _needs_toolchain(spec, env)
        if missing:
            record["status"] = "NOT_RUN"
            record["reason"] = f"Missing toolchain: {missing}"
            build_results.append(record)
            print(f"       [{key}] BUILD NOT_RUN — missing {missing}")
            continue

        command = _select_command(spec, is_windows)
        if not command:
            record["status"] = "NOT_APPLICABLE"
            record["reason"] = "No build/rebuild command declared"
            build_results.append(record)
            print(f"       [{key}] BUILD NOT_APPLICABLE — no command")
            continue

        # Resolve target directory
        if key in special_paths:
            target = special_paths[key]
        else:
            target = workspace["repos"] / key

        # For Python venv style commands, make them more robust
        if "venv" in command and "pip install" in command:
            if is_windows:
                command = (
                    "python -m venv .venv && "
                    ".venv\\Scripts\\python -m pip install --upgrade pip && "
                    ".venv\\Scripts\\python -m pip install -r requirements.txt"
                )
            else:
                command = (
                    "python3 -m venv .venv && "
                    ". .venv/bin/activate && "
                    "pip install --upgrade pip && "
                    "pip install -r requirements.txt"
                )

        log_path = logs_dir / f"build_{key}.log"
        record["command"] = command

        print(f"       [{key}] Building... ({command[:60]}...)")
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

        build_results.append(record)
        print(f"       [{key}] BUILD {record['status']} ({record['duration_seconds']}s)")

        if record["status"] == "FAIL":
            ledger.record_failure("build", f"{key}: {record.get('reason')}")

    return build_results
