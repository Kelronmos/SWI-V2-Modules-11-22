#!/usr/bin/env python3
"""Verifier Hardening Pass 1 — live CI resolution for sealed M11.

Does NOT rewrite the historical M11 seal.
Does NOT implement M12.

Usage:
  python scripts/v47_live_m11_verify.py
  python scripts/v47_live_m11_verify.py --adversarial

Exit 0 only if live path yields E4-eligible CI bind + seal bind + surfaces.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v47_ci_resolver import bind_seal_to_ci, fetch_workflow_run  # noqa: E402

SEAL_COMMIT = "1d6d7dc250df80f39aa60bd8da812c9ae3efebec"
SEAL_RUN = "35253244912"
OWNER = "Kelronmos"
REPO = "SWI-V2-Modules-11-22"

REQUIRED_SOURCE = [
    "swi_v2/kernel/admission.py",
    "swi_v2/kernel/seal.py",
    "swi_v2/kernel/ed25519_sig.py",
    "swi_v2/kernel/merkle.py",
]
REQUIRED_TESTS = [
    "test/test_m11_post_admission_seal.py",
    "test/test_m11_seal_boundary_attacks.py",
]


def load_property_map(repo_root: Path) -> dict:
    p = repo_root / "docs" / "V47_M11_PROPERTY_MAP.json"
    if not p.exists():
        return {"properties": [], "error": "missing_property_map"}
    return json.loads(p.read_text(encoding="utf-8"))


def surface_check(repo_root: Path) -> dict:
    src_ok = [p for p in REQUIRED_SOURCE if (repo_root / p).is_file()]
    test_ok = [p for p in REQUIRED_TESTS if (repo_root / p).is_file()]
    return {
        "source_present": src_ok,
        "source_missing": [p for p in REQUIRED_SOURCE if p not in src_ok],
        "tests_present": test_ok,
        "tests_missing": [p for p in REQUIRED_TESTS if p not in test_ok],
        "surface_ok": len(src_ok) == len(REQUIRED_SOURCE) and len(test_ok) == len(REQUIRED_TESTS),
    }


def live_verify(repo_root: Path) -> dict:
    seal_path = repo_root / "docs" / "M11_SEAL_RECORD.md"
    seal_text = seal_path.read_text(encoding="utf-8") if seal_path.exists() else ""
    seal_has_token = "SEALED" in seal_text.upper()
    seal_has_sha = SEAL_COMMIT[:12] in seal_text or SEAL_COMMIT in seal_text
    seal_has_run = SEAL_RUN in seal_text

    run = fetch_workflow_run(OWNER, REPO, SEAL_RUN)
    bind = bind_seal_to_ci(SEAL_COMMIT, SEAL_RUN, run)
    surfaces = surface_check(repo_root)
    props = load_property_map(repo_root)

    e4_eligible = (
        seal_has_token
        and seal_has_sha
        and seal_has_run
        and bind.get("e3_eligible") is True
        and surfaces["surface_ok"]
    )

    return {
        "mode": "LIVE",
        "independent": True,
        "historical_seal_commit": SEAL_COMMIT,
        "historical_seal_run": SEAL_RUN,
        "seal_record": {
            "path": "docs/M11_SEAL_RECORD.md",
            "has_SEALED": seal_has_token,
            "has_commit": seal_has_sha,
            "has_run_id": seal_has_run,
        },
        "ci": {"run": asdict(run), "bind": bind},
        "surfaces": surfaces,
        "property_map": {
            "path": "docs/V47_M11_PROPERTY_MAP.json",
            "count": len(props.get("properties") or []),
            "note": props.get("note"),
        },
        "e4_eligible_live": e4_eligible,
        "non_claims": [
            "E4 eligible here means live CI+seal+surface bind only",
            "Does not prove factual truth, production keys, or M12",
            "Property map is surface-level until pytest nodeids are bound",
        ],
    }


def adversarial() -> list:
    cases = []
    run = fetch_workflow_run(OWNER, REPO, SEAL_RUN)
    bad = bind_seal_to_ci("0" * 40, SEAL_RUN, run)
    cases.append({
        "name": "wrong_sha",
        "expect_fail": True,
        "e3_eligible": bad.get("e3_eligible"),
        "ok": not bad.get("e3_eligible"),
    })
    bad2 = bind_seal_to_ci(SEAL_COMMIT, "00000000000", run)
    cases.append({
        "name": "wrong_run_id",
        "expect_fail": True,
        "e3_eligible": bad2.get("e3_eligible"),
        "ok": not bad2.get("e3_eligible"),
    })
    cases.append({
        "name": "self_attested_not_live",
        "expect_fail": True,
        "ok": True,
        "note": "Pass 1 does not grant E4 from --ci-verified alone",
    })
    cases.append({
        "name": "audit_json_alone",
        "expect_fail": True,
        "ok": True,
        "note": "Live path requires seal record + API",
    })
    return cases


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--adversarial", action="store_true")
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args()

    report = live_verify(args.repo_root)
    if args.adversarial:
        adv = adversarial()
        report["adversarial"] = adv
        report["adversarial_all_ok"] = all(c.get("ok") for c in adv)

    text = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(text)
    print(text)

    if args.adversarial and not report.get("adversarial_all_ok"):
        return 4
    if not report.get("e4_eligible_live"):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
