"""
Repository-determined status engine.

YES / NO / UNKNOWN / CONFLICT are first-class.
Never: UNKNOWN→YES, NOT_RUN→FAIL, TESTED→PROVEN, BOOT→READY.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

YES = "YES"
NO = "NO"
UNKNOWN = "UNKNOWN"
CONFLICT = "CONFLICT"
MISSING = "MISSING"
STALE = "STALE"
NOT_APPLICABLE = "NOT_APPLICABLE"

CONFIRMED = "CONFIRMED"
REFUTED = "REFUTED"
UNRESOLVED = "UNRESOLVED"


@dataclass
class StatusField:
    status: str = UNKNOWN
    declared_status: Any = None
    observed_status: Any = None
    effective_status: str = UNKNOWN
    evidence_state: str = UNKNOWN
    resolution: str = UNRESOLVED
    requires_revalidation: bool = False
    sources: list = field(default_factory=list)
    blocking_conditions: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_status(
    *,
    declared: Any = None,
    observed: Any = None,
    required: bool | None = None,
    evidence_present: bool = False,
) -> StatusField:
    """Resolve declared vs observed without inventing certainty."""
    sources: list[dict] = []
    if declared is not None:
        sources.append({"type": "repository_declaration", "value": declared})
    if observed is not None:
        sources.append({"type": "current_observation", "value": observed})

    # Normalize booleans / strings
    def norm(v: Any) -> str | None:
        if v is None:
            return None
        if isinstance(v, bool):
            return YES if v else NO
        s = str(v).strip().upper()
        if s in (YES, NO, UNKNOWN, CONFLICT, MISSING, STALE, NOT_APPLICABLE,
                 "TRUE", "FALSE", "PASS", "FAIL"):
            if s == "TRUE":
                return YES
            if s == "FALSE":
                return NO
            if s == "PASS":
                return YES
            if s == "FAIL":
                return NO
            return s
        return UNKNOWN

    d = norm(declared)
    o = norm(observed)

    if d is None and o is None:
        if required is True:
            return StatusField(
                status=MISSING if not evidence_present else UNKNOWN,
                effective_status=MISSING if not evidence_present else UNKNOWN,
                evidence_state=UNKNOWN,
                resolution=UNRESOLVED,
                sources=sources,
                blocking_conditions=["required condition not established"] if required else [],
            )
        return StatusField(
            status=UNKNOWN,
            effective_status=UNKNOWN,
            evidence_state=UNKNOWN,
            resolution=UNRESOLVED,
            sources=sources,
        )

    if d is not None and o is not None and d != o:
        return StatusField(
            status=CONFLICT,
            declared_status=d,
            observed_status=o,
            effective_status=CONFLICT,
            evidence_state=CONFLICT,
            resolution=UNRESOLVED,
            requires_revalidation=True,
            sources=sources,
            blocking_conditions=["conflicting status evidence"],
        )

    value = d if d is not None else o
    return StatusField(
        status=value or UNKNOWN,
        declared_status=d,
        observed_status=o,
        effective_status=value or UNKNOWN,
        evidence_state=CONFIRMED if evidence_present else UNKNOWN,
        resolution="RESOLVED" if value in (YES, NO) and evidence_present else UNRESOLVED,
        sources=sources,
    )


def repository_status_object(
    repository: str,
    commit_sha: str | None,
    *,
    declared: dict | None = None,
    observed: dict | None = None,
) -> dict[str, Any]:
    """Build dual declared/observed status for one repository."""
    declared = declared or {}
    observed = observed or {}

    fields = {}
    for key in (
        "designed", "implemented", "tested", "verified",
        "proven", "sealed", "production_ready", "production_authorized",
    ):
        fields[key] = resolve_status(
            declared=declared.get(key),
            observed=observed.get(key),
            evidence_present=key in declared or key in observed,
        ).to_dict()

    # Hard ceiling: never promote production_authorized to YES from runner alone
    pa = fields["production_authorized"]
    if pa["effective_status"] == YES and not declared.get("production_authorized"):
        fields["production_authorized"] = resolve_status(
            declared=declared.get("production_authorized"),
            observed=None,
        ).to_dict()

    return {
        "repository": repository,
        "commit_sha": commit_sha,
        **fields,
        "status_source": list(declared.keys()) + list(observed.keys()),
        "evidence": [],
        "blocking_conditions": [],
    }


def overall_swi_ceiling() -> dict[str, Any]:
    """Current known SWI claim ceiling — not upgraded by runner success."""
    return {
        "system_completion": "INCOMPLETE",
        "proven": NO,
        "sealed": NO,
        "production_ready": UNKNOWN,  # no declaration → UNKNOWN, not NO
        "production_authorized": NO,  # explicitly locked false in packages claims
        "authorization_granted": False,
        "action_permitted": False,
        "note": (
            "Runner observation does not manufacture production readiness. "
            "UNKNOWN remains UNKNOWN. BOOT_PASS ≠ PRODUCTION_READY."
        ),
    }
