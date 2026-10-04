"""
Regression: every stage function signature must match main.py keyword call pattern.
Prevents the Windows TypeError class (missing positional argument).
"""
from __future__ import annotations

import inspect

from runner.build import build_repositories
from runner.tests import test_repositories
from runner.admission import run_admission_tests
from runner.firefly import run_firefly_tests
from runner.inventory import run_inventory, evaluate_components
from runner.simulation import run_simulation
from runner.repositories import materialize_repositories
from runner.reporting import write_final_status, write_html_report


def _params(fn) -> list[str]:
    return list(inspect.signature(fn).parameters.keys())


def test_materialize_signature():
    assert _params(materialize_repositories) == ["packages", "workspace", "mode", "ledger"]


def test_build_signature():
    assert _params(build_repositories) == [
        "packages", "repo_results", "workspace", "env", "ledger"
    ]


def test_test_signature():
    assert _params(test_repositories) == [
        "packages", "repo_results", "build_results", "workspace", "env", "ledger"
    ]


def test_admission_signature():
    assert _params(run_admission_tests) == [
        "packages", "repo_results", "v1_build", "v1_test", "workspace", "ledger"
    ]


def test_firefly_signature():
    assert _params(run_firefly_tests) == [
        "packages", "repo_results", "workspace", "ledger"
    ]


def test_inventory_signature():
    assert _params(run_inventory) == ["packages", "repo_results", "workspace"]


def test_evaluate_components_signature():
    assert _params(evaluate_components) == ["packages", "repo_results", "inventory"]


def test_simulation_signature():
    assert _params(run_simulation) == ["case_count", "packages", "ledger"]


def test_write_final_status_signature():
    assert _params(write_final_status) == [
        "reports_dir", "ledger", "components", "simulation"
    ]


def test_write_html_report_signature():
    assert _params(write_html_report) == ["reports_dir", "final_report"]
