"""Institutional demonstration models — configuration/evidence, not authority engines."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


ALLOWED_AUTHORITY_STATES = frozenset(
    {"VALID", "EXPIRED", "REVOKED", "UNKNOWN", "PENDING", "CONFLICTING"}
)
ALLOWED_ACCESS_STATES = frozenset(
    {
        "ALLOWED",
        "BLOCKED",
        "WITHHELD",
        "ESCALATED",
        "AWAITING",
        "UNKNOWN",
        "UNDER_REVIEW",
        "RESOLVED",
        "REVOKED",
        "EXPIRED",
    }
)
CASE_STATES = frozenset(
    {
        "CREATED",
        "RECEIVED",
        "EVIDENCE_PENDING",
        "ADMITTED",
        "UNDER_REVIEW",
        "ALLOWED",
        "BLOCKED",
        "WITHHELD",
        "ESCALATED",
        "AWAITING",
        "RESOLVED",
        "RECONCILED",
        "ARCHIVED",
    }
)

INVALID_CASE_TRANSITIONS = frozenset(
    {
        ("BLOCKED", "EXECUTED"),
        ("UNKNOWN", "APPROVED"),
        ("WITHHELD", "DISCLOSED"),
        ("TESTED", "AUTHORIZED"),
        ("ESCALATED", "APPROVED"),
        ("CREATED", "ARCHIVED"),
        ("BLOCKED", "ALLOWED"),
    }
)


@dataclass
class OrganizationNode:
    node_id: str
    node_type: str
    jurisdiction: str
    parent_node: Optional[str] = None
    authority_scope: List[str] = field(default_factory=list)
    privacy_scope: List[str] = field(default_factory=list)
    allowed_actions: List[str] = field(default_factory=list)
    blocked_actions: List[str] = field(default_factory=list)
    escalation_targets: List[str] = field(default_factory=list)
    status: str = "ACTIVE"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuthorityRecord:
    authority_id: str
    actor_id: str
    role: str
    subject_scope: List[str]
    resource_scope: List[str]
    action_scope: List[str]
    jurisdiction: str
    authority_source: str
    valid_from: str
    valid_until: Optional[str]
    status: str
    human_authority_required: bool = False
    evidence_required: bool = True
    privacy_constraints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def is_usable(self) -> bool:
        return self.status == "VALID"


@dataclass
class AccessRequest:
    request_id: str
    actor: str
    subject: str
    resource: str
    requested_action: str
    purpose: str
    jurisdiction: str
    authority_ref: Optional[str] = None
    evidence_refs: List[str] = field(default_factory=list)
    privacy_constraints: List[str] = field(default_factory=list)
    policy_refs: List[str] = field(default_factory=list)
    law_refs: List[str] = field(default_factory=list)
    decision: Optional[str] = None
    reason: Optional[str] = None
    receipt_id: Optional[str] = None
    timestamp: Optional[str] = None
    source_commit: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Case:
    case_id: str
    subject_id: str
    created_by: str
    status: str = "CREATED"
    evidence_refs: List[str] = field(default_factory=list)
    authority_refs: List[str] = field(default_factory=list)
    request_ids: List[str] = field(default_factory=list)
    withhold_reasons: List[str] = field(default_factory=list)
    receipt_ids: List[str] = field(default_factory=list)
    jurisdiction: str = "example"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Receipt:
    receipt_id: str
    junction: str
    case_id: Optional[str]
    request_id: Optional[str]
    actor_id: str
    authority_ref: Optional[str]
    evidence_refs: List[str]
    status: str
    reason: str
    source_tip: str
    timestamp: str
    integrity_hash: str = ""
    previous_receipt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class WithholdRecord:
    withhold_id: str
    case_id: str
    what: str
    why: str
    rule: str
    requester: str
    authorized_reviewer: Optional[str]
    release_condition: str
    evidence_refs: List[str]
    authority_refs: List[str]
    receipt_id: str
    status: str = "WITHHELD"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EscalationRecord:
    escalation_id: str
    case_id: str
    from_authority: str
    to_authority: str
    reason: str
    trigger: str
    evidence_refs: List[str]
    authority_refs: List[str]
    privacy_constraints: List[str]
    status: str
    receipt_id: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
