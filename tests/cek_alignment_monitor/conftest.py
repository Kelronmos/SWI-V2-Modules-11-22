"""Shared fixtures for CEK Alignment Monitor verification suite."""

from __future__ import annotations

import pytest

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from experimental.cek_alignment_monitor.vector import AlignmentVector
from experimental.cek_alignment_monitor.visibility import VisibilityLevel


@pytest.fixture
def mon() -> AlignmentMonitor:
    return AlignmentMonitor()


@pytest.fixture
def ideal_vector() -> AlignmentVector:
    return AlignmentVector.from_sequence([1.0] * 6)


@pytest.fixture
def sample_vector() -> AlignmentVector:
    return AlignmentVector.from_sequence([0.9, 0.85, 0.8, 0.9, 0.7, 0.75])


@pytest.fixture
def hidden_edge_steps():
    return [
        ("ORIGIN", VisibilityLevel.OBSERVABLE, "request"),
        ("CONTEXT", VisibilityLevel.OBSERVABLE, "context"),
        ("EVIDENCE", VisibilityLevel.TRACEABLE, "evidence"),
        ("ADMISSION", VisibilityLevel.TRACEABLE, "admission"),
        ("NEXT_EDGE", VisibilityLevel.UNKNOWN, "hidden transition"),
        ("EXECUTION", VisibilityLevel.OBSERVABLE, "outcome observed"),
    ]


def assert_no_authority(obj) -> None:
    if hasattr(obj, "authority_established"):
        assert obj.authority_established() is False
    if hasattr(obj, "execution_permitted"):
        assert obj.execution_permitted() is False
    if hasattr(obj, "is_authoritative"):
        assert obj.is_authoritative() is False
    if hasattr(obj, "permits_execution"):
        assert obj.permits_execution() is False
    if hasattr(obj, "admits"):
        assert obj.admits() is False
    if hasattr(obj, "seals"):
        assert obj.seals() is False


def assert_monitor_surface(mon: AlignmentMonitor) -> None:
    for name in ("authorize", "permit", "execute", "seal", "admit", "bind", "dispatch", "approve"):
        assert not hasattr(mon, name)
