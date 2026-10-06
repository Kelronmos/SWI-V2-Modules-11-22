"""Privacy scope — minimum necessary disclosure. URGENCY ≠ PRIVACY BYPASS."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class PrivacyLevel(str, Enum):
    PUBLIC_META = "PUBLIC_META"
    OPERATIONAL = "OPERATIONAL"
    RESTRICTED = "RESTRICTED"
    HIGHLY_RESTRICTED = "HIGHLY_RESTRICTED"


@dataclass(frozen=True)
class PrivacyScope:
    level: PrivacyLevel
    purpose: str
    data_scope: str


def minimum_necessary(requested: PrivacyLevel, permitted: PrivacyLevel) -> PrivacyLevel:
    order = list(PrivacyLevel)
    return requested if order.index(requested) <= order.index(permitted) else permitted


def disclosure_allowed(*, recipient_max: PrivacyLevel, representation_level: PrivacyLevel) -> bool:
    order = list(PrivacyLevel)
    return order.index(representation_level) <= order.index(recipient_max)
