"""Offline demonstrator runner — no fabricated hardware PASS."""
from __future__ import annotations
import json, time
from pathlib import Path
from .models import Session
from .registry import CapabilityRegistry
from .evidence import EvidenceBinder
from . import adapters as A

GREETING = "WELCOME TO SWI"

def run_offline_demo(out_dir: Path | None = None) -> dict:
    session = Session.create(workflow_id="device-bind-demo", action_id="observe-capabilities")
    reg = CapabilityRegistry()
    binder = EvidenceBinder()
    tests = [
        A.device_discovery(session),
        A.user_session_check(session),
        A.camera_observation(session),
        A.face_presence(session, detector_available=False),
        A.hand_landmarks(session, detector_available=False),
        A.microphone(session),
        A.speaker(session, playback_cmd_ok=False),
        A.keyboard_challenge(session, expected="SWI", received=None),
        A.biometric(session, adapter_available=False),
        A.network(session),
        A.device_time(session),
    ]
    for obs in tests:
        reg.record(binder.bind(obs, session))
    report = {
        "greeting": GREETING,
        "schema": "SWI_DEVICE_BINDING_REPORT_0.1",
        "PROVEN": "NO",
        "SEALED": "NO",
        "PRODUCTION_AUTHORIZED": "NO",
        "session_id": session.session_id,
        "workflow_id": session.workflow_id,
        "action_id": session.action_id,
        "environment": "offline_non_android" if not A.is_android_termux() else "android_termux",
        "capability_matrix": reg.matrix(),
        "status_counts": reg.summary_counts(),
        "note": "Physical-device tests remain NOT_RUN/BLOCKED until executed on Android/Termux.",
        "generated_utc": time.time(),
    }
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "device_binding_report.json"
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        report["report_path"] = str(path)
    return report
