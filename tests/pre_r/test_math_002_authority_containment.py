"""MATH-002 — Authority Containment property tests.

Property (property-scoped only):
    Envelope / delegated authority must be contained by the originating authority.

Implementation under test:
    experimental.response_boundary.core.AuthorityScope.contains

Status:
    EXPERIMENTAL · RESEARCH ONLY
    NOT SEALED · NOT PRODUCTION · M11 UNTOUCHED

These tests do not claim process-wide enforcement.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from experimental.response_boundary.core import AuthorityScope

NOW = datetime(2026, 9, 23, 0, 0, tzinfo=timezone.utc)


def make_scope(
    *,
    principal: str = "alice",
    actions: frozenset[str] | None = None,
    resources: frozenset[str] | None = None,
    destinations: frozenset[str] | None = None,
    expires_at: datetime | None = None,
    revoked: bool = False,
) -> AuthorityScope:
    return AuthorityScope(
        principal=principal,
        actions=actions if actions is not None else frozenset({"read", "write"}),
        resources=resources if resources is not None else frozenset({"record-1", "record-2"}),
        destinations=destinations if destinations is not None else frozenset({"alice-ui"}),
        expires_at=expires_at if expires_at is not None else NOW + timedelta(hours=1),
        revoked=revoked,
    )


# ---------------------------------------------------------------------------
# MATH-002 deterministic cases
# ---------------------------------------------------------------------------

def test_math_002_equal_scope_is_contained():
    """CASE 001 — identical authority is contained."""
    outer = make_scope()
    inner = make_scope()
    assert outer.contains(inner) is True


def test_math_002_subset_actions_is_contained():
    """CASE 002 — smaller action set is contained."""
    outer = make_scope(actions=frozenset({"read", "write"}))
    inner = make_scope(actions=frozenset({"read"}))
    assert outer.contains(inner) is True


def test_math_002_rejects_action_expansion():
    """CASE 003 — more actions than granted → not contained."""
    outer = make_scope(actions=frozenset({"read"}))
    inner = make_scope(actions=frozenset({"read", "delete"}))
    assert outer.contains(inner) is False


def test_math_002_rejects_resource_expansion():
    """CASE 004 — more resources than granted → not contained."""
    outer = make_scope(resources=frozenset({"record-1"}))
    inner = make_scope(resources=frozenset({"record-1", "record-2"}))
    assert outer.contains(inner) is False


def test_math_002_rejects_destination_expansion():
    """CASE 005 — more destinations than granted → not contained."""
    outer = make_scope(destinations=frozenset({"alice-ui"}))
    inner = make_scope(destinations=frozenset({"alice-ui", "bob-ui"}))
    assert outer.contains(inner) is False


def test_math_002_rejects_principal_mismatch():
    """CASE 006 — different principal → not contained."""
    outer = make_scope(principal="alice")
    inner = make_scope(principal="bob")
    assert outer.contains(inner) is False


def test_math_002_rejects_later_expiry():
    """CASE 007 — later expiry than outer → not contained."""
    outer = make_scope(expires_at=NOW + timedelta(hours=1))
    inner = make_scope(expires_at=NOW + timedelta(hours=2))
    assert outer.contains(inner) is False


def test_math_002_revocation_rule():
    """CASE 008 — revoked constraints must be consistent."""
    # both revoked → contained
    outer_rev = make_scope(revoked=True)
    inner_rev = make_scope(revoked=True)
    assert outer_rev.contains(inner_rev) is True

    # outer not revoked, inner revoked → not contained under current rule
    outer_ok = make_scope(revoked=False)
    inner_rev2 = make_scope(revoked=True)
    assert outer_ok.contains(inner_rev2) is False
