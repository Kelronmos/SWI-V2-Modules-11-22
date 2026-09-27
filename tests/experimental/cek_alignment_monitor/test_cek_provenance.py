"""Tests for ProvenanceRecord."""

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.provenance import ProvenanceRecord, ProvenanceError


def test_provenance_not_authority():
    mon = AlignmentMonitor()
    m = mon.measure([0.9] * 6)
    p = ProvenanceRecord.from_measurement(m, source_identifier="src", origin_identifier="orig")
    assert p.is_authoritative() is False
    assert p.permits_execution() is False


def test_empty_source_rejected():
    mon = AlignmentMonitor()
    m = mon.measure([0.9] * 6)
    with pytest.raises(ProvenanceError):
        ProvenanceRecord.from_measurement(m, source_identifier="", origin_identifier="orig")
