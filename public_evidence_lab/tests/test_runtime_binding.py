"""Tests for the observation-only runtime binding adapter.

These tests do not establish RUNTIME_BOUND=YES against a real SWI spine
unless local git metadata is present. They never elevate authority claims.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runner.runtime_binding import bind, observe_git, observe_process


def test_authority_claims_locked_false():
    record = bind(include_status_ceiling=False)
    auth = record["authority"]
    assert auth["adapter_writes_authority"] is False
    assert auth["proven"] is False
    assert auth["sealed"] is False
    assert auth["production_authorized"] is False
    assert auth["independent_review_approved"] is False


def test_user_entered_sha_never_verified():
    record = bind(expected_commit="a" * 40, include_status_ceiling=False)
    assert record["user_entered_sha_treated_as_verified"] is False


def test_schema_present():
    record = bind(include_status_ceiling=False)
    assert record["schema"] == "swi.public-evidence-lab.runtime-binding.v1"
    assert "observed_utc" in record
    assert "runtime_bound_status" in record


def test_process_observation():
    proc = observe_process()
    assert "pid" in proc
    assert "python" in proc
    assert "cwd" in proc


def test_missing_git_yields_not_verified(tmp_path):
    # tmp_path is not a git repo
    git = observe_git(tmp_path)
    assert git["is_git_repo"] is False
    assert git["binding_status"] == "NOT_VERIFIED"
    record = bind(cwd=tmp_path, include_status_ceiling=False)
    assert record["runtime_bound"] is False
    assert record["runtime_bound_status"] == "NOT_VERIFIED"
