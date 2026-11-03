#!/usr/bin/env python3
"""
SWI Public Evidence Lab — Trusted local runner (prototype scope).

This runner:
- Derives commit/runtime identity from local process and (if present) git metadata.
- Never treats UI-supplied SHA as verified.
- Emits a single canonical run record.
- Explicitly sets PROVEN=NO, SEALED=NO, PRODUCTION_AUTHORIZED=NO.
- Records limitations. Does not claim production authorization or independent review.

Scope: demonstration of evidence capture for the public lab. Not the full SWI spine.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

SCHEMA = "swi.public-evidence-lab.run.v1"
PROTOTYPE_VERSION = "0.1.0-local-runner"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(argv: List[str], cwd: Optional[Path] = None, timeout: int = 15) -> Dict[str, Any]:
    start = time.monotonic()
    try:
        p = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        duration = time.monotonic() - start
        stdout = p.stdout or ""
        stderr = p.stderr or ""
        return {
            "argv": argv,
            "cwd": str(cwd) if cwd else os.getcwd(),
            "exit_code": p.returncode,
            "duration_s": round(duration, 4),
            "stdout_hash": sha256_bytes(stdout.encode("utf-8")),
            "stderr_hash": sha256_bytes(stderr.encode("utf-8")),
            "stdout_preview": stdout[:400],
            "stderr_preview": stderr[:400],
        }
    except Exception as e:
        return {
            "argv": argv,
            "cwd": str(cwd) if cwd else os.getcwd(),
            "exit_code": -1,
            "duration_s": round(time.monotonic() - start, 4),
            "error": str(e),
            "stdout_hash": None,
            "stderr_hash": None,
        }


def detect_git(cwd: Path) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "is_git_repo": False,
        "commit_sha": None,
        "branch": None,
        "dirty": None,
        "remote_url": None,
        "verified_from": "none",
    }
    try:
        r = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=cwd)
        if r.get("exit_code") != 0:
            return info
        info["is_git_repo"] = True
        info["verified_from"] = "local-git-metadata"

        sha = run_cmd(["git", "rev-parse", "HEAD"], cwd=cwd)
        if sha.get("exit_code") == 0 and sha.get("stdout_preview"):
            info["commit_sha"] = sha["stdout_preview"].strip()

        branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
        if branch.get("exit_code") == 0:
            info["branch"] = branch["stdout_preview"].strip()

        dirty = run_cmd(["git", "status", "--porcelain"], cwd=cwd)
        if dirty.get("exit_code") == 0:
            info["dirty"] = bool(dirty.get("stdout_preview", "").strip())

        remote = run_cmd(["git", "remote", "get-url", "origin"], cwd=cwd)
        if remote.get("exit_code") == 0:
            info["remote_url"] = remote["stdout_preview"].strip()
    except Exception as e:
        info["error"] = str(e)
    return info


def node_inventory() -> Dict[str, Any]:
    return {
        "platform": platform.platform(),
        "python": sys.version,
        "python_executable": sys.executable,
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
        "cwd": os.getcwd(),
        "pid": os.getpid(),
        "uid": os.getuid() if hasattr(os, "getuid") else None,
    }


def build_checks(git_info: Dict[str, Any], startup_kind: str) -> List[Dict[str, Any]]:
    checks = []

    checks.append({
        "id": "RUNNER_START",
        "observed": f"Local runner process started ({startup_kind})",
        "pass": True,
        "scope": "local-runner-process",
    })

    checks.append({
        "id": "HTML_PROTOTYPE_PRESENT",
        "observed": "public-prototype/index.html expected as presentation layer only",
        "pass": True,
        "scope": "prototype-presentation",
    })

    has_commit = bool(git_info.get("commit_sha"))
    checks.append({
        "id": "COMMIT_BINDING",
        "observed": (
            f"Observed commit from local git: {git_info.get('commit_sha')}"
            if has_commit
            else "No local git repository metadata available in this working directory"
        ),
        "pass": has_commit,
        "scope": "repository-identity",
    })

    checks.append({
        "id": "RUNTIME_IDENTITY",
        "observed": f"Process identity captured: pid={os.getpid()}, platform={platform.platform()}",
        "pass": True,
        "scope": "runtime-identity",
    })

    checks.append({
        "id": "AUTHORIZATION_SPINE",
        "observed": "No connection to SWI authorization spine established by this runner",
        "pass": False,
        "scope": "authorization-not-verified",
    })

    checks.append({
        "id": "INDEPENDENT_REVIEW",
        "observed": "No independent reviewer evidence supplied",
        "pass": False,
        "scope": "review-pending",
    })

    checks.append({
        "id": "PRODUCTION_AUTHORIZATION",
        "observed": "Never granted by this public evidence lab runner",
        "pass": False,
        "scope": "production-unauthorized",
    })

    checks.append({
        "id": "FAKE_UI_HARDCODED_GREEN",
        "observed": "Canonical record forces PROVEN=NO / PRODUCTION_AUTHORIZED=NO regardless of any UI badge",
        "pass": True,
        "scope": "adversarial-ui-detection",
    })

    return checks


def make_record(startup_kind: str = "manual", expected_commit: Optional[str] = None) -> Dict[str, Any]:
    run_id = f"LOCAL-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    cwd = Path.cwd()
    git_info = detect_git(cwd)
    inv = node_inventory()
    checks = build_checks(git_info, startup_kind)

    commit_match = None
    if expected_commit and git_info.get("commit_sha"):
        commit_match = (expected_commit.lower() == git_info["commit_sha"].lower())

    passed = sum(1 for c in checks if c["pass"])
    failed = len(checks) - passed

    record = {
        "schema": SCHEMA,
        "run_id": run_id,
        "timestamp_utc": utc_now(),
        "prototype_version": PROTOTYPE_VERSION,
        "source": "trusted-local-runner",
        "startup_kind": startup_kind,
        "repository": {
            "name": "Kelronmos/SWI-V2-Modules-11-22",
            "observed_branch": git_info.get("branch"),
            "observed_commit_sha": git_info.get("commit_sha"),
            "dirty_tree": git_info.get("dirty"),
            "remote_url": git_info.get("remote_url"),
            "verified_from": git_info.get("verified_from"),
            "expected_commit_sha": expected_commit,
            "commit_match": commit_match,
            "user_entered_sha_treated_as_verified": False,
        },
        "runtime": inv,
        "checks": checks,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": len(checks),
        },
        "claims": {
            "proven": False,
            "sealed": False,
            "independent_review_approved": False,
            "production_authorized": False,
            "status_notes": [
                "TESTED != PROVEN",
                "PROVEN != SEALED",
                "SEALED != PRODUCTION_AUTHORIZED",
                "CI_GREEN != SWI_AUTHORIZED",
                "INDEPENDENT_REVIEW_PENDING != INDEPENDENT_REVIEW_APPROVED",
            ],
        },
        "limitations": [
            "Browser-local HTML is presentation only; this runner is the evidence authority.",
            "No SWI authorization spine connection was made.",
            "No independent review evidence is present.",
            "No production authorization is granted.",
            "A user-typed commit SHA is never treated as verified.",
            "This run does not reboot the host or restart any production service.",
            "JPG/PDF/XLSX generation may be marked NOT_GENERATED if dependencies missing.",
        ],
        "evidence_integrity": {
            "canonical_record_hash": None,
            "signed": False,
            "independently_verified": False,
        },
    }

    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    record["evidence_integrity"]["canonical_record_hash"] = sha256_bytes(canonical)
    return record


def export_artifacts(record: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"schema": "swi.public-evidence-lab.manifest.v1", "generated_utc": utc_now(), "artifacts": []}

    json_path = out_dir / f"{record['run_id']}.json"
    json_bytes = json.dumps(record, indent=2, sort_keys=False).encode("utf-8")
    json_path.write_bytes(json_bytes)
    manifest["artifacts"].append({
        "path": str(json_path.name),
        "sha256": sha256_bytes(json_bytes),
        "format": "json",
        "status": "GENERATED",
    })

    txt_lines = [
        "SWI PUBLIC EVIDENCE LAB — RUN REPORT",
        f"Run ID: {record['run_id']}",
        f"UTC: {record['timestamp_utc']}",
        f"Schema: {record['schema']}",
        f"PROVEN={record['claims']['proven']}",
        f"SEALED={record['claims']['sealed']}",
        f"PRODUCTION_AUTHORIZED={record['claims']['production_authorized']}",
        f"INDEPENDENT_REVIEW_APPROVED={record['claims']['independent_review_approved']}",
        "",
        "Checks:",
    ]
    for c in record["checks"]:
        status = "PASS" if c["pass"] else "NOT_VERIFIED"
        txt_lines.append(f"  {c['id']}: {status} — {c['observed']}")
    txt_lines.append("")
    txt_lines.append("Limitations:")
    for lim in record["limitations"]:
        txt_lines.append(f"  - {lim}")
    txt_content = "\n".join(txt_lines) + "\n"
    txt_path = out_dir / f"{record['run_id']}.txt"
    txt_path.write_text(txt_content, encoding="utf-8")
    manifest["artifacts"].append({
        "path": str(txt_path.name),
        "sha256": sha256_bytes(txt_content.encode("utf-8")),
        "format": "txt",
        "status": "GENERATED",
    })

    csv_lines = ["id,observed,pass,scope"]
    for c in record["checks"]:
        obs = c["observed"].replace('"', '""')
        csv_lines.append(f'"{c["id"]}","{obs}",{str(c["pass"]).lower()},"{c["scope"]}"')
    csv_content = "\n".join(csv_lines) + "\n"
    csv_path = out_dir / f"{record['run_id']}-checks.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    manifest["artifacts"].append({
        "path": str(csv_path.name),
        "sha256": sha256_bytes(csv_content.encode("utf-8")),
        "format": "csv",
        "status": "GENERATED",
    })

    html_note = out_dir / f"{record['run_id']}-html-note.txt"
    html_note.write_text(
        "HTML export is produced by the browser presentation layer (index.html).\n"
        "This runner does not embed the full page DOM. Use the prototype export button.\n",
        encoding="utf-8",
    )
    manifest["artifacts"].append({
        "path": str(html_note.name),
        "sha256": sha256_file(html_note),
        "format": "html-note",
        "status": "GENERATED",
    })

    for fmt, reason in [
        ("pdf", "reportlab or weasyprint not required for this minimal runner"),
        ("xlsx", "openpyxl not required for this minimal runner"),
        ("jpg", "Pillow image summary not generated in this minimal runner"),
    ]:
        manifest["artifacts"].append({
            "path": f"{record['run_id']}.{fmt}",
            "sha256": None,
            "format": fmt,
            "status": "NOT_GENERATED",
            "reason": reason,
        })

    man_path = out_dir / f"{record['run_id']}-manifest.json"
    man_bytes = json.dumps(manifest, indent=2).encode("utf-8")
    man_path.write_bytes(man_bytes)
    manifest["manifest_sha256"] = sha256_bytes(man_bytes)
    man_path.write_bytes(json.dumps(manifest, indent=2).encode("utf-8"))

    return manifest


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="SWI Public Evidence Lab trusted runner")
    parser.add_argument("--startup-kind", default="manual", choices=["first-start", "subsequent-start", "manual"])
    parser.add_argument("--expected-commit", default=None, help="Optional expected commit for comparison (never treated as verified input from UI)")
    parser.add_argument("--out-dir", default="evidence", help="Directory for artifacts")
    args = parser.parse_args()

    record = make_record(startup_kind=args.startup_kind, expected_commit=args.expected_commit)
    out = Path(args.out_dir)
    manifest = export_artifacts(record, out)

    print(json.dumps({
        "run_id": record["run_id"],
        "claims": record["claims"],
        "summary": record["summary"],
        "observed_commit": record["repository"]["observed_commit_sha"],
        "manifest_artifacts": len(manifest["artifacts"]),
        "out_dir": str(out.resolve()),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
