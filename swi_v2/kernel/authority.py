"""Authority boundary — fail-closed non-escalation helper (Lane A).

STATUS: IMPLEMENTED / TESTED (not sealed).

Invariant:
  DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION

Information may cross a boundary without authority crossing that boundary.

Undeclared authority-bearing fields are REJECTED (not stripped silently).
Missing required authorization for ACTION yields HALT semantics via AuthorityHalt.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, FrozenSet, Iterable, Mapping, Optional

from .errors import AuthorityError, AuthorityHalt


class AuthorityLayer(str, Enum):
    DATA = "data"
    EVIDENCE = "evidence"
    ADMISSION = "admission"
    AUTHORIZATION = "authorization"
    ACTION = "action"


FORBIDDEN_AUTHORITY_FIELDS: FrozenSet[str] = frozenset(
    {
        "verified",
        "trusted",
        "truth",
        "authority",
        "m11_admitted",
        "replay_verified",
        "security_level",
        "system_authority",
        "admin_authority",
        "verified_truth",
        "policy_authorized",
        "human_approved",
        "authorized",
        "permission",
        "privilege",
    }
)


@dataclass(frozen=True)
class AuthorityDecision:
    """Record of an authority-boundary check (evidence of rejection/permit)."""

    allowed: bool
    layer: AuthorityLayer
    reason: str
    entered_keys: tuple[str, ...] = ()
    rejected_fields: tuple[str, ...] = ()
    contract_id: str = "authority_boundary_v0"
    next_state: str = "CONTINUE"  # CONTINUE | REJECT | HALT


def scan_undeclared_authority(
    payload: Mapping[str, Any],
    *,
    allowed_fields: Optional[Iterable[str]] = None,
    layer: AuthorityLayer = AuthorityLayer.DATA,
) -> AuthorityDecision:
    """Reject undeclared authority-bearing keys; do not strip and continue."""
    allowed = frozenset(allowed_fields or ())
    keys = tuple(sorted(payload.keys()))
    rejected = []
    for k in payload.keys():
        if k in FORBIDDEN_AUTHORITY_FIELDS and k not in allowed:
            rejected.append(k)
    if rejected:
        return AuthorityDecision(
            allowed=False,
            layer=layer,
            reason="undeclared_authority_field",
            entered_keys=keys,
            rejected_fields=tuple(sorted(rejected)),
            next_state="REJECT",
        )
    return AuthorityDecision(
        allowed=True,
        layer=layer,
        reason="no_undeclared_authority",
        entered_keys=keys,
        rejected_fields=(),
        next_state="CONTINUE",
    )


def require_no_authority_escalation(
    payload: Mapping[str, Any],
    *,
    layer: AuthorityLayer,
    allowed_fields: Optional[Iterable[str]] = None,
) -> AuthorityDecision:
    """Raise AuthorityError on undeclared authority fields (fail closed)."""
    decision = scan_undeclared_authority(
        payload, allowed_fields=allowed_fields, layer=layer
    )
    if not decision.allowed:
        raise AuthorityError(
            f"{layer.value}: undeclared authority fields {list(decision.rejected_fields)}; "
            f"contract={decision.contract_id}; next={decision.next_state}"
        )
    return decision


def assert_layer_does_not_imply(
    source: AuthorityLayer, target: AuthorityLayer
) -> None:
    """Crossing upward never auto-grants the target layer (documentation helper)."""
    return None


def require_authorization_for_action(
    *,
    authorization_present: bool,
    authorization_scope: Optional[str],
    requested_action: str,
    declared_scopes: Optional[Iterable[str]] = None,
) -> AuthorityDecision:
    """ACTION requires explicit authorization; missing → HALT; out of scope → REJECT."""
    if not authorization_present:
        raise AuthorityHalt(
            f"action={requested_action!r} missing authorization; next=HALT"
        )
    scopes = frozenset(declared_scopes or ())
    scope_ok = authorization_scope is not None and (
        not scopes or authorization_scope in scopes
    )
    action_ok = not scopes or requested_action in scopes
    if not scope_ok or not action_ok:
        raise AuthorityError(
            f"action={requested_action!r} scope={authorization_scope!r} "
            f"exceeds declared scopes {sorted(scopes)}; next=REJECT"
        )
    return AuthorityDecision(
        allowed=True,
        layer=AuthorityLayer.ACTION,
        reason="authorization_scope_ok",
        entered_keys=(authorization_scope or "",),
        rejected_fields=(),
        next_state="CONTINUE",
    )


def layer_non_implication_matrix() -> dict[str, tuple[str, ...]]:
    """Static matrix: success at a layer must not imply the listed layers."""
    return {
        "data": ("evidence", "admission", "authorization", "action"),
        "evidence": ("admission", "authorization", "action"),
        "admission": ("authorization", "action"),
        "authorization": ("action_beyond_scope",),
        "action": (),
    }
