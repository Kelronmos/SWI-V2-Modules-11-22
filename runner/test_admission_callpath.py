"""
Regression: admission stage call path must match run_admission_tests signature.

Invokes the same argument pattern used by runner/main.py.
Does not invent admission mechanisms or claim authority.
"""
from __future__ import annotations

import inspect
from pathlib import Path
from unittest.mock import MagicMock

from runner.admission import run_admission_tests
from runner.evidence import EvidenceLedger


def test_run_admission_tests_signature_has_workspace_and_ledger():
    sig = inspect.signature(run_admission_tests)
    params = list(sig.parameters.keys())
    assert params == [
        "packages",
        "repo_results",
        "v1_build",
        "v1_test",
        "workspace",
        "ledger",
    ], f"Unexpected signature params: {params}"


def test_main_call_pattern_accepts_keyword_args(tmp_path: Path):
    """Same keyword call used by runner/main.py must not raise TypeError."""
    packages = {"schema": "swi.online.test.rebuild.packages.v3", "repositories": {}}
    repo_results = [{"key": "v1", "status": "NOT_RUN", "commit_sha": None}]
    workspace = {
        "v1": tmp_path / "v1",
        "v2": tmp_path / "v2",
        "repos": tmp_path / "repos",
        "reports": tmp_path / "reports",
        "logs": tmp_path / "logs",
        "artifacts": tmp_path / "artifacts",
        "downloads": tmp_path / "downloads",
        "root": tmp_path,
    }
    for p in workspace.values():
        if isinstance(p, Path):
            p.mkdir(parents=True, exist_ok=True)

    ledger = EvidenceLedger(run_id="TEST-REGRESSION", runner_version="0.0.0")

    # Exact call pattern from main.py (keyword arguments)
    result = run_admission_tests(
        packages=packages,
        repo_results=repo_results,
        v1_build=None,
        v1_test=None,
        workspace=workspace,
        ledger=ledger,
    )

    assert isinstance(result, dict)
    assert result.get("boundary") == "V1"
    primary = result.get("primary") or {}
    # Never fabricated authority
    assert primary.get("authorization_granted") is False
    assert primary.get("action_permitted") is False
    # V1 not materialized → NOT_FOUND path
    assert primary.get("status") in ("NOT_FOUND", "NOT_EXECUTABLE", "NOT_ESTABLISHED", "EXECUTED")


def test_positional_omission_of_workspace_raises_typeerror():
    """Document the failure mode the Windows run observed."""
    packages = {}
    repo_results = []
    ledger = EvidenceLedger(run_id="T", runner_version="0")
    try:
        # Deliberately wrong: missing workspace (historical bug)
        run_admission_tests(packages, repo_results, None, None, ledger)  # type: ignore[arg-type]
        raised = False
    except TypeError:
        raised = True
    assert raised, "Expected TypeError when workspace is omitted"
