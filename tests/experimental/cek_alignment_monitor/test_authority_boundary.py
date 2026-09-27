"""
Critical Stage-2 authority-boundary attack suite.

None of the following transformations may succeed merely because
CEK observed or measured something:

  UNKNOWN → PERMIT
  UNKNOWN → AUTHORITY
  UNKNOWN → EXECUTION
  EVIDENCE → AUTHORITY
  SIGNATURE → AUTHORITY
  OBSERVATION → AUTHORITY
  STABLE → AUTHORITY
  EXECUTION OBSERVED → NEW AUTHORITY
"""

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.vector import AlignmentVector
from experimental.cek_alignment_monitor.visibility import VisibilityLevel


@pytest.fixture
def monitor():
    return AlignmentMonitor()


def test_stable_does_not_authorize(monitor):
    m = monitor.measure([1.0] * 6)
    assert m.classification.value == "STABLE"
    assert m.is_authoritative() is False
    assert m.permits_execution() is False
    assert monitor.authority_established() is False
    assert monitor.execution_permitted() is False


def test_high_drift_does_not_authorize(monitor):
    m = monitor.measure([0.0] * 6)
    assert m.classification.value == "HIGH_DRIFT"
    assert m.is_authoritative() is False
    assert m.permits_execution() is False


def test_observation_never_authorizes(monitor):
    obs = monitor.observe([0.9] * 6)
    assert obs.authority_established() is False
    assert obs.execution_permitted() is False
    assert obs.is_authoritative() is False


def test_injected_authorized_context_is_stripped(monitor):
    obs = monitor.observe(
        [0.9] * 6,
        context={
            "authorized": True,
            "permit": True,
            "execute": True,
            "seal": True,
            "admit": True,
            "approved": True,
            "authority": "GRANTED",
            "legitimate": "value",
        },
    )
    for key in ("authorized", "permit", "execute", "seal", "admit", "approved", "authority"):
        assert key not in obs.context
    assert "legitimate" in obs.context
    assert obs.authority_established() is False


def test_hidden_edge_authority_not_established(monitor):
    obs, finding, report = monitor.full_hidden_edge_observation()
    assert report.has_unknown_edge is True
    assert report.frontier == "NEXT_EDGE"
    assert report.authority_established is False
    assert obs.authority_established() is False
    assert obs.execution_permitted() is False
    assert finding.is_authoritative() is False
    assert finding.visibility.value == "UNKNOWN"


def test_unknown_edge_does_not_permit(monitor):
    """Attack 001 / 002 / 003: UNKNOWN must never become PERMIT / AUTHORITY / EXECUTION."""
    obs, finding, report = monitor.full_hidden_edge_observation()
    assert report.has_unknown_edge
    assert not hasattr(obs, "permit")
    assert not hasattr(obs, "authorize")
    assert not hasattr(obs, "execute")
    assert obs.execution_permitted() is False
    assert finding.permits_execution() is False


def test_evidence_does_not_become_authority(monitor):
    """Attack 004: EVIDENCE → AUTHORITY must fail."""
    obs = monitor.observe(
        [0.8] * 6,
        evidence_reference="some-evidence-hash",
    )
    assert obs.evidence_reference is not None
    assert obs.authority_established() is False


def test_finding_never_authoritative(monitor):
    obs = monitor.observe([0.7] * 6)
    finding = monitor.finding_from_observation(obs)
    assert finding.is_authoritative() is False
    assert finding.permits_execution() is False


def test_monitor_surface_has_no_execution_methods(monitor):
    """Structural check: the public surface must not expose execution / seal APIs."""
    forbidden = {
        "authorize",
        "permit",
        "execute",
        "seal",
        "admit",
        "approve",
        "dispatch",
        "run",
        "invoke",
    }
    public = {name for name in dir(monitor) if not name.startswith("_")}
    overlap = public & forbidden
    assert overlap == set(), f"Forbidden methods exposed: {overlap}"
