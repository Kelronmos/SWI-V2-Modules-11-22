#!/usr/bin/env python3
"""
SWI Public Evidence Lab — Runtime Binding Adapter (observation only)

Purpose:
  Observe repository and process identity for the Evidence Lab.
  Optionally surface the existing status_engine claim ceiling.

Hard rules:
  - Does NOT create a second authorization engine.
  - Does NOT modify PERMIT / AUTHORIZATION / EXECUTION_PERMISSION.
  - Does NOT set PROVEN / SEALED / PRODUCTION_AUTHORIZED to True.
  - User-entered SHAs are never treated as verified.
  - Missing binding → RUNTIME_BOUND = NOT_VERIFIED (fail closed).
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _run_git(args: List[str], cwd: Path, timeout: int = 10) -> Optional[str]:
    try:
        p = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if p.returncode != 0:
            return None
        return (p.stdout or "").strip() or None
    except Exception:
        return None


def observe_git(cwd: Optional[Path] = None) -> Dict[str, Any]:
    """Derive repository identity from local git metadata only."""
    root = cwd or Path.cwd()
    inside = _run_git(["rev-parse", "--is-inside-work-tree"], root)
    if inside != "true":
        return {
            "is_git_repo": False,
            "commit_sha": None,
            "branch": None,
            "dirty": None,
            "remote_url": None,
            "verified_from": "none",
            "binding_status": "NOT_VERIFIED",
        }

    commit = _run_git(["rev-parse", "HEAD"], root)
    branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], root)
    porcelain = _run_git(["status", "--porcelain"], root)
    remote = _run_git(["remote", "get-url", "origin"], root)

    return {
        "is_git_repo": True,
        "commit_sha": commit,
        "branch": branch,
        "dirty": bool(porcelain) if porcelain is not None else None,
        "remote_url": remote,
        "verified_from": "local-git-metadata",
        "binding_status": "OBSERVED" if commit else "NOT_VERIFIED",
    }


def observe_process() -> Dict[str, Any]:
    return {
        "pid": os.getpid(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cwd": os.getcwd(),
    }


def observe_status_ceiling() -> Dict[str, Any]:
    """
    Best-effort read of the existing runner status_engine ceiling.
    Observation only — import failure becomes NOT_VERIFIED, never YES.
    """
    try:
        # Import from repository runner package if available on path
        from runner.status_engine import overall_swi_ceiling  # type: ignore

        ceiling = overall_swi_ceiling()
        return {
            "available": True,
            "ceiling": ceiling,
            "note": "Read-only observation of existing status_engine ceiling",
        }
    except Exception as exc:
        return {
            "available": False,
            "ceiling": None,
            "error": str(exc),
            "note": "status_engine not importable from this context; binding remains NOT_VERIFIED",
        }


def bind(
    *,
    cwd: Optional[Path] = None,
    expected_commit: Optional[str] = None,
    include_status_ceiling: bool = True,
) -> Dict[str, Any]:
    """
    Produce a runtime-binding observation record.

    Returns RUNTIME_BOUND = NOT_VERIFIED unless local git commit is observed.
    Never elevates authority claims.
    """
    git = observe_git(cwd)
    proc = observe_process()
    ceiling = observe_status_ceiling() if include_status_ceiling else {"available": False}

    commit_match = None
    if expected_commit and git.get("commit_sha"):
        commit_match = expected_commit.lower() == str(git["commit_sha"]).lower()

    runtime_bound = git.get("binding_status") == "OBSERVED" and bool(git.get("commit_sha"))

    return {
        "schema": "swi.public-evidence-lab.runtime-binding.v1",
        "observed_utc": utc_now(),
        "runtime_bound": runtime_bound,
        "runtime_bound_status": "OBSERVED" if runtime_bound else "NOT_VERIFIED",
        "git": git,
        "process": proc,
        "expected_commit": expected_commit,
        "commit_match": commit_match,
        "user_entered_sha_treated_as_verified": False,
        "status_ceiling": ceiling,
        "authority": {
            "adapter_writes_authority": False,
            "proven": False,
            "sealed": False,
            "production_authorized": False,
            "independent_review_approved": False,
            "note": (
                "This adapter is observation-only. "
                "It does not modify the SWI governing spine or elevate claims."
            ),
        },
        "limitations": [
            "Binding is derived from local git/process metadata only.",
            "Absence of git metadata yields RUNTIME_BOUND=NOT_VERIFIED.",
            "status_engine ceiling is read-only when importable.",
            "No authorization decision is produced or altered by this module.",
        ],
    }


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="SWI Public Evidence Lab runtime binding (observe only)")
    parser.add_argument("--cwd", default=None, help="Working directory to inspect")
    parser.add_argument("--expected-commit", default=None)
    parser.add_argument("--no-ceiling", action="store_true")
    args = parser.parse_args()

    record = bind(
        cwd=Path(args.cwd) if args.cwd else None,
        expected_commit=args.expected_commit,
        include_status_ceiling=not args.no_ceiling,
    )
    print(json.dumps(record, indent=2))
    # Exit 0 even when NOT_VERIFIED — observation succeeded; binding may be absent
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
