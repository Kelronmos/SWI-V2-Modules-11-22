#!/usr/bin/env python3
"""
SWI Universal Test / Demonstration Runner — rebuild / boot diagnostic.

V1 = mandatory admission boundary, not the endpoint.
ENVIRONMENT/ACQUISITION/TOOLCHAIN ≠ SWI architecture failure.
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
from runner.component_discovery import discover_components
from runner.status_engine import repository_status_object, overall_swi_ceiling
from runner.hash_manifest import write_sha256_manifest
from runner.failure_domains import classify_all, rebuild_report_header


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
    print("RUN TYPE:                 SWI REBUILD / BOOT DIAGNOSTIC")
    print("MODE:                     TEST + SIMULATION + EVIDENCE")
    print("REAL-WORLD ACTION:        NONE")
    print("PRODUCTION AUTHORIZATION: NO")
    print("V1 ADMISSION BOUNDARY:    ENFORCED (entrance, not endpoint)")
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
    discovery: list = []
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
        write_final_status(reports_dir=workspace["reports"], ledger=ledger)
        return 1
    print(f"     Materialized: {sum(1 for r in repo_results if r.get('status')=='MATERIALIZED')}/{len(repo_results)}")
    print()

    print("[05] Inventory + component evaluation...")
    try:
        inventory = run_inventory(packages=packages, repo_results=repo_results, workspace=workspace)
        components = evaluate_components(packages=packages, repo_results=repo_results, inventory=inventory)
    except Exception as exc:
        runner_error = True
        runner_error_detail = f"inventory: {exc}"
        print(f"     ERROR: {exc}")
        inventory, components = {}, []
    print(f"     Components declared={len(components)} present={sum(1 for c in components if c.get('status', {}).get('present'))}")
    print()

    print("[05b] Evidence-based component discovery...")
    try:
        discovery = discover_components(packages=packages, repo_results=repo_results, workspace=workspace)
        n_found = sum(1 for d in discovery if d.get("discovery", {}).get("status") == "FOUND" or d.get("classification") == "FOUND")
        n_miss = sum(1 for d in discovery if d.get("classification") in ("PATH_NOT_ESTABLISHED",) or d.get("discovery", {}).get("status") == "PATH_NOT_ESTABLISHED")
        print(f"     Map={len(discovery)} FOUND~={n_found} PATH_NOT_ESTABLISHED~={n_miss}")
    except Exception as exc:
        discovery = []
        print(f"     Discovery error: {exc}")
    print()

    print("[06] BUILD (all declared repositories)...")
    if args.mode != "audit":
        try:
            build_results = build_repositories(
                packages=packages, repo_results=repo_results, workspace=workspace, env=env, ledger=ledger,
            )
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
    print(f"     V1 BUILD: {v1_build_status}  V2 BUILD: {v2_build_status}")
    print()

    print("[07] TEST (all declared repositories)...")
    if args.mode != "audit":
        try:
            test_results = test_repositories(
                packages=packages, repo_results=repo_results, build_results=build_results,
                workspace=workspace, env=env, ledger=ledger,
            )
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
    print(f"     V1 TEST: {v1_test_status}  V2 TEST: {v2_test_status}")
    print()

    print("[08] V1 ADMISSION...")
    admission_mode = "ISOLATED_DIAGNOSTIC" if v1_test_status == "FAIL" else "NORMAL"
    if admission_mode == "ISOLATED_DIAGNOSTIC":
        print("     ADMISSION_MODE = ISOLATED_DIAGNOSTIC (V1 TEST=FAIL)")
    if args.mode == "audit":
        admission = {
            "primary": {"status": "NOT_ESTABLISHED", "authorization_granted": False, "action_permitted": False},
            "admission_established": False,
            "discovery": {"status": "SKIPPED"},
            "report_section": {"V1": {"FOUND": False, "EXECUTED": False, "RESULT": "NOT_ESTABLISHED"},
                               "V2": {"ADMISSION_AUTHORITY": False}},
        }
    else:
        try:
            admission = run_admission_tests(
                packages=packages, repo_results=repo_results, v1_build=v1_build,
                v1_test=v1_test, workspace=workspace, ledger=ledger,
            )
        except Exception as exc:
            runner_error = True
            runner_error_detail = f"admission: {exc}"
            tb = traceback.format_exc()
            print(f"     ERROR: {exc}")
            admission = {
                "primary": {"status": "ERROR", "authorization_granted": False, "action_permitted": False,
                            "reason": str(exc), "traceback": tb},
                "admission_established": False,
                "discovery": {"status": "ERROR"},
                "execution": {"executed": False, "live_pass": 0, "live_fail": 0},
                "report_section": {"V1": {"FOUND": False, "EXECUTED": False, "RESULT": "ERROR"},
                                   "V2": {"ADMISSION_AUTHORITY": False}},
            }
            ledger.record_failure("admission", str(exc))

    admission["admission_mode"] = admission_mode
    primary = admission.get("primary") or {}
    primary_status = primary.get("status") or "UNKNOWN"
    if isinstance(primary.get("admission"), dict):
        primary_status = primary["admission"].get("status") or primary_status
    admission_ok = bool(admission.get("admission_established", False))
    if admission_mode == "ISOLATED_DIAGNOSTIC":
        admission_ok = False
        admission["admission_established"] = False

    print(f"     Status: {primary_status}  established={admission_ok}  mode={admission_mode}")
    print()

    v1_to_v2_handoff = "NOT_FOUND"
    downstream_flow = "REACHED" if (admission_ok and v1_to_v2_handoff == "FOUND") else "NOT_REACHED"

    print(f"[09] V1	oV2 HANDOFF: {v1_to_v2_handoff}")
    print(f"[09] V2 BUILD: {v2_build_status}  V2 TEST: {v2_test_status}  continuation={downstream_flow}")
    print()

    print("[11] Firefly (not an admission path)...")
    if args.mode != "audit":
        try:
            firefly_results = run_firefly_tests(
                packages=packages, repo_results=repo_results, workspace=workspace, ledger=ledger,
            )
        except Exception as exc:
            firefly_results = {"status": "ERROR", "error": str(exc)}
            ledger.record_failure("firefly", str(exc))
    else:
        firefly_results = {"status": "SKIPPED"}
    print()

    print("[12] Synthetic simulation...")
    if args.mode != "audit":
        try:
            simulation_results = run_simulation(case_count=args.cases, packages=packages, ledger=ledger)
            simulation_results["admission_bypass"] = False
            simulation_results["note"] = "SIMULATION ≠ PROOF"
        except Exception as exc:
            simulation_results = {"status": "ERROR", "error": str(exc)}
    else:
        simulation_results = {"status": "SKIPPED"}
    print()

    print("[13–14] Reports + failure domains + SHA-256...")
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

    claims = packages.get("claims", {})
    repo_status_list = []
    for rr in repo_results:
        observed: dict[str, Any] = {}
        b = next((x for x in build_results if x.get("key") == rr["key"]), None)
        te = next((x for x in test_results if x.get("key") == rr["key"]), None)
        if b and b.get("status") == "PASS":
            observed["implemented"] = True
        if te and te.get("status") == "PASS":
            observed["tested"] = True
        declared = {}
        if rr["key"] in ("v1", "v2"):
            declared = {
                "proven": claims.get("proven", False),
                "sealed": claims.get("sealed", False),
                "production_authorized": claims.get("production_authorized", False),
            }
        repo_status_list.append(
            repository_status_object(rr["key"], rr.get("commit_sha"), declared=declared, observed=observed)
        )

    ceiling = overall_swi_ceiling()
    failure_domains = classify_all(repo_results, build_results, test_results)
    rebuild_header = rebuild_report_header(env, run_id, __version__, args.mode)

    write_json_report(reports, "ENVIRONMENT.json", env)
    write_json_report(reports, "REBUILD_CONTEXT.json", rebuild_header)
    write_json_report(reports, "REPOSITORIES.json", repo_results)
    write_json_report(reports, "inventory.json", inventory)
    write_json_report(reports, "component_status.json", components)
    write_json_report(reports, "COMPONENT_DISCOVERY.json", discovery)
    write_json_report(reports, "REPOSITORY_STATUS.json", repo_status_list)
    write_json_report(reports, "SWI_CEILING.json", ceiling)
    write_json_report(reports, "BUILD_RESULTS.json", build_results)
    write_json_report(reports, "TEST_RESULTS.json", test_results)
    write_json_report(reports, "FAILURE_DOMAINS.json", failure_domains)
    write_json_report(reports, "ADMISSION_RESULTS.json", admission)
    write_json_report(reports, "FIREFLY_RESULTS.json", firefly_results)
    write_json_report(reports, "simulation_results.json", simulation_results)
    write_json_report(reports, "STAGE_STATUS.json", stage_status)

    report_section = admission.get("report_section", {})
    final_report = {
        "schema": "swi.execution.report.v5",
        "rebuild_context": rebuild_header,
        "execution": {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "platform": env.get("os"),
            "python": env.get("python"),
            "runner_version": __version__,
            "mode": args.mode,
            "cases_requested": args.cases,
            "real_world_action": "NONE",
        },
        "stage_status": stage_status,
        "failure_domains": failure_domains,
        "swi_ceiling": ceiling,
        "repository_status": repo_status_list,
        "component_discovery": discovery,
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
        "repositories": repo_results,
        "components": components,
        "toolchain": env,
        "build": build_results,
        "tests": test_results,
        "firefly": firefly_results,
        "simulation": {
            "summary": simulation_results.get("summary") if isinstance(simulation_results, dict) else None,
            "note": "SIMULATION ≠ PROOF",
        },
        "limitations": [
            "RUN TYPE = SWI REBUILD / BOOT DIAGNOSTIC — not production proof",
            "SOURCE_DIRTY / missing toolchain = ENVIRONMENT/ACQUISITION, not SWI defect",
            "Executed TEST FAIL = INVESTIGATION_REQUIRED, not automatic architecture failure",
            "CHECK_PASSED ≠ authority ADMITTED",
            "v1_to_v2_handoff NOT_FOUND — not invented",
            runner_error_detail,
        ],
    }
    write_json_report(reports, "final_report.json", final_report)
    write_html_report(reports_dir=reports, final_report=final_report)
    write_final_status(reports_dir=reports, ledger=ledger, components=components, simulation=simulation_results)
    hash_manifest = write_sha256_manifest(reports)

    mat = sum(1 for r in repo_results if r.get("status") == "MATERIALIZED")
    dirty = sum(1 for r in repo_results if r.get("status") == "SOURCE_DIRTY")
    bp = sum(1 for b in build_results if b.get("status") == "PASS")
    bf = sum(1 for b in build_results if b.get("status") == "FAIL")
    tp = sum(1 for x in test_results if x.get("status") == "PASS")
    tf = sum(1 for x in test_results if x.get("status") == "FAIL")
    sim_sum = simulation_results.get("summary") if isinstance(simulation_results, dict) else {}
    inv_req = failure_domains.get("summary", {}).get("investigation_required", 0)
    env_blk = failure_domains.get("summary", {}).get("environment_blocked", 0)

    print()
    print("=" * 60)
    print("SWI REBUILD / BOOT DIAGNOSTIC")
    print("=" * 60)
    print()
    print("ENVIRONMENT")
    print(f"  RUN TYPE        : SWI REBUILD / BOOT DIAGNOSTIC")
    print(f"  PLATFORM        : {env.get('os')}")
    print(f"  PYTHON          : {env.get('python')}")
    print(f"  GIT             : {env.get('git')}")
    print(f"  NODE            : {env.get('node')}")
    print(f"  RUST            : {env.get('rust')}")
    print(f"  MODE            : {args.mode}")
    print(f"  REAL-WORLD      : NONE")
    print(f"  RUN_ID          : {run_id}")
    print(f"  RUNNER VERSION  : {__version__}")
    print()
    print("NOTE: ENVIRONMENT/ACQUISITION/TOOLCHAIN ≠ SWI architecture failure")
    print("      Executed TEST FAIL → INVESTIGATION_REQUIRED (not auto 'SWI failed')")
    print()
    print("ACQUISITION")
    print(f"  Materialized:            {mat}/{len(repo_results)}")
    print(f"  SOURCE_DIRTY:            {dirty}")
    print()
    print("BUILD")
    print(f"  PASS:                    {bp}")
    print(f"  FAIL:                    {bf}")
    print()
    print("TEST")
    print(f"  PASS:                    {tp}")
    print(f"  FAIL:                    {tf}")
    print()
    print("FAILURE DOMAINS")
    print(f"  Environment/acquisition blocked: {env_blk}")
    print(f"  Investigation required:          {inv_req}")
    print(f"  SWI defect proven by runner:     0 (never auto)")
    print()
    print("V1 Admission (live API assertions, not rebuild-only):")
    print(f"  Executed:                {report_section.get('V1', {}).get('EXECUTED')}")
    print(f"  Live PASS/FAIL:          {admission.get('execution', {}).get('live_pass', 0)}/{admission.get('execution', {}).get('live_fail', 0)}")
    print(f"  Mode:                    {admission_mode}")
    print()
    print(f"V1	oV2 Handoff:           {v1_to_v2_handoff}")
    print(f"Downstream:                {downstream_flow}")
    print()
    print("Evidence:")
    print(f"  FAILURE_DOMAINS.json     : {reports / 'FAILURE_DOMAINS.json'}")
    print(f"  REBUILD_CONTEXT.json     : {reports / 'REBUILD_CONTEXT.json'}")
    print(f"  final_report.json        : {reports / 'final_report.json'}")
    print(f"  SHA-256                  : {reports / 'sha256-manifest.json'} ({hash_manifest.get('count', 0)} files)")
    print()
    print("=" * 60)
    print("SYSTEM COMPLETION:         INCOMPLETE")
    print("PROVEN:                    NO")
    print("SEALED:                    NO")
    print("PRODUCTION AUTHORIZED:     NO")
    print("=" * 60)
    print()
    print("Windows rebuild result ≠ SWI architecture failed")
    print("BUILD ≠ TEST ≠ ASSERTION ≠ PROOF ≠ PRODUCTION READINESS")
    print()

    return 1 if runner_error else 0


if __name__ == "__main__":
    sys.exit(main())
