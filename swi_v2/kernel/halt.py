"""Kernel HALT records — machine-readable, terminal until explicit recovery (not implemented)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HaltRecord:
    module: str
    reason_code: str
    stage: str
    severity: str = "halt"
    evidence_reference: Optional[str] = None
    detail: Optional[str] = None


class HaltedWorkflow:
    def __init__(self, record: HaltRecord):
        self.record = record
        self.state = "HALTED"

    def may_execute(self) -> bool:
        return False
