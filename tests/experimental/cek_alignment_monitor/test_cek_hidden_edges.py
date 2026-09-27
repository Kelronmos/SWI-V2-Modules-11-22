"""Hidden-edge centrepiece: UNKNOWN remains UNKNOWN; authority never established."""

from __future__ import annotations

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.visibility import VisibilityLevel
from tests.experimental.cek_alignment_monitor.conftest import assert_no_authority


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
        {"valid_signature": "sig"},
        {"valid_hash": "hash"},
        {"human_approval": True},
        {"authorized": True, "execute": True},
        {"post_execution_evidence": "ev-001"},
    ):
        obs = mon.observe(
            [0.9] * 6,
            visibility_steps=hidden_edge_steps,
            context=inject,
            evidence_reference="post-exec",
        )
        assert obs.visibility.has_unknown_edge
        assert_no_authority(obs)
        finding = mon.finding_from_observation(obs)
        assert_no_authority(finding)


def test_stable_alignment_does_not_fill_unknown(mon: AlignmentMonitor, hidden_edge_steps) -> None:
    obs = mon.observe([1.0] * 6, visibility_steps=hidden_edge_steps)
    assert obs.visibility.has_unknown_edge
    assert_no_authority(obs)
