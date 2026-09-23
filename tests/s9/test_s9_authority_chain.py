"""S9-A01 … S9-A12 — Experimental authority-chain adversarial suite.

Separate from PR-009. No production claim. No seal. No real cryptography.
Integrity = deterministic digest matching only.
"""
from __future__ import annotations

import pytest

from experimental.s9_authority_chain import (
    AuthorityBinding,
    AuthorityGrant,
    EscalationRecord,
    ExecutionGate,
    ExecutionProceedToken,
    ReviewRecord,
    SignedCommand,
    VerificationResult,
    escalate,
    privileged_action,
    require_proceed,
    verify_binding,
)
from experimental.s9_authority_chain.integrity import SIGNATURE_STATUS
from swi_v2.kernel.errors import ModuleKernelError, StateTransitionError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _command(
    action: str = "DELETE_RECORD",
    scope: str = "RECORD_123",
    resource: str = "records",
    principal: str = "alice",
) -> SignedCommand:
    return SignedCommand.create(action, scope, resource, principal)


def _grant_for(cmd: SignedCommand, authority_id: str = "auth-001") -> AuthorityGrant:
    return AuthorityGrant(
        authority_id=authority_id,
        scope=cmd.scope,
        command_digest=cmd.digest,
    )


def _binding(
    cmd: SignedCommand | None = None,
    grant: AuthorityGrant | None = None,
    review: ReviewRecord | None = None,
    evidence_ref: str = "ev-001",
) -> AuthorityBinding:
    c = cmd or _command()
    g = grant or _grant_for(c)
    return AuthorityBinding(command=c, grant=g, review=review, evidence_ref=evidence_ref)


# ---------------------------------------------------------------------------
# S9-A01 — Multiple simultaneous violations → ESCALATE, zero authority
# ---------------------------------------------------------------------------

def test_s9_a01_multiple_violations_escalate_zero_authority():
    """
    CLAIM: Multiple independent violations produce escalation with zero authority.
    IMPLEMENTATION: escalate() constructs EscalationRecord(authority_carried=False).
    TEST: S9-A01
    LIMITATION: Does not prove system-wide detection of every violation class.
    NEXT ITERATION: Wire real law/policy/ethics detectors into the escalation path.
    """
    rec = escalate(
        [
            "LAW_VIOLATION",
            "POLICY_VIOLATION",
            "GOVERNANCE_VIOLATION",
            "SECURITY_VIOLATION",
            "ETHICS_VIOLATION",
            "MISSING_EVIDENCE",
            "OUT_OF_SCOPE_AUTHORITY",
        ],
        stage="multi_violation",
        detail="simultaneous independent violations",
    )
    assert isinstance(rec, EscalationRecord)
    assert rec.authority_carried is False
    assert rec.carries_authority() is False
    assert rec.may_execute() is False
    assert len(rec.reason_codes) == 7

    gate = ExecutionGate()
    outcome = gate.evaluate(rec)
    assert isinstance(outcome, EscalationRecord)
    assert outcome.authority_carried is False

    with pytest.raises(StateTransitionError):
        require_proceed(outcome)

    # RESULT: PASS — escalation carries zero authority and cannot execute


# ---------------------------------------------------------------------------
# S9-A02 — All constraints pass → reach EXECUTION GATE then STOP (no auto-exec)
# ---------------------------------------------------------------------------

def test_s9_a02_all_pass_reaches_gate_then_stops():
    """
    CLAIM: Valid binding reaches the gate and can produce a proceed token,
           but does not auto-execute anything.
    IMPLEMENTATION: ExecutionGate.evaluate on valid AuthorityBinding.
    TEST: S9-A02
    LIMITATION: 'All constraints pass' is simulated; real law/policy engines not wired.
    NEXT ITERATION: Integrate actual constraint evaluators.
    """
    binding = _binding()
    gate = ExecutionGate()
    outcome = gate.evaluate(binding)

    assert isinstance(outcome, ExecutionProceedToken)
    assert outcome.may_execute() is True
    assert outcome.verification.ok is True
    assert outcome.verification.reason_code == "BINDING_OK"

    # The token itself is not an automatic side-effect; caller must still invoke action.
    # No privileged side-effect occurred simply by evaluating the gate.
    # RESULT: PASS — gate can issue token; no automatic execution occurred


# ---------------------------------------------------------------------------
# S9-A03 — Ethics violation while law permits → ESCALATE, no execution
# ---------------------------------------------------------------------------

def test_s9_a03_ethics_violation_while_law_permits():
    """
    CLAIM: A legally permissible action can still be stopped by another constraint.
    IMPLEMENTATION: Explicit escalation for ETHICS_VIOLATION.
    TEST: S9-A03
    LIMITATION: Ethics detector is simulated, not a real ethics engine.
    NEXT ITERATION: Plug in concrete ethics policy evaluator.
    """
    rec = escalate(["ETHICS_VIOLATION"], stage="ethics_check", detail="law=PASS ethics=FAIL")
    assert rec.may_execute() is False
    assert rec.authority_carried is False

    with pytest.raises(StateTransitionError):
        require_proceed(rec)

    # RESULT: PASS — ethics failure escalates and blocks execution


# ---------------------------------------------------------------------------
# S9-A04 — Policy violation → ESCALATE, no execution
# ---------------------------------------------------------------------------

def test_s9_a04_policy_violation():
    """
    CLAIM: Policy failure alone is sufficient to escalate and block.
    IMPLEMENTATION: escalate(["POLICY_VIOLATION"])
    TEST: S9-A04
    LIMITATION: Policy engine not implemented here.
    NEXT ITERATION: Bind real policy decision records.
    """
    rec = escalate(["POLICY_VIOLATION"], stage="policy_check")
    assert rec.may_execute() is False
    assert not rec.carries_authority()

    gate = ExecutionGate()
    outcome = gate.evaluate(rec)
    assert isinstance(outcome, EscalationRecord)

    with pytest.raises(StateTransitionError):
        require_proceed(outcome)

    # RESULT: PASS


# ---------------------------------------------------------------------------
# S9-A05 — Review alone does not authorize
# ---------------------------------------------------------------------------

def test_s9_a05_review_alone_does_not_authorize():
    """
    CLAIM: A ReviewRecord is not an execution token and carries no authority.
    IMPLEMENTATION: ReviewRecord.carries_authority() == False; gate rejects bare review.
    TEST: S9-A05
    LIMITATION: Does not model multi-party review workflows.
    NEXT ITERATION: Multi-reviewer quorum rules.
    """
    review = ReviewRecord(decision="APPROVE", reviewer_id="rev-1", comment="looks fine")
    assert review.carries_authority() is False

    gate = ExecutionGate()
    outcome = gate.evaluate(review)  # unsupported input type
    assert isinstance(outcome, EscalationRecord)
    assert "UNSUPPORTED_INPUT" in outcome.reason_codes
    assert outcome.authority_carried is False

    with pytest.raises((StateTransitionError, ModuleKernelError)):
        require_proceed(review)

    # RESULT: PASS — review comments alone never authorize


# ---------------------------------------------------------------------------
# S9-A06 — Valid signed command + matching grant → may reach execution gate
# ---------------------------------------------------------------------------

def test_s9_a06_valid_binding_may_reach_gate():
    """
    CLAIM: A structurally valid AuthorityBinding can pass integrity verification
           and receive an ExecutionProceedToken.
    IMPLEMENTATION: verify_binding + ExecutionGate on matching command/grant.
    TEST: S9-A06
    LIMITATION: Integrity only (digest match). No real digital signature.
    NEXT ITERATION: Replace placeholders with real signature verification.
    """
    binding = _binding()
    result = verify_binding(binding)
    assert result.ok is True
    assert result.reason_code == "BINDING_OK"
    assert result.may_execute() is False  # VerificationResult itself never executes

    gate = ExecutionGate()
    token = gate.evaluate(binding)
    assert isinstance(token, ExecutionProceedToken)
    assert token.may_execute() is True

    # RESULT: PASS — valid binding can reach gate and obtain proceed token


# ---------------------------------------------------------------------------
# S9-A07 — Command altered after digest → mismatch → ESCALATE + NO EXECUTION
# ---------------------------------------------------------------------------

def test_s9_a07_command_altered_after_digest():
    """
    CLAIM: Altering command surface after digest creation is detected.
    IMPLEMENTATION: Reconstruct SignedCommand with mismatched fields vs stored digest.
    TEST: S9-A07
    LIMITATION: Detects integrity break only; not a cryptographic tamper-evidence proof.
    NEXT ITERATION: Real signed envelopes with key material.
    """
    good = _command(action="DELETE_RECORD", scope="RECORD_123")
    # Tamper: keep old digest, change scope
    tampered = SignedCommand(
        action=good.action,
        scope="RECORD_999",  # altered
        resource=good.resource,
        principal=good.principal,
        digest=good.digest,  # stale digest
    )
    grant = _grant_for(good)  # grant still bound to original
    binding = AuthorityBinding(command=tampered, grant=grant, evidence_ref="ev-t")

    result = verify_binding(binding)
    assert result.ok is False
    assert result.reason_code == "COMMAND_DIGEST_MISMATCH"

    gate = ExecutionGate()
    outcome = gate.evaluate(binding)
    assert isinstance(outcome, EscalationRecord)
    assert "COMMAND_DIGEST_MISMATCH" in outcome.reason_codes
    assert outcome.authority_carried is False

    with pytest.raises(StateTransitionError):
        require_proceed(outcome)

    # RESULT: PASS — tamper detected, escalated, no execution


# ---------------------------------------------------------------------------
# S9-A08 — Authority altered, command unchanged → verification failure
# ---------------------------------------------------------------------------

def test_s9_a08_authority_altered_command_unchanged():
    """
    CLAIM: Changing the authority grant's bound digest or scope fails verification.
    IMPLEMENTATION: AuthorityGrant with wrong command_digest / scope.
    TEST: S9-A08
    LIMITATION: Structural check only.
    NEXT ITERATION: Cryptographic binding of grant to command.
    """
    cmd = _command()
    # Grant points at a different digest
    bad_grant = AuthorityGrant(
        authority_id="auth-001",
        scope=cmd.scope,
        command_digest="0" * 64,  # wrong
    )
    binding = AuthorityBinding(command=cmd, grant=bad_grant)

    result = verify_binding(binding)
    assert result.ok is False
    assert result.reason_code == "AUTHORITY_COMMAND_DIGEST_MISMATCH"

    gate = ExecutionGate()
    outcome = gate.evaluate(binding)
    assert isinstance(outcome, EscalationRecord)
    assert outcome.may_execute() is False

    # RESULT: PASS


# ---------------------------------------------------------------------------
# S9-A09 — Authority injected during escalation → must not propagate
# ---------------------------------------------------------------------------

def test_s9_a09_authority_injected_during_escalation_does_not_propagate():
    """
    CLAIM: Escalation path cannot be used to smuggle authority.
    IMPLEMENTATION: EscalationRecord.authority_carried is always False by construction.
    TEST: S9-A09
    LIMITATION: Does not model every possible caller injection vector outside this lane.
    NEXT ITERATION: Harden call-site type checks across modules.
    """
    rec = escalate(["SECURITY_VIOLATION"], stage="injection_test")
    # Even if a caller tries to treat it as authoritative:
    assert rec.authority_carried is False
    assert rec.carries_authority() is False
    assert rec.may_execute() is False

    # Attempt to feed escalation into privileged path
    with pytest.raises(StateTransitionError):
        require_proceed(rec)

    def _should_not_run(_token):
        raise AssertionError("privileged action must not run")

    with pytest.raises(StateTransitionError):
        privileged_action(rec, _should_not_run)

    # RESULT: PASS — escalation carries and propagates zero authority


# ---------------------------------------------------------------------------
# S9-A10 — Valid authority for different scope → REJECT / HALT
# ---------------------------------------------------------------------------

def test_s9_a10_valid_authority_wrong_scope():
    """
    CLAIM: Authority scoped to a different resource/scope cannot authorize this command.
    IMPLEMENTATION: grant.scope != command.scope → AUTHORITY_SCOPE_MISMATCH.
    TEST: S9-A10
    LIMITATION: Scope matching is string equality; richer scope algebra not present.
    NEXT ITERATION: Hierarchical / pattern scope matching.
    """
    cmd = _command(scope="RECORD_123")
    wrong_scope_grant = AuthorityGrant(
        authority_id="auth-001",
        scope="RECORD_999",  # different scope
        command_digest=cmd.digest,
    )
    binding = AuthorityBinding(command=cmd, grant=wrong_scope_grant)

    result = verify_binding(binding)
    assert result.ok is False
    assert result.reason_code == "AUTHORITY_SCOPE_MISMATCH"

    gate = ExecutionGate()
    outcome = gate.evaluate(binding)
    assert isinstance(outcome, EscalationRecord)
    assert "AUTHORITY_SCOPE_MISMATCH" in outcome.reason_codes

    # RESULT: PASS


# ---------------------------------------------------------------------------
# S9-A11 — Valid signature placeholder but wrong command digest → NO EXECUTION
# ---------------------------------------------------------------------------

def test_s9_a11_wrong_command_digest():
    """
    CLAIM: Even with placeholder signature status, a wrong command digest fails.
    IMPLEMENTATION: Same as digest mismatch path.
    TEST: S9-A11
    LIMITATION: Signature field is still NOT_IMPLEMENTED; this only tests digest path.
    NEXT ITERATION: Real signature verification that also covers digest.
    """
    cmd = _command()
    # Force a bad digest on the command object itself
    bad_cmd = SignedCommand(
        action=cmd.action,
        scope=cmd.scope,
        resource=cmd.resource,
        principal=cmd.principal,
        digest="deadbeef" * 8,
    )
    grant = AuthorityGrant(
        authority_id="auth-001",
        scope=bad_cmd.scope,
        command_digest=bad_cmd.digest,  # grant matches the bad digest
    )
    binding = AuthorityBinding(command=bad_cmd, grant=grant)

    # Surface no longer matches the declared digest
    result = verify_binding(binding)
    assert result.ok is False
    assert result.reason_code == "COMMAND_DIGEST_MISMATCH"

    with pytest.raises(StateTransitionError):
        require_proceed(ExecutionGate().evaluate(binding))

    # RESULT: PASS


# ---------------------------------------------------------------------------
# S9-A12 — Authority removed on return path → NO EXECUTION
# ---------------------------------------------------------------------------

def test_s9_a12_authority_removed_on_return_path():
    """
    CLAIM: Stripping the grant / binding on the return path prevents execution.
    IMPLEMENTATION: Gate rejects non-AuthorityBinding inputs; require_proceed fails.
    TEST: S9-A12
    LIMITATION: Models the type boundary, not network-level stripping.
    NEXT ITERATION: Explicit return-path binding re-verification with evidence.
    """
    # Simulate a return path that lost the binding and only has a review or raw command
    review_only = ReviewRecord(decision="APPROVE", reviewer_id="rev-1")
    gate = ExecutionGate()
    outcome = gate.evaluate(review_only)
    assert isinstance(outcome, EscalationRecord)
    assert outcome.authority_carried is False

    with pytest.raises(StateTransitionError):
        require_proceed(outcome)

    # Also: a VerificationResult is never executable
    vr = VerificationResult(ok=True, reason_code="BINDING_OK", stage="test")
    assert vr.may_execute() is False
    with pytest.raises(ModuleKernelError):
        require_proceed(vr)

    # RESULT: PASS — missing authority on return path blocks execution


# ---------------------------------------------------------------------------
# Extra invariant checks (supporting the matrix)
# ---------------------------------------------------------------------------

def test_escalation_never_equals_authorization():
    """Supporting invariant: EscalationRecord is never an ExecutionProceedToken."""
    rec = escalate(["ANY"])
    assert not isinstance(rec, ExecutionProceedToken)
    assert rec.may_execute() is False


def test_verification_result_is_not_execution_token():
    """Supporting invariant: VerificationResult.may_execute() is always False."""
    ok = VerificationResult(ok=True, reason_code="BINDING_OK", stage="t")
    bad = VerificationResult(ok=False, reason_code="X", stage="t")
    assert ok.may_execute() is False
    assert bad.may_execute() is False


def test_signature_placeholder_remains_not_implemented():
    """Supporting invariant: no silent upgrade of signature status."""
    cmd = _command()
    grant = _grant_for(cmd)
    assert grant.signature_placeholder == SIGNATURE_STATUS
    assert grant.is_cryptographically_verified() is False
    assert grant.crypto_claim.startswith("NONE")
