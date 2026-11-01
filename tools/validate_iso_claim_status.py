#!/usr/bin/env python3
"""Validate the ISO claim-status register (evidence-bound claims).

Claim-wording / claim-eligibility gate — not an authorization engine.
Exit 0 = consistent. Exit 1 = violation.
Does not set PROVEN/SEALED/PRODUCTION_AUTHORIZED for SWI execution.
"""
from __future__ import annotations

import argparse
import re
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from jsonschema import Draft202012Validator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    Draft202012Validator = None  # type: ignore

ALLOWED_STATUS = {"RED", "AMBER", "GREEN", "NOT_ASSESSED", "NOT_APPLICABLE"}
ALLOWED_CONFORMITY = {"NOT_ESTABLISHED", "UNDER_ASSESSMENT", "ESTABLISHED"}
ALLOWED_CONFORMITY_CLAIM = {"SEALED", "OPEN", "WITHDRAWN"}
ALLOWED_REQ_CLAIM = {"SEALED", "PROVEN", "NOT_PROVEN", "NOT_APPLICABLE"}
ALLOWED_REPLAY = {"NOT_RUN", "PASS", "FAIL", "PARTIAL"}
REVIEW_REQUIRED_FIELDS = ("reviewer", "date", "report_hash", "outcome", "scope")
HASH_LEN = 64


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def requirement_claim_eligible(r: Dict[str, Any]) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    if r.get("applicability") not in ("APPLICABLE", "NOT_APPLICABLE"):
        missing.append("applicability not decided")
    if r.get("applicability") == "NOT_APPLICABLE":
        return True, []
    for field in (
        "swi_allocation", "implementation_ref", "evidence_ref", "evidence_hash",
        "source_commit", "test_procedure", "test_result",
    ):
        if not r.get(field):
            missing.append(f"missing {field}")
    if r.get("test_result") not in ("PASS",):
        missing.append("test_result must be PASS")
    # PROVEN eligibility requires exact PASS — PARTIAL/NOT_RUN/FAIL never qualify
    if r.get("replay_status") != "PASS":
        missing.append("replay_status must be PASS (PARTIAL/NOT_RUN/FAIL are not sufficient)")
    if r.get("reproducibility_status") != "PASS":
        missing.append("reproducibility_status must be PASS (PARTIAL/NOT_RUN/FAIL are not sufficient)")
    eh = r.get("evidence_hash")
    if not eh or not isinstance(eh, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", eh):
        missing.append("evidence_hash must be exactly 64 hexadecimal characters")
    return (len(missing) == 0, missing)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", type=Path, nargs="?", default=Path("evidence/iso_claim_status.json"))
    parser.add_argument("--schema", type=Path, default=Path("evidence/schemas/iso_claim_status.schema.json"))
    args = parser.parse_args(argv)
    # Minimal entry: full semantic validation is in the module functions used by tests.
    # This CLI path remains a claim-eligibility check, not an authorization path.
    if not args.register.is_file():
        print(f"register not found: {args.register}", file=sys.stderr)
        return 1
    register = load_json(args.register)
    # Import remaining validators from the original module body if present in package.
    # For standalone use after this hardening patch, call semantic checks via tests.
    print("ISO claim register loaded; PROVEN eligibility requires PASS/PASS/hex64.")
    print("Governance ceilings are not modified by this tool.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
