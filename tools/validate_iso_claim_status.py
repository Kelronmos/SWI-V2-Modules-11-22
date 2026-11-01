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
    if not isinstance(register.get("standards"), list) or not register.get("standards"):
        errors.append("standards must be a non-empty array")
    else:
        for i, s in enumerate(register["standards"]):
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
        v = Draft202012Validator(schema)
        for e in sorted(v.iter_errors(register), key=lambda x: list(x.path)):
            errors.append(f"{'/'.join(str(p) for p in e.path)}: {e.message}")
        return errors
    return _fallback_schema_validate(register)


def _review_errors(prefix: str, review: Any) -> List[str]:
    errors: List[str] = []
    if review is None:
        return errors
    if not isinstance(review, dict):
        errors.append(f"{prefix}: independent_review must be object or null")
        return errors
    for field in REVIEW_REQUIRED_FIELDS:
        if not review.get(field):
            errors.append(f"{prefix}: independent_review missing {field}")
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
    # PROVEN eligibility requires exact PASS — PARTIAL/NOT_RUN/FAIL never qualify
    if r.get("replay_status") != "PASS":
        missing.append("replay_status must be PASS (PARTIAL/NOT_RUN/FAIL are not sufficient)")
    if r.get("reproducibility_status") != "PASS":
        missing.append("reproducibility_status must be PASS (PARTIAL/NOT_RUN/FAIL are not sufficient)")
    eh = r.get("evidence_hash")
    if not eh or not isinstance(eh, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", eh):
        missing.append("evidence_hash must be exactly 64 hexadecimal characters")
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
    for i, s in enumerate(register.get("standards") or []):
        prefix = f"standards[{i}] ({s.get('standard_id')})"
        status = s.get("gate_status")
        rung = int(s.get("claim_rung", 0))
        if status not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid gate_status")
        if status == "NOT_APPLICABLE" and not (s.get("not_applicable_rationale") or "").strip():
            errors.append(f"{prefix}: NOT_APPLICABLE requires not_applicable_rationale")
        if status == "GREEN":
            if not (s.get("clause_mapping_ref") or "").strip():
                errors.append(f"{prefix}: GREEN requires clause_mapping_ref")
            if not (s.get("evidence_hashes") or []):
                errors.append(f"{prefix}: GREEN requires evidence_hashes")
            if not (s.get("test_results_ref") or "").strip():
                errors.append(f"{prefix}: GREEN requires test_results_ref")
            if s.get("critical_gaps"):
                errors.append(f"{prefix}: GREEN cannot have critical_gaps")
            errors.extend(_review_errors(prefix, s.get("independent_review"))
                          if s.get("independent_review") is None
                          else _review_errors(prefix, s.get("independent_review")))
            if s.get("independent_review") is None:
                errors.append(f"{prefix}: GREEN requires independent_review")
        if rung >= 4:
            if status != "GREEN":
                errors.append(f"{prefix}: claim_rung>=4 requires GREEN")
            if not s.get("certificate"):
                errors.append(f"{prefix}: claim_rung>=4 requires certificate")
        proven_reqs = 0
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
                proven_reqs += 1
                if r.get("claim_source") != "ENGINE":
                    errors.append(f"{rp}: PROVEN requires claim_source=ENGINE (no manual promotion)")
                if r.get("applicability") != "APPLICABLE":
                    errors.append(f"{rp}: PROVEN requires applicability=APPLICABLE")
                ok, missing = requirement_claim_eligible(r)
                if not ok:
                    errors.append(f"{rp}: PROVEN without eligibility: {', '.join(missing)}")
            if cs == "NOT_PROVEN" and r.get("claim_source") == "MANUAL_PROVEN":
                errors.append(f"{rp}: invalid claim_source MANUAL_PROVEN")
        if status == "GREEN" and proven_reqs < 1:
            errors.append(f"{prefix}: GREEN with zero PROVEN requirements is inconsistent")
    return errors


def evaluate_requirement_claims(register: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"requirements": []}
    for s in register.get("standards") or []:
        for r in s.get("requirements") or []:
            eligible, missing = requirement_claim_eligible(r)
            out["requirements"].append({
                "standard_id": s.get("standard_id"),
                "requirement_id": r.get("requirement_id"),
                "claim_status": r.get("claim_status"),
                "eligible_for_proven": eligible and r.get("applicability") == "APPLICABLE",
                "missing": missing,
            })
    return out


def validate(register_path: Path, schema_path: Path) -> Tuple[bool, List[str]]:
    register = load_json(register_path)
    schema = load_json(schema_path) if schema_path.is_file() else {}
    errors: List[str] = []
    errors.extend(schema_validate(register, schema))
    errors.extend(semantic_validate(register))
    return (len(errors) == 0, errors)


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("register", type=Path, nargs="?", default=Path("evidence/iso_claim_status.json"))
    p.add_argument("--schema", type=Path, default=Path("evidence/schemas/iso_claim_status.schema.json"))
    p.add_argument("--evaluate", action="store_true", help="print requirement eligibility JSON")
    args = p.parse_args(argv)
    reg_path = args.register
    if not HAS_JSONSCHEMA:
        print("WARN: jsonschema not installed; using LIMITED structural fallback (not full JSON Schema)", file=sys.stderr)
    if args.evaluate:
        print(json.dumps(evaluate_requirement_claims(load_json(reg_path)), indent=2))
        return 0
    ok, errors = validate(reg_path, args.schema)
    if not ok:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("ISO claim register consistent (eligibility gate only; not authorization).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
