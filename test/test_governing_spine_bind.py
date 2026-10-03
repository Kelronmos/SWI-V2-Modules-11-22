"""Spine-bind tests: governing_permit on existing authority path.

STATUS: TESTED candidate only.
PROVEN: NO | SEALED: NO | PRODUCTION_AUTHORIZED: NO
"""
from __future__ import annotations

import pytest

from swi_v2.kernel.authority import require_governing_permit_for_action
from swi_v2.kernel.errors import AuthorityError, AuthorityHalt

C = frozenset({"scope:read", "target:sandbox"})


def test_spine_all_layers_and_evidence_continue():
    d = require_governing_permit_for_action(
        conditions=C,
        L=C,
        G=C,
        S=C,
        H=C,
        evidence={"receipt": "e1"},
        requested_action="read",
    )
    assert d.allowed is True
    assert d.next_state == "CONTINUE"
    assert "governing_permit_ok" in d.reason


def test_spine_law_fail_rejects():
    with pytest.raises(AuthorityError) as exc:
        require_governing_permit_for_action(
            conditions=C, L=frozenset({"other"}), G=C, S=C, H=C,
            evidence={"receipt": "e2"}, requested_action="read",
        )
    assert "REJECT" in str(exc.value)


def test_spine_unknown_h_halts():
    with pytest.raises(AuthorityHalt) as exc:
        require_governing_permit_for_action(
            conditions=C, L=C, G=C, S=C, H=None,
            evidence={"receipt": "e3"}, requested_action="read",
        )
    assert "HALT" in str(exc.value)
    assert "production_authorized=false" in str(exc.value)


def test_spine_empty_evidence_rejects():
    with pytest.raises(AuthorityError) as exc:
        require_governing_permit_for_action(
            conditions=C, L=C, G=C, S=C, H=C,
            evidence=None, requested_action="read",
        )
    assert "REJECT" in str(exc.value)


def test_spine_observation_cannot_satisfy_missing_h():
    with pytest.raises(AuthorityHalt):
        require_governing_permit_for_action(
            conditions=C, L=C, G=C, S=C, H=None,
            evidence={"cek": "aligned", "kind": "observation"},
            requested_action="read",
        )


def test_spine_does_not_claim_production():
    d = require_governing_permit_for_action(
        conditions=C, L=C, G=C, S=C, H=C,
        evidence={"ok": True}, requested_action="read",
    )
    assert d.allowed is True
    assert getattr(d, "production_authorized", False) is False
