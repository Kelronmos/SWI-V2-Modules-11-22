#!/usr/bin/env python3
"""
SWI Universal Test / Demonstration Runner — entry point.

Usage:
    python -m runner.main
    python -m runner.main --cases 100
    python -m runner.main --mode smoke
    python -m runner.main --mode full
    python -m runner.main --mode audit
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
from runner.evidence import EvidenceLedger, FINAL_CLAIMS
from runner.reporting import write_final_status, write_json_report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SWI Universal Test / Demonstration Runner (TEST_ONLY)"
    )
    parser.add_argument(
        "--cases",
        type=int,
        default=100,
        choices=[10, 100, 1000, 8000],
        help="Number of demonstration cases to generate (default: 100)",
    )
    parser.add_argument(
        "--mode",
        choices=["smoke", "full", "audit"],
        default="smoke",
        help="Execution mode (default: smoke)",
    )
    parser.add_argument(
        "--packages",
        type=Path,
        default=None,
        help="Path to packages.json (default: ./packages.json)",
    )
    return parser.parse_args(argv)


def banner() -> None:
    print("=" * 60)
    print(RUNNER_NAME)
    print("=" * 60)
    print()
    print("MODE:")
    print("  TEST + SIMULATION + EVIDENCE COLLECTION")
    print()
    print("REAL-WORLD ACTION:")
    print("  NONE")
    print()
    print("PRODUCTION AUTHORIZATION:")
    print("  NO")
    print()
    print("=" * 60)
    print()


def load_packages(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"packages.json not found: {path}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if data.get("schema") not in (
        "swi.online.test.rebuild.packages.v1",
        "swi.online.test.rebuild.packages.v2",
    ):
        raise ValueError(f"Unsupported packages.json schema: {data.get('schema')}")
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

    # 2. Environment detection
    print("[2/10] Detecting environment...")
    env = detect_environment()
    ledger.record_environment(env)
    print(f"       OS      : {env.get('os')}")
    print(f"       Python  : {env.get('python')}")
    print(f"       Git     : {env.get('git')}")
    print(f"       Node    : {env.get('node', 'not found')}")
    print(f"       Rust    : {env.get('rust', 'not found')}")
    print()

    # 3. Workspace
    print("[3/10] Ensuring workspace...")
    workspace = ensure_workspace(script_dir, packages.get("workspace", {}))
    print(f"       Root    : {workspace['root']}")
    print()

    # 4. Materialize repositories
    print("[4/10] Materializing repositories...")
    try:
        repo_results = materialize_repositories(
            packages=packages,
            workspace=workspace,
            mode=args.mode,
            ledger=ledger,
        )
    except Exception as exc:
        print(f"FATAL during materialization: {exc}")
        ledger.record_failure("materialization", str(exc))
        write_final_status(workspace["reports"], ledger)
        return 1

    materialized = sum(1 for r in repo_results if r.get("status") == "MATERIALIZED")
    print(f"       Materialized: {materialized}/{len(repo_results)}")
    print()

    # Remaining stages are stubs in Phase 1 — they record NOT_RUN
    print("[5/10] Inventory          — Phase 1 stub (NOT_RUN)")
    print("[6/10] Build              — Phase 1 stub (NOT_RUN)")
    print("[7/10] Repository tests   — Phase 1 stub (NOT_RUN)")
    print("[8/10] Firefly tests      — Phase 1 stub (NOT_RUN)")
    print("[9/10] Demonstrations     — Phase 1 stub (NOT_RUN)")
    print("[10/10] Reporting...")

    write_json_report(workspace["reports"], "ENVIRONMENT.json", env)
    write_json_report(workspace["reports"], "REPOSITORIES.json", repo_results)
    write_final_status(workspace["reports"], ledger)

    print()
    print("=" * 60)
    print("SWI UNIVERSAL TEST — PHASE 1 COMPLETE (SKELETON)")
    print("=" * 60)
    print()
    print("Reports written under:", workspace["reports"])
    print()
    for k, v in FINAL_CLAIMS.items():
        print(f"{k.upper():<28}: {v}")
    print()
    print("NOTE: Phase 1 is scaffolding only.")
    print("      Full build/test/Firefly/8K engines are not yet implemented.")
    print("      No claim upgrade has occurred.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
