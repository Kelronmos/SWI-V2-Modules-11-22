"""
Two execution domains: DISCOVERY vs TEST ASSERTION.

DISCOVERY answers: what exists?
ASSERTION answers: does executable behavior match expectation?

Never convert discovery into PASS/FAIL.
"""
from __future__ import annotations

from typing import Any

# --- Discovery outcomes (NOT test results) ---
FOUND = "FOUND"
NOT_FOUND = "NOT_FOUND"
PATH_NOT_ESTABLISHED = "PATH_NOT_ESTABLISHED"
DOCUMENTED_ONLY = "DOCUMENTED_ONLY"
IMPLEMENTATION_FOUND = "IMPLEMENTATION_FOUND"
TEST_SUITE_FOUND = "TEST_SUITE_FOUND"
INTERFACE_FOUND = "INTERFACE_FOUND"
UNKNOWN = "UNKNOWN"
TERM_FOUND = "TERM_FOUND"

# --- Assertion outcomes (require execution) ---
PASS = "PASS"
FAIL = "FAIL"
ERROR = "ERROR"
NOT_RUN = "NOT_RUN"
BLOCKED = "BLOCKED"
NOT_APPLICABLE = "NOT_APPLICABLE"
NO_TEST_SUITE_FOUND = "NO_TEST_SUITE_FOUND"

DISCOVERY_STATUSES = {
    FOUND, NOT_FOUND, PATH_NOT_ESTABLISHED, DOCUMENTED_ONLY,
    IMPLEMENTATION_FOUND, TEST_SUITE_FOUND, INTERFACE_FOUND,
    UNKNOWN, TERM_FOUND,
}

ASSERTION_STATUSES = {
    PASS, FAIL, ERROR, NOT_RUN, BLOCKED, NOT_APPLICABLE, NO_TEST_SUITE_FOUND,
}


def make_discovery_record(
    component: str,
    *,
    status: str = PATH_NOT_ESTABLISHED,
    path: str | None = None,
    repository: str | None = None,
    commit_sha: str | None = None,
    implementation_found: bool = False,
    test_suite_found: bool = False,
    documentation_found: bool = False,
    hits: dict | None = None,
) -> dict[str, Any]:
    """Discovery record — tests always start as NOT_RUN / empty assertions."""
    if status not in DISCOVERY_STATUSES and status not in {
        "IMPLEMENTED",  # legacy classification mapped below
    }:
        # Map legacy component_discovery classifications
        pass

    # Map legacy labels into discovery status
    if status == "IMPLEMENTED":
        status = FOUND if implementation_found else FOUND
    elif status == "DOCUMENTED_ONLY":
        status = DOCUMENTED_ONLY
    elif status == "TERM_FOUND":
        status = TERM_FOUND
    elif status == "PATH_NOT_ESTABLISHED":
        status = PATH_NOT_ESTABLISHED

    tests_status = NOT_RUN
    if implementation_found and not test_suite_found:
        tests_status = NO_TEST_SUITE_FOUND
    elif not implementation_found and status in (PATH_NOT_ESTABLISHED, DOCUMENTED_ONLY, TERM_FOUND):
        tests_status = NOT_RUN

    return {
        "component": component,
        "discovery": {
            "status": status,
            "path": path,
            "repository": repository,
            "commit_sha": commit_sha,
            "implementation_found": implementation_found,
            "test_suite_found": test_suite_found,
            "documentation_found": documentation_found,
            "hits": hits or {},
        },
        "tests": {
            "status": tests_status,
            "assertions": [],  # empty until real assertions execute
            "executed": False,
        },
    }


def make_assertion_record(
    test_id: str,
    component: str,
    assertion: str,
    *,
    expected: Any,
    actual: Any,
    result: str,
    preconditions: list | None = None,
    attempted: bool = True,
    exit_code: int | None = 0,
) -> dict[str, Any]:
    if result not in ASSERTION_STATUSES:
        raise ValueError(f"Invalid assertion result: {result}")
    return {
        "test_id": test_id,
        "component": component,
        "assertion": assertion,
        "preconditions": preconditions or [],
        "execution": {
            "attempted": attempted,
            "exit_code": exit_code,
        },
        "expected": expected,
        "actual": actual,
        "result": result,
    }


def discovery_to_test_forbidden(discovery_status: str) -> bool:
    """True if using this discovery status as a test PASS/FAIL would be illegal."""
    return discovery_status in DISCOVERY_STATUSES
