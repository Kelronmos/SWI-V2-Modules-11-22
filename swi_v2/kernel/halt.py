"""Kernel HALT records — machine-readable, terminal until explicit recovery.

Common SWI terminal decision for execution-blocking workflow conditions.
HASH != AUTHORITY != TRUTH: evidence_hash protects record integrity only.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class HaltRecord:
    """Common SWI HALT error / terminal record.

    Required: module, reason_code, stage.
    Optional fields use None when not applicable — do not fabricate IDs.
    """

    module: str
    reason_code: str
    stage: str
    severity: str = "halt"
    evidence_reference: Optional[str] = None
    detail: Optional[str] = None
    halt_id: Optional[str] = None
    workflow_id: Optional[str] = None
    route_id: Optional[str] = None
    node_id: Optional[str] = None
    input_id: Optional[str] = None
    policy_id: Optional[str] = None
    admission_id: Optional[str] = None
    decision: str = "HALT"
    reason: Optional[str] = None
    previous_state: Optional[str] = None
    expected_state: Optional[Dict[str, Any]] = None
    received_state: Optional[Dict[str, Any]] = None
    execution_allowed: bool = False
    execution_occurred: bool = False
    retry_count: int = 0
    retry_required: bool = False
    escalation_required: bool = False
    timestamp: float = field(default_factory=time.time)
    evidence_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

    def with_evidence_hash(self) -> "HaltRecord":
        """Return a new record with deterministic SHA-256 of canonical payload (excluding evidence_hash)."""
        payload = self.to_dict()
        payload.pop("evidence_hash", None)
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        h = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return HaltRecord(**{**payload, "evidence_hash": h})


class HaltedWorkflow:
    def __init__(self, record: HaltRecord):
        self.record = record
        self.state = "HALTED"

    def may_execute(self) -> bool:
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "record": self.record.to_dict(),
            "execution_allowed": False,
            "may_execute": False,
        }
