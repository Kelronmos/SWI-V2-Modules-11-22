"""Experimental resource-budget checks (not production SLA claims)."""

import time

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.vector import VectorValidationError


def test_large_metadata_stripped_and_bounded():
    mon = AlignmentMonitor()
    big = {"authorized": True, "payload": "x" * 100_000}
    t0 = time.perf_counter()
    obs = mon.observe([0.5] * 6, context=big)
    assert obs.authority_established() is False
    assert "authorized" not in obs.context
    assert time.perf_counter() - t0 < 5.0


def test_oversized_vector_rejected():
    mon = AlignmentMonitor()
    with pytest.raises((VectorValidationError, TypeError, ValueError)):
        mon.measure([0.5] * 10_000)


def test_repeated_replay_budget():
    mon = AlignmentMonitor()
    m = mon.measure([0.9] * 6)
    t0 = time.perf_counter()
    for _ in range(200):
        assert mon.replay(m).match is True
    assert time.perf_counter() - t0 < 10.0
