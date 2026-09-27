"""Tests for DistanceCalculator."""
import math
import pytest
from experimental.cek_alignment_monitor.distance import DistanceCalculator, DistanceError, Classification
from experimental.cek_alignment_monitor.monitor import AlignmentMonitor

def test_identical_zero_distance():
    mon = AlignmentMonitor()
    m = mon.measure([1.0] * 6)
    assert m.distance == 0.0
    assert m.classification == Classification.STABLE

def test_single_axis_deviation():
    """Equal weights are normalized (sum=1); one-axis 0.1 delta => sqrt(0.01/6)."""
    mon = AlignmentMonitor()
    m = mon.measure([0.9, 1, 1, 1, 1, 1])
    expected = math.sqrt((0.1 ** 2) / 6)
    assert math.isclose(m.distance, expected, abs_tol=1e-9)

def test_negative_weight_rejected():
    with pytest.raises(DistanceError):
        DistanceCalculator(weights=[-1] + [1] * 5)

def test_nan_weight_rejected():
    with pytest.raises(DistanceError):
        DistanceCalculator(weights=[float("nan")] + [1] * 5)

def test_zero_total_weight_rejected():
    with pytest.raises(DistanceError):
        DistanceCalculator(weights=[0.0] * 6)

def test_high_drift_label_only():
    mon = AlignmentMonitor()
    m = mon.measure([0.0] * 6)
    assert m.classification == Classification.HIGH_DRIFT
    assert m.is_authoritative() is False
