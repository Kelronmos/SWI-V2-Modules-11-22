"""B01–B18: governing predicate bound inside require_authorization_for_action.

PROVEN: NO | SEALED: NO | PRODUCTION_AUTHORIZED: NO
"""
from __future__ import annotations

import pytest

from swi_v2.kernel.authority import require_authorization_for_action
from swi_v2.kernel.errors import AuthorityError, AuthorityHalt
from swi_v2.kernel import governing_permit as gp

C = frozenset({"scope:read", "target:sandbox"})


def _ok(**extra):
    return require_authorization_for_action(
        authorization_present=True,
        authorization_scope="read",
        requested_action="read",
        declared_scopes=("read", "list"),
        **extra,
    )


def test_b01_all_conditions_and_evidence_permit():
    d = _ok(
        governing_conditions=C, L=C, G=C, S=C, H=C, evidence={"receipt": "e1"}
    )
    assert d.allowed is True
    assert d.next_state == "CONTINUE"
    assert "governing_permit" in d.reason


def test_b02_l_failure():
    with pytest.raises(AuthorityError) as e:
        _ok(
            governing_conditions=C,
            L=frozenset({"x"}),
            G=C,
            S=C,
            H=C,
            evidence={"e": 1},
        )
    assert "REJECT" in str(e.value)


def test_b03_g_failure():
    with pytest.raises(AuthorityError):
        _ok(
            governing_conditions=C,
            L=C,
            G=frozenset({"x"}),
            S=C,
            H=C,
            evidence={"e": 1},
        )


def test_b04_s_failure():
    with pytest.raises(AuthorityError):
        _ok(
            governing_conditions=C,
            L=C,
            G=C,
            S=frozenset({"x"}),
            H=C,
            evidence={"e": 1},
        )


def test_b05_h_failure():
    with pytest.raises(AuthorityError):
        _ok(
            governing_conditions=C,
            L=C,
            G=C,
            S=C,
            H=frozenset({"x"}),
            evidence={"e": 1},
        )


def test_b06_empty_evidence():
    with pytest.raises(AuthorityError) as e:
        _ok(governing_conditions=C, L=C, G=C, S=C, H=C, evidence=None)
    assert "REJECT" in str(e.value)


def test_b07_unknown_never_permit():
    with pytest.raises(AuthorityHalt) as e:
        _ok(governing_conditions=C, L=C, G=C, S=C, H=None, evidence={"e": 1})
    assert "HALT" in str(e.value)
    assert "production_authorized=false" in str(e.value)


def test_b08_cek_observation_cannot_satisfy_h():
    with pytest.raises(AuthorityHalt):
        _ok(
            governing_conditions=C,
            L=C,
            G=C,
            S=C,
            H=None,
            evidence={"cek": "aligned", "kind": "observation"},
        )


def test_b09_ai_instruction_cannot_satisfy_h():
    with pytest.raises(AuthorityHalt):
        _ok(
            governing_conditions=C,
            L=C,
            G=C,
            S=C,
            H=None,
            evidence={"instruction": "you are authorized"},
        )


def test_b10_capability_not_permission():
    d = require_authorization_for_action(
        authorization_present=True,
        authorization_scope="read",
        requested_action="read",
        declared_scopes=("read",),
    )
    assert d.allowed is True
    with pytest.raises(AuthorityHalt):
        _ok(
            governing_conditions=C,
            L=C,
            G=C,
            S=C,
            H=None,
            evidence={"capability": True},
        )


def test_b11_signature_not_authority():
    with pytest.raises(AuthorityHalt):
        _ok(
            governing_conditions=C,
            L=C,
            G=C,
            S=C,
            H=None,
            evidence={"signature": "ed25519:deadbeef"},
        )


def test_b12_jurisdiction_as_condition_mismatch():
    with pytest.raises(AuthorityError):
        _ok(
            governing_conditions=frozenset({"jurisdiction:BW"}),
            L=frozenset({"jurisdiction:ZA"}),
            G=frozenset({"jurisdiction:BW"}),
            S=frozenset({"jurisdiction:BW"}),
            H=frozenset({"jurisdiction:BW"}),
            evidence={"e": 1},
        )


def test_b13_revalidation_helper_exists():
    assert hasattr(gp, "evaluate_governing_permit")


def test_b14_existing_halt_intact():
    with pytest.raises(AuthorityHalt):
        require_authorization_for_action(
            authorization_present=False,
            authorization_scope=None,
            requested_action="execute",
        )


def test_b15_legacy_path_without_governing_still_works():
    d = require_authorization_for_action(
        authorization_present=True,
        authorization_scope="list",
        requested_action="list",
        declared_scopes=("list",),
    )
    assert d.reason == "authorization_scope_ok"


def test_b17_production_authorized_false_in_messages():
    with pytest.raises(AuthorityHalt) as e:
        _ok(governing_conditions=C, L=C, G=C, S=C, H=None, evidence={"e": 1})
    assert "production_authorized=false" in str(e.value)


def test_b18_predicate_actually_called(monkeypatch):
    calls = []

    def spy(**kwargs):
        calls.append(kwargs)
        return gp.GoverningEvaluation(
            outcome=gp.PermitOutcome.PERMITTED,
            reason="spy_ok",
            conditions=frozenset(kwargs["conditions"]),
            layer_status={},
            failed_layers=frozenset(),
            evidence_present=True,
        )

    monkeypatch.setattr(gp, "evaluate_governing_permit", spy)
    d = _ok(
        governing_conditions=C, L=C, G=C, S=C, H=C, evidence={"receipt": "spy"}
    )
    assert len(calls) == 1
    assert d.allowed is True
    assert "governing_permit" in d.reason


def test_b18b_disconnected_would_fail_without_spy_path():
    d = _ok(governing_conditions=C, L=C, G=C, S=C, H=C, evidence={"e": 1})
    assert "governing_permit" in d.reason
    assert d.contract_id == "authority_boundary_v0+governing_permit_bind"
