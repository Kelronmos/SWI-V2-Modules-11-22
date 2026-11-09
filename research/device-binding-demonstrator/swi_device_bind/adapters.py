"""Device observation adapters.

Off-device / non-Termux environment: return BLOCKED or NOT_IMPLEMENTED honestly.
Never invent PASS for camera, face, hand, mic, biometric, or speaker hearing.
"""
from __future__ import annotations
import platform, sys, time, uuid, os
from typing import Optional
from .models import Observation, Session
from .status import CapStatus, Lifecycle

SOFT = "0.1.0-demo"
ADAPTER = "0.1.0-offline"

def _base(session: Session, capability: str, **kw) -> Observation:
    return Observation(
        capability=capability,
        status=kw.get("status", CapStatus.NOT_RUN.value),
        lifecycle=kw.get("lifecycle", Lifecycle.NOT_DISCOVERED.value),
        session_id=session.session_id,
        device_obs_id=str(uuid.uuid4()),
        workflow_id=session.workflow_id,
        action_id=session.action_id,
        software_version=SOFT,
        adapter_version=ADAPTER,
        timestamp_utc=kw.get("timestamp_utc", time.time()),
        timezone=time.tzname[0] if time.tzname else "UTC",
        permission_state=kw.get("permission_state", "UNKNOWN"),
        result=kw.get("result", {}),
        error=kw.get("error"),
    )

def is_android_termux() -> bool:
    return os.environ.get("PREFIX", "").endswith("com.termux") or "ANDROID_ROOT" in os.environ

def device_discovery(session: Session) -> Observation:
    info = {
        "system": platform.system(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "android_termux": is_android_termux(),
        "note": "Host facts only; not proof of human identity",
    }
    return _base(session, "device_discovery", status=CapStatus.PASS.value,
                 lifecycle=Lifecycle.OBSERVED.value, permission_state="N/A", result=info)

def camera_observation(session: Session, permission_granted: Optional[bool] = None) -> Observation:
    if permission_granted is False:
        return _base(session, "camera", status=CapStatus.FAIL.value, permission_state="DENIED",
                     error="CAMERA_PERMISSION_DENIED", result={"cameras": []})
    if not is_android_termux():
        return _base(session, "camera", status=CapStatus.BLOCKED.value, permission_state="UNKNOWN",
                     error="NOT_ON_ANDROID_DEVICE", lifecycle=Lifecycle.NOT_DISCOVERED.value,
                     result={"cameras": [], "note": "Physical Android required"})
    return _base(session, "camera", status=CapStatus.NOT_IMPLEMENTED.value,
                 error="CAMERA_ADAPTER_REQUIRES_TERMUX_API_OR_NATIVE", permission_state="UNKNOWN", result={})

def face_presence(session: Session, detector_available: bool = False, faces: Optional[int] = None) -> Observation:
    if not detector_available:
        return _base(session, "face_presence", status=CapStatus.UNKNOWN.value,
                     error="FACE_DETECTOR_UNAVAILABLE", result={"face_count": None, "recognition": False})
    if faces is None:
        return _base(session, "face_presence", status=CapStatus.UNKNOWN.value,
                     error="UNCERTAIN_FACE_RESULT", result={"face_count": None})
    if faces == 0:
        return _base(session, "face_presence", status=CapStatus.FAIL.value, lifecycle=Lifecycle.OBSERVED.value,
                     result={"face_count": 0, "recognition": False})
    return _base(session, "face_presence", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value,
                 result={"face_count": faces, "recognition": False, "note": "Presence only — not identity matching"})

def hand_landmarks(session: Session, detector_available: bool = False, finger_count: Optional[int] = None, occluded: bool = False) -> Observation:
    if not detector_available:
        return _base(session, "hand_landmarks", status=CapStatus.UNKNOWN.value,
                     error="HAND_DETECTOR_UNAVAILABLE", result={"fingers": None})
    if occluded or finger_count is None:
        return _base(session, "hand_landmarks", status=CapStatus.UNKNOWN.value,
                     error="OCCLUDED_OR_INCOMPLETE_LANDMARKS", result={"fingers": None})
    if finger_count < 0 or finger_count > 5:
        return _base(session, "hand_landmarks", status=CapStatus.ERROR.value,
                     error="INVALID_FINGER_COUNT", result={"fingers": finger_count})
    return _base(session, "hand_landmarks", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value,
                 result={"fingers": finger_count, "hardcoded": False})

def microphone(session: Session, permission_granted: Optional[bool] = None, recording_ok: Optional[bool] = None) -> Observation:
    if permission_granted is False:
        return _base(session, "microphone", status=CapStatus.FAIL.value, permission_state="DENIED",
                     error="MICROPHONE_PERMISSION_DENIED", result={})
    if not is_android_termux():
        return _base(session, "microphone", status=CapStatus.BLOCKED.value, error="NOT_ON_ANDROID_DEVICE", result={})
    if recording_ok is False:
        return _base(session, "microphone", status=CapStatus.FAIL.value, permission_state="GRANTED",
                     error="EMPTY_OR_FAILED_RECORDING", result={})
    return _base(session, "microphone", status=CapStatus.NOT_IMPLEMENTED.value,
                 error="MIC_ADAPTER_REQUIRES_TERMUX_API", permission_state="UNKNOWN", result={})

def speaker(session: Session, playback_cmd_ok: bool = False, human_heard: Optional[bool] = None) -> Observation:
    if not playback_cmd_ok:
        return _base(session, "speaker", status=CapStatus.NOT_RUN.value,
                     result={"playback_cmd": False, "human_confirmed": None})
    if human_heard is None:
        return _base(session, "speaker", status=CapStatus.UNKNOWN.value,
                     error="SPEAKER_PLAYBACK_WITHOUT_HUMAN_CONFIRMATION",
                     result={"playback_cmd": True, "human_confirmed": None})
    if human_heard is False:
        return _base(session, "speaker", status=CapStatus.FAIL.value,
                     result={"playback_cmd": True, "human_confirmed": False})
    return _base(session, "speaker", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value,
                 result={"playback_cmd": True, "human_confirmed": True})

def keyboard_challenge(session: Session, expected: str, received: Optional[str] = None) -> Observation:
    if received is None:
        return _base(session, "keyboard", status=CapStatus.NOT_RUN.value,
                     result={"expected": expected, "received": None})
    if received != expected:
        return _base(session, "keyboard", status=CapStatus.FAIL.value, error="KEYBOARD_CHALLENGE_MISMATCH",
                     lifecycle=Lifecycle.OBSERVED.value, result={"expected": expected, "received": received})
    return _base(session, "keyboard", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value,
                 result={"expected": expected, "received": received, "scope": "application_input_only"})

def biometric(session: Session, adapter_available: bool = False, outcome: Optional[str] = None) -> Observation:
    if not adapter_available:
        return _base(session, "biometric", status=CapStatus.BLOCKED.value,
                     error="FINGERPRINT_ADAPTER_UNAVAILABLE", result={"templates_accessed": False})
    if outcome == "cancelled":
        return _base(session, "biometric", status=CapStatus.FAIL.value, error="FINGERPRINT_CANCELLED",
                     result={"templates_accessed": False})
    if outcome == "rejected":
        return _base(session, "biometric", status=CapStatus.FAIL.value, error="FINGERPRINT_REJECTED",
                     result={"templates_accessed": False})
    if outcome == "success":
        return _base(session, "biometric", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value,
                     result={"templates_accessed": False, "method": "android_biometric_prompt"})
    return _base(session, "biometric", status=CapStatus.NOT_RUN.value, result={"templates_accessed": False})

def network(session: Session, connected: Optional[bool] = None, dns_ok: Optional[bool] = None, https_ok: Optional[bool] = None) -> Observation:
    if connected is False:
        return _base(session, "network", status=CapStatus.FAIL.value, error="NETWORK_DISCONNECTED", result={})
    if dns_ok is False:
        return _base(session, "network", status=CapStatus.FAIL.value, error="DNS_FAILURE", result={"connected": connected})
    if https_ok is False:
        return _base(session, "network", status=CapStatus.FAIL.value, error="HTTPS_FAILURE",
                     result={"connected": connected, "dns_ok": dns_ok})
    if connected is None:
        return _base(session, "network", status=CapStatus.NOT_RUN.value, result={})
    return _base(session, "network", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value,
                 result={"connected": connected, "dns_ok": dns_ok, "https_ok": https_ok,
                         "note": "Reachability ≠ SWI authorization"})

def device_time(session: Session, skew_seconds: Optional[float] = None) -> Observation:
    local = time.time()
    result = {"device_utc": local, "timezone": time.tzname[0] if time.tzname else "UTC"}
    if skew_seconds is None:
        return _base(session, "device_time", status=CapStatus.UNKNOWN.value, error="NO_TRUSTED_TIME_SOURCE",
                     lifecycle=Lifecycle.OBSERVED.value, result=result)
    result["skew_seconds"] = skew_seconds
    if abs(skew_seconds) > 120:
        return _base(session, "device_time", status=CapStatus.REVIEW.value, error="DEVICE_CLOCK_DISCREPANCY",
                     lifecycle=Lifecycle.OBSERVED.value, result=result)
    return _base(session, "device_time", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value, result=result)

def user_session_check(session: Session) -> Observation:
    if not session.established:
        return _base(session, "user_session", status=CapStatus.FAIL.value, error="MISSING_USER_SESSION",
                     result={"established": False})
    return _base(session, "user_session", status=CapStatus.PASS.value, lifecycle=Lifecycle.OBSERVED.value,
                 result={"established": True, "session_id": session.session_id,
                         "note": "Session reference only — not Android UID identity"})
