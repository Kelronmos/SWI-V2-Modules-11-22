"""Environment detection and workspace preparation."""

from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any


def _run_version(cmd: list[str]) -> str | None:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10, check=False
        )
        if result.returncode == 0:
            return (result.stdout or result.stderr or "").strip().splitlines()[0]
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


def detect_environment() -> dict[str, Any]:
    """Detect OS and toolchain versions. Never installs anything."""
    env: dict[str, Any] = {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "git": _run_version(["git", "--version"]),
        "node": _run_version(["node", "--version"]),
        "npm": _run_version(["npm", "--version"]),
        "rust": _run_version(["rustc", "--version"]),
        "cargo": _run_version(["cargo", "--version"]),
    }
    return env


def ensure_workspace(script_dir: Path, workspace_cfg: dict) -> dict[str, Path]:
    """Create the standard workspace layout and return resolved paths."""
    root_name = workspace_cfg.get("root", "swi-test-workspace")
    root = script_dir / root_name

    paths = {
        "root": root,
        "v1": root / "v1",
        "v2": root / "v2",
        "repos": root / "repos",
        "artifacts": root / "artifacts",
        "reports": root / "reports",
        "logs": root / "logs",
        "downloads": root / "downloads",
    }

    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)

    return paths
