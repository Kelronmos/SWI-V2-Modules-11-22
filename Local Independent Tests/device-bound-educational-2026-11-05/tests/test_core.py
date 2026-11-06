"""Package-local tests for educational device-bound demo.
NOT integration tests against the V2 authorization spine.
"""
import pytest
from swi_device.core import authorize, digest, record_admission, record_key_rotation

def request(**updates):
    data = {
        "human_authenticated": False,
        "authority_verified": False,
        "consent": True,
        "device_id": "D1",
        "workflow_id": "W1",
        "action_id": "A1",
        "cost": 5,
        "cost_limit": 10,
        "evidence_hash": "abc123",
    }
    data.update(updates)
    return data

def test_missing_human_authentication_pauses():
    result = authorize(request(), "D1", "W1", "A1")
    assert result["decision"] == "PAUSE"
    assert result["EXECUTE"] is False
    assert result.get("PRODUCTION_AUTHORIZED") is False

def test_unverified_authority_pauses():
    result = authorize(request(human_authenticated=True), "D1", "W1", "A1")
    assert result["reason"] == "AUTHORITY_SOURCE_NOT_VERIFIED"
    assert result["EXECUTE"] is False

@pytest.mark.parametrize("field,value,reason", [
    ("device_id", "D2", "DEVICE_MISMATCH"),
    ("workflow_id", "W2", "WORKFLOW_MISMATCH"),
    ("action_id", "A2", "ACTION_MISMATCH"),
    ("consent", False, "CONSENT_REQUIRED"),
    ("cost", 20, "COST_LIMIT_EXCEEDED"),
    ("evidence_hash", "", "EVIDENCE_REQUIRED"),
])
def test_invalid_conditions_pause(field, value, reason):
    data = request(human_authenticated=True, authority_verified=True)
    data[field] = value
    result = authorize(data, "D1", "W1", "A1")
    assert result["reason"] == reason
    assert result["EXECUTE"] is False

def test_conditions_met_still_does_not_execute():
    result = authorize(
        request(human_authenticated=True, authority_verified=True),
        "D1", "W1", "A1",
    )
    assert result["EXECUTE"] is False
    assert result.get("PRODUCTION_AUTHORIZED") is False

def test_digest_stable():
    a = digest({"x": 1, "y": 2})
    b = digest({"y": 2, "x": 1})
    assert a == b
