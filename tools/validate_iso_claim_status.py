#!/usr/bin/env python3
"""Validate the ISO claim-status register (evidence-bound claims).

Claim-wording / claim-eligibility gate — not an authorization engine.
Exit 0 = consistent. Exit 1 = violation.
Does not set PROVEN/SEALED/PRODUCTION_AUTHORIZED for SWI execution.
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
ALLOWED_CONFORMITY_CLAIM = {"SEALED", "OPEN", "WITHDRAWN"}
ALLOWED_REQ_CLAIM = {"SEALED", "PROVEN", "NOT_PROVEN", "NOT_APPLICABLE"}
ALLOWED_REPLAY = {"NOT_RUN", "PASS", "FAIL", "PARTIAL"}
REVIEW_REQUIRED_FIELDS = ("reviewer", "date", "report_hash", "outcome", "scope")
HASH_LEN = 64


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _fallback_schema_validate(register: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if register.get("schema_version") != "iso_claim_status_v1":
        errors.append("schema_version must be iso_claim_status_v1")
    if not isinstance(register.get("updated_utc"), str) or len(register.get("updated_utc") or "") < 10:
        errors.append("updated_utc must be a string")
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
        cc = gov.get("CONFORMITY_CLAIM")
        if cc is not None and cc not in ALLOWED_CONFORMITY_CLAIM:
            errors.append("governance.CONFORMITY_CLAIM invalid")
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
                errors.append(f"{prefix} missing {req}")
        if s.get("gate_status") not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid gate_status")
        if not isinstance(s.get("claim_rung"), int) or not (0 <= s.get("claim_rung", -1) <= 4):
            errors.append(f"{prefix}: claim_rung must be 0..4")
        reqs = s.get("requirements")
        if reqs is not None and not isinstance(reqs, list):
            errors.append(f"{prefix}: requirements must be array")
    return errors


def schema_validate(register: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    if HAS_JSONSCHEMA:
        errors: List[str] = []
        try:
            validator = Draft202012Validator(schema)
            for e in sorted(validator.iter_errors(register), key=lambda x: list(x.path)):
                errors.append(f"{'/'.join(str(p) for p in e.path)}: {e.message}")
        except Exception as ex:
            errors.append(f"schema validation error: {ex}")
        errors.extend(_fallback_schema_validate(register))
        return list(dict.fromkeys(errors))
    return _fallback_schema_validate(register)


def _review_errors(prefix: str, review: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(review, dict):
        return [f"{prefix}: independent_review must be an object"]
    for field in REVIEW_REQUIRED_FIELDS:
        val = review.get(field)
        if val is None or (isinstance(val, str) and not str(val).strip()):
            errors.append(f"{prefix}: independent_review.{field} is required")
    if "independence_attestation" not in review:
        errors.append(f"{prefix}: independent_review.independence_attestation is required")
    outcome = review.get("outcome")
    if outcome is not None and outcome not in (
        "SUPPORTS_CLAIM", "PARTIAL", "DOES_NOT_SUPPORT", "INCONCLUSIVE",
    ):
        errors.append(f"{prefix}: independent_review.outcome invalid")
    return errors


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
    if r.get("replay_status") not in ("PASS", "PARTIAL"):
        missing.append("replay_status must be PASS or PARTIAL")
    if r.get("reproducibility_status") not in ("PASS", "PARTIAL"):
        missing.append("reproducibility_status must be PASS or PARTIAL")
    eh = r.get("evidence_hash")
    if eh and (not isinstance(eh, str) or len(eh) != HASH_LEN):
        missing.append("evidence_hash must be 64-char hex")
    return (len(missing) == 0, missing)


def semantic_validate(register: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    gov = register.get("governance") or {}
    if gov.get("PRODUCTION_AUTHORIZED") is True:
        errors.append(
            "governance.PRODUCTION_AUTHORIZED must remain false unless separate authorization process sets it"
        )
    if gov.get("ISO_CONFORMITY") == "NOT_ESTABLISHED":
        cc = gov.get("CONFORMITY_CLAIM", "SEALED")
        if cc != "SEALED":
            errors.append("when ISO_CONFORMITY=NOT_ESTABLISHED, CONFORMITY_CLAIM must be SEALED")
    if gov.get("ISO_CONFORMITY") == "ESTABLISHED":
        for i, s in enumerate(register.get("standards") or []):
            prefix = f"standards[{i}] ({s.get('standard_id')})"
            if s.get("gate_status") != "GREEN":
                errors.append(f"ISO_CONFORMITY=ESTABLISHED requires {prefix} GREEN")
            if int(s.get("claim_rung", 0)) < 3:
                errors.append(f"ISO_CONFORMITY=ESTABLISHED requires {prefix} claim_rung>=3")
            if s.get("critical_gaps"):
                errors.append(f"ISO_CONFORMITY=ESTABLISHED blocked by {prefix} critical_gaps")
            review = s.get("independent_review")
            if not review:
                errors.append(f"ISO_CONFORMITY=ESTABLISHED requires {prefix} independent_review")
            else:
                errors.extend(_review_errors(prefix, review))
    for i, s in enumerate(register.get("standards") or []):
        if not isinstance(s, dict):
            continue
        prefix = f"standards[{i}] ({s.get('standard_id')})"
        status = s.get("gate_status")
        try:
            rung = int(s.get("claim_rung", 0))
        except (TypeError, ValueError):
            errors.append(f"{prefix}: invalid claim_rung")
            continue
        gaps = s.get("critical_gaps") or []
        review = s.get("independent_review")
        cert = s.get("certificate")
        if status not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid gate_status")
        if not (0 <= rung <= 4):
            errors.append(f"{prefix}: claim_rung must be 0..4")
        if status == "GREEN":
            if not s.get("scope"):
                errors.append(f"{prefix}: GREEN requires scope")
            if not s.get("clause_mapping_ref"):
                errors.append(f"{prefix}: GREEN requires clause_mapping_ref")
            if not (s.get("evidence_hashes") or []):
                errors.append(f"{prefix}: GREEN requires evidence_hashes")
            if not s.get("test_results_ref"):
                errors.append(f"{prefix}: GREEN requires test_results_ref")
            if not review:
                errors.append(f"{prefix}: GREEN requires independent_review")
            else:
                errors.extend(_review_errors(prefix, review))
            if gaps:
                errors.append(f"{prefix}: GREEN requires empty critical_gaps")
            if rung < 1:
                errors.append(f"{prefix}: GREEN inconsistent with claim_rung=0")
        if status == "NOT_APPLICABLE" and not s.get("not_applicable_rationale"):
            errors.append(f"{prefix}: NOT_APPLICABLE requires rationale")
        if rung >= 2:
            if not review:
                errors.append(f"{prefix}: claim_rung>={rung} requires independent_review")
            else:
                errors.extend(_review_errors(prefix, review))
        if rung >= 4:
            if status != "GREEN":
                errors.append(f"{prefix}: claim_rung=4 requires GREEN")
            if not isinstance(cert, dict) or not cert.get("body") or not cert.get("number"):
                errors.append(f"{prefix}: claim_rung=4 requires certificate body/number")
            if isinstance(cert, dict) and not cert.get("scope"):
                errors.append(f"{prefix}: claim_rung=4 requires certificate.scope")
        proven_reqs = 0
        for j, r in enumerate(s.get("requirements") or []):
            if not isinstance(r, dict):
                errors.append(f"{prefix}.requirements[{j}] must be object")
                continue
            rp = f"{prefix}.requirements[{j}] ({r.get('requirement_id')})"
            cs = r.get("claim_status")
            if cs not in ALLOWED_REQ_CLAIM:
                errors.append(f"{rp}: invalid claim_status")
            if r.get("replay_status") not in ALLOWED_REPLAY:
                errors.append(f"{rp}: invalid replay_status")
            if r.get("reproducibility_status") not in ALLOWED_REPLAY:
                errors.append(f"{rp}: invalid reproducibility_status")
            if cs == "PROVEN":
                proven_reqs += 1
                if r.get("claim_source") != "ENGINE":
                    errors.append(f"{rp}: PROVEN requires claim_source=ENGINE (no manual promotion)")
                ok, missing = requirement_claim_eligible(r)
                if not ok:
                    errors.append(f"{rp}: PROVEN without eligibility: {', '.join(missing)}")
            if cs == "NOT_PROVEN" and r.get("claim_source") == "MANUAL_PROVEN":
                errors.append(f"{rp}: invalid claim_source MANUAL_PROVEN")
        if status == "GREEN" and proven_reqs < 1:
            errors.append(f"{prefix}: GREEN with zero PROVEN requirements is inconsistent")
        display = s.get("display")
        if display is not None and not display.get("visible", True):
            errors.append(f"{prefix}: allocated standard must remain visible (display.visible)")
    return errors


def evaluate_requirement_claims(register: Dict[str, Any]) -> Dict[str, Any]:
    out = {"standards": []}
    for s in register.get("standards") or []:
        rows = []
        for r in s.get("requirements") or []:
            eligible, missing = requirement_claim_eligible(r)
            rows.append({
                "requirement_id": r.get("requirement_id"),
                "recorded_claim_status": r.get("claim_status"),
                "eligible_for_proven": eligible and r.get("applicability") == "APPLICABLE",
                "missing": missing,
                "would_seal": not eligible,
            })
        out["standards"].append({
            "standard_id": s.get("standard_id"),
            "gate_status": s.get("gate_status"),
            "requirements": rows,
        })
    return out


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
    p.add_argument("--evaluate-claims", action="store_true")
    args = p.parse_args(argv)
    if not HAS_JSONSCHEMA:
        print("WARN: jsonschema not installed; using complete structural fallback", file=sys.stderr)
    reg_path = Path(args.register)
    ok, errors = validate(reg_path, Path(args.schema))
    if args.evaluate_claims:
        print(json.dumps(evaluate_requirement_claims(load_json(reg_path)), indent=2))
    if ok:
        print("PASS: ISO claim-status register is consistent")
        print("NOTE: does not establish ISO conformity or production authorization")
        print("NOTE: CONFORMITY_CLAIM remains SEALED while ISO_CONFORMITY=NOT_ESTABLISHED")
        return 0
    print("FAIL: ISO claim-status register violations:")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
