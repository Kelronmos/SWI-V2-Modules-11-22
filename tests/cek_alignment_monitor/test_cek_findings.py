"""Tests for Finding."""

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_finding_not_authoritative():
    mon = AlignmentMonitor()
    obs = mon.observe([0.9] * 6)
    f = mon.finding_from_observation(obs)
    assert f.is_authoritative() is False
    assert f.permits_execution() is False


def test_finding_from_hidden_edge():
    mon = AlignmentMonitor()
    obs, finding, report = mon.full_hidden_edge_observation()
    assert finding.is_authoritative() is False
    assert report.authority_established is False
