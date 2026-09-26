"""Closed transition engine for SWI repair / state progression.

STATUS:
  RESEARCH / EXPERIMENTAL
  DESIGN LOCKED
  IMPLEMENTED (decision kernel only)
  NOT SEALED
  NOT PRODUCTION AUTHORIZED
  PRODUCTION: BLOCKED

Machine invariant:

  UNKNOWN TRANSITION              → REJECT
  KNOWN TRANSITION + FAILED GATE  → BLOCK
  INTEGRITY FAILURE               → QUARANTINE
  KNOWN TRANSITION + ALL GATES OK → ALLOW

Hard constraints:
  REJECT / BLOCK / QUARANTINE → NO STATE MUTATION
  TAMPERED  ↛  VERIFIED / SEALED / AUTHORIZED / ACTION
  CI_GREEN  ↛  AUTHORIZED
  SIGNATURE_VALID  ↛  AUTHORIZED
  TECHNICAL_VERIFICATION  ↛  HUMAN_AUTHORITY

Privacy is a gate. It is not a state-transition permission by itself.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping, Optional, Set


class TransitionDecision(str, Enum):
    ALLOW = "ALLOW"
    REJECT = "REJECT"
    BLOCK = "BLOCK"
    QUARANTINE = "QUARANTINE"


# ---------------------------------------------------------------------------
# State registry — existence only
# ---------------------------------------------------------------------------

DEFAULT_STATES: frozenset[str] = frozenset({
    "UNASSESSED",
    "INTACT",
    "TAMPERED",
    "QUARANTINED",
    "REPAIR_REQUESTED",
    "HUMAN_REVIEW",
    "ESCALATED",
    "REPAIR_AUTHORIZED",
    "REPAIRED",
    "REVALIDATED",
    "NEW_EVIDENCE",
    "READMISSION",
    "REVERIFIED",
    "DEFINED",
    "IMPLEMENTED",
    "TESTED",
    "VERIFIED",
    "SEAL_REVIEW",
    "SEALED",
    "PRODUCTION_REVIEW",
    "AUTHORIZED",
    "ACTION",
    "BLOCKED",
    "REJECTED",
})


class StateRegistry:
    """What states exist. Existence ≠ permission to enter."""

    def __init__(self, states: Optional[Set[str]] = None):
        self._states: frozenset[str] = frozenset(states) if states is not None else DEFAULT_STATES

    def contains(self, state: str) -> bool:
        return state in self._states

    def all_states(self) -> frozenset[str]:
        return self._states


# ---------------------------------------------------------------------------
# Gate specification
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GateSpec:
    """Conditions that must be satisfied for a permitted transition."""

    integrity_required: bool = False
    authority_required: bool = False
    evidence_required: bool = False
    privacy_required: bool = False
    # Explicit bans — cannot be satisfied by technical properties alone
    forbid_ci_green_as_authority: bool = True
    forbid_signature_as_authority: bool = True
    forbid_technical_as_human: bool = True


# ---------------------------------------------------------------------------
# Transition registry — permission only
# ---------------------------------------------------------------------------

# (from, to) → GateSpec
DEFAULT_TRANSITIONS: Mapping[tuple[str, str], GateSpec] = {
    # Integrity / quarantine path
    ("UNASSESSED", "INTACT"): GateSpec(integrity_required=True),
    ("UNASSESSED", "TAMPERED"): GateSpec(integrity_required=True),
    ("TAMPERED", "QUARANTINED"): GateSpec(integrity_required=True),
    ("QUARANTINED", "REPAIR_REQUESTED"): GateSpec(),
    ("REPAIR_REQUESTED", "HUMAN_REVIEW"): GateSpec(),
    ("HUMAN_REVIEW", "ESCALATED"): GateSpec(),
    ("HUMAN_REVIEW", "REPAIR_AUTHORIZED"): GateSpec(
        integrity_required=True,
        authority_required=True,
    ),
    ("ESCALATED", "REPAIR_AUTHORIZED"): GateSpec(
        integrity_required=True,
        authority_required=True,
    ),
    ("REPAIR_AUTHORIZED", "REPAIRED"): GateSpec(
        integrity_required=True,
        authority_required=True,
    ),
    ("REPAIRED", "REVALIDATED"): GateSpec(
        integrity_required=True,
        evidence_required=True,
    ),
    ("REVALIDATED", "NEW_EVIDENCE"): GateSpec(evidence_required=True),
    ("NEW_EVIDENCE", "READMISSION"): GateSpec(
        evidence_required=True,
        integrity_required=True,
    ),
    ("READMISSION", "REVERIFIED"): GateSpec(
        evidence_required=True,
        integrity_required=True,
        authority_required=True,
    ),
    # Ordinary progression (closed — no shortcuts)
    ("DEFINED", "IMPLEMENTED"): GateSpec(),
    ("IMPLEMENTED", "TESTED"): GateSpec(),
    ("TESTED", "VERIFIED"): GateSpec(
        integrity_required=True,
        evidence_required=True,
    ),
    ("VERIFIED", "SEAL_REVIEW"): GateSpec(
        integrity_required=True,
        evidence_required=True,
        authority_required=True,
    ),
    ("SEAL_REVIEW", "SEALED"): GateSpec(
        integrity_required=True,
        evidence_required=True,
        authority_required=True,
    ),
    ("SEALED", "PRODUCTION_REVIEW"): GateSpec(
        integrity_required=True,
        evidence_required=True,
        authority_required=True,
    ),
    ("PRODUCTION_REVIEW", "AUTHORIZED"): GateSpec(
        integrity_required=True,
        evidence_required=True,
        authority_required=True,
        privacy_required=True,
    ),
    ("AUTHORIZED", "ACTION"): GateSpec(
        integrity_required=True,
        evidence_required=True,
        authority_required=True,
        privacy_required=True,
    ),
    # Explicit failure / block paths
    ("DEFINED", "BLOCKED"): GateSpec(),
    ("IMPLEMENTED", "BLOCKED"): GateSpec(),
    ("TESTED", "BLOCKED"): GateSpec(),
    ("VERIFIED", "BLOCKED"): GateSpec(),
    ("SEALED", "BLOCKED"): GateSpec(),
}


class TransitionRegistry:
    """Which (from, to) pairs are permitted. Permission ≠ gate satisfaction."""

    def __init__(
        self,
        transitions: Optional[Mapping[tuple[str, str], GateSpec]] = None,
    ):
        self._transitions = dict(transitions) if transitions is not None else dict(DEFAULT_TRANSITIONS)

    def get(self, current: str, requested: str) -> Optional[GateSpec]:
        return self._transitions.get((current, requested))

    def is_permitted(self, current: str, requested: str) -> bool:
        return (current, requested) in self._transitions

    def register(self, current: str, requested: str, gate: GateSpec) -> None:
        """Add a transition. Does not auto-satisfy gates."""
        self._transitions[(current, requested)] = gate


# ---------------------------------------------------------------------------
# Context supplied by the caller
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TransitionContext:
    """Facts presented for gate evaluation. No side effects."""

    integrity_valid: bool = False
    authority_present: bool = False
    authority_is_human: bool = False
    evidence_valid: bool = False
    privacy_satisfied: bool = False
    # Technical properties that MUST NOT substitute for human authority
    ci_green: bool = False
    signature_valid: bool = False
    technical_verification: bool = False
    # Optional privacy decision from the privacy gate (ALLOW/BLOCK/ESCALATE/REDACT)
    privacy_decision: Optional[str] = None


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TransitionResult:
    decision: TransitionDecision
    reason: str
    current_state: str
    requested_state: str
    state_mutated: bool
    decided_at: str
    gate_failures: tuple[str, ...] = field(default_factory=tuple)

    @property
    def allowed(self) -> bool:
        return self.decision == TransitionDecision.ALLOW


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Core decision function — pure, no mutation
# ---------------------------------------------------------------------------

def attempt_transition(
    current: str,
    requested: str,
    context: TransitionContext,
    *,
    states: Optional[StateRegistry] = None,
    transitions: Optional[TransitionRegistry] = None,
) -> TransitionResult:
    """Evaluate a requested state transition.

    Pure function: never mutates external state.
    REJECT / BLOCK / QUARANTINE all leave state_mutated=False.
    """
    state_reg = states or StateRegistry()
    trans_reg = transitions or TransitionRegistry()
    _ = state_reg  # existence registry available for future callers

    # 1. Transition must be explicitly registered.
    #    A registered transition is authoritative even for newly introduced
    #    state names (adding a state does not auto-create transitions;
    #    adding a transition does not auto-satisfy gates).
    gate = trans_reg.get(current, requested)
    if gate is None:
        return TransitionResult(
            decision=TransitionDecision.REJECT,
            reason=f"UNDEFINED_TRANSITION: ({current} → {requested})",
            current_state=current,
            requested_state=requested,
            state_mutated=False,
            decided_at=_utc_now(),
            gate_failures=("UNDEFINED_TRANSITION",),
        )

    # 2. Integrity failure → QUARANTINE (overrides ordinary block when integrity is required)
    if gate.integrity_required and not context.integrity_valid:
        return TransitionResult(
            decision=TransitionDecision.QUARANTINE,
            reason="INTEGRITY_FAILURE: required integrity check failed",
            current_state=current,
            requested_state=requested,
            state_mutated=False,
            decided_at=_utc_now(),
            gate_failures=("INTEGRITY_FAILURE",),
        )

    failures: list[str] = []

    # 3. Authority gate — human authority only; technical props cannot substitute
    if gate.authority_required:
        if not context.authority_present:
            failures.append("AUTHORITY_MISSING")
        elif not context.authority_is_human:
            failures.append("AUTHORITY_NOT_HUMAN")
        # Explicit substitution bans
        if gate.forbid_ci_green_as_authority and context.ci_green and not context.authority_is_human:
            failures.append("CI_GREEN_NOT_AUTHORITY")
        if gate.forbid_signature_as_authority and context.signature_valid and not context.authority_is_human:
            failures.append("SIGNATURE_NOT_AUTHORITY")
        if gate.forbid_technical_as_human and context.technical_verification and not context.authority_is_human:
            failures.append("TECHNICAL_NOT_HUMAN_AUTHORITY")

    # 4. Evidence gate
    if gate.evidence_required and not context.evidence_valid:
        failures.append("EVIDENCE_MISSING_OR_INVALID")

    # 5. Privacy gate (consumes external privacy decision; does not invent policy)
    if gate.privacy_required:
        if context.privacy_decision is not None:
            if context.privacy_decision != "ALLOW":
                failures.append(f"PRIVACY_{context.privacy_decision}")
        elif not context.privacy_satisfied:
            failures.append("PRIVACY_NOT_SATISFIED")

    if failures:
        return TransitionResult(
            decision=TransitionDecision.BLOCK,
            reason="REQUIRED_CONDITION_MISSING: " + ", ".join(failures),
            current_state=current,
            requested_state=requested,
            state_mutated=False,
            decided_at=_utc_now(),
            gate_failures=tuple(failures),
        )

    # 6. All gates passed
    return TransitionResult(
        decision=TransitionDecision.ALLOW,
        reason=f"Transition permitted: {current} → {requested}",
        current_state=current,
        requested_state=requested,
        state_mutated=False,  # caller is responsible for applying; engine never mutates
        decided_at=_utc_now(),
        gate_failures=(),
    )
