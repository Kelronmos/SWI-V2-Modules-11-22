"""Delivery lifecycle — DELIVERY ≠ AUTHORIZATION; ACK ≠ AUTHORIZATION."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DeliveryState(str, Enum):
    DELIVERED = "DELIVERED"
    RECEIVED = "RECEIVED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    REVIEWED = "REVIEWED"


@dataclass(frozen=True)
class DeliveryRecord:
    notice_id: str
    recipient_role: str
    state: DeliveryState
    channel: str
    authorized: bool = False


def delivery_authorizes(record: DeliveryRecord) -> bool:
    return False


def next_state(current: DeliveryState) -> Optional[DeliveryState]:
    order = list(DeliveryState)
    i = order.index(current)
    if i + 1 < len(order):
        return order[i + 1]
    return None
