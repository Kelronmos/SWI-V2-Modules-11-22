"""PR-009 / T20 — fail-safe: REJECT cannot be used for privileged execution."""
from datetime import datetime, timedelta, timezone
from dataclasses import replace
import pytest

from experimental.response_boundary import (
    RequestBinding,
    AuthorityScope,
    EvidenceCarrier,
    BoundaryDecision,
    ReturnGate,
    build_response,
    enforce,
    require_executable,
    privileged_action,
    attempt_recovery_without_authority,
    AdmittedResponse,
)
from swi_v2.kernel.halt import HaltedWorkflow
from swi_v2.kernel.errors import StateTransitionError, ModuleKernelError

NOW = datetime(2026, 9, 19, 8, 0, tzinfo=timezone.utc)


def fixtures():
    request = RequestBinding(
        "R1", "alice", "read", "record-1", "alice-ui", NOW + timedelta(minutes=10)
    )
    authority = AuthorityScope(
        "alice",
        frozenset({"read"}),
        frozenset({"record-1"}),
        frozenset({"alice-ui"}),
        NOW + timedelta(minutes=10),
    )
    evidence = EvidenceCarrier("E1", "sha256:abc", "producer")
    envelope = build_response(
        response_id="X1",
        request=request,
        authority=authority,
        result={"value": 1},
        evidence=evidence,
        destination="alice-ui",
        issued_at=NOW,
        expires_at=NOW + timedelta(minutes=5),
    )
    return request, authority, envelope


def _enforce(envelope, request, authority, **kw):
    return enforce(
        envelope,
        request,
        authority,
        NOW,
        expected_destination=kw.get("expected_destination", "alice-ui"),
        action=kw.get("action", "read"),
        resource=kw.get("resource", "record-1"),
        principal=kw.get("principal", "alice"),
        policy_allows=kw.get("policy_allows", True),
    )


def test_t20_valid_admits_and_may_execute():
    r, a, x = fixtures()
    out = _enforce(x, r, a)
    assert isinstance(out, AdmittedResponse)
    assert out.decision == BoundaryDecision.ADMIT
    assert out.may_execute() is True
    assert require_executable(out) is out


def test_t20_a_reject_blocks_privileged_action():
    r, a, x = fixtures()
    bad = replace(x, destination="evil-ui").with_integrity()
    out = _enforce(bad, r, a)
    assert isinstance(out, HaltedWorkflow)
    assert out.may_execute() is False
    assert out.state == "HALTED"

    executed = {"ran": False}

    def priv(_env):
        executed["ran"] = True
        return "secrets"

    with pytest.raises(StateTransitionError):
        privileged_action(out, priv)
    assert executed["ran"] is False


def test_t20_b_halted_may_execute_false():
    r, a, x = fixtures()
    out = _enforce(x, r, a, policy_allows=False)
    assert isinstance(out, HaltedWorkflow)
    assert out.may_execute() is False


def test_t20_c_require_executable_rejects_halted():
    r, a, x = fixtures()
    out = _enforce(replace(x, evidence=None).with_integrity(), r, a)
    with pytest.raises(StateTransitionError):
        require_executable(out)


def test_t20_c_require_executable_rejects_raw_envelope():
    r, a, x = fixtures()
    with pytest.raises(ModuleKernelError):
        require_executable(x)


def test_t20_d_no_automatic_recovery():
    r, a, x = fixtures()
    halted = _enforce(x, r, a, policy_allows=False)
    still = attempt_recovery_without_authority(halted)
    assert still is halted
    assert still.may_execute() is False
    with pytest.raises(StateTransitionError):
        privileged_action(still, lambda e: e.result)


def test_t20_e_reject_output_not_released_via_privileged_path():
    r, a, x = fixtures()
    halted = _enforce(replace(x, destination="other").with_integrity(), r, a)
    released = []

    def release(env):
        released.append(env.result)
        return env.result

    with pytest.raises(StateTransitionError):
        privileged_action(halted, release)
    assert released == []


def test_t20_admit_allows_privileged_read():
    r, a, x = fixtures()
    out = _enforce(x, r, a)
    result = privileged_action(out, lambda env: env.result)
    assert result == {"value": 1}


def test_gate_still_independent_of_enforcement():
    """ReturnGate alone still only returns strings; enforcement adds the token."""
    r, a, x = fixtures()
    d = ReturnGate().evaluate(
        x, r, a, NOW,
        expected_destination="alice-ui",
        action="read",
        resource="record-1",
        principal="alice",
    )
    assert d == BoundaryDecision.ADMIT
    assert not hasattr(d, "may_execute")


# ---------------------------------------------------------------------------
# Adversarial boundary diagnosis (2026-09-21)
# Claim under test: invalid state cannot be converted into an executable
# state without passing the intended boundary.
# ---------------------------------------------------------------------------

import pickle
import copy


def test_adversarial_serialize_deserialize_halted_remains_non_executable():
    """REJECT → HaltedWorkflow → serialize → deserialize → still blocked."""
    r, a, x = fixtures()
    halted = _enforce(x, r, a, policy_allows=False)
    assert isinstance(halted, HaltedWorkflow)
    assert halted.may_execute() is False

    # Attempt pickle round-trip (if it fails, that itself is a documented result)
    try:
        serialized = pickle.dumps(halted)
        restored = pickle.loads(serialized)
    except Exception as exc:
        # Documented outcome: object cannot safely be serialized
        assert True, f"serialization refused: {type(exc).__name__}"
        return

    assert isinstance(restored, HaltedWorkflow)
    assert restored.may_execute() is False

    executed = {"ran": False}

    def priv(_env):
        executed["ran"] = True
        return "secrets"

    with pytest.raises((StateTransitionError, ModuleKernelError, TypeError, AttributeError)):
        privileged_action(restored, priv)
    assert executed["ran"] is False

    with pytest.raises((StateTransitionError, ModuleKernelError)):
        require_executable(restored)


def test_adversarial_reject_string_cannot_reach_privileged_action():
    """Raw REJECT string must not be usable as an executable token."""
    with pytest.raises((ModuleKernelError, StateTransitionError, TypeError, AttributeError)):
        privileged_action(BoundaryDecision.REJECT, lambda e: e)


def test_adversarial_raw_envelope_cannot_reach_privileged_action():
    """Raw ResponseEnvelope (never passed through enforce) must be rejected."""
    r, a, x = fixtures()
    with pytest.raises((ModuleKernelError, StateTransitionError)):
        privileged_action(x, lambda e: e.result)
    with pytest.raises((ModuleKernelError, StateTransitionError)):
        require_executable(x)


def test_adversarial_mutated_admitted_object_blocked():
    """An AdmittedResponse whose may_execute is forced False must be blocked."""
    r, a, x = fixtures()
    out = _enforce(x, r, a)
    assert isinstance(out, AdmittedResponse)
    assert out.may_execute() is True

    # Attempt to create a mutated view that claims may_execute False
    class MutatedAdmitted:
        def __init__(self, original):
            self.envelope = original.envelope
            self.decision = original.decision

        def may_execute(self):
            return False

    mutated = MutatedAdmitted(out)
    with pytest.raises((StateTransitionError, ModuleKernelError, TypeError)):
        require_executable(mutated)
    with pytest.raises((StateTransitionError, ModuleKernelError, TypeError)):
        privileged_action(mutated, lambda e: e.result)


def test_adversarial_halted_with_altered_fields_still_blocked():
    """HaltedWorkflow with altered record / state attributes remains non-executable."""
    r, a, x = fixtures()
    halted = _enforce(x, r, a, policy_allows=False)
    assert isinstance(halted, HaltedWorkflow)

    # Direct attribute mutation attempts
    try:
        halted.state = "ADMITTED"  # type: ignore[misc]
    except Exception:
        pass  # frozen or protected — acceptable

    # Even if mutation succeeded, may_execute must still be False
    assert halted.may_execute() is False

    with pytest.raises((StateTransitionError, ModuleKernelError)):
        require_executable(halted)
    with pytest.raises((StateTransitionError, ModuleKernelError)):
        privileged_action(halted, lambda e: e.result)


def test_adversarial_copy_of_halted_still_blocked():
    """Shallow/deep copy of HaltedWorkflow must not become executable."""
    r, a, x = fixtures()
    halted = _enforce(x, r, a, policy_allows=False)

    for copied in (copy.copy(halted), copy.deepcopy(halted)):
        assert copied.may_execute() is False
        with pytest.raises((StateTransitionError, ModuleKernelError)):
            require_executable(copied)
        with pytest.raises((StateTransitionError, ModuleKernelError)):
            privileged_action(copied, lambda e: "leaked")
