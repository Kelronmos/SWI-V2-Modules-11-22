"""Local runtime supervisor for Termux-hosted SWI components.

STATUS: PROTOTYPE
PROVEN = NO · SEALED = NO · PRODUCTION_AUTHORIZED = NO

Provides:
- Service registration and status tracking
- Health-check recording
- Restart policy bookkeeping
- Checkpoint persistence hooks

Does NOT:
- Authorize actions
- Execute model-generated instructions
- Implement Firefly (gate closed)
- Claim OS-level isolation beyond what Termux provides
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional
import json
import os
import time

from .status import ServiceState, StatusRecord, mark_stale_if_old, missing_evidence


@dataclass
class ServiceSpec:
    name: str
    start_cmd: Optional[str] = None
    health_check: Optional[Callable[[], StatusRecord]] = None
    max_restarts: int = 3
    restart_window_seconds: float = 600.0


@dataclass
class RuntimeSupervisor:
    """In-process supervisor. Not a system init replacement."""

    base_dir: Path
    services: Dict[str, ServiceSpec] = field(default_factory=dict)
    status_log: List[StatusRecord] = field(default_factory=list)
    restart_counts: Dict[str, List[float]] = field(default_factory=dict)
    pid: int = field(default_factory=os.getpid)

    def __post_init__(self) -> None:
        self.base_dir = Path(self.base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        (self.base_dir / "checkpoints").mkdir(exist_ok=True)
        (self.base_dir / "logs").mkdir(exist_ok=True)

    def register(self, spec: ServiceSpec) -> None:
        self.services[spec.name] = spec
        self.restart_counts.setdefault(spec.name, [])

    def record(self, record: StatusRecord) -> StatusRecord:
        self.status_log.append(record)
        return record

    def check(self, name: str, *,
              max_age_seconds: float = 300.0) -> StatusRecord:
        spec = self.services.get(name)
        if spec is None:
            return self.record(
                missing_evidence(name, "service not registered")
            )
        if spec.health_check is None:
            return self.record(
                missing_evidence(name, "no health_check configured")
            )
        try:
            result = spec.health_check()
        except Exception as exc:  # noqa: BLE001 — record failure honestly
            result = StatusRecord(
                component=name,
                state=ServiceState.FAILED,
                observed_at=time.time(),
                detail=f"health_check_exception: {exc}",
                evidence_present=True,
            )
        result = mark_stale_if_old(result, max_age_seconds=max_age_seconds)
        return self.record(result)

    def can_restart(self, name: str) -> bool:
        now = time.time()
        window = self.services[name].restart_window_seconds
        recent = [t for t in self.restart_counts.get(name, []) if now - t < window]
        self.restart_counts[name] = recent
        return len(recent) < self.services[name].max_restarts

    def note_restart(self, name: str) -> None:
        self.restart_counts.setdefault(name, []).append(time.time())

    def write_checkpoint(self, label: str, payload: dict) -> Path:
        """Persist a checkpoint. Payload is observation data only."""
        path = self.base_dir / "checkpoints" / f"{label}_{int(time.time())}.json"
        record = {
            "label": label,
            "pid": self.pid,
            "written_at": time.time(),
            "payload": payload,
            "proven": False,
            "sealed": False,
            "production_authorized": False,
        }
        path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
        return path

    def latest_statuses(self) -> Dict[str, StatusRecord]:
        latest: Dict[str, StatusRecord] = {}
        for rec in self.status_log:
            latest[rec.component] = rec
        return latest

    def identity(self) -> dict:
        return {
            "pid": self.pid,
            "base_dir": str(self.base_dir),
            "services": list(self.services.keys()),
            "proven": False,
            "sealed": False,
            "production_authorized": False,
        }
