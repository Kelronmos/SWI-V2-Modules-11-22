"""Tests for Finding."""

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.findings import FindingKind


def test_finding_from_visible_path():
    mon = AlignmentMonitor()
    obs = mon.observe([0.9] * 6)
    finding = mon.finding_from_observation(obs)
    assert finding.visibility == FindingKind.VISIBLE
    assert finding.is_authoritative() is False


def test_finding_from_hidden_edge():
    mon = AlignmentMonitor()
    obs, finding, _ = mon.full_hidden_edge_observation()
    assert finding.visibility == FindingKind.UNKNOWN
    assert finding.frontier == "NEXT_EDGE"
    assert finding.is_authoritative() is False
    assert finding.permits_execution() is False
