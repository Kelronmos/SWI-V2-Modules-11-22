"""
Failure domain classification.

REBUILD ENVIRONMENT CONDITION
  ≠ REPOSITORY FAILURE
  ≠ SWI BEHAVIORAL FAILURE
  ≠ PROOF FAILURE

SOURCE_DIRTY / missing toolchain / NOT_RUN are not SWI defects
unless an executable assertion demonstrates a defect.
"""
from __future__ import annotations

from typing import Any

DOMAIN_ENVIRONMENT = "ENVIRONMENT"
DOMAIN_ACQUISITION = "ACQUISITION"
DOMAIN_TOOLCHAIN = "TOOLCHAIN"
DOMAIN_BUILD = "BUILD"
DOMAIN_TEST = "TEST"
DOMAIN_ASSERTION = "ASSERTION"
DOMAIN_EVIDENCE = "EVIDENCE"
DOMAIN_STATUS = "STATUS"

SWI_DEFECT_NOT_ESTABLISHED = "NOT_ESTABLISHED"
SWI_DEFECT_INVESTIGATION = "INVESTIGATION_REQUIRED"
SWI_DEFECT_YES = "YES"  # only if assertion proves behavioral defect


def classify_repo_status(status: str | None, reason: str | None = None) -> dict[str, Any]:
    s = (status or "").upper()
    r = (reason or "").lower()

    if s in ("SOURCE_DIRTY",):
        return {
            "domain": DOMAIN_ACQUISITION,
            "status": "BLOCKED",
            "test_executed": False,
            "build_executed": False,
            "swi_defect": SWI_DEFECT_NOT_ESTABLISHED,
            "note": "Workspace dirty — rebuild blocked, not SWI implementation failure",
        }
    if s in ("NOT_MATERIALIZED", "CLONE_FAILED", "BLOCKED"):
        return {
            "domain": DOMAIN_ACQUISITION,
            "status": s or "BLOCKED",
            "test_executed": False,
            "build_executed": False,
            "swi_defect": SWI_DEFECT_NOT_ESTABLISHED,
            "note": "Acquisition condition — not behavioral SWI evidence",
        }
    if "missing toolchain" in r or "missing" in r and any(
        t in r for t in ("rust", "cargo", "node", "python", "git")
    ):
        return {
            "domain": DOMAIN_TOOLCHAIN,
            "status": "NOT_RUN",
            "test_executed": False,
            "build_executed": False,
            "swi_defect": SWI_DEFECT_NOT_ESTABLISHED,
            "note": "Toolchain unavailable — build/test not evidence of code failure",
        }
    if s in ("NOT_RUN", "NOT_APPLICABLE", "SKIPPED"):
        return {
            "domain": DOMAIN_ENVIRONMENT,
            "status": s,
            "test_executed": False,
            "build_executed": False,
            "swi_defect": SWI_DEFECT_NOT_ESTABLISHED,
            "note": "Not executed — no behavioral evidence",
        }
    if s == "PASS":
        return {
            "domain": DOMAIN_TEST if "test" in r else DOMAIN_BUILD,
            "status": "PASS",
            "test_executed": True,
            "build_executed": True,
            "swi_defect": SWI_DEFECT_NOT_ESTABLISHED,
            "note": "Execution succeeded — still not proof",
        }
    if s == "FAIL":
        return {
            "domain": DOMAIN_TEST if "test" in r else DOMAIN_BUILD,
            "status": "FAIL",
            "test_executed": True,
            "build_executed": True,
            "swi_defect": SWI_DEFECT_INVESTIGATION,
            "note": "Executed and failed — investigate assertion/root error; not auto SWI architecture failure",
        }
    if s == "MATERIALIZED":
        return {
            "domain": DOMAIN_ACQUISITION,
            "status": "MATERIALIZED",
            "test_executed": False,
            "build_executed": False,
            "swi_defect": SWI_DEFECT_NOT_ESTABLISHED,
            "note": "Acquired only",
        }
    return {
        "domain": DOMAIN_STATUS,
        "status": s or "UNKNOWN",
        "test_executed": False,
        "build_executed": False,
        "swi_defect": SWI_DEFECT_NOT_ESTABLISHED,
        "note": "Unclassified execution state",
    }


def classify_build_result(rec: dict[str, Any]) -> dict[str, Any]:
    status = rec.get("status")
    reason = rec.get("reason") or ""
    base = classify_repo_status(status, reason)
    base["key"] = rec.get("key")
    base["stage"] = "BUILD"
    base["exit_code"] = rec.get("exit_code")
    base["command"] = rec.get("command")
    if status == "FAIL":
        base["domain"] = DOMAIN_BUILD
        base["build_executed"] = True
        base["swi_defect"] = SWI_DEFECT_INVESTIGATION
        base["note"] = (
            "Build command executed and failed — investigate log; "
            "may be environment (exit 126/127) or code. Not automatic SWI defect."
        )
        # Shell missing command often 127; permission 126
        ec = rec.get("exit_code")
        if ec in (126, 127):
            base["domain"] = DOMAIN_ENVIRONMENT
            base["swi_defect"] = SWI_DEFECT_NOT_ESTABLISHED
            base["note"] = f"Exit {ec} often means command/shell/env issue on host, not proven SWI defect"
    elif status == "BLOCKED":
        base["domain"] = DOMAIN_ACQUISITION
        base["swi_defect"] = SWI_DEFECT_NOT_ESTABLISHED
    elif status == "NOT_RUN":
        base["domain"] = DOMAIN_TOOLCHAIN if "toolchain" in reason.lower() else DOMAIN_ENVIRONMENT
        base["swi_defect"] = SWI_DEFECT_NOT_ESTABLISHED
    return base


def classify_test_result(rec: dict[str, Any]) -> dict[str, Any]:
    status = rec.get("status")
    reason = rec.get("reason") or ""
    base = classify_repo_status(status, reason)
    base["key"] = rec.get("key")
    base["stage"] = "TEST"
    base["exit_code"] = rec.get("exit_code")
    base["command"] = rec.get("command")
    if status == "FAIL":
        base["domain"] = DOMAIN_TEST
        base["test_executed"] = True
        base["swi_defect"] = SWI_DEFECT_INVESTIGATION
        base["note"] = (
            "Test suite executed and failed — identify first assertion failure; "
            "do not flatten to 'SWI failed'."
        )
        ec = rec.get("exit_code")
        if ec in (126, 127):
            base["domain"] = DOMAIN_ENVIRONMENT
            base["swi_defect"] = SWI_DEFECT_NOT_ESTABLISHED
            base["note"] = f"Exit {ec} suggests host command/env issue before test assertions ran"
    elif status == "BLOCKED":
        base["domain"] = DOMAIN_ACQUISITION
        base["swi_defect"] = SWI_DEFECT_NOT_ESTABLISHED
    return base


def classify_all(
    repo_results: list[dict],
    build_results: list[dict],
    test_results: list[dict],
) -> dict[str, Any]:
    acquisition = [
        {"key": r.get("key"), **classify_repo_status(r.get("status"), r.get("reason"))}
        for r in repo_results
    ]
    builds = [classify_build_result(b) for b in build_results]
    tests = [classify_test_result(t) for t in test_results]

    return {
        "acquisition": acquisition,
        "build": builds,
        "test": tests,
        "summary": {
            "environment_blocked": sum(
                1 for x in acquisition + builds + tests
                if x.get("domain") in (DOMAIN_ENVIRONMENT, DOMAIN_TOOLCHAIN, DOMAIN_ACQUISITION)
                and x.get("status") in ("BLOCKED", "NOT_RUN", "SOURCE_DIRTY")
            ),
            "investigation_required": sum(
                1 for x in builds + tests
                if x.get("swi_defect") == SWI_DEFECT_INVESTIGATION
            ),
            "swi_defect_proven": 0,  # never auto-proven by runner
            "note": (
                "Windows rebuild/diagnostic execution. "
                "ENVIRONMENT/ACQUISITION/TOOLCHAIN conditions are not SWI architecture failures. "
                "INVESTIGATION_REQUIRED means an executed command failed — inspect root error."
            ),
        },
    }


def rebuild_report_header(env: dict[str, Any], run_id: str, runner_version: str, mode: str) -> dict[str, Any]:
    return {
        "run_type": "SWI REBUILD / BOOT DIAGNOSTIC",
        "platform": env.get("os") or "UNKNOWN",
        "python": env.get("python"),
        "git": env.get("git"),
        "node": env.get("node"),
        "rust": env.get("rust"),
        "cargo": env.get("cargo"),
        "mode": mode,
        "real_world_action": "NONE",
        "run_id": run_id,
        "runner_version": runner_version,
    }
