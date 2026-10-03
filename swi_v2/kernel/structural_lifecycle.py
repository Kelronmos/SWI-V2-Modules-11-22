"""SWI structural maturity + continuous review lifecycle (kernel helper).

STATUS: IMPLEMENTATION CANDIDATE — TESTED only when suite is green.
PROVEN: NO | SEALED: NO | PRODUCTION_AUTHORIZED: NO

Independent dimensions — never collapse into one GREEN:
  FUNDING | OPERATING | STRUCTURAL | EVIDENCE | TEST | AUTHORITY
  PEOPLE_READINESS | REVALIDATION | SEAL | PRODUCTION_AUTHORIZATION

99.9% = REVIEW THRESHOLD only (not authorization).
100% structural completeness ≠ automatic production authorization.
SELF_ANALYSIS ≠ AUTHORITY.
AUTHORITY_REQUEST cannot self-approve.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, FrozenSet, Iterable, Optional


class OperatingStatus(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"
    PILOT = "PILOT"
    CONTROLLED_OPERATION = "CONTROLLED_OPERATION"
    PRODUCTION_OPERATING = "PRODUCTION_OPERATING"
    STRUCTURAL_REVIEW = "STRUCTURAL_REVIEW"


class StructuralStatus(str, Enum):
    STRUCTURE_UNKNOWN = "STRUCTURE_UNKNOWN"
    STRUCTURE_BUILDING = "STRUCTURE_BUILDING"
    STRUCTURE_TESTED = "STRUCTURE_TESTED"
    STRUCTURE_REVIEWING = "STRUCTURE_REVIEWING"
    STRUCTURE_99_9_REVIEW_GATE = "STRUCTURE_99_9_REVIEW_GATE"
    STRUCTURE_REQUIRES_REPAIR = "STRUCTURE_REQUIRES_REPAIR"
    STRUCTURE_REVALIDATING = "STRUCTURE_REVALIDATING"
    STRUCTURE_COMPLETE = "STRUCTURE_COMPLETE"


class AuthorityRequestStatus(str, Enum):
    AUTHORITY_REQUIRED = "AUTHORITY_REQUIRED"
    AUTHORITY_PENDING = "AUTHORITY_PENDING"
    AUTHORITY_GRANTED = "AUTHORITY_GRANTED"
    AUTHORITY_REJECTED = "AUTHORITY_REJECTED"
    AUTHORITY_EXPIRED = "AUTHORITY_EXPIRED"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"


class ReadinessStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    NOT_READY = "NOT_READY"
    TRAINING_REQUIRED = "TRAINING_REQUIRED"
    READY = "READY"


@dataclass(frozen=True)
class StandardOwnership:
    """Ownership record — never inferred from file editors."""

    standard: str
    section: str
    jurisdiction: str
    owner: str
    accountable_authority: str
    responsible_team: str
    version: str
    approval_status: str
    dependencies: FrozenSet[str] = field(default_factory=frozenset)
    evidence: FrozenSet[str] = field(default_factory=frozenset)
    change_status: str = "STABLE"

    def ownership_complete(self) -> bool:
        required = (
            self.standard,
            self.section,
            self.jurisdiction,
            self.owner,
            self.accountable_authority,
            self.responsible_team,
            self.version,
            self.approval_status,
        )
        return all(bool(x) and x != "UNKNOWN" for x in required)


@dataclass(frozen=True)
class AuthorityRequest:
    request_id: str
    action: str
    reason: str
    affected_scope: FrozenSet[str]
    requested_authority: str
    status: AuthorityRequestStatus
    evidence: FrozenSet[str] = field(default_factory=frozenset)

    def self_approve(self) -> "AuthorityRequest":
        """Forbidden path: never auto-grants."""
        if self.status in (
            AuthorityRequestStatus.AUTHORITY_REQUIRED,
            AuthorityRequestStatus.AUTHORITY_PENDING,
        ):
            return self
        return self


@dataclass(frozen=True)
class LifecycleState:
    """Independent status dimensions for one structural scope."""

    scope_id: str
    funding: bool = False
    operating: OperatingStatus = OperatingStatus.DEVELOPMENT
    structural: StructuralStatus = StructuralStatus.STRUCTURE_UNKNOWN
    evidence_status: str = "UNKNOWN"
    test_status: str = "UNKNOWN"
    authority_status: str = "UNKNOWN"
    people_readiness: ReadinessStatus = ReadinessStatus.UNKNOWN
    revalidation_status: str = "UNKNOWN"
    seal_status: str = "NO"
    production_authorization: bool = False
    frozen_scopes: FrozenSet[str] = field(default_factory=frozenset)
    continuous_review: bool = True
    structural_ratio: Optional[float] = None
    proven: bool = False
    sealed: bool = False


def is_production_authorized(state: LifecycleState) -> bool:
    return bool(state.production_authorization)


def funded_not_fully_ready(state: LifecycleState) -> bool:
    return state.funding and not (
        state.structural is StructuralStatus.STRUCTURE_COMPLETE
        and state.production_authorization
        and state.people_readiness is ReadinessStatus.READY
    )


def enter_controlled_operation(state: LifecycleState) -> LifecycleState:
    if not state.funding:
        return state
    return replace(
        state,
        operating=OperatingStatus.CONTROLLED_OPERATION,
        continuous_review=True,
    )


def at_review_threshold(state: LifecycleState, threshold: float = 0.999) -> bool:
    if state.structural_ratio is None:
        return False
    return state.structural_ratio >= threshold


def trigger_99_9_review_pause(
    state: LifecycleState, threshold: float = 0.999
) -> LifecycleState:
    if not at_review_threshold(state, threshold):
        return state
    return replace(
        state,
        structural=StructuralStatus.STRUCTURE_99_9_REVIEW_GATE,
        operating=OperatingStatus.STRUCTURAL_REVIEW,
        continuous_review=True,
        production_authorization=False,
    )


def self_analysis_findings(
    state: LifecycleState,
    *,
    ownership: Optional[StandardOwnership] = None,
    evidence_present: bool = False,
    training_complete: bool = False,
) -> FrozenSet[str]:
    gaps = []
    if ownership is None or not ownership.ownership_complete():
        gaps.append("ownership_gap")
    if not evidence_present or state.evidence_status in ("UNKNOWN", "MISSING", "STALE"):
        gaps.append("evidence_gap")
    if state.people_readiness is not ReadinessStatus.READY and not training_complete:
        gaps.append("training_gap")
    if state.authority_status in ("UNKNOWN", "MISSING"):
        gaps.append("authority_gap")
    if state.structural is StructuralStatus.STRUCTURE_UNKNOWN:
        gaps.append("structure_unknown")
    return frozenset(gaps)


def self_analysis_cannot_authorize(
    findings: FrozenSet[str], state: LifecycleState
) -> bool:
    _ = findings
    return state.production_authorization is False


def freeze_affected_scope(
    state: LifecycleState, affected: Iterable[str]
) -> LifecycleState:
    scopes = frozenset(affected)
    return replace(
        state,
        frozen_scopes=state.frozen_scopes | scopes,
        structural=StructuralStatus.STRUCTURE_REQUIRES_REPAIR,
    )


def scope_is_frozen(state: LifecycleState, scope: str) -> bool:
    return scope in state.frozen_scopes


def unrelated_scope_may_operate(
    state: LifecycleState, scope: str, independent: bool
) -> bool:
    if scope in state.frozen_scopes:
        return False
    return independent


def mark_repair_done_requires_revalidation(state: LifecycleState) -> LifecycleState:
    return replace(
        state,
        structural=StructuralStatus.STRUCTURE_REVALIDATING,
        revalidation_status="REVALIDATION_REQUIRED",
        production_authorization=False,
    )


def create_authority_request(
    *,
    request_id: str,
    action: str,
    reason: str,
    affected_scope: Iterable[str],
    requested_authority: str,
    evidence: Iterable[str] = (),
) -> AuthorityRequest:
    return AuthorityRequest(
        request_id=request_id,
        action=action,
        reason=reason,
        affected_scope=frozenset(affected_scope),
        requested_authority=requested_authority,
        status=AuthorityRequestStatus.AUTHORITY_REQUIRED,
        evidence=frozenset(evidence),
    )


def apply_human_authority_decision(
    req: AuthorityRequest, *, granted: bool, by_human: bool
) -> AuthorityRequest:
    if not by_human:
        return req
    if granted:
        return replace(req, status=AuthorityRequestStatus.AUTHORITY_GRANTED)
    return replace(req, status=AuthorityRequestStatus.AUTHORITY_REJECTED)


def material_change_requires_revalidation(state: LifecycleState) -> LifecycleState:
    return replace(
        state,
        revalidation_status="REVALIDATION_REQUIRED",
        production_authorization=False,
    )


def people_ready(
    *,
    training_complete: bool,
    competency_check: bool,
    authority_status: str,
) -> ReadinessStatus:
    if not training_complete:
        return ReadinessStatus.TRAINING_REQUIRED
    if not competency_check or authority_status in ("UNKNOWN", "MISSING"):
        return ReadinessStatus.NOT_READY
    return ReadinessStatus.READY


def structural_complete_does_not_authorize(state: LifecycleState) -> bool:
    return True


def mark_structure_complete(state: LifecycleState) -> LifecycleState:
    return replace(
        state,
        structural=StructuralStatus.STRUCTURE_COMPLETE,
        production_authorization=False,
        continuous_review=True,
    )


def observation_is_not_authority(observation: Any) -> bool:
    return True


def signature_is_not_authority(signature: Any) -> bool:
    return True


def jurisdiction_mismatch(
    ownership: StandardOwnership, action_jurisdiction: str
) -> bool:
    return ownership.jurisdiction != action_jurisdiction
