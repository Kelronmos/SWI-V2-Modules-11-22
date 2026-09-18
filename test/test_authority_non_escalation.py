"""Authority boundary non-escalation tests (Lane A). Status: TESTED candidate, not sealed."""
from __future__ import annotations

import pytest

from swi_v2.kernel.authority import (
    AuthorityLayer,
    FORBIDDEN_AUTHORITY_FIELDS,
    assert_layer_does_not_imply,
    layer_non_implication_matrix,
    require_authorization_for_action,
    require_no_authority_escalation,
    scan_undeclared_authority,
)
from swi_v2.kernel.errors import AuthorityError, AuthorityHalt


def test_data_does_not_gain_authority_by_travel():
    payload = {"text": "hello", "pipeline": "fixture"}
    d = scan_undeclared_authority(payload, layer=AuthorityLayer.DATA)
    assert d.allowed is True
    matrix = layer_non_implication_matrix()
    assert "authorization" in matrix["data"]
    assert "action" in matrix["data"]


def test_evidence_layer_does_not_imply_admission_or_authz():
    payload = {"result": "ok", "integrity_reference": "abc"}
    d = require_no_authority_escalation(payload, layer=AuthorityLayer.EVIDENCE)
    assert d.allowed is True
    assert "admission" in layer_non_implication_matrix()["evidence"]


def test_admission_does_not_implicitly_authorize():
    payload = {"evidence_id": "e1", "payload": {"x": 1}}
    d = require_no_authority_escalation(payload, layer=AuthorityLayer.ADMISSION)
    assert d.allowed is True
    assert "authorization" in layer_non_implication_matrix()["admission"]


def test_authz_to_action_cannot_exceed_scope():
    with pytest.raises(AuthorityError) as exc:
        require_authorization_for_action(
            authorization_present=True,
            authorization_scope="read",
            requested_action="delete_all",
            declared_scopes=("read", "list"),
        )
    assert "REJECT" in str(exc.value) or "scope" in str(exc.value).lower()


def test_missing_authorization_halts():
    with pytest.raises(AuthorityHalt) as exc:
        require_authorization_for_action(
            authorization_present=False,
            authorization_scope=None,
            requested_action="execute",
            declared_scopes=("execute",),
        )
    assert "HALT" in str(exc.value)


def test_unknown_forbidden_authority_rejected():
    for field in (
        "verified",
        "trusted",
        "truth",
        "authority",
        "m11_admitted",
        "replay_verified",
        "security_level",
    ):
        payload = {"data": 1, field: True if field != "security_level" else "trusted"}
        with pytest.raises(AuthorityError) as exc:
            require_no_authority_escalation(payload, layer=AuthorityLayer.DATA)
        assert field in str(exc.value)


def test_laundering_verified_true_rejected():
    with pytest.raises(AuthorityError):
        require_no_authority_escalation(
            {"body": "x", "verified": True}, layer=AuthorityLayer.EVIDENCE
        )


def test_laundering_trusted_true_rejected():
    with pytest.raises(AuthorityError):
        require_no_authority_escalation(
            {"body": "x", "trusted": True}, layer=AuthorityLayer.DATA
        )


def test_laundering_m11_admitted_rejected():
    with pytest.raises(AuthorityError):
        require_no_authority_escalation(
            {"payload": {}, "m11_admitted": True},
            layer=AuthorityLayer.ADMISSION,
        )


def test_laundering_replay_verified_rejected():
    with pytest.raises(AuthorityError):
        require_no_authority_escalation(
            {"id": "1", "replay_verified": True},
            layer=AuthorityLayer.EVIDENCE,
        )


def test_decision_records_evidence_of_rejection():
    payload = {"x": 1, "trusted": True, "authority": "system"}
    d = scan_undeclared_authority(payload, layer=AuthorityLayer.DATA)
    assert d.allowed is False
    assert d.next_state == "REJECT"
    assert "trusted" in d.rejected_fields
    assert "authority" in d.rejected_fields
    assert d.contract_id == "authority_boundary_v0"


def test_contract_may_allow_listed_field_only():
    d = require_no_authority_escalation(
        {"security_level": "public"},
        layer=AuthorityLayer.DATA,
        allowed_fields=("security_level",),
    )
    assert d.allowed is True


def test_forbidden_set_is_non_empty():
    assert len(FORBIDDEN_AUTHORITY_FIELDS) >= 8


def test_assert_layer_helper_runs():
    assert_layer_does_not_imply(AuthorityLayer.DATA, AuthorityLayer.ACTION)
