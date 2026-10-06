"""SWI Advisory package — notification/delivery layer only.

ADVISORY ≠ AUTHORITY
DELIVERY ≠ AUTHORIZATION
NOTICE ≠ ACTION
ACKNOWLEDGEMENT ≠ AUTHORIZATION
URGENCY ≠ PERMISSION
URGENCY ≠ PRIVACY BYPASS
ROLE ≠ UNLIMITED ACCESS
LEADERSHIP ≠ AUTHORITY TRANSFER
DOCUMENT_ID ≠ REPRESENTATION_ID ≠ HASH ≠ AUTHORITY

Status: RESEARCH / EXPERIMENTAL · NOT SEALED · NOT PRODUCTION_AUTHORIZED
"""
from .roles import EducationRole, RoleScope, role_may_receive
from .privacy import PrivacyScope, PrivacyLevel, minimum_necessary, disclosure_allowed
from .urgency import Urgency, urgency_may_bypass_privacy, urgency_may_mint_authority
from .representation import Representation, RepresentationLevel, representation_hash
from .delivery import DeliveryState, DeliveryRecord, delivery_authorizes
from .invariants import assert_advisory_invariants

__all__ = [
    "EducationRole",
    "RoleScope",
    "role_may_receive",
    "PrivacyScope",
    "PrivacyLevel",
    "minimum_necessary",
    "disclosure_allowed",
    "Urgency",
    "urgency_may_bypass_privacy",
    "urgency_may_mint_authority",
    "Representation",
    "RepresentationLevel",
    "representation_hash",
    "DeliveryState",
    "DeliveryRecord",
    "delivery_authorizes",
    "assert_advisory_invariants",
]
