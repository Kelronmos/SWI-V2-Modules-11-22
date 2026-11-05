from dataclasses import dataclass, field
from enum import Enum

class Domain(str, Enum):
    POLICY = "POLICY"
    LAW = "LAW"
    REGION = "REGION"
    STANDARD = "STANDARD"

class State(str, Enum):
    SATISFIED = "SATISFIED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"

@dataclass(frozen=True)
class Requirement:
    id: str
    domain: Domain
    title: str
    state: State
    weight: float = 1.0
    mandatory: bool = False
    source_ref: str = ""
    source_version: str = ""
    jurisdiction: str = ""
    effective_from: str = ""
    effective_to: str = ""
    evidence_refs: tuple = field(default_factory=tuple)
    rationale: str = ""
    na_evidence_ref: str = ""
    prohibits_action: bool = False

    def validate(self):
        if not self.id.strip() or not self.title.strip():
            raise ValueError("Requirement ID and title required")
        if self.weight <= 0:
            raise ValueError("Weight must be positive")
        if self.state == State.SATISFIED and not self.evidence_refs:
            raise ValueError("SATISFIED requires evidence")
        if self.state == State.NOT_APPLICABLE:
            if not self.rationale.strip() or not self.na_evidence_ref.strip():
                raise ValueError("N/A requires rationale and evidence")
        if self.prohibits_action and not self.evidence_refs:
            raise ValueError("Prohibition requires evidence")

@dataclass(frozen=True)
class Board:
    domain: Domain
    requirements: tuple

    def validate(self):
        seen = set()
        for r in self.requirements:
            r.validate()
            if r.domain != self.domain:
                raise ValueError("Cross-domain requirement")
            if r.id in seen:
                raise ValueError("Duplicate requirement ID")
            seen.add(r.id)
