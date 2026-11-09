from __future__ import annotations
from typing import Dict, List
from .models import Observation

class CapabilityRegistry:
    def __init__(self):
        self._caps: Dict[str, Observation] = {}

    def record(self, obs: Observation) -> None:
        self._caps[obs.capability] = obs

    def get(self, name: str):
        return self._caps.get(name)

    def matrix(self) -> List[dict]:
        rows = []
        for name, obs in sorted(self._caps.items()):
            rows.append({
                "capability": name,
                "status": obs.status,
                "lifecycle": obs.lifecycle,
                "permission_state": obs.permission_state,
                "error": obs.error,
                "evidence_sha256": obs.evidence_sha256,
            })
        return rows

    def summary_counts(self) -> dict:
        counts = {}
        for obs in self._caps.values():
            counts[obs.status] = counts.get(obs.status, 0) + 1
        return counts
