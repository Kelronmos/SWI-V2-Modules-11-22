"""Notice classification — NOTICE ≠ ACTION."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Notice:
    notice_id: str
    classification: str
    notice_scope: str
    action_requested: bool = False
