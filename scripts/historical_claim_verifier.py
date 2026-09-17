#!/usr/bin/env python3
"""SWI Historical Claim Verifier v2 — strict E4. See docs/V47_VERIFIER_HARDENING.md"""
from __future__ import annotations
import argparse, json, re, sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

MAX_MODULE = 46
MODULE_ID_RE = re.compile(r"^M([0-9]{1,2})$", re.I)

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
    if "/test/" in f"/{p}" or p.startswith("test/"):
        return "TEST"
    if ".github/workflows/" in p:
        return "WORKFLOW"
    if p.endswith(".json") and ("audit" in p or "evidence" in p):
        return "ARTIFACT"
    if p.endswith(".py"):
        return "SOURCE"
    return "OTHER"

def is_stub_source(path: str, size: Optional[int] = None) -> bool:
    p = path.replace("\\", "/")
    if re.search(r"module\d+/__init__\.py$", p):
        return size is not None and size < 300
    return False

@dataclass
class SealParse:
    ok: bool
    status_sealed: bool = False
    v2_sha: Optional[str] = None
    ci_run: Optional[str] = None
    error: Optional[str] = None

@dataclass
class ModuleEvidence:
    module: str
    path_hits: Dict[str, List[str]] = field(default_factory=lambda: {k: [] for k in ["SOURCE", "TEST", "DOCUMENTATION", "WORKFLOW", "ARTIFACT", "OTHER"]})
    seal_record_ok: bool = False
    seal_binding_ok: bool = False
    audit_summary_ok: bool = False
    ci_verified: bool = False
    ci_self_attested: bool = False
    ci_run_id: Optional[str] = None
    sealed_at_commit: Optional[str] = None
    current_tip: Optional[str] = None
    flags: List[str] = field(default_factory=list)
    evidence_level: str = "E0_DOCUMENTED"
    notes: List[str] = field(default_factory=list)

def parse_seal_md_strict(text: str, module: str) -> SealParse:
    if not re.search(r"\bSEALED\b", text, re.I):
        return SealParse(ok=False, error="no_SEALED_token")
    shas = re.findall(r"\b([0-9a-f]{40})\b", text.lower())
    short = re.findall(r"`([0-9a-f]{7,40})`", text.lower())
    v2 = shas[0] if shas else (short[0] if short else None)
    run = None
    m = re.search(r"(?:Run ID|workflow_run|CI run|run)[:\s#`]*([0-9]{8,})", text, re.I)
    if m:
        run = m.group(1)
    if not v2 or not run:
        return SealParse(ok=False, status_sealed=True, v2_sha=v2, ci_run=run, error="SEAL_BINDING_UNVERIFIED_missing_sha_or_run")
    return SealParse(ok=True, status_sealed=True, v2_sha=v2, ci_run=run)

def parse_audit_json_strict(text: str, module: str) -> Tuple[bool, Dict[str, Any]]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False, {"error": "invalid_json"}
    if not isinstance(data, dict):
        return False, {"error": "not_object"}
    if normalize_module(str(data.get("module", ""))) != normalize_module(module):
        return False, {"error": "module_mismatch"}
    if str(data.get("status", "")).upper() != "SEALED":
        return False, {"error": "status_not_sealed"}
    return True, {"v2_sha": data.get("v2_sha"), "workflow_run": str(data.get("workflow_run", "")), "status": "SEALED"}

def score_module(ev: ModuleEvidence) -> None:
    src = [p for p in ev.path_hits["SOURCE"] if not is_stub_source(p)]
    tests = ev.path_hits["TEST"]
    level = "E0_DOCUMENTED"
    if src:
        level = "E1_IMPLEMENTATION_SURFACE"
        ev.notes.append("E1 = surface only")
    if src and tests:
        level = "E2_TESTED"
        ev.notes.append("E2 = test paths present; not proof tests passed")
    if level == "E2_TESTED" and ev.ci_verified and not ev.ci_self_attested:
        level = "E3_CI_VERIFIED"
    elif level == "E2_TESTED" and ev.ci_verified and ev.ci_self_attested:
        level = "E2_TESTED"
        ev.flags.append("CI_SELF_ATTESTED_NOT_E3")
    if ev.seal_record_ok and ev.seal_binding_ok and ev.ci_verified and not ev.ci_self_attested and src and tests:
        level = "E4_SEALED"
    elif ev.seal_record_ok and not ev.seal_binding_ok:
        ev.flags.append("SEAL_BINDING_UNVERIFIED")
    elif ev.seal_record_ok and ev.audit_summary_ok and not ev.ci_verified:
        ev.flags.append("AUDIT_JSON_ALONE_NOT_E4")
    if not src and not tests and not ev.seal_record_ok:
        ev.flags.append("UNPROVEN")
    ev.evidence_level = level

def collect_from_tree(tree: List[Dict[str, Any]], module: str) -> ModuleEvidence:
    ev = ModuleEvidence(module=module)
    n = int(re.sub(r"\D", "", module))
    patterns = [re.compile(rf"module{n:02d}\b", re.I), re.compile(rf"\bm{n:02d}\b", re.I), re.compile(rf"m{n}_", re.I)]
    for item in tree:
        path = item.get("path") or ""
        if not path or not any(p.search(path) for p in patterns):
            continue
        cls = classify_path(path)
        if cls == "SOURCE" and is_stub_source(path, item.get("size")):
            ev.notes.append(f"stub ignored: {path}")
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

def bind_seal(seal: SealParse, audited_commit: Optional[str], expected_ci_run: Optional[str]) -> Tuple[bool, List[str]]:
    flags: List[str] = []
    if not seal.ok:
        flags.append(seal.error or "SEAL_PARSE_FAIL")
        return False, flags
    if audited_commit and seal.v2_sha:
        a, s = audited_commit.lower(), seal.v2_sha.lower()
        if not (a.startswith(s) or s.startswith(a[: len(s)])):
            flags.append("SEAL_COMMIT_MISMATCH")
            return False, flags
    if expected_ci_run and seal.ci_run and expected_ci_run != seal.ci_run:
        flags.append("SEAL_CI_RUN_MISMATCH")
        return False, flags
    return True, flags

def build_report(*, tree, modules, v2_commit, audit_json_text, seal_md_text, ci_run_id, ci_verified, ci_self_attested, package_status):
    tree_paths = {item.get("path", "") for item in tree if item.get("path")}
    results, conflicts = [], []
    for mod in modules:
        ev = collect_from_tree(tree, mod)
        ev.current_tip = v2_commit
        if mod == "M11":
            attach_kernel_for_m11(ev, tree_paths)
            if seal_md_text is not None:
                seal = parse_seal_md_strict(seal_md_text, "M11")
                ev.seal_record_ok = seal.status_sealed
                ok_bind, bflags = bind_seal(seal, v2_commit, ci_run_id)
                ev.seal_binding_ok = ok_bind
                ev.sealed_at_commit = seal.v2_sha
                ev.flags.extend(bflags)
                if not seal.ok:
                    ev.flags.append("SEAL_UNVERIFIED")
            else:
                ev.flags.append("SEAL_RECORD_NOT_PROVIDED")
            if audit_json_text is not None:
                aok, adata = parse_audit_json_strict(audit_json_text, "M11")
                ev.audit_summary_ok = aok
                if aok and seal_md_text is not None:
                    seal = parse_seal_md_strict(seal_md_text, "M11")
                    if seal.ci_run and adata.get("workflow_run") and seal.ci_run != str(adata.get("workflow_run")):
                        ev.flags.append("AUDIT_SEAL_CI_CONFLICT")
                        conflicts.append("audit run != seal run")
            if ci_verified and ci_run_id:
                ev.ci_verified = True
                ev.ci_run_id = ci_run_id
                ev.ci_self_attested = ci_self_attested
            else:
                ev.flags.append("CI_UNVERIFIED")
            conflicts.append("M11: HISTORICAL ContinuityLock != CURRENT admission+seal (EVOLVED_CONTRACT)")
            ev.flags.append("EVOLVED_CONTRACT")
        score_module(ev)
        results.append(asdict(ev))
    return {
        "audit_id": f"V47-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "verifier_version": "2-strict-e4",
        "package_status": package_status,
        "repositories": {"V2": {"repository": "Kelronmos/SWI-V2-Modules-11-22", "commit": v2_commit or "UNVERIFIED"}},
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "modules": results,
        "conflicts": conflicts,
        "non_proofs": ["Audit JSON alone != E4", "Self-attested CI != independent CI", "Factual truth NOT by cryptography"],
        "conclusion": "E4 requires seal binding + independent CI + implementation surface + tests.",
    }

def demo_m11_regression():
    paths = [
        "swi_v2/kernel/seal.py", "swi_v2/kernel/admission.py", "swi_v2/kernel/ed25519_sig.py", "swi_v2/kernel/merkle.py",
        "swi_v2/module11/foundation_admission.py", "swi_v2/module12/__init__.py",
        "test/test_m11_post_admission_seal.py", "test/test_m11_seal_boundary_attacks.py", "docs/M11_SEAL_RECORD.md",
    ]
    tree = [{"path": p, "size": 500 if "module12" not in p else 61} for p in paths]
    seal_md = "# M11 Seal Record\n\n**SEALED**\n\n| **V2** | `1d6d7dc250df80f39aa60bd8da812c9ae3efebec` |\nRun ID: `35253244912`\n"
    audit = json.dumps({"module": "M11", "status": "SEALED", "workflow_run": "35253244912", "v2_sha": "1d6d7dc250df80f39aa60bd8da812c9ae3efebec"})
    return build_report(
        tree=tree, modules=["M11", "M12"], v2_commit="1d6d7dc250df80f39aa60bd8da812c9ae3efebec",
        audit_json_text=audit, seal_md_text=seal_md, ci_run_id="35253244912",
        ci_verified=True, ci_self_attested=False, package_status="STANDALONE_DOCUMENTS",
    )

def demo_fake_seal_not_e4():
    tree = [{"path": "swi_v2/kernel/seal.py", "size": 500}, {"path": "test/test_m11_post_admission_seal.py", "size": 500}]
    report = build_report(
        tree=tree, modules=["M11"], v2_commit="1d6d7dc250df80f39aa60bd8da812c9ae3efebec",
        audit_json_text=None, seal_md_text="# M11\n**SEALED**\n", ci_run_id="35253244912",
        ci_verified=True, ci_self_attested=False, package_status="STANDALONE_DOCUMENTS",
    )
    assert report["modules"][0]["evidence_level"] != "E4_SEALED"
    print("backtest_fake_seal: PASS", file=sys.stderr)

def demo_audit_alone_not_e4():
    tree = [{"path": "swi_v2/kernel/seal.py", "size": 500}, {"path": "test/test_m11_post_admission_seal.py", "size": 500}]
    audit = json.dumps({"module": "M11", "status": "SEALED"})
    report = build_report(
        tree=tree, modules=["M11"], v2_commit="1d6d7dc250df80f39aa60bd8da812c9ae3efebec",
        audit_json_text=audit, seal_md_text=None, ci_run_id=None,
        ci_verified=False, ci_self_attested=False, package_status="STANDALONE_DOCUMENTS",
    )
    assert report["modules"][0]["evidence_level"] != "E4_SEALED"
    print("backtest_audit_alone: PASS", file=sys.stderr)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo-m11-regression", action="store_true")
    ap.add_argument("--demo-backtests", action="store_true")
    ap.add_argument("--v2-tree", type=Path, default=None)
    ap.add_argument("--v2-commit", type=str, default=None)
    ap.add_argument("--audit-json", type=Path, default=None)
    ap.add_argument("--seal-md", type=Path, default=None)
    ap.add_argument("--ci-run-id", type=str, default=None)
    ap.add_argument("--ci-verified", action="store_true")
    ap.add_argument("--ci-independent", action="store_true")
    ap.add_argument("--package-status", default="NOT_VERIFIED",
                    choices=["COMPLETE_ZIP", "STANDALONE_DOCUMENTS", "INCOMPLETE", "NOT_VERIFIED"])
    ap.add_argument("--modules", default="M11,M12")
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args()
    if args.package_status == "INCOMPLETE":
        print("PACKAGE_STATUS=INCOMPLETE", file=sys.stderr)
        return 2
    if args.demo_backtests:
        demo_fake_seal_not_e4()
        demo_audit_alone_not_e4()
        return 0
    if args.demo_m11_regression:
        report = demo_m11_regression()
    else:
        if not args.v2_tree or not args.v2_tree.exists():
            print("Need --v2-tree or --demo-m11-regression", file=sys.stderr)
            return 2
        tree = json.loads(args.v2_tree.read_text())
        if isinstance(tree, dict) and "tree" in tree:
            tree = tree["tree"]
        self_attested = bool(args.ci_verified) and not bool(args.ci_independent)
        report = build_report(
            tree=tree,
            modules=[normalize_module(x) or x.strip().upper() for x in args.modules.split(",")],
            v2_commit=args.v2_commit,
            audit_json_text=args.audit_json.read_text() if args.audit_json else None,
            seal_md_text=args.seal_md.read_text() if args.seal_md else None,
            ci_run_id=args.ci_run_id,
            ci_verified=bool(args.ci_verified) or bool(args.ci_independent),
            ci_self_attested=self_attested,
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
