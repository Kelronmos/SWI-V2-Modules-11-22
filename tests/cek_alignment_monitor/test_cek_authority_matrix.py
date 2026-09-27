"""Stage 3 — Authority-boundary attack matrix (45 forbidden cells)."""
from __future__ import annotations
import pytest
from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.visibility import VisibilityLevel

SOURCES = ("UNKNOWN","EVIDENCE","OBSERVATION","STABLE","DRIFT","SIGNATURE","HALT","REJECT","EXECUTION")
TARGETS = ("PERMIT","AUTHORITY","BINDING","EXECUTE","SEAL")
FORBIDDEN = [(s,t) for s in SOURCES for t in TARGETS]
DANGEROUS = (
    "authorized","permit","execute","admit","seal","approved","authority",
    "authority_id","decision","status","human_approval","binding","permitted",
)

def _no_auth(obj) -> None:
    if hasattr(obj, "authority_established"):
        assert obj.authority_established() is False
    if hasattr(obj, "execution_permitted"):
        assert obj.execution_permitted() is False
    if hasattr(obj, "is_authoritative"):
        assert obj.is_authoritative() is False
    if hasattr(obj, "permits_execution"):
        assert obj.permits_execution() is False

@pytest.fixture
def mon():
    return AlignmentMonitor()

@pytest.mark.parametrize("source,target", FORBIDDEN)
def test_forbidden_transition_matrix(mon, source, target):
    if source == "STABLE":
        obj = mon.measure([1.0]*6)
        assert obj.classification.value == "STABLE"
    elif source == "DRIFT":
        obj = mon.measure([0.0]*6)
        assert obj.classification.value == "HIGH_DRIFT"
    elif source == "UNKNOWN":
        obs, finding, report = mon.full_hidden_edge_observation()
        assert report.has_unknown_edge
        obj = finding
    elif source == "EVIDENCE":
        obj = mon.observe([0.8]*6, evidence_reference="ev-hash-001")
    elif source == "OBSERVATION":
        obj = mon.observe([0.9]*6)
    elif source == "SIGNATURE":
        obj = mon.observe([0.9]*6, context={"valid_signature":"sig","valid_hash":"h","HSM_reference":"hsm"})
    elif source == "HALT":
        steps = [("ORIGIN", VisibilityLevel.OBSERVABLE, "start"), ("HALT", VisibilityLevel.HALTED, "halted")]
        obj = mon.finding_from_observation(mon.observe([0.5]*6, visibility_steps=steps))
    elif source == "REJECT":
        steps = [("ORIGIN", VisibilityLevel.OBSERVABLE, "start"), ("REJECT", VisibilityLevel.UNKNOWN, "rejected")]
        obj = mon.observe([0.5]*6, visibility_steps=steps)
    else:
        obs, finding, report = mon.full_hidden_edge_observation()
        obj = obs
    _no_auth(obj)
    _no_auth(mon)
    assert not hasattr(mon, "authorize")
    assert not hasattr(mon, "permit")
    assert not hasattr(mon, "execute")
    assert not hasattr(mon, "seal")

@pytest.mark.parametrize("payload", [
    {"authorized": True}, {"permit": True}, {"execute": True}, {"seal": True},
    {"admit": True}, {"authority_id": "auth-001"}, {"decision": "APPROVE"},
    {"status": "PERMITTED"}, {"human_approval": True}, {"binding": True},
    {"permitted": True}, {"meta": {"authorized": True, "execute": True}},
], ids=lambda p: str(list(p.keys())[0])[:20])
def test_dangerous_payload_cannot_authorize(mon, payload):
    obs = mon.observe([0.85]*6, context=payload)
    _no_auth(obs)
    for key in DANGEROUS:
        assert key not in obs.context
    _no_auth(mon.finding_from_observation(obs))

def test_unknown_cannot_become_permitted(mon):
    obs, finding, report = mon.full_hidden_edge_observation()
    assert report.has_unknown_edge
    assert report.authority_established is False
    assert obs.authority_established() is False
    assert finding.is_authoritative() is False

def test_stable_does_not_generate_permit(mon):
    m = mon.measure([1.0]*6)
    assert m.classification.value == "STABLE"
    d = m.to_dict()
    assert "permit" not in d and "authorized" not in d
    _no_auth(m)

def test_signature_is_not_authority(mon):
    obs = mon.observe([0.95]*6, context={
        "valid_signature": "ed25519", "valid_hash": "sha256",
        "HSM_reference": "hsm", "TPM_reference": "tpm", "authorized": True})
    _no_auth(obs)
    assert "authorized" not in obs.context

def test_stage3_matrix_size():
    assert len(FORBIDDEN) == 45
