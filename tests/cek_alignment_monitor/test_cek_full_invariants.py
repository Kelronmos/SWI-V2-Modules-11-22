"""Machine-testable CEK invariants (experimental scope only)."""

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.visibility import VisibilityLevel
from tests.cek_alignment_monitor.conftest import assert_no_authority, assert_monitor_surface


def test_measurement_is_not_authority(mon: AlignmentMonitor) -> None:
    assert_no_authority(mon.measure([0.9] * 6))


def test_observation_is_not_authority(mon: AlignmentMonitor) -> None:
    assert_no_authority(mon.observe([0.9] * 6))


def test_unknown_is_not_permitted(mon: AlignmentMonitor) -> None:
    obs, finding, report = mon.full_hidden_edge_observation()
    assert report.has_unknown_edge
    assert report.authority_established is False
    assert_no_authority(obs)
    assert_no_authority(finding)


def test_halt_cannot_execute(mon: AlignmentMonitor) -> None:
    steps = [("ORIGIN", VisibilityLevel.OBSERVABLE, ""), ("HALT", VisibilityLevel.HALTED, "halt")]
    assert_no_authority(mon.observe([0.5] * 6, visibility_steps=steps, context={"execute": True}))


def test_stable_cannot_authorize(mon: AlignmentMonitor) -> None:
    m = mon.measure([1.0] * 6)
    assert m.classification.value == "STABLE"
    assert_no_authority(m)


def test_replay_cannot_create_authority(mon: AlignmentMonitor) -> None:
    m = mon.measure([0.8] * 6)
    mon.replay(m)
    assert_no_authority(m)
    assert_monitor_surface(mon)
