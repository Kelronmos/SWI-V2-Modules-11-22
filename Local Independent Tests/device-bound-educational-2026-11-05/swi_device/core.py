import hashlib
import json
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def digest(data):
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def save_record(category, record):
    folder = ROOT / "evidence" / category
    folder.mkdir(parents=True, exist_ok=True)
    record = dict(record)
    record["record_hash"] = digest(record)
    path = folder / (record.get("id", str(uuid.uuid4())) + ".json")
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    return record

def register_device(device_id, platform, public_key_fingerprint,
                    hardware_level="UNKNOWN", attestation="UNAVAILABLE"):
    if not device_id or not public_key_fingerprint:
        raise ValueError("Device ID and public key fingerprint required")
    allowed = {"android", "linux", "macos", "windows"}
    if platform not in allowed:
        raise ValueError("Unsupported platform")
    return save_record("devices", {
        "id": device_id,
        "type": "DEVICE_REGISTRATION",
        "platform": platform,
        "public_key_fingerprint": public_key_fingerprint,
        "hardware_level": hardware_level,
        "attestation": attestation,
        "status": "REGISTERED_NOT_INDEPENDENTLY_VERIFIED",
        "created_utc": time.time()
    })

def record_admission(user_id, device_id, consent, ownership_claim,
                     research_attribution, cost_limit, currency):
    if not user_id or not device_id:
        raise ValueError("User and device identifiers required")
    if not ownership_claim or not currency:
        raise ValueError("Ownership claim and currency required")
    if cost_limit < 0:
        raise ValueError("Negative cost limit")
    return save_record("admissions", {
        "id": str(uuid.uuid4()),
        "type": "USER_ADMISSION",
        "user_id": user_id,
        "device_id": device_id,
        "consent": bool(consent),
        "ownership_claim": ownership_claim,
        "ownership_status": "USER_ASSERTED_NOT_LEGALLY_VERIFIED",
        "research_attribution": research_attribution,
        "cost_limit": cost_limit,
        "currency": currency,
        "created_utc": time.time()
    })

def authorize(request, expected_device, expected_workflow, expected_action):
    """Demonstration fail-closed checks. NOT the V1/V2 authorization spine."""
    checks = [
        (request.get("human_authenticated") is True,
         "HUMAN_AUTHENTICATION_NOT_ESTABLISHED"),
        (request.get("authority_verified") is True,
         "AUTHORITY_SOURCE_NOT_VERIFIED"),
        (request.get("consent") is True, "CONSENT_REQUIRED"),
        (request.get("device_id") == expected_device, "DEVICE_MISMATCH"),
        (request.get("workflow_id") == expected_workflow, "WORKFLOW_MISMATCH"),
        (request.get("action_id") == expected_action, "ACTION_MISMATCH"),
        (isinstance(request.get("cost"), (int, float))
         and 0 <= request["cost"] <= request.get("cost_limit", -1),
         "COST_LIMIT_EXCEEDED"),
        (bool(request.get("evidence_hash")), "EVIDENCE_REQUIRED")
    ]
    for passed, reason in checks:
        if not passed:
            return {
                "decision": "PAUSE",
                "reason": reason,
                "EXECUTE": False,
                "PRODUCTION_AUTHORIZED": False
            }
    return {
        "decision": "PROCEED_SIMULATION",
        "reason": "all_local_checks_passed",
        "EXECUTE": False,  # demonstration never executes protected action
        "PRODUCTION_AUTHORIZED": False
    }

def record_key_rotation(device_id, old_fingerprint, new_fingerprint):
    return save_record("rotations", {
        "id": str(uuid.uuid4()),
        "type": "KEY_ROTATION",
        "device_id": device_id,
        "old_fingerprint": old_fingerprint,
        "new_fingerprint": new_fingerprint,
        "status": "RECORDED_NOT_INDEPENDENTLY_VERIFIED",
        "created_utc": time.time()
    })
