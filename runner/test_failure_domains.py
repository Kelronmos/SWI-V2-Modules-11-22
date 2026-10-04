"""Failure domain classification must not flatten rebuild env into SWI defect."""
from __future__ import annotations

from runner.failure_domains import (
    classify_repo_status,
    classify_build_result,
    classify_test_result,
    DOMAIN_ACQUISITION,
    DOMAIN_ENVIRONMENT,
    DOMAIN_TOOLCHAIN,
    DOMAIN_TEST,
    DOMAIN_BUILD,
    SWI_DEFECT_NOT_ESTABLISHED,
    SWI_DEFECT_INVESTIGATION,
)


def test_source_dirty_is_acquisition_not_swi_defect():
    c = classify_repo_status("SOURCE_DIRTY")
    assert c["domain"] == DOMAIN_ACQUISITION
    assert c["swi_defect"] == SWI_DEFECT_NOT_ESTABLISHED
    assert c["test_executed"] is False


def test_missing_toolchain_not_swi_defect():
    c = classify_repo_status("NOT_RUN", "Missing toolchain: rust")
    assert c["domain"] == DOMAIN_TOOLCHAIN
    assert c["swi_defect"] == SWI_DEFECT_NOT_ESTABLISHED


def test_exit_127_build_is_environment():
    c = classify_build_result({"key": "x", "status": "FAIL", "exit_code": 127, "reason": "exit_code=127"})
    assert c["domain"] == DOMAIN_ENVIRONMENT
    assert c["swi_defect"] == SWI_DEFECT_NOT_ESTABLISHED


def test_executed_test_fail_is_investigation():
    c = classify_test_result({"key": "v1", "status": "FAIL", "exit_code": 1, "reason": "exit_code=1"})
    assert c["domain"] == DOMAIN_TEST
    assert c["test_executed"] is True
    assert c["swi_defect"] == SWI_DEFECT_INVESTIGATION


def test_blocked_build_not_swi_defect():
    c = classify_build_result({"key": "n", "status": "BLOCKED", "reason": "Repository not materialized"})
    assert c["domain"] == DOMAIN_ACQUISITION
    assert c["swi_defect"] == SWI_DEFECT_NOT_ESTABLISHED
