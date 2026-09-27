"""Tests for CEKObservation."""

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.visibility import VisibilityLevel


def test_create_observation():
    mon = AlignmentMonitor()
    obs = mon.observe([0.9] * 6, source_identifier="t", origin_identifier="o")
    assert obs.measurement is not None
    assert obs.provenance is not None
    assert obs.authority_established() is False
    assert obs.execution_permitted() is False


def test_custom_visibility_steps():
    mon = AlignmentMonitor()
    steps = [
        ("A", VisibilityLevel.KNOWN, "a"),
        ("B", VisibilityLevel.UNKNOWN, "gap"),
        ("C", VisibilityLevel.OBSERVABLE, "c"),
    ]
    obs = mon.observe(
        [0.5] * 6,
        visibility_steps=steps,
    )
    assert obs.visibility.has_unknown_edge is True
    assert obs.visibility.frontier == "B"
    assert obs.authority_established() is False
