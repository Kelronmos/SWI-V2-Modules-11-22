"""
D01–D10: Discovery must never masquerade as assertion PASS/FAIL.
"""
from __future__ import annotations

from runner.domains import (
    FOUND, PATH_NOT_ESTABLISHED, DOCUMENTED_ONLY,
    PASS, FAIL, ERROR, NOT_RUN, NO_TEST_SUITE_FOUND,
    make_discovery_record, make_assertion_record,
    DISCOVERY_STATUSES, ASSERTION_STATUSES,
)


def test_d01_found_without_tests_is_no_suite_not_pass():
    r = make_discovery_record(
        "firefly_memory",
        status=FOUND,
        implementation_found=True,
        test_suite_found=False,
    )
    assert r["discovery"]["status"] == FOUND
    assert r["tests"]["status"] == NO_TEST_SUITE_FOUND
    assert r["tests"]["assertions"] == []
    assert r["tests"]["status"] != PASS


def test_d02_path_not_established_is_not_test_fail():
    r = make_discovery_record("common_sense", status=PATH_NOT_ESTABLISHED)
    assert r["discovery"]["status"] == PATH_NOT_ESTABLISHED
    assert r["tests"]["status"] == NOT_RUN
    assert r["tests"]["status"] != FAIL
    assert r["tests"]["assertions"] == []


def test_d03_suite_found_does_not_mean_pass():
    r = make_discovery_record(
        "v1_admission",
        status=FOUND,
        implementation_found=True,
        test_suite_found=True,
    )
    assert r["discovery"]["test_suite_found"] is True
    assert r["tests"]["executed"] is False
    assert r["tests"]["status"] != PASS


def test_d04_assertion_pass_requires_execution_record():
    a = make_assertion_record(
        "A01", "status_engine",
        "UNKNOWN remains UNKNOWN",
        expected="UNKNOWN", actual="UNKNOWN", result=PASS,
    )
    assert a["result"] == PASS
    assert a["execution"]["attempted"] is True


def test_d05_assertion_fail_is_fail_not_unknown():
    a = make_assertion_record(
        "X1", "demo",
        "must halt",
        expected="HALT", actual="PASS", result=FAIL,
    )
    assert a["result"] == FAIL
    assert a["result"] not in DISCOVERY_STATUSES


def test_d06_implementation_found_without_execution():
    r = make_discovery_record(
        "v1_admission",
        status=FOUND,
        implementation_found=True,
        test_suite_found=True,
    )
    assert r["discovery"]["implementation_found"] is True
    assert r["tests"]["executed"] is False
    assert r["tests"]["status"] != PASS


def test_d07_execution_pass_is_assertion_not_discovery():
    a = make_assertion_record(
        "L01", "v1_admission",
        "valid source CHECK_PASSED",
        expected="PASS", actual="PASS", result=PASS,
    )
    assert a["result"] in ASSERTION_STATUSES
    assert a["result"] not in DISCOVERY_STATUSES


def test_d08_handoff_not_found_is_discovery_not_fail():
    r = make_discovery_record("v1_v2_handoff", status=PATH_NOT_ESTABLISHED)
    assert r["discovery"]["status"] == PATH_NOT_ESTABLISHED
    assert r["tests"]["status"] == NOT_RUN
    assert r["tests"]["status"] != FAIL


def test_d09_documented_only_not_implementation():
    r = make_discovery_record(
        "feature_x",
        status=DOCUMENTED_ONLY,
        documentation_found=True,
        implementation_found=False,
    )
    assert r["discovery"]["status"] == DOCUMENTED_ONLY
    assert r["discovery"]["implementation_found"] is False
    assert r["tests"]["status"] == NOT_RUN


def test_d10_discovered_impl_with_failing_assertion():
    r = make_discovery_record(
        "demo", status=FOUND, implementation_found=True, test_suite_found=True,
    )
    a = make_assertion_record(
        "N1", "demo", "must reject",
        expected="HALT", actual="ACCEPT", result=FAIL,
    )
    assert r["discovery"]["status"] == FOUND
    assert a["result"] == FAIL
    assert r["discovery"]["status"] != FAIL


def test_discovery_statuses_not_used_as_test_result():
    r = make_discovery_record("x", status=FOUND, implementation_found=True)
    assert r["tests"]["status"] != FOUND
    assert r["tests"]["status"] in ASSERTION_STATUSES
    for s in DISCOVERY_STATUSES:
        assert s not in {PASS, FAIL, ERROR}
