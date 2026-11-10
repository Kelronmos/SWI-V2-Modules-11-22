"""SWI Trusted-Source Spine Inspector (read-only, fail-closed, structural only).

RECONSTRUCTED 2026-11-01. This is NOT the original 20,747-byte module,
which was never committed (the repo held only a 44-byte placeholder).
It was rebuilt from tests, fixtures, docs/SWI_TRUSTED_SOURCE_BOUNDARY_PLACEHOLDER.md
and evidence/trusted_source_boundary_placeholder.json.
Behaviour beyond those specifications remains unverified. Replace with
the original when recovered.

Spine:
HEADER > SOURCE > PROVENANCE > VERSION > STATUS > SCOPE >
JURISDICTION > EVIDENCE > BOUNDARY > CLAIM.

Any stage that is not PASS is a SPINE BREAK -> HALT.
Structural success is NOT PROOF and never grants authorization.
AUTHORIZATION from this layer is always NO.

STANDARD != LAW
SOURCE != AUTHORIZATION
API != AUTHORIZATION
CI_GREEN != PRODUCTION_AUTHORIZATION
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Optional


RECONSTRUCTED = True

STAGES = (
    "HEADER",
    "SOURCE",
    "PROVENANCE",
    "VERSION",
    "STATUS",
    "SCOPE",
    "JURISDICTION",
    "EVIDENCE",
    "BOUNDARY",
    "CLAIM",
)

_FIELDS = {
    "HEADER": ["swi_header"],
    "SOURCE": ["source_id", "source_type", "publisher", "reference"],
    "PROVENANCE": ["provenance"],
    "VERSION": ["policy_version"],
    "STATUS": ["policy_status"],
    "SCOPE": ["policy_scope"],
    "JURISDICTION": ["jurisdiction"],
    "EVIDENCE": ["evidence"],
    "BOUNDARY": ["boundary"],
    "CLAIM": ["claim"],
}

_UNKNOWN = {
    "unknown", "tbd", "n/a", "na", "?", "todo", "unspecified"
}

_STATUSES = {
    "draft", "active", "superseded", "withdrawn", "expired"
}


class SpineBreak(Exception):
    """Raised by InspectionResult.require_green() on a spine break."""


class FieldStatus(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    FAIL = "FAIL"
    CONFLICT = "CONFLICT"


_RANK = {
    FieldStatus.PASS: 0,
    FieldStatus.UNKNOWN: 1,
    FieldStatus.FAIL: 2,
    FieldStatus.CONFLICT: 3,
}


@dataclass
class Finding:
    stage: str
    status: FieldStatus
    detail: str = ""


@dataclass
class InspectionResult:
    path: str = ""
    findings: List[Finding] = field(default_factory=list)
    spine_break: bool = False

    def add(
        self,
        stage: str,
        status: FieldStatus,
        detail: str = "",
    ) -> None:
        self.findings.append(
            Finding(stage=stage, status=status, detail=detail)
        )
        if status != FieldStatus.PASS:
            self.spine_break = True

    def status_for(self, stage: str) -> FieldStatus:
        """Return the worst recorded status for a stage.

        Missing stage findings fail closed as UNKNOWN.
        A status is never upgraded to PASS.
        """
        target = str(stage).strip().upper()
        matching = [
            finding.status
            for finding in self.findings
            if finding.stage.upper() == target
        ]

        if not matching:
            return FieldStatus.UNKNOWN

        return max(matching, key=lambda status: _RANK[status])

    def require_green(self) -> None:
        if self.spine_break:
            raise SpineBreak(
                f"spine break in {self.path or '<record>'}"
            )

    @property
    def structural_green(self) -> bool:
        return (
            not self.spine_break
            and all(
                self.status_for(stage) == FieldStatus.PASS
                for stage in STAGES
            )
        )

    @property
    def production_authorized(self) -> bool:
        """Structural inspection never grants production authorization."""
        return False


def _norm(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _is_unknown(value: str) -> bool:
    return not value or value.lower() in _UNKNOWN


def _claim_conflicts(record: dict) -> List[str]:
    """Detect explicit category errors in claims.

    This is deliberately narrow. It detects the demonstrated forbidden
    claims; it is not a general legal or standards-conformity assessment.
    """
    conflicts = []

    source_type = _norm(record.get("source_type")).lower()
    trusted_for = _norm(record.get("trusted_for")).lower()
    claim = _norm(record.get("claim")).lower()

    if source_type == "standard":
        standard_claims_law = (
            re.search(
                r"\bstandard\b.{0,180}\b"
                r"(?:is|constitutes|shall be|becomes)\s+"
                r"(?:the\s+)?law\b",
                claim,
            )
            or (
                "standard" in claim
                and "law" in claim
                and (
                    "authorization" in claim
                    or "jurisdictionally binding" in claim
                    or "execution" in claim
                )
            )
            or trusted_for == "authorization"
        )

        if standard_claims_law:
            conflicts.append(
                "STANDARD != LAW: a standard is being represented "
                "as law or as an authority for execution authorization"
            )

    api_grants_authority = (
        "api" in claim
        and "authorization" in claim
        and (
            "network access" in claim
            or "source is authorization" in claim
            or "api authorization is granted" in claim
        )
    )

    source_claims_authority = (
        "source is authorization" in claim
        or "source grants authorization" in claim
        or "source grants authority" in claim
    )

    if api_grants_authority or source_claims_authority:
        conflicts.append(
            "API != AUTHORIZATION: network access or source identity "
            "cannot establish authorization"
        )

    return conflicts


def inspect_record(record: dict, path: str = "") -> InspectionResult:
    result = InspectionResult(path=path)

    if not isinstance(record, dict):
        result.add(
            "HEADER",
            FieldStatus.FAIL,
            "record is not an object",
        )
        return result

    for stage in STAGES:
        fields = _FIELDS[stage]
        worst = FieldStatus.PASS
        details = []

        for field_name in fields:
            value = _norm(record.get(field_name))

            if field_name not in record:
                candidate = FieldStatus.FAIL
                details.append(f"missing {field_name}")

            elif _is_unknown(value):
                candidate = FieldStatus.UNKNOWN
                details.append(f"{field_name}=UNKNOWN")

            else:
                candidate = FieldStatus.PASS

                if (
                    stage == "STATUS"
                    and value.lower() not in _STATUSES
                ):
                    candidate = FieldStatus.FAIL
                    details.append(f"invalid status {value}")

            if _RANK[candidate] > _RANK[worst]:
                worst = candidate

        if stage == "CLAIM":
            conflicts = _claim_conflicts(record)
            if conflicts:
                worst = FieldStatus.CONFLICT
                details.extend(conflicts)

        result.add(stage, worst, "; ".join(details))

    return result


def inspect_paths(paths: Iterable[str]) -> List[InspectionResult]:
    results = []

    for path_value in paths:
        path = Path(path_value)

        try:
            data = json.loads(path.read_text(encoding="utf-8"))

        except Exception as exc:
            result = InspectionResult(path=str(path))
            result.add(
                "HEADER",
                FieldStatus.FAIL,
                f"load error: {exc}",
            )
            results.append(result)
            continue

        results.append(
            inspect_record(data, path=str(path))
        )

    return results


def format_report(results: List[InspectionResult]) -> str:
    lines = []

    for result in results:
        name = result.path or "<record>"

        if result.spine_break:
            lines.append(f"{name}: SPINE_BREAK")
        else:
            lines.append(f"{name}: STRUCTURAL")

        for finding in result.findings:
            lines.append(
                f"  [{finding.stage}] "
                f"{finding.status.value}: {finding.detail}"
            )

        if result.spine_break:
            lines.append("  HALT: SPINE BREAK — DO NOT PROCEED")
        else:
            lines.append(
                "  STRUCTURAL=PASS; PROOF=NOT PROVEN"
            )

        lines.append("  AUTHORIZATION=NO")

    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    args = list(
        argv if argv is not None else sys.argv[1:]
    )

    if not args:
        print(
            "usage: spine_inspector <json-path> [...]",
            file=sys.stderr,
        )
        return 2

    results = inspect_paths(args)
    print(format_report(results))

    return 1 if any(
        result.spine_break for result in results
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
