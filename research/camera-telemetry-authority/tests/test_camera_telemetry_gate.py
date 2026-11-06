"""Camera telemetry authority research tests — isolated harness only."""
from __future__ import annotations
import base64
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import pytest
from camera_telemetry_gate import Case, Decision, Telemetry, evaluate

@pytest.fixture
def keypair():
    priv = Ed25519PrivateKey.generate()
    return priv, priv.public_key()

def make_tel(priv, sensor_id="S1", device_id="D1", value=1.0, observed_at=None):
    observed_at = time.time() if observed_at is None else observed_at
    unsigned = Telemetry(sensor_id, device_id, "magnetic_field", value, "mT", observed_at, "CAL-1", "")
    sig = base64.b64encode(priv.sign(unsigned.payload())).decode()
    return Telemetry(sensor_id, device_id, "magnetic_field", value, "mT", observed_at, "CAL-1", sig)

def test_fresh_signed_telemetry_pass(keypair):
    priv, pub = keypair
    t = make_tel(priv)
    r = evaluate(Case("T01", telemetry=t), pub, time.time())
    assert r.decision == Decision.PASS.value
    assert r.execution_allowed is True
    assert r.execution_occurred is False

def test_camera_only_unknown(keypair):
    _, pub = keypair
    r = evaluate(Case("T02", visual_observation="door open"), pub, time.time())
    assert r.decision == Decision.UNKNOWN.value
    assert r.execution_allowed is False

def test_math_only_unknown(keypair):
    _, pub = keypair
    r = evaluate(Case("T03", model_explanation="1+1=2"), pub, time.time())
    assert r.decision == Decision.UNKNOWN.value

def test_stale_halt(keypair):
    priv, pub = keypair
    t = make_tel(priv, observed_at=time.time() - 120)
    r = evaluate(Case("T04", telemetry=t), pub, time.time())
    assert r.decision == Decision.HALT.value

def test_wrong_identity_still_verifies_payload(keypair):
    # signature covers sensor_id; wrong key fails
    priv, pub = keypair
    other = Ed25519PrivateKey.generate()
    t = make_tel(other)
    r = evaluate(Case("T05", telemetry=t), pub, time.time())
    assert r.decision == Decision.HALT.value

def test_tampered_signature_halt(keypair):
    priv, pub = keypair
    t = make_tel(priv)
    bad = Telemetry(t.sensor_id, t.device_id, t.measurement, t.value, t.unit, t.observed_at, t.calibration_id, "AAAA")
    r = evaluate(Case("T06", telemetry=bad), pub, time.time())
    assert r.decision == Decision.HALT.value

def test_replay_same_decision(keypair):
    priv, pub = keypair
    t = make_tel(priv)
    c = Case("T07", telemetry=t)
    now = time.time()
    a = evaluate(c, pub, now)
    b = evaluate(c, pub, now)
    assert a.decision == b.decision
    assert a.evidence_hash == b.evidence_hash
