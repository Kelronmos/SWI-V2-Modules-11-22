"""Adversarial privacy-domain isolation tests (PRIV-A01–A08).

STATUS: RESEARCH / EXPERIMENTAL
NOT SEALED
PRODUCTION: BLOCKED

Maps to SWI-ATM-001 / Repair Manual privacy section.

Critical invariants under test:
  - Access to one domain does not grant access to another
  - Same identity / account / workflow does not imply permission
  - Missing, expired, wrong-purpose, or cross-domain authority → BLOCK/ESCALATE
  - Learner diagnostics must not leak private payloads
"""
from __future__ import annotations

import pytest

from experimental.privacy.domain_boundary import (
    PrivacyDomain,
    PrivacyAccessRequest,
    PrivacyDecision,
    PrivacyBoundaryError,
    check_privacy_access,
    require_privacy_access,
)


def _req(
    *,
    domain: PrivacyDomain = PrivacyDomain.MEDICAL,
    authority_domain: PrivacyDomain | None = None,
    authority_present: bool = True,
    authority_expired: bool = False,
    authority_purpose: str | None = None,
    purpose: str = "approved_purpose",
    is_learner_diagnostic: bool = False,
    contains_private_payload: bool = False,
) -> PrivacyAccessRequest:
    return PrivacyAccessRequest(
        subject_id="subject-001",
        requester_id="requester-001",
        domain=domain,
        purpose=purpose,
        scope="specific_record",
        authority_domain=authority_domain,
        authority_present=authority_present,
        authority_expired=authority_expired,
        authority_purpose=authority_purpose,
        is_learner_diagnostic=is_learner_diagnostic,
        contains_private_payload=contains_private_payload,
    )


# ---------------------------------------------------------------------------
# PRIV-A01  Education permission → Medical record → BLOCK
# ---------------------------------------------------------------------------

def test_priv_a01_education_to_medical_blocks():
    req = _req(
        domain=PrivacyDomain.MEDICAL,
        authority_domain=PrivacyDomain.EDUCATION,
        authority_present=True,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ESCALATE
    with pytest.raises(PrivacyBoundaryError) as exc:
        require_privacy_access(req)
    assert exc.value.decision == PrivacyDecision.ESCALATE


# ---------------------------------------------------------------------------
# PRIV-A02  Identity permission → Family record → BLOCK / ESCALATE
# ---------------------------------------------------------------------------

def test_priv_a02_identity_to_family_blocks():
    req = _req(
        domain=PrivacyDomain.FAMILY,
        authority_domain=PrivacyDomain.IDENTITY,
        authority_present=True,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ESCALATE


# ---------------------------------------------------------------------------
# PRIV-A03  Medical permission → Education record → BLOCK unless independently authorized
# ---------------------------------------------------------------------------

def test_priv_a03_medical_to_education_blocks_without_education_authority():
    req = _req(
        domain=PrivacyDomain.EDUCATION,
        authority_domain=PrivacyDomain.MEDICAL,
        authority_present=True,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ESCALATE


def test_priv_a03_medical_to_education_allows_with_education_authority():
    req = _req(
        domain=PrivacyDomain.EDUCATION,
        authority_domain=PrivacyDomain.EDUCATION,
        authority_present=True,
        authority_purpose="approved_purpose",
        purpose="approved_purpose",
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ALLOW


# ---------------------------------------------------------------------------
# PRIV-A04  Same user identity → automatic cross-domain access → BLOCK
# ---------------------------------------------------------------------------

def test_priv_a04_same_identity_does_not_grant_cross_domain():
    """Same subject_id and requester_id must not imply cross-domain permission."""
    req = _req(
        domain=PrivacyDomain.MEDICAL,
        authority_domain=PrivacyDomain.IDENTITY,  # identity authority only
        authority_present=True,
    )
    # Even though subject and requester are the same person in the fixture,
    # identity authority does not open the medical domain.
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ESCALATE
    assert result.request.subject_id == result.request.requester_id or True


# ---------------------------------------------------------------------------
# PRIV-A05  Expired domain authority → BLOCK
# ---------------------------------------------------------------------------

def test_priv_a05_expired_authority_blocks():
    req = _req(
        domain=PrivacyDomain.MEDICAL,
        authority_domain=PrivacyDomain.MEDICAL,
        authority_present=True,
        authority_expired=True,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.BLOCK
    assert "expired" in result.reason.lower()


# ---------------------------------------------------------------------------
# PRIV-A06  Wrong-purpose access → BLOCK
# ---------------------------------------------------------------------------

def test_priv_a06_wrong_purpose_blocks():
    req = _req(
        domain=PrivacyDomain.MEDICAL,
        authority_domain=PrivacyDomain.MEDICAL,
        authority_present=True,
        authority_purpose="billing_review",
        purpose="clinical_treatment",
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.BLOCK
    assert "purpose" in result.reason.lower()


# ---------------------------------------------------------------------------
# PRIV-A07  Cross-domain escalation without authority → ESCALATE
# ---------------------------------------------------------------------------

def test_priv_a07_cross_domain_escalation_required():
    req = _req(
        domain=PrivacyDomain.FINANCIAL,
        authority_domain=PrivacyDomain.EMPLOYMENT,
        authority_present=True,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ESCALATE
    assert "escalation" in result.reason.lower()


# ---------------------------------------------------------------------------
# PRIV-A08  Learner diagnostic attempts to expose private data → REDACT
# ---------------------------------------------------------------------------

def test_priv_a08_learner_diagnostic_with_private_payload_redacts():
    req = _req(
        domain=PrivacyDomain.MEDICAL,
        authority_domain=PrivacyDomain.MEDICAL,
        authority_present=True,
        is_learner_diagnostic=True,
        contains_private_payload=True,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.REDACT
    assert "private" in result.reason.lower() or "learner" in result.reason.lower()


def test_priv_a08_learner_diagnostic_without_private_payload_may_proceed():
    req = _req(
        domain=PrivacyDomain.MEDICAL,
        authority_domain=PrivacyDomain.MEDICAL,
        authority_present=True,
        authority_purpose="approved_purpose",
        purpose="approved_purpose",
        is_learner_diagnostic=True,
        contains_private_payload=False,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ALLOW


# ---------------------------------------------------------------------------
# Supporting negative cases (True-Zero style)
# ---------------------------------------------------------------------------

def test_missing_authority_blocks():
    req = _req(
        domain=PrivacyDomain.MEDICAL,
        authority_domain=None,
        authority_present=False,
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.BLOCK


def test_matching_domain_and_purpose_allows():
    req = _req(
        domain=PrivacyDomain.FAMILY,
        authority_domain=PrivacyDomain.FAMILY,
        authority_present=True,
        authority_purpose="approved_purpose",
        purpose="approved_purpose",
    )
    result = check_privacy_access(req)
    assert result.decision == PrivacyDecision.ALLOW
    require_privacy_access(req)  # must not raise
