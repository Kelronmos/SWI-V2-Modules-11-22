#!/usr/bin/env python3
"""Validate the ISO claim-status register.

This is a claim-wording gate, not an authorization engine.
Exit 0 = register is schema-valid and semantically consistent.
Exit 1 = violation.
Does not set PROVEN, SEALED, or PRODUCTION_AUTHORIZED.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from jsonschema import Draft202012Validator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

ALLOWED_STATUS = {"RED", "AMBER", "GREEN", "NOT_ASSESSED", "NOT_APPLICABLE"}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_validate(register: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if HAS_JSONSCHEMA:
        v = Draft202012Validator(schema)
        for e in sorted(v.iter_errors(register), key=lambda x: list(x.path)):
            errors.append(f"{'/'.join(str(p) for p in e.path)}: {e.message}")
        return errors
    if register.get("schema_version") != "iso_claim_status_v1":
        errors.append("invalid schema_version")
    if "standards" not in register:
        errors.append("missing standards")
    if "governance" not in register:
        errors.append("missing governance")
    return errors


def semantic_validate(register: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    gov = register.get("governance") or {}
    if gov.get("PRODUCTION_AUTHORIZED") is True:
        errors.append(
            "governance.PRODUCTION_AUTHORIZED must remain false unless separate authorization process sets it"
        )
    if gov.get("ISO_CONFORMITY") == "ESTABLISHED":
        standards = register.get("standards") or []
        if not standards or any(s.get("gate_status") != "GREEN" for s in standards):
            errors.append("ISO_CONFORMITY=ESTABLISHED requires all standards GREEN")
        if any(s.get("critical_gaps") for s in standards):
            errors.append("ISO_CONFORMITY=ESTABLISHED not allowed while critical_gaps remain")

    for i, s in enumerate(register.get("standards") or []):
        prefix = f"standards[{i}] ({s.get('standard_id')})"
        status = s.get("gate_status")
        rung = s.get("claim_rung", 0)
        gaps = s.get("critical_gaps") or []
        review = s.get("independent_review")
        cert = s.get("certificate")
        scope = s.get("scope")
        mapping = s.get("clause_mapping_ref")
        evidence = s.get("evidence_hashes") or []
        tests = s.get("test_results_ref")

        if status not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid gate_status {status!r}")

        if status == "GREEN":
            if not scope:
                errors.append(f"{prefix}: GREEN requires non-empty scope")
            if not mapping:
                errors.append(f"{prefix}: GREEN requires clause_mapping_ref")
            if not evidence:
                errors.append(f"{prefix}: GREEN requires evidence_hashes")
            if not tests:
                errors.append(f"{prefix}: GREEN requires test_results_ref")
            if not review:
                errors.append(f"{prefix}: GREEN requires independent_review")
            if gaps:
                errors.append(f"{prefix}: GREEN requires critical_gaps to be empty")

        if status == "NOT_APPLICABLE":
            if not s.get("not_applicable_rationale"):
                errors.append(f"{prefix}: NOT_APPLICABLE requires not_applicable_rationale")

        if rung >= 2 and not review:
            errors.append(f"{prefix}: claim_rung>={rung} requires independent_review")

        if rung >= 4:
            if status != "GREEN":
                errors.append(f"{prefix}: claim_rung=4 requires gate_status=GREEN")
            if not cert or not cert.get("body") or not cert.get("number"):
                errors.append(f"{prefix}: claim_rung=4 requires certificate.body and certificate.number")

        if status == "GREEN" and rung < 1:
            errors.append(f"{prefix}: GREEN is inconsistent with claim_rung=0")

    return errors


def validate(register_path: Path, schema_path: Path) -> Tuple[bool, List[str]]:
    register = load_json(register_path)
    schema = load_json(schema_path)
    errors = schema_validate(register, schema)
    errors.extend(semantic_validate(register))
    return (len(errors) == 0, errors)


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate SWI ISO claim-status register")
    p.add_argument("register", nargs="?", default="evidence/iso_claim_status.json")
    p.add_argument("--schema", default="evidence/schemas/iso_claim_status.schema.json")
    args = p.parse_args(argv)
    ok, errors = validate(Path(args.register), Path(args.schema))
    if ok:
        print("PASS: ISO claim-status register is schema-valid and semantically consistent")
        print("NOTE: This does not establish ISO conformity or production authorization")
        return 0
    print("FAIL: ISO claim-status register violations:")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
