"""Build tip-bound S9 ZIP package. Refuses PROVEN without established tip."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

from .evaluator import evaluate_s9
from .inventory import walk_inventory
from .manifest import build_manifest
from .reconciliation import reconcile
from .replay import replay_evaluate
from .diagnostics import failure_diagnostic


class PackageRefused(Exception):
    """Raised when tip cannot be established or PROVEN is requested improperly."""


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_package(
    *,
    repo_root: Path,
    source_commit: str,
    action: Mapping[str, Any],
    out_dir: Path,
    report_id: Optional[str] = None,
    source_repository: str = "Kelronmos/SWI-V2-Modules-11-22",
) -> Dict[str, Any]:
    if not source_commit or len(source_commit) < 7:
        raise PackageRefused("Cannot create package: SOURCE_COMMIT not established")

    repo_root = Path(repo_root)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rid = report_id or f"S9-{source_commit[:12]}"

    inv = walk_inventory(repo_root, source_commit)
    rec = reconcile(inv)
    result = evaluate_s9(action)
    result_d = result.to_dict()
    replay = replay_evaluate(action, result_d)

    report_status = result.system_result
    if report_status == "SATISFIED":
        package_status = "SATISFIED_CASE_ONLY"
    else:
        package_status = report_status

    man = build_manifest(
        source_repository=source_repository,
        source_commit=source_commit,
        report_id=rid,
        report_status=package_status if package_status != "SATISFIED_CASE_ONLY" else "NOT_PROVEN",
    )

    failures = []
    if result.system_result in {"BLOCKED", "UNRESOLVED", "NOT_PROVEN"}:
        failures.append(
            failure_diagnostic(
                what=f"S9 system_result={result.system_result}",
                where=f"action {result.action_id}",
                why="; ".join(result.reasons) or result.system_result,
                expected="C(a)⊆L∩G∩S∩H ∧ E(a)≠∅ with adequate evidence and present H",
                observed=result.system_result,
                rule="S9 evaluator + evidence adequacy + no UNKNOWN→PASS",
                authority=["H"] if result.human == "MISSING" else [],
                corrective_action="Supply missing layers / adequate evidence; do not claim PROVEN",
            )
        )

    _write_json(out_dir / "00_MANIFEST.json", man)
    _write_json(out_dir / "01_CLAIM" / "claim_definition.json", {
        "action_id": action.get("action_id"),
        "claim_id": action.get("claim_id"),
        "equation": man["equation"],
    })
    _write_json(out_dir / "02_STRUCTURE" / "module_inventory.json", {
        "total_nodes": inv["total_nodes"],
        "inspected": inv["inspected"],
        "unable_to_inspect": inv["unable_to_inspect"],
        "by_type": inv["by_type"],
        "unable": inv["unable"],
    })
    _write_json(out_dir / "02_STRUCTURE" / "reconciliation.json", {
        k: rec[k] for k in rec if k != "nodes"
    })
    _write_json(out_dir / "03_L_G_S_H" / "layers.json", {
        "L": result.law,
        "G": result.governance,
        "S": result.security,
        "H": result.human,
    })
    _write_json(out_dir / "04_CONSTRAINTS" / "mapping.json", result.mapping)
    _write_json(out_dir / "05_EVIDENCE" / "adequacy.json", result.evidence_detail)
    _write_json(out_dir / "06_TESTS" / "note.json", {
        "note": "Harness unit tests are separate; structure reconciliation is not a pytest count",
    })
    _write_json(out_dir / "07_REPLAY" / "replay.json", replay)
    _write_json(out_dir / "08_S9_EVALUATION" / "equation_evaluation.json", result_d)
    _write_json(out_dir / "09_FAILURES" / "failure_diagnostics.json", failures)
    _write_json(out_dir / "10_AUTHORITY" / "authorization_state.json", {
        "human": result.human,
        "promotion_eligible": False,
        "production_authorized": False,
        "authority_input": action.get("authority") or {},
    })

    file_hashes = {}
    for p in sorted(out_dir.rglob("*.json")):
        rel = str(p.relative_to(out_dir))
        file_hashes[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    _write_json(out_dir / "11_INTEGRITY" / "hashes.json", file_hashes)
    _write_json(out_dir / "12_REPORT" / "S9_AUDIT_REPORT.json", {
        "report_id": rid,
        "source_commit": source_commit,
        "system_result": result.system_result,
        "documented_equation_result": result.documented_equation_result,
        "evidence_adequacy_result": result.evidence_adequacy_result,
        "s9_proven": False,
        "production_authorized": False,
        "promotion_eligible": False,
        "reasons": result.reasons,
        "structure": {
            "total_nodes": inv["total_nodes"],
            "inspected": inv["inspected"],
            "unable_to_inspect": inv["unable_to_inspect"],
        },
        "replay_equivalent": replay["equivalent"],
        "DURABLE_REPLAY": "NOT IMPLEMENTED",
    })

    zip_path = out_dir.parent / f"{rid}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.rglob("*")):
            if p.is_file():
                zf.write(p, arcname=str(Path("S9") / p.relative_to(out_dir)))
    zip_hash = hashlib.sha256(zip_path.read_bytes()).hexdigest()

    return {
        "report_id": rid,
        "source_commit": source_commit,
        "out_dir": str(out_dir),
        "zip_path": str(zip_path),
        "zip_sha256": zip_hash,
        "system_result": result.system_result,
        "s9_proven": False,
        "production_authorized": False,
    }
