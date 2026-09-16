"""Optional replay guard for Module 11 admission.

admit_foundation_input() alone has no concept of "already seen": the same
serialized evidence can be admitted any number of times, because
integrity_reference deliberately excludes created_at. That is correct for
what M11 verifies (schema + integrity), but replay defense, if wanted, is a
separate, explicit layer — not silently folded into admission.

Additive and opt-in: admit_foundation_input signature/behavior unchanged.

Scope (honest):
- IN-PROCESS, IN-MEMORY only — no persistence across restarts, no cross-machine
  coordination.
- Not a substitute for CRTG or a durable shared replay cache.
- Reference building block, not production replay-defense.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set

from .admission import admit_foundation_input
from .contracts import AdmittedInput
from .errors import ReplayError


@dataclass
class ReplayGuard:
    """Tracks evidence_ids admitted through this guard instance."""

    _seen: Set[str] = field(default_factory=set)

    def admit(self, candidate) -> AdmittedInput:
        """Admit via admit_foundation_input, then reject replay of evidence_id.

        Invalid candidates raise before recording; only successful admissions
        are remembered.
        """
        admitted = admit_foundation_input(candidate)
        if admitted.evidence_id in self._seen:
            raise ReplayError(
                f"evidence_id already admitted by this guard: {admitted.evidence_id!r}"
            )
        self._seen.add(admitted.evidence_id)
        return admitted

    def reset(self) -> None:
        """Clear seen-evidence state (tests / explicit re-arm only)."""
        self._seen.clear()
