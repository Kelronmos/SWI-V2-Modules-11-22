"""Tests for AlignmentVector - fail-closed validation."""
import pytest
from experimental.cek_alignment_monitor.vector import AlignmentVector, VectorValidationError

def test_valid_from_sequence():
    v = AlignmentVector.from_sequence([0.0, 0.5, 1.0, 0.25, 0.75, 0.1])
    assert v.as_tuple() == (0.0, 0.5, 1.0, 0.25, 0.75, 0.1)

def test_valid_from_mapping():
    d = {"S": 0.1, "T": 0.2, "Q": 0.3, "E": 0.4, "Se": 0.5, "U": 0.6}
    assert AlignmentVector.from_mapping(d).U == 0.6

def test_wrong_dimension_count():
    with pytest.raises(VectorValidationError):
        AlignmentVector.from_sequence([0.5] * 5)
    with pytest.raises(VectorValidationError):
        AlignmentVector.from_sequence([0.5] * 7)

def test_missing_dimension():
    with pytest.raises(VectorValidationError):
        AlignmentVector.from_mapping({"S": 0.1, "T": 0.2, "Q": 0.3, "E": 0.4, "Se": 0.5})

def test_nan_inf_out_of_range():
    with pytest.raises(VectorValidationError):
        AlignmentVector(0.5, 0.5, float("nan"), 0.5, 0.5, 0.5)
    with pytest.raises(VectorValidationError):
        AlignmentVector(0.5, float("inf"), 0.5, 0.5, 0.5, 0.5)
    with pytest.raises(VectorValidationError):
        AlignmentVector(-0.01, 0.5, 0.5, 0.5, 0.5, 0.5)
    with pytest.raises(VectorValidationError):
        AlignmentVector(0.5, 1.01, 0.5, 0.5, 0.5, 0.5)

def test_non_numeric_rejected():
    with pytest.raises(VectorValidationError):
        AlignmentVector("0.5", 0.5, 0.5, 0.5, 0.5, 0.5)  # type: ignore
