"""Evidence ledger and non-negotiable claims."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

# These values are intentionally hard-coded and must never be upgraded
# by successful builds, tests, or simulations.
FINAL_CLAIMS = {
    "system_completion": "INCOMPLETE",
    "proven": False,
    "sealed": False,
    "production_authorized": False,
    "production_authorized_str": "NO",
}


class EvidenceLedger:
    """Collects run metadata without ever promoting claims."""

    def __init__(self, run_id: str, runner_version: str) -> None:
        self.run_id = run_id
        self.runner_version = runner_version
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.environment: dict[str, Any] = {}
        self.repositories: list[dict[str, Any]] = []
        self.failures: list[dict[str, Any]] = []
        self.notes: list[str] = []

    def record_environment(self, env: dict[str, Any]) -> None:
        self.environment = env

    def record_repository(self, record: dict[str, Any]) -> None:
        self.repositories.append(record)

    def record_failure(self, stage: str, reason: str) -> None:
        self.failures.append({
            "stage": stage,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "runner_version": self.runner_version,
            "started_at": self.started_at,
            "environment": self.environment,
            "repositories": self.repositories,
            "failures": self.failures,
            "notes": self.notes,
            "claims": FINAL_CLAIMS.copy(),
        }
