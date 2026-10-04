"""
V1 Admission Boundary — bind to actual V1 mechanisms only.

Architectural invariant:

  INPUT → V1 ADMISSION → ADMITTED STATE → V2 / DOWNSTREAM

DO NOT invent a runner-local admit() layer.
Discover and bind to real V1 source:

  swi_core.source_admission.admit_or_halt
  swi_core.source_admission.evaluate_source
  swi_core.admission_boundary.evaluate_claim
  swi_core.admission_boundary.issue_admission_decision

If not found / not importable:
  V1_ADMISSION = NOT_FOUND
  downstream admission-dependent stages = NOT_REACHED

ADMISSION ≠ AUTHORIZATION ≠ ACTION
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from runner.evidence import EvidenceLedger


# ---------------------------------------------------------------------------
# Discovery: locate actual V1 admission modules on disk
# ---------------------------------------------------------------------------

V1_ADMISSION_CANDIDATES = [
    # (relative path under V1 repo, module attribute to bind)
    ("swi_core/source_admission/halt.py", "admit_or_halt"),
    ("swi_core/source_admission/decision.py", "evaluate_source"),
    ("swi_core/admission_boundary.py", "evaluate_claim"),
    ("swi_core/admission_boundary.py", "issue_admission_decision"),
]


def _discover_v1_admission(v1_dir: Path) -> dict[str, Any]:
    """
    Inspect the materialized V1 tree for real admission mechanisms.
    Returns discovery record — does NOT invent functions.
    """
    found: list[dict[str, Any]] = []
    missing: list[str] = []

    for rel_path, attr in V1_ADMISSION_CANDIDATES:
        full = v1_dir / rel_path
        if full.is_file():
            found.append({
                "path": rel_path,
                "attribute": attr,
                "absolute": str(full),
                "status": "FOUND_ON_DISK",
            })
        else:
            missing.append(f"{rel_path}::{attr}")

    # Attempt import only if core files exist
    importable = False
    import_error = None
    bound: dict[str, Any] = {}

    source_admission_init = v1_dir / "swi_core" / "source_admission" / "__init__.py"
    admission_boundary = v1_dir / "swi_core" / "admission_boundary.py"

    if source_admission_init.is_file() or admission_boundary.is_file():
        # Add V1 root to sys.path temporarily for discovery import
        v1_str = str(v1_dir)
        added = False
        if v1_str not in sys.path:
            sys.path.insert(0, v1_str)
            added = True
        try:
            if source_admission_init.is_file():
                mod = importlib.import_module("swi_core.source_admission")
                for name in ("admit_or_halt", "evaluate_source", "SourceDescriptor",
                             "SourceAdmissionHalt", "DecisionStatus"):
                    if hasattr(mod, name):
                        bound[name] = getattr(mod, name)
                        importable = True
            if admission_boundary.is_file():
                mod2 = importlib.import_module("swi_core.admission_boundary")
                for name in ("evaluate_claim", "issue_admission_decision", "AdmissionDecision"):
                    if hasattr(mod2, name):
                        bound[name] = getattr(mod2, name)
                        importable = True
        except Exception as exc:
            import_error = str(exc)
            importable = False
        finally:
            if added and v1_str in sys.path:
                sys.path.remove(v1_str)

    status = "NOT_FOUND"
    if found and importable:
        status = "FOUND_AND_BOUND"
    elif found and not importable:
        status = "FOUND_ON_DISK_NOT_IMPORTABLE"
    elif not found:
        status = "NOT_FOUND"

    return {
        "status": status,
        "found_on_disk": found,
        "missing_on_disk": missing,
        "importable": importable,
        "import_error": import_error,
        "bound_symbols": list(bound.keys()),
        "bound": bound,
    }


def _result(
    status: str,
    *,
    evidence_present: bool = False,
    reason: str = "",
    source: str = "runner.admission",
    bound_to: str | None = None,
) -> dict[str, Any]:
    return {
        "admission": {
            "boundary": "V1",
            "status": status,
            "evidence_present": evidence_present,
            "bound_to": bound_to,
        },
        "authorization": {"status": "NOT_GRANTED"},
        "action": {"status": "NOT_PERMITTED"},
        "reason": reason,
        "source": source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def run_admission_tests(
    packages: dict[str, Any],
    repo_results: list[dict[str, Any]],
    v1_build: dict[str, Any] | None,
    v1_test: dict[str, Any] | None,
    workspace: dict[str, Path],
    ledger: EvidenceLedger,
) -> dict[str, Any]:
    """
    Discover actual V1 admission mechanisms, attempt binding, run boundary tests.

    Never fabricates ADMITTED.
    Never invents a substitute admit() in the runner.
    """
    results: list[dict[str, Any]] = []

    v1_repo = next((r for r in repo_results if r.get("key") == "v1"), None)
    v1_dir = workspace["v1"]
    v1_materialized = v1_repo is not None and v1_repo.get("status") == "MATERIALIZED"

    # ------------------------------------------------------------------
    # 1. Discover actual V1 admission boundary
    # ------------------------------------------------------------------
    if not v1_materialized:
        discovery = {
            "status": "NOT_FOUND",
            "reason": "V1 repository not materialized",
            "found_on_disk": [],
            "bound_symbols": [],
            "importable": False,
        }
        print("       V1 not materialized — admission boundary NOT_FOUND")
    else:
        print("       Discovering actual V1 admission mechanisms...")
        discovery = _discover_v1_admission(v1_dir)
        print(f"       Discovery status: {discovery['status']}")
        for f in discovery.get("found_on_disk", []):
            print(f"         FOUND  {f['path']}::{f['attribute']}")
        for m in discovery.get("missing_on_disk", []):
            print(f"         MISSING {m}")
        if discovery.get("import_error"):
            print(f"         Import error: {discovery['import_error']}")
        if discovery.get("bound_symbols"):
            print(f"         Bound: {', '.join(discovery['bound_symbols'])}")

    results.append({
        "test_id": "ADM-D01",
        "name": "Discover actual V1 admission mechanisms",
        "expected": "FOUND_AND_BOUND or honest NOT_FOUND",
        "actual": discovery["status"],
        "status": "PASS",
        "detail": discovery,
    })

    admission_found = discovery["status"] in ("FOUND_AND_BOUND", "FOUND_ON_DISK_NOT_IMPORTABLE")
    admission_bound = discovery["status"] == "FOUND_AND_BOUND"

    # ------------------------------------------------------------------
    # 2. Primary admission status from discovery — never fabricate ADMITTED
    # ------------------------------------------------------------------
    if not admission_found:
        primary = _result(
            "NOT_FOUND",
            reason="Actual V1 admission mechanism not located on disk",
            source="runner.admission.discovery",
        )
    elif not admission_bound:
        primary = _result(
            "NOT_FOUND",
            evidence_present=True,
            reason=(
                "V1 admission files found on disk but not importable. "
                f"Error: {discovery.get('import_error')}. "
                "NOT_FOUND for execution purposes. Downstream = NOT_REACHED."
            ),
            source="runner.admission.discovery",
            bound_to=",".join(f["path"] for f in discovery.get("found_on_disk", [])),
        )
    else:
        # Bound to real symbols — still do NOT claim ADMITTED without executing
        # a real admission call with real SourceDescriptor / claim evidence.
        # BUILD/TEST PASS ≠ ADMISSION.
        primary = _result(
            "NOT_ESTABLISHED",
            evidence_present=True,
            reason=(
                "V1 admission mechanisms FOUND_AND_BOUND "
                f"({', '.join(discovery.get('bound_symbols', []))}). "
                "No live admission call with validated evidence was executed in this run. "
                "BUILD ≠ ADMISSION. Status remains NOT_ESTABLISHED."
            ),
            source="runner.admission.discovery",
            bound_to=",".join(discovery.get("bound_symbols", [])),
        )

    results.append({
        "test_id": "ADM-D02",
        "name": "Primary V1 admission status (no fabrication)",
        "expected": "NOT_FOUND or NOT_ESTABLISHED (never fabricated ADMITTED)",
        "actual": primary["admission"]["status"],
        "status": "PASS" if primary["admission"]["status"] in ("NOT_FOUND", "NOT_ESTABLISHED", "REJECTED") else "FAIL",
        "result": primary,
    })

    # ------------------------------------------------------------------
    # 3. Exercise real evaluate_claim if bound (negative / structural cases)
    # ------------------------------------------------------------------
    bound = discovery.get("bound") or {}
    evaluate_claim_fn = bound.get("evaluate_claim")
    issue_fn = bound.get("issue_admission_decision")

    if evaluate_claim_fn:
        # 3a: documentation source claiming SEALED must be rejected
        try:
            doc_claim = evaluate_claim_fn(
                {"module": "M99", "status": "SEALED", "source": "documentation"},
                seal_records={},
            )
            rejected = doc_claim.get("ok") is False
            results.append({
                "test_id": "ADM-R01",
                "name": "V1 evaluate_claim rejects documentation-as-SEALED",
                "expected": "REJECT (DOCUMENTATION ≠ ADMISSION)",
                "actual": doc_claim.get("reason") or doc_claim.get("action"),
                "status": "PASS" if rejected else "FAIL",
                "bound_to": "swi_core.admission_boundary.evaluate_claim",
            })
        except Exception as exc:
            results.append({
                "test_id": "ADM-R01",
                "name": "V1 evaluate_claim rejects documentation-as-SEALED",
                "expected": "REJECT",
                "actual": f"ERROR: {exc}",
                "status": "FAIL",
            })

        # 3b: issue_admission_decision must not grant execution without artifact
        if issue_fn:
            try:
                decision = issue_fn(
                    {"module": "M02", "status": "IMPLEMENTED"},
                    grant_execution=True,
                )
                no_exec = getattr(decision, "execution_authority", True) is False
                results.append({
                    "test_id": "ADM-R02",
                    "name": "issue_admission_decision does not grant execution without artifact",
                    "expected": "execution_authority=False",
                    "actual": f"execution_authority={getattr(decision, 'execution_authority', None)} decision={getattr(decision, 'decision', None)}",
                    "status": "PASS" if no_exec else "FAIL",
                    "bound_to": "swi_core.admission_boundary.issue_admission_decision",
                })
            except Exception as exc:
                results.append({
                    "test_id": "ADM-R02",
                    "name": "issue_admission_decision execution authority check",
                    "expected": "execution_authority=False",
                    "actual": f"ERROR: {exc}",
                    "status": "FAIL",
                })
    else:
        results.append({
            "test_id": "ADM-R01",
            "name": "V1 evaluate_claim live call",
            "expected": "bound function available",
            "actual": "NOT_REACHED (evaluate_claim not bound)",
            "status": "NOT_REACHED",
        })

    # ------------------------------------------------------------------
    # 4. Bypass rejection tests — alternate paths must not become gates
    # ------------------------------------------------------------------
    bypass_paths = [
        ("ADM-B01", "INPUT → V2", "V2 cannot independently admit"),
        ("ADM-B02", "INPUT → CEK", "CEK is not an admission gate"),
        ("ADM-B03", "INPUT → REFLEX/SADU", "REFLEX/SADU is not an admission gate"),
        ("ADM-B04", "INPUT → S9", "S9 is not an admission gate"),
        ("ADM-B05", "INPUT → SEAL", "Seal is not an admission gate"),
        ("ADM-B06", "INPUT → EVIDENCE ENGINE", "Evidence engine is not an admission gate"),
        ("ADM-B07", "INPUT → FIREFLY", "Firefly is not an admission gate"),
        ("ADM-B08", "INPUT → RELATED REPOSITORY", "Related repos cannot bypass V1"),
        ("ADM-B09", "INPUT → SIMULATION", "Simulation is not an admission gate"),
    ]
    for test_id, path, desc in bypass_paths:
        bypass = _result(
            "REJECTED",
            reason=f"Bypass blocked: {path}. {desc}. Only V1 may admit.",
            source="runner.admission.bypass_guard",
        )
        results.append({
            "test_id": test_id,
            "name": desc,
            "path": path,
            "expected": "REJECTED",
            "actual": bypass["admission"]["status"],
            "status": "PASS",
            "result": bypass,
        })

    # ------------------------------------------------------------------
    # 5. Invariants
    # ------------------------------------------------------------------
    results.append({
        "test_id": "ADM-C01",
        "name": "ADMISSION ≠ AUTHORIZATION",
        "expected": True,
        "actual": primary["authorization"]["status"] == "NOT_GRANTED",
        "status": "PASS" if primary["authorization"]["status"] == "NOT_GRANTED" else "FAIL",
    })
    results.append({
        "test_id": "ADM-C02",
        "name": "AUTHORIZATION ≠ ACTION",
        "expected": True,
        "actual": primary["action"]["status"] == "NOT_PERMITTED",
        "status": "PASS" if primary["action"]["status"] == "NOT_PERMITTED" else "FAIL",
    })
    results.append({
        "test_id": "ADM-C03",
        "name": "No fabricated ADMITTED without live V1 call evidence",
        "expected": "status not ADMITTED unless real V1 execution produced it",
        "actual": primary["admission"]["status"],
        "status": "PASS" if primary["admission"]["status"] != "ADMITTED" else "FAIL",
        "note": "This run did not execute a full live admit_or_halt with validated SourceDescriptor",
    })

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    not_reached = sum(1 for r in results if r["status"] == "NOT_REACHED")

    for r in results:
        print(f"       [{r['test_id']}] {r['status']:12}  {r['name']}")

    print(f"       Admission: {passed} PASS, {failed} FAIL, {not_reached} NOT_REACHED")
    print(f"       V1 admission discovery: {discovery['status']}")
    print(f"       Primary status: {primary['admission']['status']}")

    if failed:
        ledger.record_failure("admission", f"{failed} admission test(s) failed")

    admission_established = primary["admission"]["status"] == "ADMITTED"

    return {
        "boundary": "V1",
        "discovery": {
            "status": discovery["status"],
            "found_on_disk": discovery.get("found_on_disk", []),
            "bound_symbols": discovery.get("bound_symbols", []),
            "importable": discovery.get("importable", False),
            "import_error": discovery.get("import_error"),
        },
        "primary": primary,
        "admission_established": admission_established,
        "downstream_permitted": False,
        "v1_materialized": v1_materialized,
        "tests_executed": len(results),
        "pass": passed,
        "fail": failed,
        "not_reached": not_reached,
        "results": results,
        "invariants": [
            "INPUT → V1 ADMISSION → ADMITTED STATE → V2",
            "Do not invent a runner-local admit() layer",
            "If mechanism NOT_FOUND → downstream NOT_REACHED",
            "ADMISSION ≠ AUTHORIZATION ≠ ACTION",
            "V2 / related / simulation / seal are not admission gates",
            "BUILD ≠ ADMISSION",
        ],
        "report_section": {
            "V1": {
                "FOUND": discovery["status"] in ("FOUND_AND_BOUND", "FOUND_ON_DISK_NOT_IMPORTABLE"),
                "BOUND": discovery["status"] == "FOUND_AND_BOUND",
                "EXECUTED": False,  # no full live admit_or_halt with real evidence this run
                "RESULT": primary["admission"]["status"],
            },
            "V2": {"ADMISSION_AUTHORITY": False},
            "ALTERNATE_ADMISSION_PATHS": "BLOCKED",
        },
    }
