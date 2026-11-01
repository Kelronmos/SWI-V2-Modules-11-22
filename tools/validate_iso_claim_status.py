#!/usr/bin/env python3
"""Validate the ISO claim-status register.

Claim-wording gate only — not an authorization engine.
Exit 0 = schema-valid and semantically consistent.
Exit 1 = violation.
Does not set PROVEN, SEALED, or PRODUCTION_AUTHORIZED.

JSON Schema Draft 2020-12 is preferred via jsonschema. If unavailable,
a complete structural fallback runs (not a weak presence-only check).
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
    Draft202012Validator = None  # type: ignore

ALLOWED_STATUS = {"RED", "AMBER", "GREEN", "NOT_ASSESSED", "NOT_APPLICABLE"}
ALLOWED_CONFORMITY = {"NOT_ESTABLISHED", "UNDER_ASSESSMENT", "ESTABLISHED"}
REVIEW_REQUIRED_FIELDS = ("reviewer", "date", "report_hash", "outcome", "scope")
HASH_LEN = 64


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _fallback_schema_validate(register: Dict[str, Any]) -> List[str]:
    """Complete structural checks when jsonschema is unavailable."""
    errors: List[str] = []
    if register.get("schema_version") != "iso_claim_status_v1":
        errors.append("schema_version must be iso_claim_status_v1")
    if not isinstance(register.get("updated_utc"), str) or len(register.get("updated_utc") or "") < 10:
        errors.append("updated_utc must be a string (ISO-8601-like)")
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
    standards = register.get("standards")
    if not isinstance(standards, list) or not standards:
        errors.append("standards must be a non-empty array")
        return errors
    for i, s in enumerate(standards):
        prefix = f"standards[{i}]"
        if not isinstance(s, dict):
            errors.append(f"{prefix} must be object")
            continue
        for req in ("standard_id", "edition", "gate_status", "claim_rung", "critical_gaps"):
            if req not in s:
                errors.append(f"{prefix} missing required field {req}")
        if s.get("gate_status") not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid gate_status")
        if not isinstance(s.get("claim_rung"), int) or not (0 <= s.get("claim_rung", -1) <= 4):
            errors.append(f"{prefix}: claim_rung must be integer 0..4")
        if not isinstance(s.get("critical_gaps"), list):
            errors.append(f"{prefix}: critical_gaps must be array")
        for h in s.get("evidence_hashes") or []:
            if not isinstance(h, str) or len(h) != HASH_LEN or any(c not in "0123456789abcdef" for c in h):
                errors.append(f"{prefix}: evidence_hashes entries must be 64-char lowercase hex")
    return errors


def schema_validate(register: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    if HAS_JSONSCHEMA:
        errors: List[str] = []
        validator = Draft202012Validator(schema)
        for e in sorted(validator.iter_errors(register), key=lambda x: list(x.path)):
            errors.append(f"{'/'.join(str(p) for p in e.path)}: {e.message}")
        return errors
    return _fallback_schema_validate(register)


def _review_errors(prefix: str, review: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(review, dict):
        return [f"{prefix}: independent_review must be an object"]
    for field in REVIEW_REQUIRED_FIELDS:
        val = review.get(field)
        if val is None or (isinstance(val, str) and not str(val).strip()):
            errors.append(f"{prefix}: independent_review.{field} is required")
    outcome = review.get("outcome")
    if outcome is not None and outcome not in (
        "SUPPORTS_CLAIM", "PARTIAL", "DOES_NOT_SUPPORT", "INCONCLUSIVE",
    ):
        errors.append(
            f"{prefix}: independent_review.outcome must be one of "
            "SUPPORTS_CLAIM|PARTIAL|DOES_NOT_SUPPORT|INCONCLUSIVE"
        )
    if "independence_attestation" not in review:
        errors.append(f"{prefix}: independent_review.independence_attestation is required")
    return errors


def semantic_validate(register: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    gov = register.get("governance") or {}
    if gov.get("PRODUCTION_AUTHORIZED") is True:
        errors.append(
            "governance.PRODUCTION_AUTHORIZED must remain false unless a separate "
            "authorization process sets it outside this register"
        )
    standards = register.get("standards") or []
    if gov.get("ISO_CONFORMITY") == "ESTABLISHED":
        if not standards:
            errors.append("ISO_CONFORMITY=ESTABLISHED requires at least one standard entry")
        for i, s in enumerate(standards):
            prefix = f"standards[{i}] ({s.get('standard_id')})"
            if s.get("gate_status") != "GREEN":
                errors.append(f"ISO_CONFORMITY=ESTABLISHED requires {prefix} gate_status=GREEN")
            if int(s.get("claim_rung", 0)) < 3:
                errors.append(
                    f"ISO_CONFORMITY=ESTABLISHED requires {prefix} claim_rung>=3 "
                    "(organisational control support); certification is claim_rung=4"
                )
            if s.get("critical_gaps"):
                errors.append(
                    f"ISO_CONFORMITY=ESTABLISHED not allowed while {prefix} has critical_gaps"
                )
            review = s.get("independent_review")
            if not review:
                errors.append(f"ISO_CONFORMITY=ESTABLISHED requires {prefix} independent_review")
            else:
                errors.extend(_review_errors(prefix, review))
                if isinstance(review, dict) and review.get("outcome") not in (
                    "SUPPORTS_CLAIM", "PARTIAL",
                ):
                    errors.append(
                        f"ISO_CONFORMITY=ESTABLISHED requires {prefix} "
                        "independent_review.outcome in SUPPORTS_CLAIM|PARTIAL"
                    )
    for i, s in enumerate(standards):
        if not isinstance(s, dict):
            continue
        prefix = f"standards[{i}] ({s.get('standard_id')})"
        status = s.get("gate_status")
        try:
            rung = int(s.get("claim_rung", 0))
        except (TypeError, ValueError):
            errors.append(f"{prefix}: claim_rung must be integer 0..4")
            continue
        gaps = s.get("critical_gaps") or []
        review = s.get("independent_review")
        cert = s.get("certificate")
        scope = s.get("scope")
        mapping = s.get("clause_mapping_ref")
        evidence = s.get("evidence_hashes") or []
        tests = s.get("test_results_ref")
        if status not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid gate_status {status!r}")
        if not (0 <= rung <= 4):
            errors.append(f"{prefix}: claim_rung must be integer 0..4")
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
            else:
                errors.extend(_review_errors(prefix, review))
            if gaps:
                errors.append(f"{prefix}: GREEN requires critical_gaps to be empty")
            if rung < 1:
                errors.append(f"{prefix}: GREEN is inconsistent with claim_rung=0")
        if status == "NOT_APPLICABLE":
            if not s.get("not_applicable_rationale"):
                errors.append(f"{prefix}: NOT_APPLICABLE requires not_applicable_rationale")
        if rung >= 2:
            if not review:
                errors.append(f"{prefix}: claim_rung>={rung} requires independent_review")
            else:
                errors.extend(_review_errors(prefix, review))
        if rung >= 4:
            if status != "GREEN":
                errors.append(f"{prefix}: claim_rung=4 requires gate_status=GREEN")
            if not isinstance(cert, dict) or not cert.get("body") or not cert.get("number"):
                errors.append(
                    f"{prefix}: claim_rung=4 requires certificate.body and certificate.number"
                )
            if isinstance(cert, dict) and not cert.get("scope"):
                errors.append(f"{prefix}: claim_rung=4 requires certificate.scope")
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
    if not HAS_JSONSCHEMA:
        print(
            "WARN: jsonschema not installed; using complete structural fallback validator",
            file=sys.stderr,
        )
    ok, errors = validate(Path(args.register), Path(args.schema))
    if ok:
        print("PASS: ISO claim-status register is schema-valid and semantically consistent")
        print("NOTE: This does not establish ISO conformity or production authorization")
        if not HAS_JSONSCHEMA:
            print("NOTE: Prefer installing jsonschema for Draft 2020-12 validation")
        return 0
    print("FAIL: ISO claim-status register violations:")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
