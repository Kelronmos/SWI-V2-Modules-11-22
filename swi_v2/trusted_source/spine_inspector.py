"""SWI Trusted-Source Spine Inspector (read-only, fail-closed, structural only).

RECONSTRUCTED 2026-11-01. This is NOT the original 20,747-byte module, which was never
committed (the repo held only a 44-byte placeholder). It was rebuilt from
test/test_trusted_source_spine_inspector.py, test/fixtures/trusted_source/*,
docs/SWI_TRUSTED_SOURCE_BOUNDARY_PLACEHOLDER.md and evidence/trusted_source_boundary_placeholder.json.
Behaviour beyond what those specify is unverified. Replace with the original when recovered.

Spine: HEADER > SOURCE > PROVENANCE > VERSION > STATUS > SCOPE > JURISDICTION > EVIDENCE
       > BOUNDARY > CLAIM > DECISION.  Any stage that is not PASS is a SPINE BREAK -> HALT.
Structural GREEN is not authorization. AUTHORIZATION from this layer is always NO.
STANDARD != LAW . SOURCE != AUTHORIZATION . API != AUTHORIZATION . CI_GREEN != PRODUCTION_AUTHORIZATION
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
STAGES = ("HEADER", "SOURCE", "PROVENANCE", "VERSION", "STATUS", "SCOPE",
          "JURISDICTION", "EVIDENCE", "BOUNDARY", "CLAIM")
_FIELDS = {"HEADER": ["swi_header"], "SOURCE": ["source_id", "source_type", "publisher", "reference"],
           "PROVENANCE": ["provenance"], "VERSION": ["policy_version"], "STATUS": ["policy_status"],
           "SCOPE": ["policy_scope"], "JURISDICTION": ["jurisdiction"], "EVIDENCE": ["evidence"],
           "BOUNDARY": ["boundary"], "CLAIM": ["claim"]}
_UNKNOWN = {"unknown", "tbd", "n/a", "na", "?", "todo", "unspecified"}
_STATUSES = {"draft", "active", "superseded", "withdrawn", "expired"}


class SpineBreak(Exception):
    """Raised by InspectionResult.require_green() on a spine break."""


class FieldStatus(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    FAIL = "FAIL"
    CONFLICT = "CONFLICT"


_RANK = {FieldStatus.PASS: 0, FieldStatus.UNKNOWN: 1, FieldStatus.FAIL: 2, FieldStatus.CONFLICT: 3}


@dataclass
class Finding:
    stage: str
    status: FieldStatus
    detail: str


@dataclass
class InspectionResult:
    path: str = ""
    findings: List[Finding] = field(default_factory=list)
    spine_break: bool = False

    def add(self, stage: str, status: FieldStatus, detail: str = "") -> None:
        self.findings.append(Finding(stage=stage, status=status, detail=detail))
        if status != FieldStatus.PASS:
            self.spine_break = True

    def require_green(self) -> None:
        if self.spine_break:
            raise SpineBreak(f"spine break in {self.path or '<record>'}")

    @property
    def structural_green(self) -> bool:
        return not self.spine_break


def _norm(v) -> str:
    if v is None:
        return ""
    return str(v).strip()


def _is_unknown(v: str) -> bool:
    return not v or v.lower() in _UNKNOWN


def inspect_record(record: dict, path: str = "") -> InspectionResult:
    result = InspectionResult(path=path)
    if not isinstance(record, dict):
        result.add("HEADER", FieldStatus.FAIL, "record is not an object")
        return result
    for stage in STAGES:
        fields = _FIELDS.get(stage, [])
        worst = FieldStatus.PASS
        details = []
        for f in fields:
            val = _norm(record.get(f))
            if f not in record:
                worst = FieldStatus.FAIL if _RANK[FieldStatus.FAIL] > _RANK[worst] else worst
                details.append(f"missing {f}")
            elif _is_unknown(val):
                worst = FieldStatus.UNKNOWN if _RANK[FieldStatus.UNKNOWN] > _RANK[worst] else worst
                details.append(f"{f}=UNKNOWN")
            else:
                if stage == "STATUS" and val.lower() not in _STATUSES:
                    worst = FieldStatus.FAIL if _RANK[FieldStatus.FAIL] > _RANK[worst] else worst
                    details.append(f"invalid status {val}")
        result.add(stage, worst, "; ".join(details))
    # DECISION stage is informational only — never authorization
    result.add("DECISION", FieldStatus.PASS if not result.spine_break else FieldStatus.FAIL,
               "AUTHORIZATION=NO (structural inspection only)")
    return result


def inspect_paths(paths: Iterable[str]) -> List[InspectionResult]:
    results = []
    for p in paths:
        path = Path(p)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            r = InspectionResult(path=str(path))
            r.add("HEADER", FieldStatus.FAIL, f"load error: {e}")
            results.append(r)
            continue
        results.append(inspect_record(data, path=str(path)))
    return results


def format_report(results: List[InspectionResult]) -> str:
    lines = []
    for r in results:
        status = "SPINE_BREAK" if r.spine_break else "STRUCTURAL_GREEN"
        lines.append(f"{r.path or '<record>'}: {status}")
        for f in r.findings:
            lines.append(f"  [{f.stage}] {f.status.value}: {f.detail}")
        lines.append("  AUTHORIZATION=NO")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args:
        print("usage: spine_inspector <json-path> [...]", file=sys.stderr)
        return 2
    results = inspect_paths(args)
    print(format_report(results))
    return 1 if any(r.spine_break for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
