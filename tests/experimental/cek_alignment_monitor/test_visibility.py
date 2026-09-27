"""Tests for VisibilityAnalyzer and hidden-edge demo."""

from experimental.cek_alignment_monitor.visibility import (
    VisibilityAnalyzer,
    VisibilityLevel,
)


def test_hidden_edge_demo():
    analyzer = VisibilityAnalyzer()
    report = analyzer.hidden_edge_demo()
    assert report.has_unknown_edge is True
    assert report.frontier == "NEXT_EDGE"
    assert report.authority_established is False

    names = [n.name for n in report.nodes]
    assert names == [
        "ORIGIN",
        "CONTEXT",
        "EVIDENCE",
        "ADMISSION",
        "NEXT_EDGE",
        "EXECUTION",
    ]
    levels = {n.name: n.level for n in report.nodes}
    assert levels["NEXT_EDGE"] == VisibilityLevel.UNKNOWN
    assert levels["EXECUTION"] == VisibilityLevel.OBSERVABLE


def test_no_interpolation_across_unknown():
    analyzer = VisibilityAnalyzer()
    steps = [
        ("A", VisibilityLevel.KNOWN, ""),
        ("B", VisibilityLevel.TRACEABLE, ""),
        ("GAP", VisibilityLevel.UNKNOWN, "uninstrumented"),
        ("D", VisibilityLevel.OBSERVABLE, ""),
    ]
    report = analyzer.analyze(steps)
    assert report.has_unknown_edge
    assert report.frontier == "GAP"
    node_names = [n.name for n in report.nodes]
    assert "C" not in node_names
