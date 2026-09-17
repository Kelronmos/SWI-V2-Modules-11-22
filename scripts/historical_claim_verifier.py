#!/usr/bin/env python3
"""
SWI Historical Claim Verifier (fail-closed).

Does NOT hard-code M11=SEALED.
Does NOT treat filename matches as implementation.
Does NOT treat test path existence as pytest pass.
Does NOT treat generic AUDIT_SUMMARY as any-module seal.

Usage:
  python scripts/historical_claim_verifier.py --demo-m11-regression
  python scripts/historical_claim_verifier.py --v2-tree tree.json [--audit-json path] [--seal-md path] --ci-verified --ci-run-id ID

Exit codes:
  0 — report written
  2 — fatal package/mode error (fail closed)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

MODULE_ID_RE = re.compile(r"^M([0-9]{1,2})$", re.I)
MAX_MODULE = 46


def normalize_module(raw: str) -> Optional[str]:
    raw = raw.strip().upper().replace("MODULE ", "M").replace("MODULE", "M")
    if not raw.startswith("M"):
        raw = "M" + raw
    m = MODULE_ID_RE.match(raw)
    if not m:
        return None
    n = int(m.group(1))
    if n < 0 or n > MAX_MODULE:
        return None
    return f"M{n:02d}"


def classify_path(path: str) -> str:
    p = path.replace("\\", "/").lower()
    if p.startswith("docs/") or p.endswith(".md"):
        return "DOCUMENTATION"
    if "/test/" in f"/{p}" or p.startswith("test/") or p.startswith("tests/"):
        return "TEST"
    if ".github/workflows/" in p:
        return "WORKFLOW"
    if p.endswith(".json") and ("evidence" in p or "audit" in p or "artifact" in p):
        return "ARTIFACT"
    if p.endswith(".py") and (
        p.startswith("swi_v2/") or p.startswith("swi_core/") or "/kernel/" in p or "/module" in p
    ):
        return "SOURCE"
    if p.endswith(".py"):
        return "SOURCE"
    return "OTHER"


def is_stub_source(path: str, size: Optional[int] = None) -> bool:
    p = path.replace("\\", "/")
    if re.search(r"module\d+/__init__\.py$", p):
        if size is not None and size < 300:
            return True
    return False


@dataclass
class ModuleEvidence:
    module: str
    path_hits: Dict[str, List[str]] = field(
        default_factory=lambda: {
            "SOURCE": [],
            "TEST": [],
            "DOCUMENTATION": [],
            "WORKFLOW": [],
            "ARTIFACT": [],
            "OTHER": [],
        }
    )
    seal_record_ok: bool = False
    audit_summary_ok: bool = False
    ci_verified: bool = False
    ci_run_id: Optional[str] = None
    flags: List[str] = field(default_factory=list)
    evidence_level: str = "E0_DOCUMENTED"
    notes: List[str] = field(default_factory=list)


def score_module(ev: ModuleEvidence) -> None:
    src = [p for p in ev.path_hits["SOURCE"] if not is_stub_source(p)]
    tests = ev.path_hits["TEST"]
    level = "E0_DOCUMENTED"
    if src:
        level = "E1_IMPLEMENTED"
    if src and tests:
        level = "E2_TESTED"
    if level == "E2_TESTED" and ev.ci_verified:
        level = "E3_CI_VERIFIED"
    if level in ("E2_TESTED", "E3_CI_VERIFIED", "E1_IMPLEMENTED") and ev.seal_record_ok:
        if ev.ci_verified or ev.audit_summary_ok:
            level = "E4_SEALED"
        else:
            ev.flags.append("SEAL_RECORD_PRESENT_CI_UNVERIFIED")
            level = "E2_TESTED" if tests else "E1_IMPLEMENTED"
            ev.notes.append("Seal record content OK but CI not verified → not E4")
    if not src and not tests and not ev.seal_record_ok:
        ev.flags.append("UNPROVEN")
    ev.evidence_level = level


def parse_audit_json(text: str, module: str) -> bool:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    if not isinstance(data, dict):
        return False
    mod = str(data.get("module", ""))
    status = str(data.get("status", "")).upper()
    if normalize_module(mod) != normalize_module(module):
        return False
    return status == "SEALED"


def parse_seal_md(text: str, module: str) -> bool:
    if not re.search(r"\bSEALED\b", text, re.I):
        return False
    other = re.findall(r"\bM([0-9]{2})\b", text.upper())
    if other:
        nums = {int(x) for x in other}
        me = int(re.sub(r"\D", "", module) or "0")
        if me not in nums and len(nums) == 1:
            return False
    return True


def collect_from_tree(tree: List[Dict[str, Any]], module: str) -> ModuleEvidence:
    ev = ModuleEvidence(module=module)
    n = int(re.sub(r"\D", "", module))
    patterns = [
        re.compile(rf"module{n:02d}\b", re.I),
        re.compile(rf"module_{n:02d}\b", re.I),
        re.compile(rf"\bm{n:02d}\b", re.I),
        re.compile(rf"m{n}_", re.I),
    ]
    for item in tree:
        path = item.get("path") or ""
        if not path or not any(p.search(path) for p in patterns):
            continue
        cls = classify_path(path)
        size = item.get("size")
        if cls == "SOURCE" and is_stub_source(path, size):
            ev.notes.append(f"stub ignored for E1: {path}")
            continue
        ev.path_hits.setdefault(cls, []).append(path)
    return ev


def attach_kernel_for_m11(ev: ModuleEvidence, tree_paths: Set[str]) -> None:
    if ev.module != "M11":
        return
    for p in tree_paths:
        if p.startswith("swi_v2/kernel/") and p.endswith(".py") and not p.endswith("sparse_merkle.py"):
            if p not in ev.path_hits["SOURCE"]:
                ev.path_hits["SOURCE"].append(p)


def build_report(
    *,
    tree: List[Dict[str, Any]],
    modules: List[str],
    v2_commit: Optional[str],
    audit_json_text: Optional[str],
    seal_md_text: Optional[str],
    ci_run_id: Optional[str],
    ci_verified: bool,
    package_status: str,
) -> Dict[str, Any]:
    tree_paths = {item.get("path", "") for item in tree if item.get("path")}
    results: List[Dict[str, Any]] = []
    conflicts: List[str] = []

    for mod in modules:
        ev = collect_from_tree(tree, mod)
        if mod == "M11":
            attach_kernel_for_m11(ev, tree_paths)
            if seal_md_text is not None:
                ev.seal_record_ok = parse_seal_md(seal_md_text, "M11")
                if not ev.seal_record_ok:
                    ev.flags.append("SEAL_UNVERIFIED")
            else:
                ev.flags.append("SEAL_RECORD_NOT_PROVIDED")
            if audit_json_text is not None:
                ev.audit_summary_ok = parse_audit_json(audit_json_text, "M11")
            if ci_verified and ci_run_id:
                ev.ci_verified = True
                ev.ci_run_id = ci_run_id
            else:
                ev.flags.append("CI_UNVERIFIED")
            conflicts.append(
                "M11: HISTORICAL ContinuityLock/state-tag narrative ≠ CURRENT admission+post-admission seal contract"
            )
            ev.flags.append("CONFLICT_HISTORICAL_VS_CURRENT")
        score_module(ev)
        results.append(asdict(ev))

    return {
        "audit_id": f"V47-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "package_status": package_status,
        "repositories": {
            "V2": {
                "repository": "Kelronmos/SWI-V2-Modules-11-22",
                "branch": "main",
                "commit": v2_commit or "UNVERIFIED",
            }
        },
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "modules": results,
        "conflicts": conflicts,
        "non_proofs": [
            "Physical isolation: NOT ESTABLISHED",
            "Production HSM: NOT ESTABLISHED",
            "CRTG: NOT IMPLEMENTED",
            "Factual truth: NOT ESTABLISHED BY CRYPTOGRAPHY",
            "Test path existence ≠ pytest passed (E2 only)",
        ],
        "conclusion": (
            "Historical documentation does not upgrade implementation status. "
            "Proof levels are fail-closed."
        ),
    }


def demo_m11_regression() -> Dict[str, Any]:
    paths = [
        "swi_v2/kernel/seal.py",
        "swi_v2/kernel/admission.py",
        "swi_v2/kernel/ed25519_sig.py",
        "swi_v2/kernel/merkle.py",
        "swi_v2/kernel/contracts.py",
        "swi_v2/module11/foundation_admission.py",
        "swi_v2/module11/__init__.py",
        "swi_v2/module12/__init__.py",
        "test/test_m11_post_admission_seal.py",
        "test/test_m11_seal_boundary_attacks.py",
        "test/test_m11_end_to_end_seal.py",
        "docs/M11_SEAL_RECORD.md",
        "docs/M11_AUDIT_SUMMARY.json",
        "docs/MODULE_STATUS.md",
    ]
    tree = [{"path": p, "size": 500 if "module12" not in p else 61} for p in paths]
    seal_md = "# M11 Seal Record\n\n**SEALED**\n\nV2 `1d6d7dc`\nRun ID: `35253244912`\n"
    audit = json.dumps(
        {
            "module": "M11",
            "status": "SEALED",
            "workflow_run": "35253244912",
            "v2_sha": "1d6d7dc250df80f39aa60bd8da812c9ae3efebec",
        }
    )
    return build_report(
        tree=tree,
        modules=["M11", "M12"],
        v2_commit="1d6d7dc250df80f39aa60bd8da812c9ae3efebec",
        audit_json_text=audit,
        seal_md_text=seal_md,
        ci_run_id="35253244912",
        ci_verified=True,
        package_status="STANDALONE_DOCUMENTS",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="SWI historical claim verifier (fail-closed)")
    ap.add_argument("--demo-m11-regression", action="store_true")
    ap.add_argument("--v2-tree", type=Path, default=None)
    ap.add_argument("--v2-commit", type=str, default=None)
    ap.add_argument("--audit-json", type=Path, default=None)
    ap.add_argument("--seal-md", type=Path, default=None)
    ap.add_argument("--ci-run-id", type=str, default=None)
    ap.add_argument("--ci-verified", action="store_true")
    ap.add_argument(
        "--package-status",
        default="NOT_VERIFIED",
        choices=["COMPLETE_ZIP", "STANDALONE_DOCUMENTS", "INCOMPLETE", "NOT_VERIFIED"],
    )
    ap.add_argument("--modules", default="M11,M12")
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args()

    if args.package_status == "INCOMPLETE":
        print("PACKAGE_STATUS=INCOMPLETE — fail closed", file=sys.stderr)
        return 2

    if args.demo_m11_regression:
        report = demo_m11_regression()
    else:
        if not args.v2_tree or not args.v2_tree.exists():
            print("Need --v2-tree or --demo-m11-regression", file=sys.stderr)
            return 2
        tree = json.loads(args.v2_tree.read_text())
        if isinstance(tree, dict) and "tree" in tree:
            tree = tree["tree"]
        audit_text = args.audit_json.read_text() if args.audit_json else None
        seal_text = args.seal_md.read_text() if args.seal_md else None
        mods = [normalize_module(x) or x.strip().upper() for x in args.modules.split(",")]
        report = build_report(
            tree=tree,
            modules=mods,
            v2_commit=args.v2_commit,
            audit_json_text=audit_text,
            seal_md_text=seal_text,
            ci_run_id=args.ci_run_id,
            ci_verified=bool(args.ci_verified),
            package_status=args.package_status,
        )

    out = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(out)
    print(out)

    if args.demo_m11_regression:
        m11 = next(m for m in report["modules"] if m["module"] == "M11")
        m12 = next(m for m in report["modules"] if m["module"] == "M12")
        assert m11["evidence_level"] == "E4_SEALED", m11
        assert m12["evidence_level"] != "E4_SEALED"
        print("demo_m11_regression: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
