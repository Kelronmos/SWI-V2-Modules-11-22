"""Repository materialization with dirty-checkout protection."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from runner.evidence import EvidenceLedger


def _git(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _is_dirty(repo_dir: Path) -> bool:
    result = _git(["status", "--porcelain"], cwd=repo_dir)
    return bool(result.stdout.strip())


def materialize_one(
    key: str,
    spec: dict[str, Any],
    target: Path,
    ledger: EvidenceLedger,
) -> dict[str, Any]:
    """Clone or update a single repository. Never destroys user data."""
    url = spec["url"]
    branch = spec.get("branch", "main")
    role = spec.get("role", "UNKNOWN")

    record: dict[str, Any] = {
        "key": key,
        "url": url,
        "branch": branch,
        "role": role,
        "target": str(target),
        "status": "NOT_RUN",
        "commit_sha": None,
        "reason": None,
    }

    if target.exists() and (target / ".git").exists():
        if _is_dirty(target):
            record["status"] = "SOURCE_DIRTY"
            record["reason"] = (
                f"Working tree has uncommitted changes. "
                f"Refusing to synchronize. Manually remove or clean: {target}"
            )
            ledger.record_failure("SOURCE_DIRTY", record["reason"])
            print(f"       [{key}] SOURCE_DIRTY — stopping for this repo")
            return record

        # Safe fast-forward only
        fetch = _git(["fetch", "origin"], cwd=target)
        if fetch.returncode != 0:
            record["status"] = "FAIL"
            record["reason"] = f"git fetch failed: {fetch.stderr.strip()}"
            return record

        pull = _git(["pull", "--ff-only", "origin", branch], cwd=target)
        if pull.returncode != 0:
            record["status"] = "FAIL"
            record["reason"] = (
                f"git pull --ff-only failed (divergent history?). "
                f"No reset or merge performed. {pull.stderr.strip()}"
            )
            return record
    else:
        # Fresh clone
        target.parent.mkdir(parents=True, exist_ok=True)
        clone = _git(["clone", "--branch", branch, url, str(target)])
        if clone.returncode != 0:
            # fallback without --branch
            clone = _git(["clone", url, str(target)])
            if clone.returncode != 0:
                record["status"] = "SOURCE_MISSING"
                record["reason"] = f"git clone failed: {clone.stderr.strip()}"
                return record

    # Record exact SHA
    sha_result = _git(["rev-parse", "HEAD"], cwd=target)
    if sha_result.returncode == 0:
        record["commit_sha"] = sha_result.stdout.strip()
        record["status"] = "MATERIALIZED"
        print(f"       [{key}] MATERIALIZED  {record['commit_sha'][:12]}...")
    else:
        record["status"] = "FAIL"
        record["reason"] = "Could not determine commit SHA"

    return record


def materialize_repositories(
    packages: dict[str, Any],
    workspace: dict[str, Path],
    mode: str,
    ledger: EvidenceLedger,
) -> list[dict[str, Any]]:
    """Materialize all repositories declared in packages.json."""
    repos_cfg = packages.get("repositories", {})
    results: list[dict[str, Any]] = []

    # Special-case v1 / v2 into their historic locations for compatibility
    special_paths = {
        "v1": workspace["v1"],
        "v2": workspace["v2"],
    }

    for key, spec in repos_cfg.items():
        if mode == "audit":
            # Audit mode: detect only, do not clone
            results.append({
                "key": key,
                "url": spec.get("url"),
                "role": spec.get("role"),
                "status": "AUDIT_ONLY",
                "commit_sha": None,
            })
            continue

        if key in special_paths:
            target = special_paths[key]
        else:
            target = workspace["repos"] / key

        result = materialize_one(key, spec, target, ledger)
        results.append(result)
        ledger.record_repository(result)

    return results
