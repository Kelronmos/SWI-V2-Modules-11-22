"""Executable pre-R response-boundary experiment.

This uses deterministic SHA-256 integrity over canonical JSON. It does not claim
production authenticity, production key custody, semantic truth, or a module seal.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, FrozenSet, Mapping, Optional


def _utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def canonicalize(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )


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

    def canonical(self) -> dict:
        return {
            "request_id": self.request_id,
            "principal": self.principal,
            "requested_action": self.requested_action,
            "resource": self.resource,
            "destination": self.destination,
            "expires_at": _utc(self.expires_at).isoformat(),
        }

    @property
    def digest(self) -> str:
        return sha256(self.canonical())


@dataclass(frozen=True)
class AuthorityScope:
    principal: str
    actions: FrozenSet[str]
    resources: FrozenSet[str]
    destinations: FrozenSet[str]
    expires_at: datetime
    revoked: bool = False

    def permits(
        self,
        action: str,
        resource: str,
        destination: str,
        principal: str,
        now: datetime,
    ) -> bool:
        now = _utc(now)
        return (
            not self.revoked
            and principal == self.principal
            and action in self.actions
            and resource in self.resources
            and destination in self.destinations
            and now < _utc(self.expires_at)
        )

    def contains(self, other: "AuthorityScope") -> bool:
        return (
            other.principal == self.principal
            and other.actions <= self.actions
            and other.resources <= self.resources
            and other.destinations <= self.destinations
            and _utc(other.expires_at) <= _utc(self.expires_at)
            and (not other.revoked or self.revoked)
        )

    def canonical(self) -> dict:
        return {
            "principal": self.principal,
            "actions": sorted(self.actions),
            "resources": sorted(self.resources),
            "destinations": sorted(self.destinations),
            "expires_at": _utc(self.expires_at).isoformat(),
            "revoked": self.revoked,
        }


@dataclass(frozen=True)
class EvidenceCarrier:
    evidence_id: str
    evidence_type: str
    payload_reference: str

    def canonical(self) -> dict:
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type,
            "payload_reference": self.payload_reference,
        }


class IntegrityVerifier:
    @staticmethod
    def digest(material: Mapping[str, Any]) -> str:
        return sha256(dict(material))

    @staticmethod
    def verify(material: Mapping[str, Any], expected: str) -> bool:
        return IntegrityVerifier.digest(material) == expected


class BoundaryDecision:
    ADMIT = "ADMIT"
    REJECT = "REJECT"
    HALT = "HALT"


@dataclass(frozen=True)
class ResponseEnvelope:
    response_id: str
    request: RequestBinding
    authority: AuthorityScope
    result: Mapping[str, Any]
    evidence: Optional[EvidenceCarrier]
    destination: str
    issued_at: datetime
    expires_at: datetime
    integrity_digest: str = ""
    policy_allow: bool = True

    def protected_material(self) -> dict:
        return {
            "response_id": self.response_id,
            "request": self.request.canonical(),
            "request_digest": self.request.digest,
            "authority": self.authority.canonical(),
            "result": self.result,
            "evidence": None if self.evidence is None else self.evidence.canonical(),
            "destination": self.destination,
            "issued_at": _utc(self.issued_at).isoformat(),
            "expires_at": _utc(self.expires_at).isoformat(),
            "policy_allow": self.policy_allow,
        }

    def with_integrity(self) -> "ResponseEnvelope":
        return replace(self, integrity_digest=IntegrityVerifier.digest(self.protected_material()))


@dataclass(frozen=True)
class CertificateScope:
    certificate_id: str
    actions: FrozenSet[str]
    resources: FrozenSet[str]
    destinations: FrozenSet[str]

    def permits(self, action: str, resource: str, destination: str) -> bool:
        return (
            action in self.actions
            and resource in self.resources
            and destination in self.destinations
        )


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    request_id: str
    digest: str


class ReturnGate:
    """Fail-closed admission of a response across the return boundary."""

    def evaluate(
        self,
        response: ResponseEnvelope,
        original_request: RequestBinding,
        original_authority: AuthorityScope,
        now: datetime,
        *,
        expected_destination: str,
        action: str,
        resource: str,
        principal: str,
    ) -> str:
        now = _utc(now)
        if response.request.request_id != original_request.request_id:
            return BoundaryDecision.REJECT
        if response.request.digest != original_request.digest:
            return BoundaryDecision.REJECT
        if not IntegrityVerifier.verify(response.protected_material(), response.integrity_digest):
            return BoundaryDecision.REJECT
        if response.evidence is None:
            return BoundaryDecision.REJECT
        if not original_authority.contains(response.authority):
            return BoundaryDecision.REJECT
        if not response.authority.permits(action, resource, expected_destination, principal, now):
            return BoundaryDecision.REJECT
        if response.destination != expected_destination:
            return BoundaryDecision.REJECT
        if now >= _utc(response.expires_at):
            return BoundaryDecision.REJECT
        if original_authority.revoked or response.authority.revoked:
            return BoundaryDecision.REJECT
        if not response.policy_allow:
            return BoundaryDecision.REJECT
        return BoundaryDecision.ADMIT
