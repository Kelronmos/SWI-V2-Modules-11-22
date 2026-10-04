#!/usr/bin/env python3
"""
SWI Universal Test / Demonstration Runner — entry point.

Usage:
    python -m runner.main
    python -m runner.main --cases 100
    python -m runner.main --mode smoke|full|audit
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
from runner.firefly import run_firefly_tests
from runner.inventory import run_inventory, evaluate_components
from runner.simulation import run_simulation
from runner.evidence import EvidenceLedger, FINAL_CLAIMS
from runner.reporting import write_final_status, write_json_report, write_html_report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SWI Universal Test / Demonstration Runner (TEST_ONLY)"
    )
    parser.add_argument(
        "--cases", type=int, default=100,
        choices=[10, 100, 1000, 8000],
        help="Number of synthetic demonstration cases (default: 100)",
    )
    parser.add_argument(
        "--mode", choices=["smoke", "full", "audit"], default="smoke",
        help="Execution mode (default: smoke)",
    )
    parser.add_argument(
        "--packages", type=Path, default=None,
        help="Path to packages.json (default: ./packages.json)",
    )
    return parser.parse_args(argv)


def banner() -> None:
    print("=" * 60)
    print(RUNNER_NAME)
    print("=" * 60)
    print()
    print("MODE:                  TEST + SIMULATION + EVIDENCE COLLECTION")
    print("REAL-WORLD ACTION:     NONE")
    print("PRODUCTION AUTHORIZATION: NO")
    print()
    print("=" * 60)
    print()


def load_packages(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"packages.json not found: {path}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    schema = data.get("schema", "")
    if not schema.startswith("swi.online.test.rebuild.packages."):
        raise ValueError(f"Unsupported packages.json schema: {schema}")
    return data


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
        print(f"[1/10] Loaded packages.json (schema {packages.get('schema')})")
    except Exception as exc:
        print(f"FATAL: Cannot load packages.json — {exc}")
        return 1

    print("[2/10] Detecting environment...")
    env = detect_environment()
    ledger.record_environment(env)
    print(f"       OS={env.get('os')}  Python={env.get('python')}  Git={env.get('git')}")
    print(f"       Node={env.get('node') or 'not found'}  Rust={env.get('rust') or 'not found'}")
    print()

    print("[3/10] Ensuring workspace...")
    workspace = ensure_workspace(script_dir, packages.get("workspace", {}))
    print(f"       {workspace['root']}")
    print()

    print("[4/10] Materializing repositories...")
    try:
        repo_results = materialize_repositories(
            packages=packages, workspace=workspace, mode=args.mode, ledger=ledger,
        )
    except Exception as exc:
        print(f"FATAL during materialization: {exc}")
        ledger.record_failure("materialization", str(exc))
        write_final_status(workspace["reports"], ledger)
        return 1
    materialized = sum(1 for r in repo_results if r.get("status") == "MATERIALIZED")
    print(f"       Materialized: {materialized}/{len(repo_results)}")
    print()

    print("[5/10] Inventory + component evaluation...")
    inventory = run_inventory(packages, repo_results, workspace)
    components = evaluate_components(packages, repo_results, inventory)
    present = sum(1 for c in components if c["status"]["present"])
    print(f"       Components declared={len(components)}  present={present}")
    print()

    print("[6/10] Building repositories...")
    if args.mode == "audit":
        build_results = []
        print("       Skipped (audit mode)")
    else:
        build_results = build_repositories(
            packages, repo_results, workspace, env, ledger,
        )
    print(f"       Build PASS={sum(1 for b in build_results if b.get('status')=='PASS')}  "
          f"FAIL={sum(1 for b in build_results if b.get('status')=='FAIL')}")
    print()

    print("[7/10] Running repository tests...")
    if args.mode == "audit":
        test_results = []
        print("       Skipped (audit mode)")
    else:
        test_results = test_repositories(
            packages, repo_results, build_results, workspace, env, ledger,
        )
    print(f"       Test PASS={sum(1 for t in test_results if t.get('status')=='PASS')}  "
          f"FAIL={sum(1 for t in test_results if t.get('status')=='FAIL')}")
    print()

    print("[8/10] Firefly demonstration suite...")
    if args.mode == "audit":
        firefly_results = {"status": "SKIPPED", "reason": "audit mode"}
    else:
        firefly_results = run_firefly_tests(packages, repo_results, workspace, ledger)
    print()

    print("[9/10] Synthetic simulation...")
    if args.mode == "audit":
        simulation_results = {"status": "SKIPPED", "reason": "audit mode"}
    else:
        simulation_results = run_simulation(args.cases, packages, ledger)
    print()

    print("[10/10] Generating reports...")
    reports = workspace["reports"]
    write_json_report(reports, "ENVIRONMENT.json", env)
    write_json_report(reports, "REPOSITORIES.json", repo_results)
    write_json_report(reports, "inventory.json", inventory)
    write_json_report(reports, "component_status.json", components)
    write_json_report(reports, "BUILD_RESULTS.json", build_results)
    write_json_report(reports, "TEST_RESULTS.json", test_results)
    write_json_report(reports, "FIREFLY_RESULTS.json", firefly_results)
    write_json_report(reports, "simulation_results.json", simulation_results)

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
        "claims": FINAL_CLAIMS.copy(),
        "repositories": repo_results,
        "components": components,
        "toolchain": env,
        "inventory": {"repositories_inventoried": inventory.get("repositories_inventoried")},
        "build": build_results,
        "tests": test_results,
        "firefly": firefly_results,
        "simulation": {
            "summary": simulation_results.get("summary") if isinstance(simulation_results, dict) else None,
            "seed": simulation_results.get("seed") if isinstance(simulation_results, dict) else None,
            "note": "SIMULATION ≠ PROOF",
        },
        "limitations": [
            "Component paths that are null remain NOT_FOUND",
            "Successful builds/tests do not upgrade claims",
            "Simulation is synthetic only",
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
    print("Reports:", reports)
    print()
    for k, v in FINAL_CLAIMS.items():
        print(f"{k.upper():<28}: {v}")
    print()
    print("BUILD/TEST/SIMULATION INFRASTRUCTURE ≠ SWI PROOF")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
