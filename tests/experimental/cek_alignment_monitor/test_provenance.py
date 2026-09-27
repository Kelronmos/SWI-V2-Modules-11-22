"""Tests for ProvenanceRecord."""

import pytest

from experimental.cek_alignment_monitor.vector import AlignmentVector
from experimental.cek_alignment_monitor.measurement import Measurement
from experimental.cek_alignment_monitor.provenance import ProvenanceRecord, ProvenanceError


def test_from_measurement():
    v = AlignmentVector(0.8, 0.8, 0.8, 0.8, 0.8, 0.8)
    m = Measurement.create(v, measurement_id="m-001")
    p = ProvenanceRecord.from_measurement(
        m,
        source_identifier="src-1",
        origin_identifier="orig-1",
    )
    assert p.measurement_id == "m-001"
    assert p.input_hash
    assert p.output_hash == m.content_hash()
    assert p.is_authoritative() is False
    assert p.permits_execution() is False


def test_missing_identifiers_fail():
    v = AlignmentVector(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    m = Measurement.create(v)
    with pytest.raises(ProvenanceError):
        ProvenanceRecord.from_measurement(m, source_identifier="", origin_identifier="x")
    with pytest.raises(ProvenanceError):
        ProvenanceRecord.from_measurement(m, source_identifier="x", origin_identifier="")
