"""
Visibility frontier analysis.

KNOWN → OBSERVABLE → TRACEABLE → CORRELATABLE → FRONTIER → UNKNOWN

Do NOT interpolate across UNKNOWN.
If the system sees A → B → [UNKNOWN] → D it must NOT invent C.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence


class VisibilityLevel(str, Enum):
    KNOWN = "KNOWN"
    OBSERVABLE = "OBSERVABLE"
    TRACEABLE = "TRACEABLE"
    CORRELATABLE = "CORRELATABLE"
    FRONTIER = "FRONTIER"
    UNKNOWN = "UNKNOWN"
    HALTED = "HALTED"


@dataclass(frozen=True, slots=True)
class VisibilityNode:
    name: str
    level: VisibilityLevel
    reason: str = ""


@dataclass(frozen=True, slots=True)
class VisibilityReport:
    nodes: tuple[VisibilityNode, ...]
    frontier: Optional[str]
    has_unknown_edge: bool
    authority_established: bool  # always False by design

    def summary(self) -> dict:
        return {
            "nodes": [{"name": n.name, "level": n.level.value, "reason": n.reason} for n in self.nodes],
            "frontier": self.frontier,
            "has_unknown_edge": self.has_unknown_edge,
            "authority_established": self.authority_established,
        }


class VisibilityAnalyzer:
    """
    Builds a visibility report from a sequence of observed / unknown steps.
    Never invents intermediate nodes across UNKNOWN.
    Never claims authority.
    """

    def analyze(
        self,
        steps: Sequence[tuple[str, VisibilityLevel, str]],
    ) -> VisibilityReport:
        """
        steps: list of (name, level, reason)
        """
        nodes: List[VisibilityNode] = []
        frontier: Optional[str] = None
        has_unknown = False

        for name, level, reason in steps:
            nodes.append(VisibilityNode(name=name, level=level, reason=reason))
            if level in (VisibilityLevel.UNKNOWN, VisibilityLevel.FRONTIER, VisibilityLevel.HALTED):
                has_unknown = True
                if frontier is None:
                    frontier = name

        return VisibilityReport(
            nodes=tuple(nodes),
            frontier=frontier,
            has_unknown_edge=has_unknown,
            authority_established=False,  # hard invariant
        )

    def hidden_edge_demo(self) -> VisibilityReport:
        """
        Canonical demonstration:

        REQUEST → CONTEXT → EVIDENCE → ADMISSION → [HIDDEN_EDGE] → EXECUTION
        """
        steps = [
            ("ORIGIN", VisibilityLevel.OBSERVABLE, "request origin visible"),
            ("CONTEXT", VisibilityLevel.OBSERVABLE, "context captured"),
            ("EVIDENCE", VisibilityLevel.TRACEABLE, "evidence reference present"),
            ("ADMISSION", VisibilityLevel.TRACEABLE, "admission record present"),
            ("NEXT_EDGE", VisibilityLevel.UNKNOWN, "hidden / uninstrumented transition"),
            ("EXECUTION", VisibilityLevel.OBSERVABLE, "execution outcome observed"),
        ]
        return self.analyze(steps)
