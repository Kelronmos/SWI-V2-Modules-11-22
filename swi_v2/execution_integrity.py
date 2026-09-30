"""
SWI Execution Integrity / Node Quarantine — bounded component.

Status: IMPLEMENTED + TESTED (bounded component).
Does NOT modify M11, Security Maze, B1, or CRTG.
Does NOT claim production readiness or universal safety.

Claim under test:
  An arriving node remains quarantined until SWI verifies that its
  execution request is still bound to the admitted workflow, approved
  node, expected route, relevant policy, and last verified execution.
  On mismatch: HALT → RECORD → REVALIDATE/RETRY → ESCALATE.
  Retry does not grant authority. Execution counter proves non-execution.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class NodeState(str, Enum):
    QUARANTINED = "QUARANTINED"
    CHECKING = "CHECKING"
    MATCH = "MATCH"
    HALTED = "HALTED"
    EXECUTING = "EXECUTING"
    ESCALATED = "ESCALATED"


class Decision(str, Enum):
    EXECUTION_ALLOWED = "EXECUTION_ALLOWED"
    HALT = "HALT"
    ESCALATE = "ESCALATE"


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


class ExecutionIntegrityGate:
    """
    Node → Quarantine → Check Pipe → Workflow/Route/Input/Policy/Admission
    → Last-Execution Match → Time Continuity → Execute or Halt.
    """

    def __init__(
        self,
        admitted: AdmittedRoute,
        last_execution: Optional[ExecutionRecord] = None,
        time_tolerance: float = 0.0008,
        max_retries: int = 2,
    ):
        self.admitted = admitted
        self.last_execution = last_execution
        # Experimental configured threshold only — NOT a universal SWI standard.
        # Semantic meaning (seconds / sim units / drift) must be defined before
        # any normative claim.
        self.time_tolerance = time_tolerance
        self.max_retries = max_retries
        self.retry_count = 0
        self.execution_counter = 0  # proves whether protected op ran
        self.evidence_log: List[IntegrityEvidence] = []
        self.node_state = NodeState.QUARANTINED

    def _demo_action(self) -> str:
        """Harmless protected operation. Counter proves reachability."""
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

    def check(self, incoming: IncomingNode, *, attempt_retry: bool = False) -> CheckResult:
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
            self._demo_action()
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

        # Failure path
        self.node_state = NodeState.HALTED
        escalated = False
        retry_required = True

        if attempt_retry:
            self.retry_count += 1
            # Retry does NOT grant authority — re-run verification only.
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
