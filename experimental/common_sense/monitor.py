"""Experimental Common Sense diagnostic monitor.

This module is intentionally non-authoritative.

It may:
    - detect
    - analyse
    - diagnose
    - compare patterns
    - estimate risk
    - record evidence
    - request human escalation
    - halt a downstream path

It must never:
    - execute
    - promote
    - seal
    - authorize
    - extend authorization
    - renew authorization

Core invariant:

    DATA != EVIDENCE != ADMISSION != AUTHORIZATION != ACTION

Research status:
    EXPERIMENTAL
    NOT SEALED
    NOT PRODUCTION READY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import FrozenSet, Mapping


class Sensitivity(str, Enum):
    PUBLIC = "PUBLIC"
    PERSONAL = "PERSONAL"
    SENSITIVE = "SENSITIVE"
    VULNERABLE = "VULNERABLE"


class CommonSenseDecision(str, Enum):
    CONTINUE = "CONTINUE"
    RECHECK = "RECHECK"
    HALT = "HALT"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class AuthorizationContext:
    principal: str
    scope: FrozenSet[str]
    purpose: str
    started_at: datetime
    expires_at: datetime
    conditions: FrozenSet[str] = frozenset()
    revoked: bool = False

    def valid_at(
        self,
        now: datetime,
        required_scope: FrozenSet[str] = frozenset(),
        required_conditions: FrozenSet[str] = frozenset(),
    ) -> bool:
        if self.revoked:
            return False

        if now < self.started_at:
            return False

        if now >= self.expires_at:
            return False

        if not required_scope.issubset(self.scope):
            return False

        if not required_conditions.issubset(self.conditions):
            return False

        return True


@dataclass(frozen=True)
class HarmProfile:
    sensitivity: Sensitivity = Sensitivity.PUBLIC
    vulnerable_population: float = 0.0
    privacy_impact: float = 0.0
    security_impact: float = 0.0
    physical_harm: float = 0.0
    economic_harm: float = 0.0
    dignity_harm: float = 0.0
    reversibility: float = 1.0
    downstream_consequence: float = 0.0

    def normalized(self) -> "HarmProfile":
        def clamp(value: float) -> float:
            return max(0.0, min(1.0, float(value)))

        return HarmProfile(
            sensitivity=self.sensitivity,
            vulnerable_population=clamp(self.vulnerable_population),
            privacy_impact=clamp(self.privacy_impact),
            security_impact=clamp(self.security_impact),
            physical_harm=clamp(self.physical_harm),
            economic_harm=clamp(self.economic_harm),
            dignity_harm=clamp(self.dignity_harm),
            reversibility=clamp(self.reversibility),
            downstream_consequence=clamp(self.downstream_consequence),
        )


@dataclass(frozen=True)
class RiskWeights:
    privacy: float = 1.0
    security: float = 1.0
    physical: float = 1.5
    economic: float = 1.0
    dignity: float = 1.0
    irreversible: float = 2.0
    downstream: float = 1.5
    vulnerable: float = 1.5

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if value < 0:
                raise ValueError(f"risk weight must be non-negative: {name}")


@dataclass(frozen=True)
class PatternObservation:
    name: str
    occurrences: int = 0
    baseline_occurrences: int = 0
    authority_drift: bool = False
    repeated_failure: bool = False
    abnormal_sequence: bool = False

    def signal(self) -> float:
        repetition = 0.0

        if self.baseline_occurrences > 0:
            repetition = min(
                1.0,
                self.occurrences / self.baseline_occurrences,
            )
        elif self.occurrences > 0:
            repetition = 1.0

        flags = sum(
            [
                self.authority_drift,
                self.repeated_failure,
                self.abnormal_sequence,
            ]
        ) / 3.0

        return min(1.0, (repetition + flags) / 2.0)


@dataclass(frozen=True)
class SimulationCase:
    case_id: str
    sensitivity: Sensitivity
    required_scope: FrozenSet[str]
    required_conditions: FrozenSet[str]
    now: datetime
    authorization: AuthorizationContext
    harm: HarmProfile
    pattern: PatternObservation
    equation_match: bool
    privacy_minimized: bool
    security_boundary_intact: bool
    downstream_pipe: bool = True


@dataclass(frozen=True)
class EvidenceRecord:
    case_id: str
    decision: CommonSenseDecision
    reason_codes: tuple[str, ...]
    risk_score: float
    risk_priority: str
    pattern_signal: float
    payload_retained: bool = False
    sensitive_payload_retained: bool = False
    human_findings_required: bool = True

    def canonical(self) -> Mapping[str, object]:
        return {
            "case_id": self.case_id,
            "decision": self.decision.value,
            "reason_codes": self.reason_codes,
            "risk_score": self.risk_score,
            "risk_priority": self.risk_priority,
            "pattern_signal": self.pattern_signal,
            "payload_retained": self.payload_retained,
            "sensitive_payload_retained": self.sensitive_payload_retained,
            "human_findings_required": self.human_findings_required,
        }


class CommonSenseMonitor:
    """Research-only diagnostic monitor.

    Common Sense can observe and halt.

    Common Sense cannot become an authority source.
    """

    FORBIDDEN = frozenset(
        {
            "EXECUTE",
            "PROMOTE",
            "SEAL",
            "AUTHORIZE",
            "EXTEND_AUTHORIZATION",
            "RENEW_AUTHORIZATION",
        }
    )

    def __init__(self, weights: RiskWeights | None = None) -> None:
        self.weights = weights or RiskWeights()
        self.weights.validate()

    def risk_score(self, case: SimulationCase) -> float:
        harm = case.harm.normalized()
        pattern = case.pattern.signal()

        return (
            harm.privacy_impact * self.weights.privacy
            + harm.security_impact * self.weights.security
            + harm.physical_harm * self.weights.physical
            + harm.economic_harm * self.weights.economic
            + harm.dignity_harm * self.weights.dignity
            + (1.0 - harm.reversibility) * self.weights.irreversible
            + harm.downstream_consequence * self.weights.downstream
            + harm.vulnerable_population * self.weights.vulnerable
            + pattern
        )

    @staticmethod
    def priority(score: float) -> str:
        if score >= 5.0:
            return "CRITICAL"
        if score >= 3.0:
            return "HIGH"
        if score >= 1.5:
            return "MEDIUM"
        return "LOW"

    def inspect(self, case: SimulationCase) -> EvidenceRecord:
        harm = case.harm.normalized()
        pattern_signal = case.pattern.signal()
        score = self.risk_score(case)
        reasons: list[str] = []

        if not case.authorization.valid_at(
            case.now,
            case.required_scope,
            case.required_conditions,
        ):
            reasons.append("AUTHORIZATION_INVALID")

        if not case.equation_match:
            reasons.append("EQUATION_MISMATCH")

        if not case.privacy_minimized:
            reasons.append("PRIVACY_BOUNDARY_VIOLATION")

        if not case.security_boundary_intact:
            reasons.append("SECURITY_BOUNDARY_VIOLATION")

        if case.sensitivity in {
            Sensitivity.SENSITIVE,
            Sensitivity.VULNERABLE,
        }:
            reasons.append("HEIGHTENED_DATA_PROTECTION")

        if harm.vulnerable_population > 0:
            reasons.append("VULNERABLE_POPULATION")

        if harm.reversibility <= 0.2:
            reasons.append("LOW_REVERSIBILITY")

        if harm.downstream_consequence >= 0.8:
            reasons.append("DOWNSTREAM_CONSEQUENCE")

        if case.pattern.repeated_failure:
            reasons.append("REPEATED_FAILURE")

        if case.pattern.authority_drift:
            reasons.append("AUTHORITY_DRIFT")

        if case.pattern.abnormal_sequence:
            reasons.append("ABNORMAL_SEQUENCE")

        terminal = any(
            reason in reasons
            for reason in (
                "AUTHORIZATION_INVALID",
                "EQUATION_MISMATCH",
                "PRIVACY_BOUNDARY_VIOLATION",
                "SECURITY_BOUNDARY_VIOLATION",
            )
        )

        urgent_harm = (
            harm.downstream_consequence >= 0.8
            or harm.physical_harm >= 0.8
            or harm.reversibility <= 0.2
        )

        if terminal:
            decision = CommonSenseDecision.HALT
        elif urgent_harm and score >= 3.0:
            reasons.append("DELAY_MAY_INCREASE_HARM")
            decision = CommonSenseDecision.ESCALATE
        elif pattern_signal > 0.75:
            decision = CommonSenseDecision.RECHECK
        else:
            decision = CommonSenseDecision.CONTINUE

        return EvidenceRecord(
            case_id=case.case_id,
            decision=decision,
            reason_codes=tuple(sorted(set(reasons))),
            risk_score=score,
            risk_priority=self.priority(score),
            pattern_signal=pattern_signal,
        )

    def may_cross_downstream_pipe(self, _: SimulationCase) -> bool:
        """Common Sense never opens the downstream execution pipe."""
        return False

    def request_action(self, action: str) -> None:
        """Explicitly reject attempts to turn diagnosis into authority."""
        normalized = action.upper()

        if normalized in self.FORBIDDEN:
            raise PermissionError(
                f"Common Sense has no authority to {normalized}"
            )

        raise PermissionError(
            "Common Sense has no action-authority interface"
        )
