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
    if r.get("replay_status") != "PASS":
        missing.append("replay_status must be PASS (PARTIAL/NOT_RUN/FAIL are not sufficient)")
    if r.get("reproducibility_status") != "PASS":
        missing.append("reproducibility_status must be PASS (PARTIAL/NOT_RUN/FAIL are not sufficient)")
    eh = r.get("evidence_hash")
    if not eh or not isinstance(eh, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", eh):
        missing.append("evidence_hash must be exactly 64 hexadecimal characters")
    return (len(missing) == 0, missing)


def _fallback_schema_validate(register: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if register.get("schema_version") != "iso_claim_status_v1":
        errors.append("schema_version must be iso_claim_status_v1")
    gov = register.get("governance")
    if not isinstance(gov, dict):
        errors.append("governance must be an object")
    else:
        for key in ("PROVEN", "SEALED", "PRODUCTION_AUTHORIZED"):
            if key not in gov:
                errors.append(f"governance missing {key}")
            elif not isinstance(gov[key], bool):
                errors.append(f"governance.{key} must be boolean")
        if gov.get("ISO_CONFORMITY") not in ALLOWED_CONFORMITY:
            errors.append("governance.ISO_CONFORMITY invalid")
    if not isinstance(register.get("standards"), list):
        errors.append("standards must be an array")
    return errors


def schema_validate(register: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    if HAS_JSONSCHEMA:
        errors: List[str] = []
        v = Draft202012Validator(schema)
        for e in sorted(v.iter_errors(register), key=lambda x: list(x.path)):
            errors.append(f"{'/'.join(str(p) for p in e.path)}: {e.message}")
        return errors
    return _fallback_schema_validate(register)


def semantic_validate(register: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    gov = register.get("governance") or {}
    if gov.get("PRODUCTION_AUTHORIZED") is True:
        errors.append(
            "governance.PRODUCTION_AUTHORIZED must remain false unless separate authorization process sets it"
        )
    if gov.get("ISO_CONFORMITY") == "NOT_ESTABLISHED":
        if gov.get("CONFORMITY_CLAIM", "SEALED") != "SEALED":
            errors.append("when ISO_CONFORMITY=NOT_ESTABLISHED, CONFORMITY_CLAIM must be SEALED")
    for i, s in enumerate(register.get("standards") or []):
        prefix = f"standards[{i}] ({s.get('standard_id')})"
        status = s.get("gate_status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid gate_status")
        for j, r in enumerate(s.get("requirements") or []):
            rp = f"{prefix}.requirements[{j}] ({r.get('requirement_id')})"
            cs = r.get("claim_status")
            if cs not in ALLOWED_REQ_CLAIM:
                errors.append(f"{rp}: invalid claim_status")
            if r.get("replay_status") not in ALLOWED_REPLAY:
                errors.append(f"{rp}: invalid replay_status")
            if r.get("reproducibility_status") not in ALLOWED_REPLAY:
                errors.append(f"{rp}: invalid reproducibility_status")
            if cs == "PROVEN":
                if r.get("claim_source") != "ENGINE":
                    errors.append(f"{rp}: PROVEN requires claim_source=ENGINE (no manual promotion)")
                ok, missing = requirement_claim_eligible(r)
                if not ok:
                    errors.append(f"{rp}: PROVEN without eligibility: {', '.join(missing)}")
    return errors


def validate(register_path: Path, schema_path: Path) -> Tuple[bool, List[str]]:
    register = load_json(register_path)
    schema = load_json(schema_path) if schema_path.is_file() else {}
    errors = schema_validate(register, schema) + semantic_validate(register)
    return (len(errors) == 0, errors)


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("register", type=Path, nargs="?", default=Path("evidence/iso_claim_status.json"))
    p.add_argument("--schema", type=Path, default=Path("evidence/schemas/iso_claim_status.schema.json"))
    args = p.parse_args(argv)
    ok, errors = validate(args.register, args.schema)
    if not ok:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("ISO claim register consistent (eligibility gate only; not authorization).")
    if not HAS_JSONSCHEMA:
        print("NOTE: jsonschema not installed; used limited fallback structural check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
