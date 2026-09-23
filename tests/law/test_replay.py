"""Replay guard tests (in-process only).

STATUS: RESEARCH / EXPERIMENTAL
"""
from __future__ import annotations

import pytest

from experimental.law.replay import LawReplayGuard
from swi_v2.kernel.errors import ReplayError


def test_first_event_accepted():
    guard = LawReplayGuard()
    guard.check_and_record("evt-001")


def test_replay_rejected():
    guard = LawReplayGuard()
    guard.check_and_record("evt-001")
    with pytest.raises(ReplayError, match="replayed event"):
        guard.check_and_record("evt-001")


def test_empty_event_id_rejected():
    guard = LawReplayGuard()
    with pytest.raises(ReplayError, match="event_id required"):
        guard.check_and_record("")
