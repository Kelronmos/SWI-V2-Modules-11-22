"""
Evidence-based component DISCOVERY (Domain A).

Answers: what exists, where, what can be inspected?
Does NOT produce test PASS/FAIL.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from runner.domains import (
    FOUND, PATH_NOT_ESTABLISHED, DOCUMENTED_ONLY, TERM_FOUND,
    make_discovery_record,
)

COMPONENT_SEARCH = {
    "v1_admission": ["admit_or_halt", "evaluate_source", "source_admission", "admission_boundary"],
    "v2_modules": ["swi_v2", "module11", "admit_foundation_input"],
    "node_access_boundary": ["node_access", "node-access", "NodeAccess"],
    "mathematical_evidence_engine": ["mathematical_evidence", "math_evidence"],
    "firefly_memory": ["firefly", "FireflyMemory"],
    "structured_workflow_intelligence": ["structured_workflow"],
    "rust_governance_engine": ["governance"],
    "v103_api_foundation": ["v103", "api_foundation"],
    "common_sense": ["common_sense", "CommonSense"],
    "reflex_sadu": ["reflex", "sadu", "SADU"],
    "cek": ["\\bcek\\b", "CEK"],
    "scar": ["\\bscar\\b", "SCAR"],
    "seeder": ["seeder", "SEEDER"],
    "s9_security_maze": ["s9", "security_maze"],
    "zero_trust_task_travel": ["zero_trust", "task_travel"],
    "structured_seal": ["structured_seal", "create_seal", "SealedEvidence"],
    "runtime_seal": ["runtime_seal", "RuntimeSeal"],
    "mathematical_zero": ["mathematical_zero", "true_zero"],
    "geometric_zero": ["geometric_zero"],
    "evidence_engine": ["evidence_engine", "EvidenceEngine"],
    "consequence_gate": ["consequence_gate", "ConsequenceGate"],
    "authorization_gate": ["authorization_gate", "AuthorizationGate"],
    "jurisdiction_binding": ["jurisdiction"],
    "pre_revalidation": ["REQUIRES_REVALIDATION", "revalidation"],
}

SKIP_DIRS = {
    ".git", ".venv", "node_modules", "__pycache__", "target", "dist", "build",
    ".tox", ".mypy_cache", "swi-test-workspace",
}


def _scan_repo(repo_path: Path, tokens: list[str], max_hits: int = 20) -> dict[str, Any]:
    term_hits: list[str] = []
    code_hits: list[str] = []
    test_hits: list[str] = []
    doc_hits: list[str] = []

    if not repo_path.is_dir():
        return {
            "term_found": False, "code_found": False,
            "test_found": False, "doc_found": False,
            "term_hits": [], "code_hits": [], "test_hits": [], "doc_hits": [],
        }

    patterns = []
    for t in tokens:
        try:
            patterns.append(re.compile(t, re.IGNORECASE))
        except re.error:
            patterns.append(re.compile(re.escape(t), re.IGNORECASE))

    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        if path.suffix.lower() not in {
            ".py", ".rs", ".ts", ".js", ".mjs", ".md", ".json", ".toml", ".txt", ".bat", ".sh"
        }:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(path.relative_to(repo_path))
        matched = any(p.search(text) or p.search(rel) for p in patterns)
        if not matched:
            continue

        lower = rel.lower()
        if any(x in lower for x in ("test", "spec", "__tests__")):
            if len(test_hits) < max_hits:
                test_hits.append(rel)
        elif path.suffix.lower() == ".md":
            if len(doc_hits) < max_hits:
                doc_hits.append(rel)
        else:
            if len(code_hits) < max_hits:
                code_hits.append(rel)
        if len(term_hits) < max_hits:
            term_hits.append(rel)
        if len(term_hits) >= max_hits:
            break

    return {
        "term_found": bool(term_hits),
        "code_found": bool(code_hits),
        "test_found": bool(test_hits),
        "doc_found": bool(doc_hits),
        "term_hits": term_hits[:10],
        "code_hits": code_hits[:10],
        "test_hits": test_hits[:10],
        "doc_hits": doc_hits[:10],
    }


def _classify_discovery(scan: dict[str, Any]) -> str:
    if scan.get("code_found"):
        return FOUND
    if scan.get("doc_found") and not scan.get("code_found"):
        return DOCUMENTED_ONLY
    if scan.get("term_found"):
        return TERM_FOUND
    return PATH_NOT_ESTABLISHED


def discover_components(
    packages: dict[str, Any],
    repo_results: list[dict[str, Any]],
    workspace: dict[str, Path],
) -> list[dict[str, Any]]:
    """
    Domain A only: discovery records.
    Each record has discovery.* and tests.status=NOT_RUN | NO_TEST_SUITE_FOUND.
    assertions list is always empty here.
    """
    special = {"v1": workspace["v1"], "v2": workspace["v2"]}
    repo_paths: dict[str, Path] = {}
    sha_by_key: dict[str, str | None] = {}

    for r in repo_results:
        key = r["key"]
        sha_by_key[key] = r.get("commit_sha")
        if r.get("status") != "MATERIALIZED":
            continue
        if key in special:
            repo_paths[key] = special[key]
        else:
            repo_paths[key] = workspace["repos"] / key

    declared_ids = {c.get("id") for c in packages.get("components", []) if isinstance(c, dict)}
    all_ids = list(dict.fromkeys(list(COMPONENT_SEARCH.keys()) + list(declared_ids)))

    results: list[dict[str, Any]] = []

    for cid in all_ids:
        tokens = COMPONENT_SEARCH.get(cid, [cid])
        best_scan: dict[str, Any] | None = None
        best_repo: str | None = None
        best_cls = PATH_NOT_ESTABLISHED
        rank = {
            PATH_NOT_ESTABLISHED: 0,
            TERM_FOUND: 1,
            DOCUMENTED_ONLY: 2,
            FOUND: 3,
        }

        for rkey, rpath in repo_paths.items():
            scan = _scan_repo(rpath, tokens)
            cls = _classify_discovery(scan)
            if rank.get(cls, 0) > rank.get(best_cls, 0):
                best_scan = scan
                best_repo = rkey
                best_cls = cls

        if best_scan is None:
            best_scan = {
                "term_found": False, "code_found": False,
                "test_found": False, "doc_found": False,
                "code_hits": [], "test_hits": [], "doc_hits": [], "term_hits": [],
            }

        record = make_discovery_record(
            cid,
            status=best_cls,
            path=(best_scan.get("code_hits") or best_scan.get("term_hits") or [None])[0],
            repository=best_repo,
            commit_sha=sha_by_key.get(best_repo) if best_repo else None,
            implementation_found=bool(best_scan.get("code_found")),
            test_suite_found=bool(best_scan.get("test_found")),
            documentation_found=bool(best_scan.get("doc_found")),
            hits={
                "code": best_scan.get("code_hits", []),
                "test": best_scan.get("test_hits", []),
                "doc": best_scan.get("doc_hits", []),
            },
        )
        # Preserve legacy fields for older report consumers (discovery-only meaning)
        record["classification"] = best_cls
        record["code_found"] = record["discovery"]["implementation_found"]
        record["test_found"] = record["discovery"]["test_suite_found"]
        record["doc_found"] = record["discovery"]["documentation_found"]
        results.append(record)

    return results
