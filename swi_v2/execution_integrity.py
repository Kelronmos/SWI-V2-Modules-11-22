"""
SWI Execution Integrity / Node Quarantine — bounded component.

Status: IMPLEMENTED + TESTED (bounded component + boundary hardening).
Does NOT modify M11, Security Maze, B1, or CRTG.
Does NOT claim production readiness, process-wide OS isolation, or universal safety.
Supported API: check()/execute(); direct _demo_action without permit is blocked.

Claim under test:
  An arriving node remains quarantined until SWI verifies that its
  execution request is still bound to the admitted workflow, approved
  node, expected route, relevant policy, and last verified execution.
  On mismatch: HALT → RECORD → REVALIDATE/RETRY → ESCALATE.
  Retry does not grant authority. Execution counter proves non-execution.
  New information that affects the evidence boundary INVALIDATES prior
  decisions; without bound authority the result is UNKNOWN (no execution).
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from swi_v2.kernel.halt import HaltRecord, HaltedWorkflow


class NodeState(str, Enum):
    QUARANTINED = "QUARANTINED"
    CHECKING = "CHECKING"
    MATCH = "MATCH"
    HALTED = "HALTED"
    PAUSED = "PAUSED"
    EXECUTING = "EXECUTING"
    ESCALATED = "ESCALATED"


class Decision(str, Enum):
    EXECUTION_ALLOWED = "EXECUTION_ALLOWED"
    HALT = "HALT"
    ESCALATE = "ESCALATE"
    UNKNOWN = "UNKNOWN"


class FailureReason(str, Enum):
    NODE_MISMATCH = "NODE_MISMATCH"
    WORKFLOW_MISMATCH = "WORKFLOW_MISMATCH"
    ROUTE_CHANGED = "ROUTE_CHANGED"
    INPUT_CHANGED = "INPUT_CHANGED"
    POLICY_CHANGED = "POLICY_CHANGED"
    ADMISSION_MISMATCH = "ADMISSION_MISMATCH"
    LAST_EXECUTION_MISMATCH = "LAST_EXECUTION_MISMATCH"
    TIME_CONTINUITY_EXCEEDED = "TIME_CONTINUITY_EXCEEDED"
    RETRY_LIMIT_EXCEEDED = "RETRY_LIMIT_EXCEEDED"
    NOT_ADMITTED = "NOT_ADMITTED"
    NEW_INFORMATION_INVALIDATES = "NEW_INFORMATION_INVALIDATES"
    BOUNDARY_INSUFFICIENT = "BOUNDARY_INSUFFICIENT"
    AUTHORITY_REQUIRED = "AUTHORITY_REQUIRED"
    AUTHORITY_INVALID = "AUTHORITY_INVALID"


@dataclass(frozen=True)
class AdmittedRoute:
    workflow_id: str
    route_hash: str
    node_id: str
    input_hash: str
    policy_hash: str
    admission_hash: str

    def identity_tuple(self) -> tuple:
        return (
            self.workflow_id,
            self.route_hash,
            self.node_id,
            self.input_hash,
            self.policy_hash,
            self.admission_hash,
        )


@dataclass(frozen=True)
class ExecutionRecord:
    execution_id: str
    workflow_id: str
    node_id: str
    route_hash: str
    input_hash: str
    timestamp: float


@dataclass
class IncomingNode:
    """Candidate only. Never mutates AdmittedRoute."""
    node_id: str
    workflow_id: str
    route_hash: str
    input_hash: str
    policy_hash: str
    admission_hash: Optional[str] = None
    current_time: Optional[float] = None


@dataclass(frozen=True)
class NewInformation:
    """Candidate new information. Does not mutate AdmittedRoute."""
    description: str
    affects_evidence_boundary: bool
    information_id: str = ""
    proposed_route_hash: Optional[str] = None
    proposed_input_hash: Optional[str] = None
    proposed_policy_hash: Optional[str] = None


@dataclass(frozen=True)
class HumanAuthority:
    authority_id: str
    workflow_id: str
    action_id: str
    token: str


@dataclass(frozen=True)
class ValidatedAuthority:
    authority_id: str
    workflow_id: str
    action_id: str
    bound: bool = True

    def covers(self, workflow_id: str, action_id: str) -> bool:
        return self.bound and self.workflow_id == workflow_id and self.action_id == action_id


def validate_human_authority(
    authority: HumanAuthority, *, workflow_id: str, action_id: str
) -> ValidatedAuthority:
    """Bind human authority to exact workflow/action. Library-level only."""
    if not isinstance(authority, HumanAuthority):
        raise ValueError("authority must be HumanAuthority")
    if not authority.authority_id or not authority.token:
        raise ValueError("authority_id and token required")
    if authority.workflow_id != workflow_id or authority.action_id != action_id:
        raise ValueError("authority not bound to requested workflow/action")
    return ValidatedAuthority(
        authority_id=authority.authority_id,
        workflow_id=workflow_id,
        action_id=action_id,
        bound=True,
    )


@dataclass
class IntegrityEvidence:
    event: str
    workflow_id: str
    node_id: str
    expected: Dict[str, Any]
    received: Dict[str, Any]
    decision: str
    execution_allowed: bool
    execution_occurred: bool
    reasons: List[str]
    node_state: str
    retry_count: int
    retry_required: bool
    escalated: bool
    evidence_hash: str = ""
    timestamp: float = field(default_factory=time.time)

    def finalize(self) -> "IntegrityEvidence":
        payload = {
            "event": self.event,
            "workflow_id": self.workflow_id,
            "node_id": self.node_id,
            "expected": self.expected,
            "received": self.received,
            "decision": self.decision,
            "execution_allowed": self.execution_allowed,
            "execution_occurred": self.execution_occurred,
            "reasons": self.reasons,
            "node_state": self.node_state,
            "retry_count": self.retry_count,
            "retry_required": self.retry_required,
            "escalated": self.escalated,
            "timestamp": self.timestamp,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        self.evidence_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return self


@dataclass
class CheckResult:
    decision: Decision
    reasons: List[FailureReason]
    evidence: IntegrityEvidence
    execution_occurred: bool
    node_state: NodeState


class _ExecutionPermit:
    __slots__ = ("_gate_id", "_nonce", "_consumed")

    def __init__(self, gate_id: int, nonce: int) -> None:
        self._gate_id = gate_id
        self._nonce = nonce
        self._consumed = False


class ExecutionIntegrityGate:
    def __init__(
        self,
        admitted: AdmittedRoute,
        last_execution: Optional[ExecutionRecord] = None,
        time_tolerance: float = 0.0008,
        max_retries: int = 2,
    ):
        self.admitted = admitted
        self.last_execution = last_execution
        self.time_tolerance = time_tolerance
        self.max_retries = max_retries
        self.retry_count = 0
        self.execution_counter = 0
        self.evidence_log: List[IntegrityEvidence] = []
        self.node_state = NodeState.QUARANTINED
        self._permit_nonce = 0
        self._decision_invalidated: bool = False
        self._boundary_insufficient: bool = False
        self._bound_authority: Optional[ValidatedAuthority] = None
        self._pending_new_information: Optional[NewInformation] = None

    def _mint_permit(self) -> _ExecutionPermit:
        self._permit_nonce += 1
        return _ExecutionPermit(gate_id=id(self), nonce=self._permit_nonce)

    def _demo_action(self, permit: Optional[_ExecutionPermit] = None) -> str:
        if permit is None:
            raise PermissionError(
                "protected operation requires a valid integrity permit; "
                "use check()/execute() — direct invocation is blocked"
            )
        if not isinstance(permit, _ExecutionPermit):
            raise PermissionError("invalid permit type")
        if permit._gate_id != id(self) or permit._nonce != self._permit_nonce:
            raise PermissionError("stale or foreign integrity permit")
        if permit._consumed:
            raise PermissionError("permit already consumed")
        permit._consumed = True
        self.execution_counter += 1
        return "DEMO_ACTION_EXECUTED"

    def _compare(self, incoming: IncomingNode) -> List[FailureReason]:
        reasons: List[FailureReason] = []
        adm = self.admitted
        if incoming.admission_hash is None or incoming.admission_hash != adm.admission_hash:
            reasons.append(
                FailureReason.ADMISSION_MISMATCH
                if incoming.admission_hash
                else FailureReason.NOT_ADMITTED
            )
        if incoming.node_id != adm.node_id:
            reasons.append(FailureReason.NODE_MISMATCH)
        if incoming.workflow_id != adm.workflow_id:
            reasons.append(FailureReason.WORKFLOW_MISMATCH)
        if incoming.route_hash != adm.route_hash:
            reasons.append(FailureReason.ROUTE_CHANGED)
        if incoming.input_hash != adm.input_hash:
            reasons.append(FailureReason.INPUT_CHANGED)
        if incoming.policy_hash != adm.policy_hash:
            reasons.append(FailureReason.POLICY_CHANGED)
        if self.last_execution is not None:
            le = self.last_execution
            if (
                le.workflow_id != adm.workflow_id
                or le.node_id != adm.node_id
                or le.route_hash != adm.route_hash
            ):
                reasons.append(FailureReason.LAST_EXECUTION_MISMATCH)
            t = incoming.current_time if incoming.current_time is not None else time.time()
            if abs(t - le.timestamp) > self.time_tolerance:
                reasons.append(FailureReason.TIME_CONTINUITY_EXCEEDED)
        return reasons

    def apply_new_information(
        self, info: NewInformation, *, action_id: str = "default_action"
    ) -> CheckResult:
        """Invalidate current decision when new information arrives.

        If it affects the evidence boundary and required authority is absent,
        result is UNKNOWN — execution must not proceed.
        """
        if not isinstance(info, NewInformation):
            raise TypeError("info must be NewInformation")
        self._decision_invalidated = True
        self._pending_new_information = info
        self._permit_nonce += 1
        expected = {
            "workflow_id": self.admitted.workflow_id,
            "route_hash": self.admitted.route_hash,
            "node_id": self.admitted.node_id,
            "input_hash": self.admitted.input_hash,
            "policy_hash": self.admitted.policy_hash,
            "admission_hash": self.admitted.admission_hash,
        }
        received = {
            "information_id": info.information_id,
            "description": info.description,
            "affects_evidence_boundary": info.affects_evidence_boundary,
            "proposed_route_hash": info.proposed_route_hash,
            "proposed_input_hash": info.proposed_input_hash,
            "proposed_policy_hash": info.proposed_policy_hash,
        }
        if not info.affects_evidence_boundary:
            evidence = IntegrityEvidence(
                event="NEW_INFORMATION_NO_BOUNDARY_IMPACT",
                workflow_id=self.admitted.workflow_id,
                node_id=self.admitted.node_id,
                expected=expected,
                received=received,
                decision=Decision.HALT.value,
                execution_allowed=False,
                execution_occurred=False,
                reasons=[FailureReason.NEW_INFORMATION_INVALIDATES.value],
                node_state=NodeState.QUARANTINED.value,
                retry_count=self.retry_count,
                retry_required=True,
                escalated=False,
            ).finalize()
            self.evidence_log.append(evidence)
            self.node_state = NodeState.QUARANTINED
            return CheckResult(
                decision=Decision.HALT,
                reasons=[FailureReason.NEW_INFORMATION_INVALIDATES],
                evidence=evidence,
                execution_occurred=False,
                node_state=self.node_state,
            )
        self._boundary_insufficient = True
        auth_ok = self._bound_authority is not None and self._bound_authority.covers(
            self.admitted.workflow_id, action_id
        )
        if not auth_ok:
            reasons = [
                FailureReason.NEW_INFORMATION_INVALIDATES,
                FailureReason.BOUNDARY_INSUFFICIENT,
                FailureReason.AUTHORITY_REQUIRED,
            ]
            self.node_state = NodeState.PAUSED
            evidence = IntegrityEvidence(
                event="NEW_INFORMATION_BOUNDARY_INSUFFICIENT",
                workflow_id=self.admitted.workflow_id,
                node_id=self.admitted.node_id,
                expected=expected,
                received=received,
                decision=Decision.UNKNOWN.value,
                execution_allowed=False,
                execution_occurred=False,
                reasons=[r.value for r in reasons],
                node_state=NodeState.PAUSED.value,
                retry_count=self.retry_count,
                retry_required=True,
                escalated=False,
            ).finalize()
            self.evidence_log.append(evidence)
            return CheckResult(
                decision=Decision.UNKNOWN,
                reasons=reasons,
                evidence=evidence,
                execution_occurred=False,
                node_state=self.node_state,
            )
        self.node_state = NodeState.QUARANTINED
        evidence = IntegrityEvidence(
            event="NEW_INFORMATION_AUTHORITY_PRESENT_RECHECK_REQUIRED",
            workflow_id=self.admitted.workflow_id,
            node_id=self.admitted.node_id,
            expected=expected,
            received=received,
            decision=Decision.HALT.value,
            execution_allowed=False,
            execution_occurred=False,
            reasons=[FailureReason.NEW_INFORMATION_INVALIDATES.value],
            node_state=NodeState.QUARANTINED.value,
            retry_count=self.retry_count,
            retry_required=True,
            escalated=False,
        ).finalize()
        self.evidence_log.append(evidence)
        return CheckResult(
            decision=Decision.HALT,
            reasons=[FailureReason.NEW_INFORMATION_INVALIDATES],
            evidence=evidence,
            execution_occurred=False,
            node_state=self.node_state,
        )

    def bind_authority(self, authority: ValidatedAuthority, *, action_id: str) -> None:
        if not isinstance(authority, ValidatedAuthority) or not authority.bound:
            raise ValueError("ValidatedAuthority required")
        if not authority.covers(self.admitted.workflow_id, action_id):
            raise ValueError("authority does not cover this workflow/action")
        self._bound_authority = authority
        if self._boundary_insufficient:
            self._boundary_insufficient = False

    def recheck(
        self,
        incoming: IncomingNode,
        *,
        authority: Optional[ValidatedAuthority] = None,
        action_id: str = "default_action",
        attempt_retry: bool = False,
    ) -> CheckResult:
        if authority is not None:
            self.bind_authority(authority, action_id=action_id)
        if self._boundary_insufficient:
            auth_ok = self._bound_authority is not None and self._bound_authority.covers(
                self.admitted.workflow_id, action_id
            )
            if not auth_ok:
                return self.apply_new_information(
                    self._pending_new_information
                    or NewInformation(description="pending", affects_evidence_boundary=True),
                    action_id=action_id,
                )
        result = self.check(incoming, attempt_retry=attempt_retry)
        if result.decision == Decision.EXECUTION_ALLOWED:
            self._decision_invalidated = False
            self._pending_new_information = None
        return result

    def check(self, incoming: IncomingNode, *, attempt_retry: bool = False) -> CheckResult:
        if self._boundary_insufficient:
            auth_ok = self._bound_authority is not None and self._bound_authority.covers(
                self.admitted.workflow_id, "default_action"
            )
            if not auth_ok:
                info = self._pending_new_information or NewInformation(
                    description="boundary_insufficient", affects_evidence_boundary=True
                )
                return self.apply_new_information(info, action_id="default_action")
        self.node_state = NodeState.CHECKING
        reasons = self._compare(incoming)
        expected = {
            "workflow_id": self.admitted.workflow_id,
            "route_hash": self.admitted.route_hash,
            "node_id": self.admitted.node_id,
            "input_hash": self.admitted.input_hash,
            "policy_hash": self.admitted.policy_hash,
            "admission_hash": self.admitted.admission_hash,
        }
        received = {
            "workflow_id": incoming.workflow_id,
            "route_hash": incoming.route_hash,
            "node_id": incoming.node_id,
            "input_hash": incoming.input_hash,
            "policy_hash": incoming.policy_hash,
            "admission_hash": incoming.admission_hash,
        }
        if not reasons:
            self.node_state = NodeState.MATCH
            permit = self._mint_permit()
            self._demo_action(permit)
            evidence = IntegrityEvidence(
                event="EXECUTION_INTEGRITY_PASS",
                workflow_id=self.admitted.workflow_id,
                node_id=incoming.node_id,
                expected=expected,
                received=received,
                decision=Decision.EXECUTION_ALLOWED.value,
                execution_allowed=True,
                execution_occurred=True,
                reasons=[],
                node_state=NodeState.EXECUTING.value,
                retry_count=self.retry_count,
                retry_required=False,
                escalated=False,
            ).finalize()
            self.evidence_log.append(evidence)
            self.node_state = NodeState.EXECUTING
            return CheckResult(
                decision=Decision.EXECUTION_ALLOWED,
                reasons=[],
                evidence=evidence,
                execution_occurred=True,
                node_state=self.node_state,
            )
        self.node_state = NodeState.HALTED
        escalated = False
        retry_required = True
        if attempt_retry:
            self.retry_count += 1
            reasons_after = self._compare(incoming)
            if reasons_after:
                if self.retry_count >= self.max_retries:
                    escalated = True
                    self.node_state = NodeState.ESCALATED
                    reasons = reasons_after + [FailureReason.RETRY_LIMIT_EXCEEDED]
                    retry_required = False
                else:
                    reasons = reasons_after
        evidence = IntegrityEvidence(
            event="EXECUTION_INTEGRITY_FAILURE",
            workflow_id=self.admitted.workflow_id,
            node_id=incoming.node_id,
            expected=expected,
            received=received,
            decision=Decision.ESCALATE.value if escalated else Decision.HALT.value,
            execution_allowed=False,
            execution_occurred=False,
            reasons=[r.value for r in reasons],
            node_state=self.node_state.value,
            retry_count=self.retry_count,
            retry_required=retry_required,
            escalated=escalated,
        ).finalize()
        self.evidence_log.append(evidence)
        return CheckResult(
            decision=Decision.ESCALATE if escalated else Decision.HALT,
            reasons=reasons,
            evidence=evidence,
            execution_occurred=False,
            node_state=self.node_state,
        )

    def to_halt_record(self, result: CheckResult) -> HaltRecord:
        if result.decision == Decision.EXECUTION_ALLOWED:
            raise ValueError("to_halt_record requires HALT, ESCALATE, or UNKNOWN decision")
        primary = result.reasons[0].value if result.reasons else "INTEGRITY_FAILURE"
        reason_codes = [r.value for r in result.reasons]
        rec = HaltRecord(
            module="execution_integrity",
            reason_code=primary,
            stage="CHECK_PIPE",
            detail=";".join(reason_codes) if reason_codes else None,
            workflow_id=result.evidence.workflow_id,
            route_id=result.evidence.expected.get("route_hash"),
            node_id=result.evidence.node_id,
            input_id=result.evidence.expected.get("input_hash"),
            policy_id=result.evidence.expected.get("policy_hash"),
            admission_id=result.evidence.expected.get("admission_hash"),
            decision=result.decision.value,
            reason=primary,
            expected_state=dict(result.evidence.expected),
            received_state=dict(result.evidence.received),
            execution_allowed=False,
            execution_occurred=bool(result.execution_occurred),
            retry_count=result.evidence.retry_count,
            retry_required=result.evidence.retry_required,
            escalation_required=result.evidence.escalated,
            evidence_reference=result.evidence.evidence_hash or None,
        )
        return rec.with_evidence_hash()

    def to_halted_workflow(self, result: CheckResult) -> HaltedWorkflow:
        return HaltedWorkflow(self.to_halt_record(result))

    def execute(self, incoming: IncomingNode, *, attempt_retry: bool = False) -> CheckResult:
        return self.check(incoming, attempt_retry=attempt_retry)
