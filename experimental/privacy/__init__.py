"""SWI privacy domain boundary.

STATUS:
  RESEARCH / EXPERIMENTAL
  IMPLEMENTED (boundary gate only)
  NOT SEALED
  NOT PRODUCTION AUTHORIZED
"""
from experimental.privacy.domain_boundary import (
    PrivacyDomain,
    PrivacyAccessRequest,
    PrivacyDecision,
    PrivacyBoundaryError,
    check_privacy_access,
)

__all__ = [
    "PrivacyDomain",
    "PrivacyAccessRequest",
    "PrivacyDecision",
    "PrivacyBoundaryError",
    "check_privacy_access",
]
