"""Append-only experimental law registry.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED

Artifacts are immutable evidence.
Lifecycle changes are separate immutable events.
Nothing rewrites the original law record.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from swi_v2.kernel.errors import ModuleKernelError

from .authority import LawMutation, authorize_law_mutation
from .integrity import IntegrityOutcome, verify_integrity
from .models import (
    LawArtifact,
    LawLifecycleEvent,
    LawStatus,
    LifecycleEventType,
)


class LawRegistryError(ModuleKernelError):
    pass


class LawRegistry:
    """In-memory versioned store for demonstration.

    Key = (law_id, version). Never overwrites an existing artifact.
    Supersession is recorded only via LawLifecycleEvent.
    """

    def __init__(self) -> None:
        self._artifacts: Dict[Tuple[str, str], LawArtifact] = {}
        self._events: Dict[str, LawLifecycleEvent] = {}

    def get(self, law_id: str, version: str) -> Optional[LawArtifact]:
        return self._artifacts.get((law_id, version))

    def list_versions(self, law_id: str) -> List[str]:
        return sorted(
            version for lid, version in self._artifacts if lid == law_id
        )

    def events(self, law_id: str, version: str) -> List[LawLifecycleEvent]:
        return [
            event
            for event in self._events.values()
            if event.law_id == law_id and event.version == version
        ]

    def ingest(
        self,
        artifact: LawArtifact,
        *,
        authorization_present: bool,
        authorization_scope: Optional[str],
    ) -> LawArtifact:
        authorize_law_mutation(
            mutation=LawMutation.INGEST,
            authorization_present=authorization_present,
            authorization_scope=authorization_scope,
        )

        key = (artifact.law_id, artifact.version)
        if key in self._artifacts:
            raise LawRegistryError("existing version cannot be overwritten")

        result = verify_integrity(artifact)
        if result.outcome != IntegrityOutcome.PASS:
            raise LawRegistryError(f"integrity failed: {result.reason}")

        self._artifacts[key] = artifact
        return artifact

    def append_event(self, event: LawLifecycleEvent) -> LawLifecycleEvent:
        if event.event_id in self._events:
            raise LawRegistryError("event already exists")
        if not event.event_hash:
            raise LawRegistryError("event must be hashed before storage")

        self._events[event.event_id] = event
        return event

    def supersede(
        self,
        old: LawArtifact,
        new: LawArtifact,
        *,
        authorization_present: bool,
        authorization_scope: Optional[str],
        event: LawLifecycleEvent,
    ) -> LawArtifact:
        """Record supersession via event only. Never rewrite the old artifact."""
        authorize_law_mutation(
            mutation=LawMutation.SUPERSEDE,
            authorization_present=authorization_present,
            authorization_scope=authorization_scope,
        )

        if old.law_id != new.law_id:
            raise LawRegistryError("supersede requires same law_id")
        if old.version == new.version:
            raise LawRegistryError("new version required")

        current_old = self.get(old.law_id, old.version)
        if current_old != old:
            raise LawRegistryError("old artifact does not match registry")

        # Verify and store new evidence first (append-only).
        self.ingest(
            new,
            authorization_present=authorization_present,
            authorization_scope=authorization_scope,
        )

        if event.event_type != LifecycleEventType.SUPERSEDE:
            raise LawRegistryError("invalid lifecycle event")
        if event.related_version != new.version:
            raise LawRegistryError("supersession event mismatch")

        self.append_event(event)

        # IMPORTANT: old artifact is NOT rewritten.
        return new
