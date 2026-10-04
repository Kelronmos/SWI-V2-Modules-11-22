#!/usr/bin/env python3
"""
SWI Universal Test / Demonstration Runner — entry point.

Order:
  TOOLCHAIN → MANIFEST → MATERIALIZE → INVENTORY
  → V1 BUILD → V1 TEST → V1 ADMISSION
  → V2 / downstream (only evidence collection; not alternate admission)
  → REPORTS

V1 test FAIL is never overwritten by build PASS.
Admission after V1 test FAIL runs only as ISOLATED_DIAGNOSTIC.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from runner import __version__, RUNNER_NAME
from runner.bootstrap import detect_environment, ensure_workspace
from runner.repositories import materialize_repositories
from runner.build import build_repositories
from runner.tests import test_repositories
from runner.admission import run_admission_tests
from runner.firefly import run_firefly_tests
from runner.inventory import run_inventory, evaluate_components
from runner.simulation import run_simulation
from runner.evidence import EvidenceLedger, FINAL_CLAIMS
from runner.reporting import write_final_status, write_json_report, write_html_report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SWI Universal Test / Demonstration Runner (TEST_ONLY)"
    )
    parser.add_argument("--cases", type=int, default=100, choices=[10, 100, 1000, 8000])
    parser.add_argument("--mode", choices=["smoke", "full", "audit"], default="smoke")
    parser.add_argument("--packages", type=Path, default=None)
    return parser.parse_args(argv)


def banner() -> None:
    print("=" * 60)
    print(RUNNER_NAME)
    print("=" * 60)
    print("MODE:                     TEST + SIMULATION + EVIDENCE")
    print("REAL-WORLD ACTION:        NONE")
    print("PRODUCTION AUTHORIZATION: NO")
    print("V1 ADMISSION BOUNDARY:    ENFORCED")
    print("=" * 60)
    print()


def load_packages(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"packages.json not found: {path}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not str(data.get("schema", "")).startswith("swi.online.test.rebuild.packages."):
        raise ValueError(f"Unsupported schema: {data.get('schema')}")
    return data


def _split_by_key(results: list[dict], key: str) -> dict | None:
    for r in results:
        if r.get("key") == key:
            return r
    return None


def _status_of(rec: dict | None, default: str = "NOT_RUN") -> str:
    if not rec:
        return default
    return str(rec.get("status") or default)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    banner()

    script_dir = Path(__file__).resolve().parent.parent
    packages_path = args.packages or (script_dir / "packages.json")
    run_id = f"SWI-RUN-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    print(f"RUN_ID          : {run_id}")
    print(f"Runner version  : {__version__}")
    print(f"Mode            : {args.mode}")
    print(f"Cases requested : {args.cases}")
    print()

    ledger = EvidenceLedger(run_id=run_id, runner_version=__version__)
    runner_error = False
    runner_error_detail: str | None = None

    # Defaults for final status fields
    build_results: list[dict] = []
    test_results: list[dict] = []
    admission: dict[str, Any] = {}
    firefly_results: dict[str, Any] = {}
    simulation_results: dict[str, Any] = {}
    inventory: dict[str, Any] = {}
    components: list = []
    repo_results: list = []
    env: dict[str, Any] = {}
    workspace: dict[str, Path] = {}

    try:
        packages = load_packages(packages_path)
        print(f"[01] Manifest loaded (schema {packages.get('schema')})")
    except Exception as exc:
        print(f"FATAL: {exc}")
        return 1

    print("[02] Toolchain detection...")
    env = detect_environment()
    ledger.record_environment(env)
    print(f"     OS={env.get('os')} Python={env.get('python')} Git={env.get('git')}")
    print()

    print("[03] Workspace...")
    workspace = ensure_workspace(script_dir, packages.get("workspace", {}))
    print(f"     {workspace['root']}")
    print()

    print("[04] Materialize repositories + record SHAs...")
    try:
        repo_results = materialize_repositories(
            packages=packages, workspace=workspace, mode=args.mode, ledger=ledger,
        )
    except Exception as exc:
        runner_error = True
        runner_error_detail = f"materialization: {exc}"
        print(f"FATAL: {exc}")
        write_final_status(workspace["reports"], ledger)
        return 1
    print(f"     Materialized: {sum(1 for r in repo_results if r.get('status')=='MATERIALIZED')}/{len(repo_results)}")
    print()

    print("[05] Inventory + component evaluation...")
    inventory = run_inventory(packages, repo_results, workspace)
    components = evaluate_components(packages, repo_results, inventory)
    print(f"     Components declared={len(components)} present={sum(1 for c in components if c['status']['present'])}")
    print()

    # ---- V1 BUILD ----
    print("[06] V1 BUILD...")
    if args.mode == "audit":
        build_results = []
    else:
        build_results = build_repositories(packages, repo_results, workspace, env, ledger)
    v1_build = _split_by_key(build_results, "v1")
    v2_build = _split_by_key(build_results, "v2")
    v1_build_status = _status_of(v1_build)
    print(f"     V1 BUILD: {v1_build_status}")
    print()

    # ---- V1 TEST (result is independent; never overwritten by build) ----
    print("[07] V1 TEST...")
    if args.mode == "audit":
        test_results = []
    else:
        test_results = test_repositories(
            packages, repo_results, build_results, workspace, env, ledger,
        )
    v1_test = _split_by_key(test_results, "v1")
    v2_test = _split_by_key(test_results, "v2")
    v1_test_status = _status_of(v1_test)
    print(f"     V1 TEST: {v1_test_status}")
    print()

    # ---- V1 ADMISSION ----
    # Signature (authoritative):
    #   run_admission_tests(packages, repo_results, v1_build, v1_test, workspace, ledger)
    # Always use keyword arguments to prevent positional drift.
    print("[08] V1 ADMISSION — discover and bind actual mechanisms...")
    admission_mode = "NORMAL"
    if v1_test_status == "FAIL":
        # Diagnostics still useful; must not authorize downstream
        admission_mode = "ISOLATED_DIAGNOSTIC"
        print("     ADMISSION_MODE = ISOLATED_DIAGNOSTIC (V1 TEST=FAIL)")

    if args.mode == "audit":
        admission = {
            "primary": {"status": "NOT_ESTABLISHED", "authorization_granted": False, "action_permitted": False},
            "admission_established": False,
            "discovery": {"status": "SKIPPED", "three_state": "SKIPPED"},
            "report_section": {
                "V1": {"FOUND": False, "EXECUTABLE": False, "EXECUTED": False, "RESULT": "NOT_ESTABLISHED"},
                "V2": {"ADMISSION_AUTHORITY": False},
                "ALTERNATE_ADMISSION_PATHS": "NOT_TESTED",
            },
        }
        print("     Skipped (audit mode)")
    else:
        try:
            admission = run_admission_tests(
                packages=packages,
                repo_results=repo_results,
                v1_build=v1_build,
                v1_test=v1_test,
                workspace=workspace,
                ledger=ledger,
            )
        except TypeError as exc:
            runner_error = True
            runner_error_detail = f"admission TypeError: {exc}"
            tb = traceback.format_exc()
            print(f"     ERROR: {exc}")
            admission = {
                "primary": {
                    "status": "ERROR",
                    "authorization_granted": False,
                    "action_permitted": False,
                    "reason": str(exc),
                    "traceback": tb,
                },
                "admission_established": False,
                "discovery": {"status": "ERROR", "three_state": "ERROR"},
                "execution": {"executed": False, "executions": []},
                "report_section": {
                    "V1": {"FOUND": False, "EXECUTABLE": False, "EXECUTED": False, "RESULT": "ERROR"},
                    "V2": {"ADMISSION_AUTHORITY": False},
                    "ALTERNATE_ADMISSION_PATHS": "NOT_TESTED",
                },
                "error": str(exc),
                "traceback": tb,
            }
            ledger.record_failure("admission", str(exc))
        except Exception as exc:
            runner_error = True
            runner_error_detail = f"admission: {exc}"
            tb = traceback.format_exc()
            print(f"     ERROR: {exc}")
            admission = {
                "primary": {
                    "status": "ERROR",
                    "authorization_granted": False,
                    "action_permitted": False,
                    "reason": str(exc),
                    "traceback": tb,
                },
                "admission_established": False,
                "discovery": {"status": "ERROR", "three_state": "ERROR"},
                "execution": {"executed": False, "executions": []},
                "report_section": {
                    "V1": {"FOUND": False, "EXECUTABLE": False, "EXECUTED": False, "RESULT": "ERROR"},
                    "V2": {"ADMISSION_AUTHORITY": False},
                    "ALTERNATE_ADMISSION_PATHS": "NOT_TESTED",
                },
                "error": str(exc),
                "traceback": tb,
            }
            ledger.record_failure("admission", str(exc))

    admission["admission_mode"] = admission_mode
    primary = admission.get("primary") or {}
    # Support both shapes: primary.status and primary.admission.status
    if isinstance(primary.get("admission"), dict):
        primary_status = primary["admission"].get("status") or primary.get("status") or "UNKNOWN"
    else:
        primary_status = primary.get("status") or "UNKNOWN"

    admission_ok = bool(admission.get("admission_established", False))
    # Isolated diagnostic can never establish downstream authority
    if admission_mode == "ISOLATED_DIAGNOSTIC":
        admission_ok = False
        admission["admission_established"] = False
        admission["downstream_permitted"] = False

    discovery_status = (admission.get("discovery") or {}).get("status", "UNKNOWN")
    print(f"     Discovery: {discovery_status}")
    print(f"     Primary admission status: {primary_status}")
    print(f"     Admission established: {admission_ok}")
    print(f"     ADMISSION_MODE: {admission_mode}")
    print()

    # V1→V2 handoff: do not invent; report NOT_FOUND / NOT_TESTED only
    v1_to_v2_handoff = "NOT_FOUND"  # no defined handoff interface located/executed

    # Downstream reachability
    if admission_ok and v1_to_v2_handoff == "FOUND":
        downstream_flow = "REACHED"
    else:
        downstream_flow = "NOT_REACHED"

    if not admission_ok:
        print("[09] NOTE: V1 admission not established — downstream = NOT_REACHED")
        print()

    print("[09] V2 BUILD status...")
    v2_build_status = _status_of(v2_build)
    print(f"     V2 BUILD: {v2_build_status}")
    print()

    print("[10] V2 TEST status...")
    v2_test_status = _status_of(v2_test)
    print(f"     V2 TEST: {v2_test_status}")
    print()

    print("[11] Firefly (not an admission path)...")
    if args.mode == "audit":
        firefly_results = {"status": "SKIPPED"}
    else:
        try:
            firefly_results = run_firefly_tests(packages, repo_results, workspace, ledger)
        except Exception as exc:
            firefly_results = {"status": "ERROR", "error": str(exc)}
            ledger.record_failure("firefly", str(exc))
    print()

    print("[12] Synthetic simulation (not an admission path)...")
    if args.mode == "audit":
        simulation_results = {"status": "SKIPPED"}
    else:
        try:
            simulation_results = run_simulation(args.cases, packages, ledger)
            simulation_results["admission_bypass"] = False
            simulation_results["note"] = "SIMULATION ≠ PROOF. Simulation is not an admission gate."
        except Exception as exc:
            simulation_results = {"status": "ERROR", "error": str(exc)}
            ledger.record_failure("simulation", str(exc))
    print()

    print("[13–14] Reports + FINAL STATUS...")
    reports = workspace["reports"]

    stage_status = {
        "runner_error": runner_error,
        "runner_error_detail": runner_error_detail,
        "v1_build": v1_build_status,
        "v1_test": v1_test_status,
        "v1_admission": primary_status,
        "admission_mode": admission_mode,
        "v1_to_v2_handoff": v1_to_v2_handoff,
        "downstream_flow": downstream_flow,
        "v2_build": v2_build_status,
        "v2_test": v2_test_status,
        "proven": False,
        "sealed": False,
        "production_authorized": False,
    }

    write_json_report(reports, "ENVIRONMENT.json", env)
    write_json_report(reports, "REPOSITORIES.json", repo_results)
    write_json_report(reports, "inventory.json", inventory)
    write_json_report(reports, "component_status.json", components)
    write_json_report(reports, "BUILD_RESULTS.json", build_results)
    write_json_report(reports, "TEST_RESULTS.json", test_results)
    write_json_report(reports, "ADMISSION_RESULTS.json", admission)
    write_json_report(reports, "FIREFLY_RESULTS.json", firefly_results)
    write_json_report(reports, "simulation_results.json", simulation_results)
    write_json_report(reports, "STAGE_STATUS.json", stage_status)

    report_section = admission.get("report_section", {})
    final_report = {
        "schema": "swi.execution.report.v3",
        "execution": {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "platform": env.get("os"),
            "python": env.get("python"),
            "runner_version": __version__,
            "mode": args.mode,
            "cases_requested": args.cases,
        },
        "stage_status": stage_status,
        "architecture": {
            "admission_boundary": "V1",
            "v2_role": "DOWNSTREAM / CONTINUATION",
            "v1_to_v2_handoff": v1_to_v2_handoff,
            "bypass_forbidden": [
                "INPUT → V2",
                "INPUT → CEK",
                "INPUT → REFLEX/SADU",
                "INPUT → S9",
                "INPUT → SEAL",
                "INPUT → EVIDENCE ENGINE",
                "INPUT → FIREFLY",
                "INPUT → RELATED",
                "INPUT → SIMULATION",
            ],
        },
        "admission_boundary_report": report_section,
        "claims": FINAL_CLAIMS.copy(),
        "admission": primary,
        "admission_established": admission_ok,
        "admission_mode": admission_mode,
        "discovery": admission.get("discovery"),
        "repositories": repo_results,
        "components": components,
        "toolchain": env,
        "build": build_results,
        "tests": test_results,
        "firefly": firefly_results,
        "simulation": {
            "summary": simulation_results.get("summary") if isinstance(simulation_results, dict) else None,
            "note": "SIMULATION ≠ PROOF; simulation is not an admission gate",
        },
        "limitations": [
            "Runner binds to actual V1 mechanisms; does not invent admit()",
            "V1 BUILD/TEST PASS ≠ V1 ADMISSION PROVEN",
            "CHECK_PASSED ≠ authority ADMITTED",
            "V1 TEST FAIL is never overwritten by BUILD PASS",
            "ISOLATED_DIAGNOSTIC admission cannot authorize downstream",
            "v1_to_v2_handoff remains NOT_FOUND until a real interface is evidenced",
            "No alternate component may become an admission boundary",
            runner_error_detail,
        ],
    }
    write_json_report(reports, "final_report.json", final_report)
    write_html_report(reports, final_report)
    write_final_status(reports, ledger, components=components, simulation=simulation_results)

    print()
    print("=" * 60)
    print("SWI UNIVERSAL TEST — RUN COMPLETE")
    print("=" * 60)
    print()
    print("STAGE STATUS")
    print(f"  runner_error        : {runner_error}")
    print(f"  v1_build            : {v1_build_status}")
    print(f"  v1_test             : {v1_test_status}")
    print(f"  v1_admission        : {primary_status}")
    print(f"  admission_mode      : {admission_mode}")
    print(f"  v1_to_v2_handoff    : {v1_to_v2_handoff}")
    print(f"  downstream_flow     : {downstream_flow}")
    print()
    for k, v in FINAL_CLAIMS.items():
        print(f"{k.upper():<28}: {v}")
    print()
    print("CHECK_PASSED ≠ ADMITTED  |  ACCEPT_CLAIM_ONLY ≠ execution authority")
    print("BUILD ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION")
    print()

    return 1 if runner_error else 0


if __name__ == "__main__":
    sys.exit(main())
