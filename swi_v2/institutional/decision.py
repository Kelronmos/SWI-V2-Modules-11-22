"""Access decision — pure evaluation; does not authorize production or invent H."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence

from .models import (
    AccessRequest,
    AuthorityRecord,
    ALLOWED_ACCESS_STATES,
    INVALID_CASE_TRANSITIONS,
    Receipt,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def find_authority(
    authorities: Sequence[AuthorityRecord],
    actor: str,
    subject: str,
    resource: str,
    action: str,
    jurisdiction: str,
) -> Optional[AuthorityRecord]:
    for a in authorities:
        if a.actor_id != actor:
            continue
        if a.status != "VALID":
            continue
        if a.jurisdiction not in (jurisdiction, "*"):
            continue
        if subject not in a.subject_scope and "*" not in a.subject_scope:
            continue
        if resource not in a.resource_scope and "*" not in a.resource_scope:
            continue
        if action not in a.action_scope and "*" not in a.action_scope:
            continue
        return a
    return None


def evaluate_access(
    request: AccessRequest,
    authorities: Sequence[AuthorityRecord],
    *,
    evidence: Optional[Sequence[Mapping[str, Any]]] = None,
    law: Optional[Sequence[str]] = None,
    governance: Optional[Sequence[str]] = None,
    security: Optional[Sequence[str]] = None,
    human: Optional[Sequence[str]] = None,
    constraints: Optional[Sequence[str]] = None,
    source_commit: str = "",
    previous_receipt: Optional[str] = None,
) -> Dict[str, Any]:
    """Evaluate one access request. Never infers authority from role name alone."""
    evidence = list(evidence or [])
    law = list(law or [])
    governance = list(governance or [])
    security = list(security or [])
    human = list(human or [])
    constraints = list(constraints or request.law_refs or ["access_constraint"])

    reasons: List[str] = []
    auth = None
    if request.authority_ref:
        for a in authorities:
            if a.authority_id == request.authority_ref:
                auth = a
                break
    if auth is None:
        auth = find_authority(
            authorities,
            request.actor,
            request.subject,
            request.resource,
            request.requested_action,
            request.jurisdiction,
        )

    if auth is None:
        decision = "BLOCKED"
        reasons.append("NO AUTHORITY matching actor/subject/resource/action/jurisdiction")
    elif auth.status == "EXPIRED":
        decision = "EXPIRED"
        reasons.append("authority EXPIRED")
    elif auth.status == "REVOKED":
        decision = "REVOKED"
        reasons.append("authority REVOKED")
    elif auth.status in ("UNKNOWN", "PENDING", "CONFLICTING"):
        decision = "UNKNOWN" if auth.status == "UNKNOWN" else "AWAITING"
        reasons.append(f"authority status={auth.status}")
    elif not auth.is_usable():
        decision = "BLOCKED"
        reasons.append(f"authority not usable: {auth.status}")
    else:
        decision = "ALLOWED"

    if auth and decision == "ALLOWED":
        if request.resource in ("student_private_history", "cross_student_record"):
            if "private_history" not in (auth.resource_scope if auth else []):
                decision = "WITHHELD"
                reasons.append("WITHHELD_PRIVACY: private/cross resource outside authority resource_scope")

    if auth and auth.human_authority_required and not human:
        if decision in ("ALLOWED",):
            decision = "AWAITING"
            reasons.append("AWAITING HUMAN AUTHORITY: human_authority_required and H empty")

    if auth and auth.evidence_required and not evidence and decision == "ALLOWED":
        decision = "BLOCKED"
        reasons.append("EVIDENCE MISSING: evidence_required and E(a) empty")

    e_exists = len(evidence) > 0
    e_adequate = False
    if e_exists:
        e_adequate = all(
            str(item.get("relevance", "")).upper() == "PASS"
            and str(item.get("freshness", "")).upper() == "PASS"
            and str(item.get("scope", "")).upper() == "PASS"
            and str(item.get("provenance", "")).upper() == "PASS"
            and str(item.get("integrity", "")).upper() == "PASS"
            for item in evidence
        )
        if not e_adequate and decision == "ALLOWED":
            decision = "BLOCKED"
            reasons.append("evidence exists but NOT adequate (relevance/freshness/scope/provenance/integrity)")

    s9_block = False
    try:
        from swi_v2.s9.evaluator import evaluate_s9

        s9_action = {
            "action_id": request.request_id,
            "constraints": constraints,
            "law": law,
            "governance": governance,
            "security": security,
            "human": human,
            "evidence": evidence,
            "authority": {
                "required": bool(auth and auth.human_authority_required),
                "present": bool(human),
            },
        }
        s9 = evaluate_s9(s9_action)
        if s9.system_result in ("BLOCKED", "UNRESOLVED", "NOT_PROVEN") and decision == "ALLOWED":
            if not law or not governance or not security or not human:
                decision = "BLOCKED" if s9.system_result == "BLOCKED" else "AWAITING"
                reasons.append(f"S9 gate: {s9.system_result}; {'; '.join(s9.reasons)}")
                s9_block = True
        s9_summary = {
            "system_result": s9.system_result,
            "documented_equation_result": s9.documented_equation_result,
            "evidence_adequacy_result": s9.evidence_adequacy_result,
            "s9_proven": False,
            "reasons": s9.reasons,
        }
    except Exception as exc:
        s9_summary = {"available": False, "note": str(exc), "s9_proven": False}

    if decision not in ALLOWED_ACCESS_STATES:
        decision = "UNKNOWN"
        reasons.append("normalized unknown decision state")

    receipt_body = {
        "request_id": request.request_id,
        "actor": request.actor,
        "subject": request.subject,
        "resource": request.resource,
        "action": request.requested_action,
        "decision": decision,
        "reasons": reasons,
        "authority_id": auth.authority_id if auth else None,
        "source_commit": source_commit,
    }
    rid = f"RCPT-{_hash(receipt_body)[:16]}"
    receipt = Receipt(
        receipt_id=rid,
        junction="ACCESS_DECISION",
        case_id=None,
        request_id=request.request_id,
        actor_id=request.actor,
        authority_ref=auth.authority_id if auth else None,
        evidence_refs=list(request.evidence_refs),
        status=decision,
        reason="; ".join(reasons) or decision,
        source_tip=source_commit or "UNBOUND",
        timestamp=_now(),
        integrity_hash=_hash(receipt_body),
        previous_receipt=previous_receipt,
    )

    return {
        "decision": decision,
        "reasons": reasons,
        "authority": auth.to_dict() if auth else None,
        "e_exists": e_exists,
        "e_adequate": e_adequate,
        "s9": s9_summary,
        "s9_tightened": s9_block,
        "receipt": receipt.to_dict(),
        "production_authorized": False,
        "s9_proven": False,
    }


def case_transition_allowed(from_status: str, to_status: str) -> bool:
    if (from_status, to_status) in INVALID_CASE_TRANSITIONS:
        return False
    if to_status == "EXECUTED":
        return False
    if to_status == "APPROVED":
        return False
    if to_status == "DISCLOSED" and from_status == "WITHHELD":
        return False
    return True
