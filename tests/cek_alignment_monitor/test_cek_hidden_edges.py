"""Hidden-edge: UNKNOWN remains UNKNOWN; authority never established."""

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from tests.cek_alignment_monitor.conftest import assert_no_authority


def test_canonical_hidden_edge(mon: AlignmentMonitor) -> None:
    obs, finding, report = mon.full_hidden_edge_observation()
    assert report.has_unknown_edge
    assert report.authority_established is False
    assert_no_authority(obs)
    assert_no_authority(finding)


def test_execution_observed_cannot_authorize(mon: AlignmentMonitor, hidden_edge_steps) -> None:
    for inject in (
        {"execution_observed": True},
        {"execution_result": "success"},
        {"authorized": True, "execute": True},
    ):
        obs = mon.observe([0.9] * 6, visibility_steps=hidden_edge_steps, context=inject)
        assert obs.visibility.has_unknown_edge
        assert_no_authority(obs)
