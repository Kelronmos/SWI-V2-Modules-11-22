"""Adversarial and positive-control tests for device binding demonstrator."""
import time
import pytest
from swi_device_bind.models import Session
from swi_device_bind.evidence import EvidenceBinder
from swi_device_bind.status import CapStatus
from swi_device_bind import adapters as A

@pytest.fixture
def session():
    return Session.create("wf-test", "act-test", established=True)

@pytest.fixture
def binder():
    return EvidenceBinder()

def test_device_discovery_pass(session, binder):
    obs = A.device_discovery(session)
    bound = binder.bind(obs, session)
    assert bound.status == CapStatus.PASS.value
    assert bound.evidence_sha256

def test_missing_session(binder):
    s = Session.create("wf", "act", established=False)
    obs = A.device_discovery(s)
    bound = binder.bind(obs, s)
    assert bound.error == "MISSING_USER_SESSION"

def test_wrong_session_binding(session, binder):
    obs = A.device_discovery(session)
    other = Session.create("wf-test", "act-test")
    obs.session_id = other.session_id
    bound = binder.bind(obs, session)
    assert bound.error == "WRONG_SESSION_BINDING"

def test_wrong_workflow(session, binder):
    obs = A.device_discovery(session)
    obs.workflow_id = "other-wf"
    bound = binder.bind(obs, session)
    assert bound.error == "WRONG_WORKFLOW_BINDING"

def test_wrong_action(session, binder):
    obs = A.device_discovery(session)
    obs.action_id = "other-act"
    bound = binder.bind(obs, session)
    assert bound.error == "WRONG_ACTION_BINDING"

def test_stale_observation(session, binder):
    obs = A.device_discovery(session)
    obs.timestamp_utc = time.time() - 9999
    bound = binder.bind(obs, session)
    assert bound.error == "STALE_OBSERVATION"

def test_camera_permission_denied(session):
    obs = A.camera_observation(session, permission_granted=False)
    assert obs.error == "CAMERA_PERMISSION_DENIED"

def test_camera_not_on_device(session):
    obs = A.camera_observation(session)
    assert obs.status in (CapStatus.BLOCKED.value, CapStatus.NOT_IMPLEMENTED.value)

def test_face_detector_unavailable(session):
    assert A.face_presence(session, detector_available=False).error == "FACE_DETECTOR_UNAVAILABLE"

def test_no_face(session):
    assert A.face_presence(session, detector_available=True, faces=0).status == CapStatus.FAIL.value

def test_uncertain_face(session):
    assert A.face_presence(session, detector_available=True, faces=None).error == "UNCERTAIN_FACE_RESULT"

def test_hand_unavailable(session):
    assert A.hand_landmarks(session, detector_available=False).error == "HAND_DETECTOR_UNAVAILABLE"

def test_occluded_fingers(session):
    assert A.hand_landmarks(session, detector_available=True, occluded=True).error == "OCCLUDED_OR_INCOMPLETE_LANDMARKS"

def test_mic_permission_denied(session):
    assert A.microphone(session, permission_granted=False).error == "MICROPHONE_PERMISSION_DENIED"

def test_speaker_without_confirmation(session):
    assert A.speaker(session, playback_cmd_ok=True, human_heard=None).error == "SPEAKER_PLAYBACK_WITHOUT_HUMAN_CONFIRMATION"

def test_keyboard_mismatch(session):
    assert A.keyboard_challenge(session, expected="SWI", received="WRONG").error == "KEYBOARD_CHALLENGE_MISMATCH"

def test_fingerprint_cancelled(session):
    assert A.biometric(session, adapter_available=True, outcome="cancelled").error == "FINGERPRINT_CANCELLED"

def test_fingerprint_rejected(session):
    assert A.biometric(session, adapter_available=True, outcome="rejected").error == "FINGERPRINT_REJECTED"

def test_fingerprint_unavailable(session):
    assert A.biometric(session, adapter_available=False).error == "FINGERPRINT_ADAPTER_UNAVAILABLE"

def test_network_disconnected(session):
    assert A.network(session, connected=False).error == "NETWORK_DISCONNECTED"

def test_dns_failure(session):
    assert A.network(session, connected=True, dns_ok=False).error == "DNS_FAILURE"

def test_https_failure(session):
    assert A.network(session, connected=True, dns_ok=True, https_ok=False).error == "HTTPS_FAILURE"

def test_clock_discrepancy(session):
    assert A.device_time(session, skew_seconds=500).error == "DEVICE_CLOCK_DISCREPANCY"

def test_no_hardcoded_five_fingers(session):
    obs = A.hand_landmarks(session, detector_available=True, finger_count=3)
    assert obs.result.get("fingers") == 3 and obs.result.get("hardcoded") is False

def test_face_not_recognition(session):
    assert A.face_presence(session, detector_available=True, faces=1).result.get("recognition") is False

def test_offline_runner_no_fake_pass():
    from swi_device_bind.runner import run_offline_demo
    report = run_offline_demo()
    assert report["PROVEN"] == "NO" and report["PRODUCTION_AUTHORIZED"] == "NO"
    cam = next(r for r in report["capability_matrix"] if r["capability"] == "camera")
    assert cam["status"] != "PASS"
