"""
Node / filesystem inventory.

Records actual filesystem evidence only.
Does not invent SWI nodes from directory names alone.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def _file_sha256(path: Path, max_bytes: int = 2_000_000) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            remaining = max_bytes
            while remaining > 0:
                chunk = f.read(min(65536, remaining))
                if not chunk:
                    break
                h.update(chunk)
                remaining -= len(chunk)
        return h.hexdigest()
    except OSError:
        return None


def inventory_repository(
    key: str,
    repo_dir: Path,
    commit_sha: str | None,
    max_files: int = 5000,
) -> dict[str, Any]:
    """Walk a materialized repository and record filesystem evidence."""
    if not repo_dir.is_dir():
        return {
            "repository": key,
            "commit_sha": commit_sha,
            "status": "MISSING",
            "file_count": 0,
            "files": [],
        }

    files: list[dict[str, Any]] = []
    count = 0
    for path in sorted(repo_dir.rglob("*")):
        if not path.is_file():
            continue
        # Skip common noise
        rel = path.relative_to(repo_dir).as_posix()
        if any(
            part.startswith(".") or part in ("node_modules", ".venv", "__pycache__", "target", "dist")
            for part in rel.split("/")
        ):
            continue
        count += 1
        if len(files) < max_files:
            try:
                size = path.stat().st_size
            except OSError:
                size = -1
            files.append({
                "path": rel,
                "size": size,
                "sha256": _file_sha256(path) if size >= 0 and size < 2_000_000 else None,
            })

    return {
        "repository": key,
        "commit_sha": commit_sha,
        "status": "INVENTORIED",
        "file_count": count,
        "files_recorded": len(files),
        "files": files,
    }


def run_inventory(
    packages: dict[str, Any],
    repo_results: list[dict[str, Any]],
    workspace: dict[str, Path],
) -> dict[str, Any]:
    """Inventory all materialized repositories."""
    special = {"v1": workspace["v1"], "v2": workspace["v2"]}
    inventories = []

    for repo in repo_results:
        key = repo["key"]
        if repo.get("status") != "MATERIALIZED":
            inventories.append({
                "repository": key,
                "commit_sha": repo.get("commit_sha"),
                "status": "NOT_REACHED",
                "reason": repo.get("status"),
            })
            continue
        target = special.get(key, workspace["repos"] / key)
        inv = inventory_repository(key, target, repo.get("commit_sha"))
        inventories.append(inv)
        print(f"       [{key}] files≈{inv.get('file_count', 0)}")

    return {
        "repositories_inventoried": len([i for i in inventories if i.get("status") == "INVENTORIED"]),
        "inventories": inventories,
    }


def evaluate_components(
    packages: dict[str, Any],
    repo_results: list[dict[str, Any]],
    inventory: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Evaluate each declared component against filesystem evidence.
    present=true only when a concrete path exists and is found.
    """
    components_cfg = packages.get("components", [])
    repo_status = {r["key"]: r for r in repo_results}
    inv_by_repo = {
        i["repository"]: i for i in inventory.get("inventories", [])
    }

    results = []
    for comp in components_cfg:
        cid = comp["id"]
        source = comp.get("source", {})
        repo_key = source.get("repository")
        declared_path = source.get("path")

        status = {
            "declared": True,
            "present": False,
            "materialized": False,
            "built": False,
            "tested": False,
            "proven": False,
            "sealed": False,
            "production_authorized": False,
        }

        source_status = "NOT_FOUND"
        notes = list(comp.get("notes", []) if isinstance(comp.get("notes"), list) else ([comp["notes"]] if comp.get("notes") else []))

        repo_rec = repo_status.get(repo_key) if repo_key else None
        if repo_rec and repo_rec.get("status") == "MATERIALIZED":
            status["materialized"] = True
            inv = inv_by_repo.get(repo_key, {})
            if declared_path:
                # Check whether the path appears in inventory
                files = inv.get("files", [])
                if any(f.get("path") == declared_path or f.get("path", "").startswith(declared_path.rstrip("/") + "/") for f in files):
                    status["present"] = True
                    source_status = "FOUND"
                else:
                    source_status = "NOT_FOUND"
                    notes.append(f"Declared path '{declared_path}' not found in inventory")
            else:
                source_status = "PATH_NOT_ESTABLISHED"
                notes.append("source.path is null — cannot confirm presence from filesystem")
        else:
            source_status = "REPOSITORY_NOT_MATERIALIZED"
            if repo_rec:
                notes.append(f"Repository status: {repo_rec.get('status')}")

        if comp.get("status_hint") == "DEVELOPMENT_SUSPENDED":
            notes.append("Manifest status_hint: DEVELOPMENT_SUSPENDED")

        results.append({
            "id": cid,
            "display_name": comp.get("display_name", cid),
            "type": comp.get("type", "component"),
            "source": source,
            "source_status": source_status,
            "status": status,
            "invariants": comp.get("invariants", []),
            "notes": notes,
        })

        present_flag = "PRESENT" if status["present"] else source_status
        print(f"       [{cid}] {present_flag}")

    return results
