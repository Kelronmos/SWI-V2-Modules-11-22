"""Research harness: separate camera/model claims from authenticated telemetry.

This is an isolated test harness, NOT a production actuator or replacement SWI gate.
It demonstrates a fail-closed policy for physical actions.
"""
from __future__ import annotations
import base64, hashlib, json, math, time
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

class Decision(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    HALT = "HALT"

@dataclass(frozen=True)
class Telemetry:
    sensor_id: str
    device_id: str
    measurement: str
    value: float
    unit: str
    observed_at: float
    calibration_id: str
    signature_b64: str
    def payload(self) -> bytes:
        obj = {"sensor_id":self.sensor_id,"device_id":self.device_id,"measurement":self.measurement,
               "value":self.value,"unit":self.unit,"observed_at":self.observed_at,
               "calibration_id":self.calibration_id}
        return json.dumps(obj, sort_keys=True, separators=(",",":"), allow_nan=False).encode()

@dataclass(frozen=True)
class Case:
    name: str
    visual_observation: Optional[str] = None
    model_explanation: Optional[str] = None
    telemetry: Optional[Telemetry] = None

@dataclass
class Result:
    case: str
    decision: str
    reason: str
    execution_allowed: bool
    execution_occurred: bool
    observation_present: bool
    model_explanation_present: bool
    telemetry_present: bool
    evidence_hash: str
    # telemetry metadata (added after schema extension)
    sensor_id: Optional[str] = None
    observed_at: Optional[float] = None
    signature_valid: Optional[bool] = None

def _verify(telemetry: Telemetry, public_key: Ed25519PublicKey) -> bool:
    try:
        sig = base64.b64decode(telemetry.signature_b64)
        public_key.verify(sig, telemetry.payload())
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False

def evaluate(case: Case, public_key: Ed25519PublicKey, now: float, max_age_s: float = 30.0) -> Result:
    """Fail-closed evaluator.

    - Pure visual or pure mathematical explanation → UNKNOWN (no execution)
    - Missing / stale / wrong-identity / bad-signature telemetry → HALT
    - Fresh, correctly signed, matching sensor → PASS (simulation only)
    """
    obs = case.visual_observation is not None
    model = case.model_explanation is not None
    tel = case.telemetry is not None

    if not tel:
        return Result(
            case=case.name, decision=Decision.UNKNOWN.value,
            reason="no authenticated telemetry; observation or model only",
            execution_allowed=False, execution_occurred=False,
            observation_present=obs, model_explanation_present=model,
            telemetry_present=False, evidence_hash=_hash(case),
        )

    t = case.telemetry
    age = now - t.observed_at
    if age > max_age_s or age < 0:
        return Result(
            case=case.name, decision=Decision.HALT.value,
            reason=f"stale or future telemetry (age={age:.1f}s)",
            execution_allowed=False, execution_occurred=False,
            observation_present=obs, model_explanation_present=model,
            telemetry_present=True, evidence_hash=_hash(case),
            sensor_id=t.sensor_id, observed_at=t.observed_at, signature_valid=None,
        )

    valid = _verify(t, public_key)
    if not valid:
        return Result(
            case=case.name, decision=Decision.HALT.value,
            reason="telemetry signature invalid or sensor identity mismatch",
            execution_allowed=False, execution_occurred=False,
            observation_present=obs, model_explanation_present=model,
            telemetry_present=True, evidence_hash=_hash(case),
            sensor_id=t.sensor_id, observed_at=t.observed_at, signature_valid=False,
        )

    # PASS path is simulation only — no real actuator is called
    return Result(
        case=case.name, decision=Decision.PASS.value,
        reason="fresh signed telemetry accepted (simulation)",
        execution_allowed=True, execution_occurred=False,  # never occurs in this harness
        observation_present=obs, model_explanation_present=model,
        telemetry_present=True, evidence_hash=_hash(case),
        sensor_id=t.sensor_id, observed_at=t.observed_at, signature_valid=True,
    )

def _hash(case: Case) -> str:
    blob = json.dumps({
        "name": case.name,
        "visual": case.visual_observation,
        "model": case.model_explanation,
        "telemetry": case.telemetry.payload().decode() if case.telemetry else None,
    }, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()
