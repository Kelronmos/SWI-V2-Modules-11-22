"""Executable pre-R response-boundary experiment.

This uses deterministic SHA-256 integrity over canonical JSON. It does not claim
production authenticity, production key custody, semantic truth, or a module seal.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, json
from typing import Any, FrozenSet, Mapping

def _utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

def canonicalize(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def sha256(value: Any) -> str:
    return hashlib.sha256(canonicalize(value).encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class RequestBinding:
    request_id: str
    principal: str
    requested_action: str
    resource: str
    destination: str
    expires_at: datetime
    def canonical(self):
        return {"request_id": self.request_id, "principal": self.principal,
                "requested_action": self.requested_action, "resource": self.resource,
                "destination": self.destination, "expires_at": _utc(self.expires_at).isoformat()}
    @property
    def digest(self): return sha256(self.canonical())

@dataclass(frozen=True)
class AuthorityScope:
    principal: str
    actions: FrozenSet[str]
    resources: FrozenSet[str]
    destinations: FrozenSet[str]
    expires_at: datetime
    revoked: bool = False
    def permits(self, action, resource, destination, principal, now):
        now = _utc(now)
        return (not self.revoked and principal == self.principal and
                action in self.actions and resource in self.resources and
                destination in self.destinations and now < _utc(self.expires_at))
    def contains(self, other):
        return (other.principal == self.principal and other.actions <= self.actions and
                other.resources <= self.resources and other.destinations <= self.destinations and
                _utc(other.expires_at) <= _utc(self.expires_at) and
                (not other.revoked or self.revoked))
    def canonical(self):
        return {"principal": self.principal, "actions": sorted(self.actions),
                "resources": sorted(self.resources), "destinations": sorted(self.destinations),
                "expires_at": _utc(self.expires_at).isoformat(), "revoked": self.revoked}

@dataclass(frozen=True)
class EvidenceCarrier:
    evidence_id: str
    evidence_type: str
    payload: Any
    def canonical(self):
        return {"evidence_id": self.evidence_id, "evidence_type": self.evidence_type, "payload": self.payload}

@dataclass(frozen=True)
class CertificateScope:
    certificate_id: str
    actions: FrozenSet[str]
    resources: FrozenSet[str]
    destinations: FrozenSet[str]
    def permits(self, action, resource, destination):
        return action in self.actions and resource in self.resources and destination in self.destinations

@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    request_id: str
    digest: str

class IntegrityVerifier:
    @staticmethod
    def digest(material: Mapping[str, Any]) -> str:
        return sha256(dict(material))
    @staticmethod
    def verify(material, expected_digest: str) -> bool:
        return IntegrityVerifier.digest(material) == expected_digest

@dataclass(frozen=True)
class ResponseEnvelope:
    response_id: str
    request: RequestBinding
    authority: AuthorityScope
    result: Any
    evidence: EvidenceCarrier | None
    destination: str
    issued_at: datetime
    expires_at: datetime
    integrity_digest: str = field(default="")
    def protected_material(self):
        return {"response_id": self.response_id, "request": self.request.canonical(),
                "authority": self.authority.canonical(), "result": self.result,
                "evidence": None if self.evidence is None else self.evidence.canonical(),
                "destination": self.destination, "issued_at": _utc(self.issued_at).isoformat(),
                "expires_at": _utc(self.expires_at).isoformat()}
    def with_integrity(self):
        return ResponseEnvelope(self.response_id, self.request, self.authority, self.result,
            self.evidence, self.destination, self.issued_at, self.expires_at,
            IntegrityVerifier.digest(self.protected_material()))

class BoundaryDecision:
    ADMIT = "ADMIT"
    REJECT = "REJECT"
    HALT = "HALT"

@dataclass(frozen=True)
class ReturnGate:
    require_evidence: bool = True
    def evaluate(self, envelope, originating_request, originating_authority, now,
                 *, expected_destination, action, resource, principal, policy_allows=True):
        now = _utc(now)
        if envelope.request.digest != originating_request.digest: return BoundaryDecision.REJECT
        if not originating_authority.contains(envelope.authority): return BoundaryDecision.REJECT
        if not originating_authority.permits(action, resource, expected_destination, principal, now): return BoundaryDecision.REJECT
        if envelope.destination != expected_destination: return BoundaryDecision.REJECT
        if envelope.destination not in originating_authority.destinations: return BoundaryDecision.REJECT
        if now >= _utc(envelope.expires_at): return BoundaryDecision.REJECT
        if self.require_evidence and envelope.evidence is None: return BoundaryDecision.REJECT
        if not policy_allows: return BoundaryDecision.REJECT
        if not IntegrityVerifier.verify(envelope.protected_material(), envelope.integrity_digest): return BoundaryDecision.REJECT
        return BoundaryDecision.ADMIT

def build_response(*, response_id, request, authority, result, evidence, destination, issued_at, expires_at):
    return ResponseEnvelope(response_id, request, authority, result, evidence, destination, issued_at, expires_at).with_integrity()
