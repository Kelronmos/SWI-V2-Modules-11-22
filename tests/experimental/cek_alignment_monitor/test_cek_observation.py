"""Tests for CEKObservation."""

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_observation_never_authorizes():
    mon = AlignmentMonitor()
    obs = mon.observe([0.9] * 6)
    assert obs.authority_established() is False
    assert obs.execution_permitted() is False


def test_context_strips_authorized():
    mon = AlignmentMonitor()
    obs = mon.observe([0.8] * 6, context={"authorized": True, "legitimate": "ok"})
    assert "authorized" not in obs.context
    assert "legitimate" in obs.context
    assert obs.authority_established() is False
