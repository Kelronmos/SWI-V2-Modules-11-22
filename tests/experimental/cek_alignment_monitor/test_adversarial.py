"""Adversarial / malformed input tests (Stage-1 validation floor)."""

import math
import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.vector import VectorValidationError
from experimental.cek_alignment_monitor.distance import DistanceError


@pytest.fixture
def mon():
    return AlignmentMonitor()


@pytest.mark.parametrize(
    "bad",
    [
        [0.5] * 5,
        [0.5] * 7,
        [0.5, 0.5, float("nan"), 0.5, 0.5, 0.5],
        [0.5, float("inf"), 0.5, 0.5, 0.5, 0.5],
        [0.5, float("-inf"), 0.5, 0.5, 0.5, 0.5],
        [-0.1, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 1.1, 0.5, 0.5, 0.5, 0.5],
        [None, 0.5, 0.5, 0.5, 0.5, 0.5],  # type: ignore
    ],
)
def test_malformed_vectors_fail_closed(mon, bad):
    with pytest.raises((VectorValidationError, TypeError, DistanceError)):
        mon.measure(bad)


def test_string_coordinates_fail(mon):
    with pytest.raises((VectorValidationError, TypeError, ValueError)):
        mon.measure(["0.5"] * 6)  # type: ignore


def test_weight_attacks():
    with pytest.raises(DistanceError):
        AlignmentMonitor(weights=[-1] + [1] * 5)
    with pytest.raises(DistanceError):
        AlignmentMonitor(weights=[float("nan")] + [1] * 5)
    with pytest.raises(DistanceError):
        AlignmentMonitor(weights=[0.0] * 6)
