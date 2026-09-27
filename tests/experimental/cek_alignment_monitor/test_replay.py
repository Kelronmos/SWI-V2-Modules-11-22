"""Tests for ReplayEngine."""

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.vector import AlignmentVector
from experimental.cek_alignment_monitor.measurement import Measurement
from experimental.cek_alignment_monitor.distance import DistanceCalculator
from experimental.cek_alignment_monitor.replay import ReplayEngine, ReplayError


def test_replay_match():
    mon = AlignmentMonitor()
    m = mon.measure([0.85, 0.85, 0.85, 0.85, 0.85, 0.85], measurement_id="replay-1")
    result = mon.replay(m)
    assert result.match is True
    assert result.original_hash == result.replay_hash
    assert abs(result.original_distance - result.replay_distance) < 1e-12


def test_replay_mismatch_on_mutation():
    mon = AlignmentMonitor()
    original = mon.measure([0.9] * 6, measurement_id="orig")
    mutated_vector = AlignmentVector(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    mutated = Measurement.create(
        mutated_vector,
        calculator=DistanceCalculator(target=original.target, weights=original.weights),
        measurement_id=original.measurement_id,
    )
    engine = ReplayEngine()
    assert engine.replay(original).match is True
    assert mutated.distance != original.distance
