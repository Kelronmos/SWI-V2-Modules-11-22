"""Append-only experimental law registry.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED

Artifacts are immutable evidence.
Lifecycle changes are separate immutable events.
Nothing rewrites the original law record.

Fixes applied:
- Authority binding respects kernel contract (action ∈ declared_scopes)
- Supersession is atomic: full validation before any write
- Lifecycle event hashes are recomputed and verified
- append_event is authority-gated (no public write bypass)
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from swi_v2.kernel.errors import ModuleKernelError

from .authority import LawMutation, authorize_law_mutation
from .canonical import compute_event_hash
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

    def _verify_event_integrity(self, event: LawLifecycleEvent) -> None:
        """Recompute hash; reject if mismatch or empty."""
        if not event.event_hash:
            raise LawRegistryError("event must be hashed before storage")

        fields = {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "law_id": event.law_id,
            "version": event.version,
            "actor": event.actor,
            "authority_scope": event.authority_scope,
            "created_at": event.created_at,
            "previous_status": (
                event.previous_status.value if event.previous_status else None
            ),
            "resulting_status": event.resulting_status.value,
            "related_version": event.related_version,
        }
        expected = compute_event_hash(fields)
        if event.event_hash != expected:
            raise LawRegistryError(
                f"lifecycle event hash mismatch: expected {expected}, "
                f"got {event.event_hash}"
            )

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

    def append_event(
        self,
        event: LawLifecycleEvent,
        *,
        authorization_present: bool,
        authorization_scope: Optional[str],
    ) -> LawLifecycleEvent:
        """Authority-gated event append. Integrity is not permission."""
        authorize_law_mutation(
            mutation=LawMutation.INGEST,
            authorization_present=authorization_present,
            authorization_scope=authorization_scope,
        )

        if event.event_id in self._events:
            raise LawRegistryError("event already exists")

        self._verify_event_integrity(event)

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
        """Atomic supersession: validate everything, then write both or neither.

        Never rewrites the old artifact.
        """
        # 1. Authority first
        authorize_law_mutation(
            mutation=LawMutation.SUPERSEDE,
            authorization_present=authorization_present,
            authorization_scope=authorization_scope,
        )

        # 2. Structural checks (no writes yet)
        if old.law_id != new.law_id:
            raise LawRegistryError("supersede requires same law_id")
        if old.version == new.version:
            raise LawRegistryError("new version required")

        current_old = self.get(old.law_id, old.version)
        if current_old != old:
            raise LawRegistryError("old artifact does not match registry")

        new_key = (new.law_id, new.version)
        if new_key in self._artifacts:
            raise LawRegistryError("new version already exists")

        if event.event_type != LifecycleEventType.SUPERSEDE:
            raise LawRegistryError("invalid lifecycle event")
        if event.related_version != new.version:
            raise LawRegistryError("supersession event mismatch")
        if event.law_id != old.law_id or event.version != old.version:
            raise LawRegistryError("event does not reference the superseded version")

        # 3. Integrity of the new artifact (still no writes)
        result = verify_integrity(new)
        if result.outcome != IntegrityOutcome.PASS:
            raise LawRegistryError(f"integrity failed on new artifact: {result.reason}")

        # 4. Integrity of the lifecycle event (still no writes)
        self._verify_event_integrity(event)

        if event.event_id in self._events:
            raise LawRegistryError("event already exists")

        # 5. All checks passed — perform both writes
        self._artifacts[new_key] = new
        self._events[event.event_id] = event

        # IMPORTANT: old artifact is NOT rewritten.
        return new
