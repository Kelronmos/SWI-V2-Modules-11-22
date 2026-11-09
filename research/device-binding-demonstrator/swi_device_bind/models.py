from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional
import hashlib, json, time, uuid

def _canon(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

@dataclass
class Observation:
    capability: str
    status: str
    lifecycle: str
    session_id: str
    device_obs_id: str
    workflow_id: str
    action_id: str
    software_version: str
    adapter_version: str
    timestamp_utc: float
    timezone: str
    permission_state: str
    result: dict
    error: Optional[str] = None
    evidence_sha256: Optional[str] = None

    def bind_hash(self) -> str:
        payload = {
            "capability": self.capability,
            "status": self.status,
            "lifecycle": self.lifecycle,
            "session_id": self.session_id,
            "device_obs_id": self.device_obs_id,
            "workflow_id": self.workflow_id,
            "action_id": self.action_id,
            "software_version": self.software_version,
            "adapter_version": self.adapter_version,
            "timestamp_utc": self.timestamp_utc,
            "timezone": self.timezone,
            "permission_state": self.permission_state,
            "result": self.result,
            "error": self.error,
        }
        h = hashlib.sha256(_canon(payload)).hexdigest()
        self.evidence_sha256 = h
        return h

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Session:
    session_id: str
    workflow_id: str
    action_id: str
    established: bool
    created_utc: float = field(default_factory=time.time)

    @staticmethod
    def create(workflow_id: str, action_id: str, established: bool = True) -> "Session":
        return Session(
            session_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            action_id=action_id,
            established=established,
        )
