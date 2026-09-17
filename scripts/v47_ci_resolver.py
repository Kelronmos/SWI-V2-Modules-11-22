#!/usr/bin/env python3
"""Independent GitHub Actions CI resolution for V4.7 verifier.

--ci-verified is an ASSERTION only.
Evidence requires API resolution of run.status, conclusion, head_sha.

Usage:
  python scripts/v47_ci_resolver.py --owner Kelronmos --repo SWI-V2-Modules-11-22 \
    --run-id 35253244912 --seal-commit 1d6d7dc250df80f39aa60bd8da812c9ae3efebec
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class CIRunEvidence:
    ok: bool
    run_id: Optional[str] = None
    head_sha: Optional[str] = None
    status: Optional[str] = None
    conclusion: Optional[str] = None
    html_url: Optional[str] = None
    error: Optional[str] = None
    independent: bool = False


def fetch_workflow_run(
    owner: str,
    repo: str,
    run_id: str,
    token: Optional[str] = None,
) -> CIRunEvidence:
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "swi-v47-verifier",
    }
    tok = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return CIRunEvidence(ok=False, run_id=run_id, error=f"HTTP_{e.code}", independent=False)
    except Exception as e:
        return CIRunEvidence(ok=False, run_id=run_id, error=str(e)[:200], independent=False)

    head = data.get("head_sha")
    status = data.get("status")
    conclusion = data.get("conclusion")
    ok = status == "completed" and conclusion == "success" and bool(head)
    return CIRunEvidence(
        ok=ok,
        run_id=str(data.get("id", run_id)),
        head_sha=head,
        status=status,
        conclusion=conclusion,
        html_url=data.get("html_url"),
        independent=True,
        error=None if ok else f"status={status} conclusion={conclusion}",
    )


def bind_seal_to_ci(
    sealed_commit: str,
    seal_run_id: str,
    evidence: CIRunEvidence,
) -> Dict[str, Any]:
    result = {
        "ci_independent": evidence.independent,
        "ci_ok": evidence.ok,
        "run_match": False,
        "sha_match": False,
        "e3_eligible": False,
        "flags": [],
    }
    if not evidence.independent:
        result["flags"].append("CI_NOT_INDEPENDENT")
        return result
    if not evidence.ok:
        result["flags"].append("CI_RUN_NOT_SUCCESS")
        if evidence.error:
            result["flags"].append(evidence.error)
        return result
    result["run_match"] = str(evidence.run_id) == str(seal_run_id)
    if not result["run_match"]:
        result["flags"].append("SEAL_CI_RUN_MISMATCH")
    sc = (sealed_commit or "").lower()
    hs = (evidence.head_sha or "").lower()
    result["sha_match"] = bool(
        sc and hs and (hs.startswith(sc[:7]) or sc.startswith(hs[:7]) or sc == hs)
    )
    if not result["sha_match"]:
        result["flags"].append("SEAL_COMMIT_NE_RUN_HEAD_SHA")
    result["e3_eligible"] = result["run_match"] and result["sha_match"] and evidence.ok
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Independent CI run resolution for V4.7")
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--seal-commit", default="")
    ap.add_argument("--token", default=None)
    args = ap.parse_args()
    ev = fetch_workflow_run(args.owner, args.repo, args.run_id, token=args.token)
    bind = bind_seal_to_ci(args.seal_commit, args.run_id, ev) if args.seal_commit else {}
    out = {"run": asdict(ev), "bind": bind}
    print(json.dumps(out, indent=2))
    if not ev.independent or not ev.ok:
        return 2
    if args.seal_commit and not bind.get("e3_eligible"):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
