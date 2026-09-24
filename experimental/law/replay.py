"""In-process replay defence only.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED
This does NOT claim durable distributed replay protection.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from swi_v2.kernel.errors import ReplayError


@dataclass
class LawReplayGuard:
    """Rejects duplicate event_id within this process."""

    _seen: set[str] = field(default_factory=set)

    def check_and_record(self, event_id: str) -> None:
        if not event_id:
            raise ReplayError("event_id required")

        if event_id in self._seen:
            raise ReplayError(f"replayed event: {event_id}")

        self._seen.add(event_id)

    def reset(self) -> None:
        self._seen.clear()
