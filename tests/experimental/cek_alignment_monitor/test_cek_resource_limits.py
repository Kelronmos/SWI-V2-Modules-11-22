"""Experimental resource-budget checks (not production SLA claims)."""

from __future__ import annotations

import time

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.vector import VectorValidationError
from tests.experimental.cek_alignment_monitor.conftest import assert_no_authority


def test_large_metadata_stripped_and_bounded(mon: AlignmentMonitor) -> None:
    big = {"authorized": True, "payload": "x" * 100_000}
    t0 = time.perf_counter()
    obs = mon.observe([0.5] * 6, context=big)
    elapsed = time.perf_counter() - t0
    assert_no_authority(obs)
    assert "authorized" not in obs.context
    assert elapsed < 5.0


def test_oversized_vector_rejected(mon: AlignmentMonitor) -> None:
    with pytest.raises((VectorValidationError, TypeError, ValueError)):
        mon.measure([0.5] * 10_000)


def test_repeated_replay_budget(mon: AlignmentMonitor) -> None:
    m = mon.measure([0.9] * 6)
    t0 = time.perf_counter()
    for _ in range(200):
        r = mon.replay(m)
        assert r.match is True
    assert time.perf_counter() - t0 < 10.0
