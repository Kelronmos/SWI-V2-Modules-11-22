"""Tests for AlignmentVector — fail-closed validation."""

import math
import pytest

from experimental.cek_alignment_monitor.vector import (
    AlignmentVector,
    VectorValidationError,
    DIMENSIONS,
    DIM_COUNT,
)


def test_valid_vector_from_sequence():
    v = AlignmentVector.from_sequence([0.0, 0.5, 1.0, 0.25, 0.75, 0.1])
    assert v.as_tuple() == (0.0, 0.5, 1.0, 0.25, 0.75, 0.1)


def test_valid_vector_from_mapping():
    d = {"S": 0.1, "T": 0.2, "Q": 0.3, "E": 0.4, "Se": 0.5, "U": 0.6}
    v = AlignmentVector.from_mapping(d)
    assert v.S == 0.1 and v.U == 0.6


def test_identical_construction():
    v1 = AlignmentVector(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    v2 = AlignmentVector.from_sequence([0.5] * 6)
    assert v1.as_tuple() == v2.as_tuple()


def test_wrong_dimension_count():
    with pytest.raises(VectorValidationError, match="exactly 6"):
        AlignmentVector.from_sequence([0.5] * 5)
    with pytest.raises(VectorValidationError, match="exactly 6"):
        AlignmentVector.from_sequence([0.5] * 7)


def test_missing_dimension():
    d = {"S": 0.1, "T": 0.2, "Q": 0.3, "E": 0.4, "Se": 0.5}
    with pytest.raises(VectorValidationError, match="Missing"):
        AlignmentVector.from_mapping(d)


def test_extra_dimension():
    d = {k: 0.5 for k in DIMENSIONS}
    d["EXTRA"] = 0.9
    with pytest.raises(VectorValidationError, match="Unknown"):
        AlignmentVector.from_mapping(d)


def test_nan_rejected():
    with pytest.raises(VectorValidationError, match="NaN"):
        AlignmentVector(0.5, 0.5, float("nan"), 0.5, 0.5, 0.5)


def test_inf_rejected():
    with pytest.raises(VectorValidationError, match="infinite"):
        AlignmentVector(0.5, float("inf"), 0.5, 0.5, 0.5, 0.5)
    with pytest.raises(VectorValidationError, match="infinite"):
        AlignmentVector(0.5, float("-inf"), 0.5, 0.5, 0.5, 0.5)


def test_out_of_range_rejected():
    with pytest.raises(VectorValidationError, match="outside"):
        AlignmentVector(-0.01, 0.5, 0.5, 0.5, 0.5, 0.5)
    with pytest.raises(VectorValidationError, match="outside"):
        AlignmentVector(0.5, 1.01, 0.5, 0.5, 0.5, 0.5)


def test_non_numeric_rejected():
    with pytest.raises(VectorValidationError):
        AlignmentVector("0.5", 0.5, 0.5, 0.5, 0.5, 0.5)  # type: ignore


def test_canonical_repr_deterministic():
    v = AlignmentVector(0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    r1 = v.canonical_repr()
    r2 = v.canonical_repr()
    assert r1 == r2
    assert "S=0.1000000000" in r1
