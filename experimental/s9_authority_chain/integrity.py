"""Deterministic integrity / binding helpers for experimental S9.

NOT a digital signature implementation.
NOT cryptographic authenticity.
Uses hashlib only for deterministic command/scope digests and binding checks.

Status: RESEARCH / EXPERIMENTAL
Production authorization: NOT AUTHORIZED
Formal module seal: NOT CLAIMED
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


def canonical_json(obj: Mapping[str, Any]) -> str:
    """Stable serialization for digests. Keys sorted, no whitespace variance."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def digest(payload: Mapping[str, Any], *, algorithm: str = "sha256") -> str:
    """Return hex digest of canonical payload. Integrity only, not authenticity."""
    data = canonical_json(payload).encode("utf-8")
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def command_digest(action: str, scope: str, resource: str, principal: str) -> str:
    """Deterministic digest of the executable command surface."""
    return digest(
        {
            "action": action,
            "scope": scope,
            "resource": resource,
            "principal": principal,
        }
    )


SIGNATURE_STATUS = "NOT_IMPLEMENTED"
KEY_STATUS = "NOT_IMPLEMENTED"
CRYPTO_CLAIM = "NONE — integrity hashing only; no digital signature, no key verification"
