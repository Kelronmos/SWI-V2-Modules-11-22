#!/usr/bin/env python3
"""
SWI Universal Test / Demonstration Runner — entry point.

Order:
  TOOLCHAIN → MANIFEST → MATERIALIZE → INVENTORY
  → V1 BUILD → V1 TEST → V1 ADMISSION
  → V2 / downstream (evidence collection only; not alternate admission)
  → REPORTS

All stage functions are invoked with keyword arguments to prevent
positional signature drift (the class of TypeError seen on Windows).

V1 test FAIL is never overwritten by build PASS.
Admission after V1 test FAIL runs only as ISOLATED_DIAGNOSTIC.
"""

from __future__ import annotations

import argparse
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
        import json
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
            packages=packages,
            workspace=workspace,
            mode=args.mode,
            ledger=ledger,
        )
    except Exception as exc:
        runner_error = True
        runner_error_detail = f"materialization: {exc}"
        print(f"FATAL: {exc}")
        write_final_status(reports_dir=workspace["reports"], ledger=ledger)
        return 1
    print(f"     Materialized: {sum(1 for r in repo_results if r.get('status')=='MATERIALIZED')}/{len(repo_results)}")
    print()

    print("[05] Inventory + component evaluation...")
    try:
        inventory = run_inventory(
            packages=packages,
            repo_results=repo_results,
            workspace=workspace,
        )
        components = evaluate_components(
            packages=packages,
            repo_results=repo_results,
            inventory=inventory,
        )
    except TypeError as exc:
        runner_error = True
        runner_error_detail = f"inventory TypeError: {exc}"
        print(f"     ERROR: {exc}")
        inventory, components = {}, []
    except Exception as exc:
        runner_error = True
        runner_error_detail = f"inventory: {exc}"
        print(f"     ERROR: {exc}")
        inventory, components = {}, []
    print(f"     Components declared={len(components)} present={sum(1 for c in components if c.get('status', {}).get('present'))}")
    print()

    # ---- BUILD (V1 + V2 and all declared repos) ----
    print("[06] BUILD (all declared repositories)...")
    if args.mode == "audit":
        build_results = []
    else:
        try:
            build_results = build_repositories(
                packages=packages,
                repo_results=repo_results,
                workspace=workspace,
                env=env,
                ledger=ledger,
            )
        except TypeError as exc:
            runner_error = True
            runner_error_detail = f"build TypeError: {exc}"
            print(f"     ERROR: {exc}")
            print(traceback.format_exc())
            build_results = []
            ledger.record_failure("build", str(exc))
        except Exception as exc:
            runner_error = True
            runner_error_detail = f"build: {exc}"
            print(f"     ERROR: {exc}")
            build_results = []
            ledger.record_failure("build", str(exc))
    v1_build = _split_by_key(build_results, "v1")
    v2_build = _split_by_key(build_results, "v2")
    v1_build_status = _status_of(v1_build)
    v2_build_status = _status_of(v2_build)
    print(f"     V1 BUILD: {v1_build_status}")
    print(f"     V2 BUILD: {v2_build_status}")
    print()

    # ---- TEST (independent; never overwritten by build) ----
    print("[07] TEST (all declared repositories)...")
    if args.mode == "audit":
        test_results = []
    else:
        try:
            test_results = test_repositories(
                packages=packages,
                repo_results=repo_results,
                build_results=build_results,
                workspace=workspace,
                env=env,
                ledger=ledger,
            )
        except TypeError as exc:
            runner_error = True
            runner_error_detail = f"test TypeError: {exc}"
            print(f"     ERROR: {exc}")
            print(traceback.format_exc())
            test_results = []
            ledger.record_failure("test", str(exc))
        except Exception as exc:
            runner_error = True
            runner_error_detail = f"test: {exc}"
            print(f"     ERROR: {exc}")
            test_results = []
            ledger.record_failure("test", str(exc))
    v1_test = _split_by_key(test_results, "v1")
    v2_test = _split_by_key(test_results, "v2")
    v1_test_status = _status_of(v1_test)
    v2_test_status = _status_of(v2_test)
    print(f"     V1 TEST: {v1_test_status}")
    print(f"     V2 TEST: {v2_test_status}")
    print()

    # ---- V1 ADMISSION ----
    print("[08] V1 ADMISSION — discover and bind actual mechanisms...")
    admission_mode = "NORMAL"
    if v1_test_status == "FAIL":
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
    if isinstance(primary.get("admission"), dict):
        primary_status = primary["admission"].get("status") or primary.get("status") or "UNKNOWN"
    else:
        primary_status = primary.get("status") or "UNKNOWN"

    admission_ok = bool(admission.get("admission_established", False))
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

    v1_to_v2_handoff = "NOT_FOUND"
    downstream_flow = "REACHED" if (admission_ok and v1_to_v2_handoff == "FOUND") else "NOT_REACHED"

    if not admission_ok:
        print("[09] NOTE: V1 admission not established — downstream = NOT_REACHED")
        print()

    print("[09] V2 BUILD status (from shared build stage)...")
    print(f"     V2 BUILD: {v2_build_status}")
    print()

    print("[10] V2 TEST status (from shared test stage)...")
    print(f"     V2 TEST: {v2_test_status}")
    print()

    print("[11] Firefly (not an admission path)...")
    if args.mode == "audit":
        firefly_results = {"status": "SKIPPED"}
    else:
        try:
            firefly_results = run_firefly_tests(
                packages=packages,
                repo_results=repo_results,
                workspace=workspace,
                ledger=ledger,
            )
        except TypeError as exc:
            runner_error = True
            runner_error_detail = f"firefly TypeError: {exc}"
            firefly_results = {"status": "ERROR", "error": str(exc), "traceback": traceback.format_exc()}
            ledger.record_failure("firefly", str(exc))
        except Exception as exc:
            firefly_results = {"status": "ERROR", "error": str(exc)}
            ledger.record_failure("firefly", str(exc))
    print()

    print("[12] Synthetic simulation (not an admission path)...")
    if args.mode == "audit":
        simulation_results = {"status": "SKIPPED"}
    else:
        try:
            simulation_results = run_simulation(
                case_count=args.cases,
                packages=packages,
                ledger=ledger,
            )
            simulation_results["admission_bypass"] = False
            simulation_results["note"] = "SIMULATION ≠ PROOF. Simulation is not an admission gate."
        except TypeError as exc:
            runner_error = True
            runner_error_detail = f"simulation TypeError: {exc}"
            simulation_results = {"status": "ERROR", "error": str(exc), "traceback": traceback.format_exc()}
            ledger.record_failure("simulation", str(exc))
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
            "All stage calls use keyword arguments to prevent positional TypeError",
            "V1 BUILD/TEST PASS ≠ V1 ADMISSION PROVEN",
            "CHECK_PASSED ≠ authority ADMITTED",
            "V1 TEST FAIL is never overwritten by BUILD PASS",
            "ISOLATED_DIAGNOSTIC admission cannot authorize downstream",
            "v1_to_v2_handoff remains NOT_FOUND until a real interface is evidenced",
            runner_error_detail,
        ],
    }
    write_json_report(reports, "final_report.json", final_report)
    write_html_report(reports_dir=reports, final_report=final_report)
    write_final_status(
        reports_dir=reports,
        ledger=ledger,
        components=components,
        simulation=simulation_results,
    )

    print()
    print("=" * 60)
    print("SWI UNIVERSAL TEST — RUN COMPLETE")
    print("=" * 60)
    print()
    print("STAGE STATUS")
    print(f"  runner_error        : {runner_error}")
    if runner_error_detail:
        print(f"  runner_error_detail : {runner_error_detail}")
    print(f"  v1_build            : {v1_build_status}")
    print(f"  v1_test             : {v1_test_status}")
    print(f"  v1_admission        : {primary_status}")
    print(f"  admission_mode      : {admission_mode}")
    print(f"  v1_to_v2_handoff    : {v1_to_v2_handoff}")
    print(f"  downstream_flow     : {downstream_flow}")
    print(f"  v2_build            : {v2_build_status}")
    print(f"  v2_test             : {v2_test_status}")
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
