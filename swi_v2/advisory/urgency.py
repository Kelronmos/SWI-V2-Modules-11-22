"""Urgency classification — affects priority only, never authority or privacy."""
from __future__ import annotations
from enum import Enum


class Urgency(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    EMERGENCY = "EMERGENCY"


def urgency_may_bypass_privacy(urgency: Urgency) -> bool:
    return False


def urgency_may_mint_authority(urgency: Urgency) -> bool:
    return False
