#!/usr/bin/env python3
"""Build tip-bound S9 evaluation package. Does not prove S9 or authorize production.

Usage:
  python scripts/s9_build_package.py --commit aa62042888886f5252e2b80e7aec8dce49e4bab3 --out /tmp/s9_out
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_v2.s9.package import build_package, PackageRefused


def resolve_commit(explicit: str | None) -> str:
    if explicit:
        return explicit
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def main() -> int:
    p = argparse.ArgumentParser(description="S9 ZIP package builder (NOT a proof of S9)")
    p.add_argument("--commit", default=None, help="SOURCE_COMMIT (required tip binding)")
    p.add_argument("--out", default="artifacts/s9_package", help="Output directory")
    p.add_argument("--action-json", default=None, help="Optional action JSON path")
    args = p.parse_args()

    commit = resolve_commit(args.commit)
    if not commit or len(commit) < 7:
        print("REFUSED: SOURCE_COMMIT not established", file=sys.stderr)
        return 2

    if args.action_json:
        action = json.loads(Path(args.action_json).read_text())
    else:
        action = {
            "action_id": "A-CONSEQUENTIAL-SYSTEM",
            "claim_id": "CLAIM-S9-SYSTEM",
            "constraints": ["system_integrity"],
            "law": [],
            "governance": [],
            "security": [],
            "human": [],
            "evidence": [],
            "dependencies": [],
            "authority": {"required": True, "present": False},
        }

    out_dir = Path(args.out)
    try:
        result = build_package(
            repo_root=ROOT,
            source_commit=commit,
            action=action,
            out_dir=out_dir / "S9_CONTENT",
        )
    except PackageRefused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2

    print(json.dumps({
        "source_commit": result["source_commit"],
        "system_result": result["system_result"],
        "s9_proven": result["s9_proven"],
        "production_authorized": result["production_authorized"],
        "zip_path": result["zip_path"],
        "zip_sha256": result["zip_sha256"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
