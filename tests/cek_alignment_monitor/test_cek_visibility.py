"""Tests for VisibilityAnalyzer."""

from experimental.cek_alignment_monitor.visibility import VisibilityAnalyzer, VisibilityLevel
from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_no_interpolation_across_unknown():
    analyzer = VisibilityAnalyzer()
    report = analyzer.analyze(
        [
            ("A", VisibilityLevel.KNOWN, ""),
            ("GAP", VisibilityLevel.UNKNOWN, "gap"),
            ("D", VisibilityLevel.OBSERVABLE, ""),
        ]
    )
    names = [n.name for n in report.nodes]
    assert "C" not in names
    assert report.has_unknown_edge
    assert report.authority_established is False


def test_hidden_edge_frontier():
    mon = AlignmentMonitor()
    obs, finding, report = mon.full_hidden_edge_observation()
    assert report.has_unknown_edge
    assert report.authority_established is False
    assert finding.is_authoritative() is False
