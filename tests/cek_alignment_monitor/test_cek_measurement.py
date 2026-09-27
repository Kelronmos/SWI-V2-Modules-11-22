"""Tests for Measurement object."""

from experimental.cek_alignment_monitor.vector import AlignmentVector
from experimental.cek_alignment_monitor.distance import Classification
from experimental.cek_alignment_monitor.measurement import Measurement


def test_create_and_content_hash_stable():
    v = AlignmentVector(0.9, 0.9, 0.9, 0.9, 0.9, 0.9)
    m1 = Measurement.create(v, measurement_id="fixed-id-001")
    m2 = Measurement.create(v, measurement_id="fixed-id-001")
    assert m1.content_hash() == m2.content_hash()
    assert m1.distance == m2.distance


def test_identical_to_target_is_stable():
    v = AlignmentVector(1, 1, 1, 1, 1, 1)
    m = Measurement.create(v)
    assert m.distance == 0.0
    assert m.classification == Classification.STABLE


def test_no_authority_fields():
    v = AlignmentVector(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    m = Measurement.create(v)
    assert m.is_authoritative() is False
    assert m.permits_execution() is False
    assert m.admits() is False
    assert m.seals() is False
    d = m.to_dict()
    for forbidden in ("authorized", "permit", "execute", "seal", "admit", "approved"):
        assert forbidden not in d
