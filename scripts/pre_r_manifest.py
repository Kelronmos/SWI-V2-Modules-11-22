#!/usr/bin/env python3
"""Generate evidence/pre_r/manifest.json — no security claims beyond recorded results."""
from __future__ import annotations
import json, hashlib, pathlib, datetime, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVID = ROOT / "evidence" / "pre_r"
EVID.mkdir(parents=True, exist_ok=True)

def sha256_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

manifest = {
    "schema": "swi.pre_r.evidence.v1",
    "repository": "Kelronmos/SWI-V2-Modules-11-22",
    "commit": git("rev-parse", "HEAD"),
    "branch": git("branch", "--show-current"),
    "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "claim": "REJECT/HALT blocks privileged execution through the enforced experimental API path",
    "scope": "experimental API boundary only",
    "proof_categories": ["P0", "P1", "P2"],
    "not_claimed": [
        "process-wide enforcement",
        "Level 4 structural coverage",
        "Level 5 independent verification",
        "M11 seal",
        "PRE-CONSEQUENCES runtime",
    ],
    "tests": [
        {"id": "pre_r_suite", "path": "tests/pre_r/", "result_file": "test-results/pre_r.out"},
        {"id": "v2_full", "path": "test/ + tests/", "result_file": "test-results/v2_full.out"},
    ],
    "artifacts": [],
    "limitations_ref": "docs/pre-R/LIMITATIONS.md",
    "laws": ["LAW-001", "LAW-002", "LAW-003", "LAW-005", "LAW-006", "LAW-007", "LAW-008", "LAW-009", "LAW-011", "LAW-012", "LAW-015"],
}

for p in sorted(EVID.rglob("*")):
    if p.is_file() and p.name != "manifest.json":
        rel = str(p.relative_to(EVID))
        manifest["artifacts"].append({"path": rel, "sha256": sha256_file(p)})

out = EVID / "manifest.json"
out.write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Wrote {out}")
print(json.dumps({"commit": manifest["commit"], "artifacts": len(manifest["artifacts"])}, indent=2))
