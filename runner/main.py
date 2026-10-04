#!/usr/bin/env python3
"""
SWI Universal Test / Demonstration Runner — entry point.

Architectural order:
  01 TOOLCHAIN
  02 MANIFEST
  03 MATERIALIZE
  04 SHA / COMMIT
  05 INVENTORY
  06 V1 BUILD
  07 V1 TEST
  08 V1 ADMISSION (discover + bind actual mechanisms)
  09 V2 BUILD / TEST
  10 FIREFLY / SIMULATION
  11 REPORTS / FINAL STATUS

If V1 admission mechanism is NOT_FOUND or not established,
downstream admission-dependent claims remain NOT_REACHED.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

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
    print("V1 ADMISSION BOUNDARY:    ENFORCED (discover actual mechanisms)")
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

    print("[06] V1 BUILD...")
    if args.mode == "audit":
        build_results = []
    else:
        build_results = build_repositories(packages, repo_results, workspace, env, ledger)
    v1_build = _split_by_key(build_results, "v1")
    v2_build = _split_by_key(build_results, "v2")
    print(f"     V1 BUILD: {(v1_build or {}).get('status', 'NOT_RUN')}")
    print()

    print("[07] V1 TEST...")
    if args.mode == "audit":
        test_results = []
    else:
        test_results = test_repositories(
            packages, repo_results, build_results, workspace, env, ledger,
        )
    v1_test = _split_by_key(test_results, "v1")
    v2_test = _split_by_key(test_results, "v2")
    print(f"     V1 TEST: {(v1_test or {}).get('status', 'NOT_RUN')}")
    print()

    print("[08] V1 ADMISSION — discover and bind actual mechanisms...")
    if args.mode == "audit":
        admission = {
            "primary": {"admission": {"status": "NOT_ESTABLISHED"}},
            "admission_established": False,
            "discovery": {"status": "SKIPPED"},
            "report_section": {
                "V1": {"FOUND": False, "BOUND": False, "EXECUTED": False, "RESULT": "NOT_ESTABLISHED"},
                "V2": {"ADMISSION_AUTHORITY": False},
                "ALTERNATE_ADMISSION_PATHS": "NOT_TESTED",
            },
        }
        print("     Skipped (audit mode)")
    else:
        admission = run_admission_tests(
            packages, repo_results, v1_build, v1_test, workspace, ledger,
        )
    admission_ok = admission.get("admission_established", False)
    primary_status = (
        admission.get("primary", {}).get("admission", {}).get("status")
        or admission.get("primary_admission", {}).get("status")
        or "UNKNOWN"
    )
    discovery_status = admission.get("discovery", {}).get("status", "UNKNOWN")
    print(f"     Discovery: {discovery_status}")
    print(f"     Primary admission status: {primary_status}")
    print(f"     Admission established: {admission_ok}")
    print()

    if not admission_ok:
        print("[09] NOTE: V1 admission not established — downstream cannot claim admission/authority")
        print()

    print("[09] V2 BUILD status...")
    print(f"     V2 BUILD: {(v2_build or {}).get('status', 'NOT_RUN')}")
    print()

    print("[10] V2 TEST status...")
    print(f"     V2 TEST: {(v2_test or {}).get('status', 'NOT_RUN')}")
    print()

    print("[11] Firefly (not an admission path)...")
    if args.mode == "audit":
        firefly_results = {"status": "SKIPPED"}
    else:
        firefly_results = run_firefly_tests(packages, repo_results, workspace, ledger)
    print()

    print("[12] Synthetic simulation (not an admission path)...")
    if args.mode == "audit":
        simulation_results = {"status": "SKIPPED"}
    else:
        simulation_results = run_simulation(args.cases, packages, ledger)
        simulation_results["admission_bypass"] = False
        simulation_results["note"] = "SIMULATION ≠ PROOF. Simulation is not an admission gate."
    print()

    print("[13–14] Reports + FINAL STATUS...")
    reports = workspace["reports"]
    write_json_report(reports, "ENVIRONMENT.json", env)
    write_json_report(reports, "REPOSITORIES.json", repo_results)
    write_json_report(reports, "inventory.json", inventory)
    write_json_report(reports, "component_status.json", components)
    write_json_report(reports, "BUILD_RESULTS.json", build_results)
    write_json_report(reports, "TEST_RESULTS.json", test_results)
    write_json_report(reports, "ADMISSION_RESULTS.json", admission)
    write_json_report(reports, "FIREFLY_RESULTS.json", firefly_results)
    write_json_report(reports, "simulation_results.json", simulation_results)

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
        "architecture": {
            "admission_boundary": "V1",
            "v2_role": "DOWNSTREAM / CONTINUATION",
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
        "admission": admission.get("primary"),
        "admission_established": admission_ok,
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
            "V1 ADMISSION ≠ AUTHORIZATION ≠ ACTION",
            "If mechanism NOT_FOUND → downstream admission-dependent = NOT_REACHED",
            "No alternate component may become an admission boundary",
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
    print("ADMISSION BOUNDARY")
    v1rep = report_section.get("V1", {})
    print(f"  V1 FOUND    : {v1rep.get('FOUND')}")
    print(f"  V1 BOUND    : {v1rep.get('BOUND')}")
    print(f"  V1 EXECUTED : {v1rep.get('EXECUTED')}")
    print(f"  V1 RESULT   : {v1rep.get('RESULT')}")
    print(f"  V2 ADMISSION AUTHORITY : {report_section.get('V2', {}).get('ADMISSION_AUTHORITY')}")
    print(f"  ALTERNATE PATHS        : {report_section.get('ALTERNATE_ADMISSION_PATHS')}")
    print()
    for k, v in FINAL_CLAIMS.items():
        print(f"{k.upper():<28}: {v}")
    print()
    print("V1 admits. V2 continues. Neither fact alone constitutes proof.")
    print("BUILD ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
