"""ZK-001 … ZK-008 — Research stubs only.

STATUS: RESEARCH STUB
IMPLEMENTATION: NOT IMPLEMENTED
CRYPTOGRAPHIC PROOF: NOT IMPLEMENTED

These tests document the intended research contracts.
They deliberately fail or skip until a real proving system is selected
and implemented against the RESEARCH_CONTRACT.
"""
from __future__ import annotations

import pytest

from experimental.s9_zkp_research import (
    CRYPTOGRAPHIC_PROOF,
    IMPLEMENTATION,
    STATUS,
)


# ---------------------------------------------------------------------------
# Meta: package posture
# ---------------------------------------------------------------------------

def test_zkp_research_package_posture():
    """
    CLAIM: The ZKP research package must advertise that nothing is implemented.
    IMPLEMENTATION: Constants in experimental.s9_zkp_research.
    TEST: Meta
    RESULT: Package reports RESEARCH_ONLY / NOT_IMPLEMENTED.
    LIMITATION: Does not prove future implementations will remain honest.
    NEXT ITERATION: Keep these constants accurate as work progresses.
    """
    assert STATUS == "RESEARCH_ONLY"
    assert IMPLEMENTATION == "NOT_IMPLEMENTED"
    assert CRYPTOGRAPHIC_PROOF == "NOT_IMPLEMENTED"


# ---------------------------------------------------------------------------
# ZK-001 — Valid constraint proof (contract)
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_001_valid_constraint_proof():
    """
    CLAIM: A correctly formed proof for a true statement should verify.
    IMPLEMENTATION: NOT IMPLEMENTED
    TEST: ZK-001
    RESULT: Expected fail until a proving system exists.
    LIMITATION: No circuit, no prover, no verifier.
    NEXT ITERATION: Implement minimal predicate + selected proving system.
    """
    raise NotImplementedError(
        "ZK-001: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )


# ---------------------------------------------------------------------------
# ZK-002 — Invalid constraint proof must fail
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_002_invalid_constraint_proof():
    """
    CLAIM: A proof for a false statement must be rejected by the verifier.
    IMPLEMENTATION: NOT IMPLEMENTED
    TEST: ZK-002
    RESULT: Expected fail until a proving system exists.
    LIMITATION: Soundness not demonstrated.
    NEXT ITERATION: Adversarial prover tests against the chosen system.
    """
    raise NotImplementedError(
        "ZK-002: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )


# ---------------------------------------------------------------------------
# ZK-003 — Private evidence remains undisclosed (specification)
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_003_private_evidence_undisclosed():
    """
    CLAIM: The witness (private evidence) must not appear in public inputs or proof.
    IMPLEMENTATION: NOT IMPLEMENTED
    TEST: ZK-003
    RESULT: Expected fail until a proving system exists.
    LIMITATION: Zero-knowledge property not demonstrated; privacy is not unconditional.
    NEXT ITERATION: Specify exact witness and check transcripts under the system model.
    """
    raise NotImplementedError(
        "ZK-003: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )


# ---------------------------------------------------------------------------
# ZK-004 — Wrong scope cannot satisfy the defined predicate
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_004_wrong_scope_fails():
    """
    CLAIM: A proof bound to scope S must not verify for scope S'.
    IMPLEMENTATION: NOT IMPLEMENTED
    TEST: ZK-004
    RESULT: Expected fail until a proving system exists.
    LIMITATION: Scope algebra not yet defined in a circuit.
    NEXT ITERATION: Encode scope containment as a constraint.
    """
    raise NotImplementedError(
        "ZK-004: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )


# ---------------------------------------------------------------------------
# ZK-005 — Altered command invalidates the proof relation
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_005_altered_command_invalidates_proof():
    """
    CLAIM: Changing the command after proof generation must make verification fail.
    IMPLEMENTATION: NOT IMPLEMENTED
    TEST: ZK-005
    RESULT: Expected fail until a proving system exists.
    LIMITATION: Command binding not yet expressed in constraints.
    NEXT ITERATION: Include command digest in public inputs / constraints.
    """
    raise NotImplementedError(
        "ZK-005: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )


# ---------------------------------------------------------------------------
# ZK-006 — Altered public input invalidates the proof relation
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_006_altered_public_input_invalidates_proof():
    """
    CLAIM: Changing any public input after proof generation must make verification fail.
    IMPLEMENTATION: NOT IMPLEMENTED
    TEST: ZK-006
    RESULT: Expected fail until a proving system exists.
    LIMITATION: Public-input binding not yet implemented.
    NEXT ITERATION: Standard public-input checks of the selected system.
    """
    raise NotImplementedError(
        "ZK-006: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )


# ---------------------------------------------------------------------------
# ZK-007 — Valid proof cannot create an AuthorityGrant
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_007_valid_proof_cannot_create_authority_grant():
    """
    CLAIM: Even a valid proof must not be convertible into an AuthorityGrant.
    IMPLEMENTATION: NOT IMPLEMENTED (boundary already enforced structurally in S9)
    TEST: ZK-007
    RESULT: Expected fail until a proving system exists to produce a real proof object.
    LIMITATION: Relies on type/API boundary; not yet tested against a real proof type.
    NEXT ITERATION: Feed a real verified proof object into AuthorityGrant constructors
                    and assert rejection.
    """
    raise NotImplementedError(
        "ZK-007: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )


# ---------------------------------------------------------------------------
# ZK-008 — Valid proof cannot bypass the ExecutionGate
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="RESEARCH STUB — cryptographic proof NOT IMPLEMENTED", strict=True)
def test_zk_008_valid_proof_cannot_bypass_execution_gate():
    """
    CLAIM: Even a valid proof must not satisfy the ExecutionGate / require_proceed path.
    IMPLEMENTATION: NOT IMPLEMENTED (gate already rejects non-binding objects)
    TEST: ZK-008
    RESULT: Expected fail until a proving system exists to produce a real proof object.
    LIMITATION: Structural rejection exists today; cryptographic interaction not tested.
    NEXT ITERATION: Present a real verified proof to ExecutionGate and assert escalation
                    or type rejection; authority and binding remain separately required.
    """
    raise NotImplementedError(
        "ZK-008: STATUS=RESEARCH STUB; IMPLEMENTATION=NOT IMPLEMENTED; "
        "CRYPTOGRAPHIC PROOF=NOT IMPLEMENTED"
    )
