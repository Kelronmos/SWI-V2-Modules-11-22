"""Classify nodes on multiple independent dimensions — no single % as proof."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping


def classify_node(node: Mapping[str, Any], tests: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    tests = tests or {}
    path = node.get("path", "")
    implemented = node.get("exists") is True and node.get("type") in {"module", "script"}
    tested = path in tests.get("tested_paths", []) or any(
        path in str(t) for t in tests.get("passed", [])
    )
    return {
        "path": path,
        "IMPLEMENTED": "YES" if implemented else "NO",
        "TESTED": "YES" if tested else "NO",
        "VERIFIED": "NO",
        "AUTHORIZED": "NO",
        "BLOCKED": "YES" if node.get("status") == "UNABLE_TO_INSPECT" else "NO",
        "UNKNOWN": "YES" if node.get("status") not in {"INSPECTED", "UNABLE_TO_INSPECT"} else "NO",
        "NOT_INSPECTED": "YES" if node.get("status") == "UNABLE_TO_INSPECT" else "NO",
    }


def reconcile(inventory: Mapping[str, Any], tests: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    nodes = inventory.get("nodes") or []
    classified = [classify_node(n, tests) for n in nodes]
    return {
        "source_commit": inventory.get("source_commit"),
        "total": len(classified),
        "implemented_yes": sum(1 for c in classified if c["IMPLEMENTED"] == "YES"),
        "tested_yes": sum(1 for c in classified if c["TESTED"] == "YES"),
        "authorized_yes": sum(1 for c in classified if c["AUTHORIZED"] == "YES"),
        "blocked": sum(1 for c in classified if c["BLOCKED"] == "YES"),
        "unknown": sum(1 for c in classified if c["UNKNOWN"] == "YES"),
        "not_inspected": sum(1 for c in classified if c["NOT_INSPECTED"] == "YES"),
        "nodes": classified,
        "note": "AUTHORIZED remains NO unless separate authority evidence is supplied",
    }
