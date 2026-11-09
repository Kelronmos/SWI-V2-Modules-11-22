"""Evidence binder — integrity relative to a reference, not truth claims."""
from __future__ import annotations
from typing import Optional
from .models import Observation, Session
from .status import CapStatus, Lifecycle

class EvidenceBinder:
    def __init__(self):
        self._seen_hashes: set[str] = set()
        self._seen_nonces: set[str] = set()

    def bind(self, obs: Observation, session: Session, max_age_s: float = 300.0, now: Optional[float] = None) -> Observation:
        import time
        now = time.time() if now is None else now
        if not session.established:
            obs.status = CapStatus.FAIL.value
            obs.error = "MISSING_USER_SESSION"
            obs.lifecycle = Lifecycle.NOT_DISCOVERED.value
            obs.bind_hash()
            return obs
        if obs.session_id != session.session_id:
            obs.status = CapStatus.FAIL.value
            obs.error = "WRONG_SESSION_BINDING"
            obs.bind_hash()
            return obs
        if obs.workflow_id != session.workflow_id:
            obs.status = CapStatus.FAIL.value
            obs.error = "WRONG_WORKFLOW_BINDING"
            obs.bind_hash()
            return obs
        if obs.action_id != session.action_id:
            obs.status = CapStatus.FAIL.value
            obs.error = "WRONG_ACTION_BINDING"
            obs.bind_hash()
            return obs
        age = now - obs.timestamp_utc
        if age > max_age_s or age < -5:
            obs.status = CapStatus.FAIL.value
            obs.error = "STALE_OBSERVATION"
            obs.bind_hash()
            return obs
        h = obs.bind_hash()
        if h in self._seen_hashes:
            obs.status = CapStatus.FAIL.value
            obs.error = "REUSED_EVIDENCE"
            return obs
        self._seen_hashes.add(h)
        if obs.status not in (CapStatus.BLOCKED.value, CapStatus.NOT_IMPLEMENTED.value, CapStatus.NOT_RUN.value, CapStatus.FAIL.value):
            obs.lifecycle = Lifecycle.BOUND.value
        return obs

    def reject_replay_nonce(self, nonce: str) -> bool:
        if nonce in self._seen_nonces:
            return False
        self._seen_nonces.add(nonce)
        return True
