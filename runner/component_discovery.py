"""
Evidence-based component discovery across materialized repositories.

TERM_FOUND ≠ CODE_FOUND ≠ TEST_FOUND ≠ EXECUTABLE_FOUND
Never invent paths. PATH_NOT_ESTABLISHED when no evidence.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# Search tokens per component (not proof of implementation)
COMPONENT_SEARCH = {
    "v1_admission": ["admit_or_halt", "evaluate_source", "source_admission", "admission_boundary"],
    "v2_modules": ["swi_v2", "module11", "admit_foundation_input"],
    "node_access_boundary": ["node_access", "node-access", "NodeAccess"],
    "mathematical_evidence_engine": ["mathematical_evidence", "math_evidence"],
    "firefly_memory": ["firefly", "FireflyMemory"],
    "structured_workflow_intelligence": ["structured_workflow", "SWI"],
    "rust_governance_engine": ["governance", "cargo.toml"],
    "v103_api_foundation": ["v103", "api_foundation"],
    "common_sense": ["common_sense", "CommonSense"],
    "reflex_sadu": ["reflex", "sadu", "SADU"],
    "cek": ["cek", "CEK", "observational"],
    "scar": ["scar", "SCAR"],
    "seeder": ["seeder", "SEEDER"],
    "s9_security_maze": ["s9", "security_maze", "SecurityMaze"],
    "zero_trust_task_travel": ["zero_trust", "task_travel", "TaskTravel"],
    "structured_seal": ["structured_seal", "create_seal", "SealedEvidence"],
    "runtime_seal": ["runtime_seal", "RuntimeSeal"],
    "mathematical_zero": ["mathematical_zero", "true_zero", "TrueZero"],
    "geometric_zero": ["geometric_zero", "GeometricZero"],
    "evidence_engine": ["evidence_engine", "EvidenceEngine"],
    "consequence_gate": ["consequence", "ConsequenceGate"],
    "authorization_gate": ["authorization_gate", "AuthorizationGate"],
    "jurisdiction_binding": ["jurisdiction", "Jurisdiction"],
    "pre_revalidation": ["revalidation", "REQUIRES_REVALIDATION", "PRE"],
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
            "term_found": False,
            "code_found": False,
            "test_found": False,
            "doc_found": False,
            "hits": [],
        }

    patterns = [re.compile(re.escape(t), re.IGNORECASE) for t in tokens if t]

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
        matched = False
        for pat in patterns:
            if pat.search(text) or pat.search(rel):
                matched = True
                break
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


def classify_discovery(scan: dict[str, Any]) -> str:
    if scan.get("code_found") and scan.get("test_found"):
        return "IMPLEMENTED"  # code+tests found; not yet executed
    if scan.get("code_found"):
        return "IMPLEMENTED"
    if scan.get("doc_found") and not scan.get("code_found"):
        return "DOCUMENTED_ONLY"
    if scan.get("term_found"):
        return "TERM_FOUND"
    return "PATH_NOT_ESTABLISHED"


def discover_components(
    packages: dict[str, Any],
    repo_results: list[dict[str, Any]],
    workspace: dict[str, Path],
) -> list[dict[str, Any]]:
    """Discover declared + known SWI components across materialized trees."""
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

    results: list[dict[str, Any]] = []

    # Merge manifest components + known search map
    declared_ids = {c.get("id") for c in packages.get("components", []) if isinstance(c, dict)}
    all_ids = list(dict.fromkeys(list(COMPONENT_SEARCH.keys()) + list(declared_ids)))

    for cid in all_ids:
        tokens = COMPONENT_SEARCH.get(cid, [cid])
        best: dict[str, Any] = {
            "component": cid,
            "repository": None,
            "commit_sha": None,
            "path": None,
            "classification": "PATH_NOT_ESTABLISHED",
            "term_found": False,
            "code_found": False,
            "test_found": False,
            "doc_found": False,
            "executable": False,  # requires actual execution elsewhere
            "build": "NOT_RUN",
            "unit_test": "NOT_RUN",
            "test_suite": "NOT_REACHED",
            "hits": {},
        }

        for rkey, rpath in repo_paths.items():
            scan = _scan_repo(rpath, tokens)
            cls = classify_discovery(scan)
            # Prefer stronger classification
            rank = {
                "PATH_NOT_ESTABLISHED": 0,
                "TERM_FOUND": 1,
                "DOCUMENTED_ONLY": 2,
                "IMPLEMENTED": 3,
            }
            if rank.get(cls, 0) > rank.get(best["classification"], 0):
                best.update({
                    "repository": rkey,
                    "commit_sha": sha_by_key.get(rkey),
                    "path": (scan.get("code_hits") or scan.get("term_hits") or [None])[0],
                    "classification": cls,
                    "term_found": scan["term_found"],
                    "code_found": scan["code_found"],
                    "test_found": scan["test_found"],
                    "doc_found": scan["doc_found"],
                    "hits": {
                        "code": scan.get("code_hits", []),
                        "test": scan.get("test_hits", []),
                        "doc": scan.get("doc_hits", []),
                    },
                })
                if scan.get("test_found"):
                    best["test_suite"] = "TEST_FOUND"
                elif scan.get("code_found"):
                    best["test_suite"] = "NO_TEST_SUITE_FOUND"

        results.append(best)

    return results
