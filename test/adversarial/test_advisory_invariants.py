"""Advisory boundary invariants — ADVISORY ≠ AUTHORITY."""
from __future__ import annotations
import pytest
from swi_v2.advisory import (
    EducationRole,
    RoleScope,
    role_may_receive,
    disclosure_allowed,
    Urgency,
    urgency_may_bypass_privacy,
    urgency_may_mint_authority,
    Representation,
    RepresentationLevel,
    representation_hash,
    DeliveryState,
    DeliveryRecord,
    delivery_authorizes,
    assert_advisory_invariants,
)
from swi_v2.advisory.privacy import PrivacyLevel as PL


def test_assert_invariants():
    assert_advisory_invariants()


def test_urgency_never_mints_authority_or_bypasses_privacy():
    for u in Urgency:
        assert urgency_may_mint_authority(u) is False
        assert urgency_may_bypass_privacy(u) is False


def test_higher_role_not_unlimited():
    teacher = RoleScope.for_role(EducationRole.TEACHER_DESIGNATED_STAFF)
    assert role_may_receive(teacher, "class_notice") is True
    assert role_may_receive(teacher, "policy_notice") is False
    gov = RoleScope.for_role(EducationRole.GOVERNMENT_COMPETENT_AUTHORITY)
    assert role_may_receive(gov, "class_notice") is False


def test_delivery_ack_not_authorization():
    for st in DeliveryState:
        rec = DeliveryRecord("n", "TEACHER", st, "email")
        assert delivery_authorizes(rec) is False


def test_representation_hash_not_authority():
    r1 = Representation("DOC-1", "REP-A", RepresentationLevel.LEVEL_1_METADATA, "meta")
    r2 = Representation("DOC-1", "REP-B", RepresentationLevel.LEVEL_3_RESTRICTED, "secret")
    h1, h2 = representation_hash(r1), representation_hash(r2)
    assert h1 != h2
    assert r1.document_id == r2.document_id
    assert r1.representation_id != r2.representation_id
    assert h1 != "AUTHORIZED"


def test_same_content_stable_hash():
    r = Representation("DOC-1", "REP-A", RepresentationLevel.LEVEL_2_OPERATIONAL, "same")
    assert representation_hash(r) == representation_hash(r)


def test_privacy_minimum_necessary():
    assert disclosure_allowed(recipient_max=PL.OPERATIONAL, representation_level=PL.PUBLIC_META) is True
    assert disclosure_allowed(recipient_max=PL.OPERATIONAL, representation_level=PL.HIGHLY_RESTRICTED) is False


def test_high_urgency_missing_authority_does_not_authorize():
    assert urgency_may_mint_authority(Urgency.EMERGENCY) is False
    assert urgency_may_bypass_privacy(Urgency.EMERGENCY) is False
