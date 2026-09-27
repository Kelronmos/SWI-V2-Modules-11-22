"""Tests for DistanceCalculator and classification."""

import math
import pytest

from experimental.cek_alignment_monitor.vector import AlignmentVector
from experimental.cek_alignment_monitor.distance import (
    DistanceCalculator,
    Classification,
    DistanceError,
    DEFAULT_MODERATE_THRESHOLD,
    DEFAULT_HIGH_THRESHOLD,
)


def test_identical_vectors_distance_zero():
    target = AlignmentVector(1, 1, 1, 1, 1, 1)
    calc = DistanceCalculator(target=target)
    v = AlignmentVector(1, 1, 1, 1, 1, 1)
    result = calc.compute(v)
    assert result.distance == 0.0
    assert result.classification == Classification.STABLE


def test_small_deviation_stable():
    calc = DistanceCalculator()
    v = AlignmentVector(0.99, 0.99, 0.99, 0.99, 0.99, 0.99)
    result = calc.compute(v)
    assert result.distance < DEFAULT_MODERATE_THRESHOLD
    assert result.classification == Classification.STABLE


def test_moderate_drift():
    calc = DistanceCalculator()
    v = AlignmentVector(0.7, 0.7, 0.7, 0.7, 0.7, 0.7)
    result = calc.compute(v)
    assert DEFAULT_MODERATE_THRESHOLD <= result.distance < DEFAULT_HIGH_THRESHOLD
    assert result.classification == Classification.MODERATE_DRIFT


def test_high_drift():
    calc = DistanceCalculator()
    v = AlignmentVector(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    result = calc.compute(v)
    assert result.distance >= DEFAULT_HIGH_THRESHOLD
    assert result.classification == Classification.HIGH_DRIFT


def test_deterministic():
    calc = DistanceCalculator()
    v = AlignmentVector(0.8, 0.7, 0.6, 0.5, 0.4, 0.3)
    r1 = calc.compute(v)
    r2 = calc.compute(v)
    assert r1.distance == r2.distance
    assert r1.classification == r2.classification


def test_invalid_weights_negative():
    with pytest.raises(DistanceError, match="negative"):
        DistanceCalculator(weights=[-1.0, 1, 1, 1, 1, 1])


def test_invalid_weights_nan():
    with pytest.raises(DistanceError, match="NaN"):
        DistanceCalculator(weights=[float("nan"), 1, 1, 1, 1, 1])


def test_invalid_weights_inf():
    with pytest.raises(DistanceError, match="infinite"):
        DistanceCalculator(weights=[float("inf"), 1, 1, 1, 1, 1])


def test_zero_total_weight():
    with pytest.raises(DistanceError, match="zero"):
        DistanceCalculator(weights=[0.0] * 6)


def test_wrong_weight_count():
    with pytest.raises(DistanceError, match="Expected 6"):
        DistanceCalculator(weights=[1.0, 1.0])


def test_threshold_order():
    with pytest.raises(DistanceError, match="strictly less"):
        DistanceCalculator(moderate_threshold=0.6, high_threshold=0.4)
