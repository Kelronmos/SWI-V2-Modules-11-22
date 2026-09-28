"""Deterministic repository inventory for S9 packages."""
from __future__ import annotations

import os
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional


SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", ".venv", "venv"}


@dataclass
class InventoryNode:
    node_id: str
    path: str
    type: str
    exists: bool
    source_commit: str
    test_refs: List[str] = field(default_factory=list)
    dependency_refs: List[str] = field(default_factory=list)
    claim_refs: List[str] = field(default_factory=list)
    status: str = "INSPECTED"
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def classify_path(rel: str) -> str:
    p = rel.replace("\\", "/").lower()
    if p.startswith("docs/") or p.endswith(".md"):
        return "doc"
    if p.startswith("test/") or p.startswith("tests/") or "/test_" in f"/{p}":
        return "test"
    if p.startswith(".github/workflows/"):
        return "workflow"
    if p.endswith((".json", ".yaml", ".yml")) and ("schema" in p or "contract" in p):
        return "schema"
    if p.startswith("scripts/"):
        return "script"
    if p.startswith("swi_v2/") and p.endswith(".py"):
        return "module"
    if p.endswith(".py"):
        return "module"
    return "other"


def walk_inventory(repo_root: Path, source_commit: str) -> Dict[str, Any]:
    """Walk repo; record unreadable nodes as UNABLE_TO_INSPECT (never silent skip)."""
    root = Path(repo_root).resolve()
    nodes: List[InventoryNode] = []
    unable: List[Dict[str, str]] = []
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            full = Path(dirpath) / name
            try:
                rel = str(full.relative_to(root)).replace("\\", "/")
            except ValueError:
                unable.append({"path": str(full), "status": "UNABLE_TO_INSPECT", "reason": "outside_root"})
                continue
            n += 1
            node_id = f"N-{n:05d}"
            try:
                full.stat()
                nodes.append(
                    InventoryNode(
                        node_id=node_id,
                        path=rel,
                        type=classify_path(rel),
                        exists=True,
                        source_commit=source_commit,
                        status="INSPECTED",
                    )
                )
            except OSError as e:
                nodes.append(
                    InventoryNode(
                        node_id=node_id,
                        path=rel,
                        type=classify_path(rel),
                        exists=False,
                        source_commit=source_commit,
                        status="UNABLE_TO_INSPECT",
                        reason=str(e),
                    )
                )
                unable.append({"path": rel, "status": "UNABLE_TO_INSPECT", "reason": str(e)})
    by_type: Dict[str, int] = {}
    for node in nodes:
        by_type[node.type] = by_type.get(node.type, 0) + 1
    return {
        "source_commit": source_commit,
        "total_nodes": len(nodes),
        "inspected": sum(1 for x in nodes if x.status == "INSPECTED"),
        "unable_to_inspect": len(unable),
        "by_type": by_type,
        "nodes": [x.to_dict() for x in nodes],
        "unable": unable,
    }
