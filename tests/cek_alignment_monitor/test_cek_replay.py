"""Tests for ReplayEngine."""

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_replay_match():
    mon = AlignmentMonitor()
    m = mon.measure([0.85] * 6, measurement_id="r1")
    assert mon.replay(m).match is True


def test_replay_does_not_authorize():
    mon = AlignmentMonitor()
    m = mon.measure([0.9] * 6)
    mon.replay(m)
    assert m.is_authoritative() is False
    assert m.permits_execution() is False


def test_content_hash_changes_on_mutation():
    mon = AlignmentMonitor()
    m1 = mon.measure([0.9] * 6, measurement_id="same")
    m2 = mon.measure([0.1] * 6, measurement_id="same")
    assert m1.content_hash() != m2.content_hash()
