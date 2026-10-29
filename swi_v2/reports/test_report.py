"""Mandatory test-report / evidence layer for SWI verification runs.

HASH != AUTHORITY != TRUTH
OBSERVATION ≠ CLAIM ≠ PROOF ≠ AUTHORIZATION
Time-stable canonical bytes = structural outcomes without wall-clock fields.
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TestResultRecord:
    test_id: str
    test_name: str
    test_class: Optional[str] = None
    module: Optional[str] = None
    workflow_id: Optional[str] = None
    route_id: Optional[str] = None
    node_id: Optional[str] = None
    input_id: Optional[str] = None
    policy_id: Optional[str] = None
    admission_id: Optional[str] = None
    expected_decision: Optional[str] = None
    actual_decision: Optional[str] = None
    expected_execution_allowed: Optional[bool] = None
    actual_execution_allowed: Optional[bool] = None
    expected_execution_occurred: Optional[bool] = None
    actual_execution_occurred: Optional[bool] = None
    expected_reason_code: Optional[str] = None
    actual_reason_code: Optional[str] = None
    execution_counter: Optional[int] = None
    halted: Optional[bool] = None
    retry_attempted: Optional[bool] = None
    revalidated: Optional[bool] = None
    escalated: Optional[bool] = None
    evidence_hash: Optional[str] = None
    status: str = "NOT_RUN"
    timestamp: float = field(default_factory=time.time)
    commit_sha: Optional[str] = None
    branch: Optional[str] = None
    detail: Optional[str] = None
    gate: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ObservationRecord:
    """Recorded information — not interpretation, admission, or authority.

    OBSERVATION ≠ CLAIM ≠ PROOF ≠ AUTHORIZATION
    """

    observation_id: str
    observation_type: str
    description: str
    source: Optional[str] = None
    timestamp: Optional[float] = None
    evidence_ref: Optional[str] = None
    observed_status: Optional[str] = None
    workflow_id: Optional[str] = None
    stage_id: Optional[str] = None
    test_id: Optional[str] = None
    incomplete: bool = False
    uncertain: bool = False
    unavailable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClaimRecord:
    """Interpreted assertion that must reference supporting observations."""

    claim_id: str
    claim_text: str
    category: str = "general"
    supporting_observation_ids: List[str] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    verification_status: str = "UNVERIFIED"
    limitations: List[str] = field(default_factory=list)
    counterevidence: List[str] = field(default_factory=list)
    unproven: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _git(cmd: List[str], cwd: Optional[Path] = None) -> str:
    try:
        return subprocess.check_output(["git"] + cmd, cwd=cwd, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""


class TestReportBuilder:
    def __init__(self, report_type: str = "execution_integrity", repository: str = "Kelronmos/SWI-V2-Modules-11-22", root: Optional[Path] = None):
        self.report_type = report_type
        self.repository = repository
        self.root = root or Path.cwd()
        self.commit_sha = _git(["rev-parse", "HEAD"], self.root) or None
        self.branch = _git(["branch", "--show-current"], self.root) or None
        self.test_command: Optional[str] = None
        self.tests: List[TestResultRecord] = []
        self.observations: List[ObservationRecord] = []
        self.claims: List[ClaimRecord] = []
        self.halt_results: List[Dict[str, Any]] = []
        self.execution_results: List[Dict[str, Any]] = []
        self.bypass_results: List[Dict[str, Any]] = []
        self.limitations: List[str] = []
        self.not_proven: List[str] = []
        self.summary = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0}
        self.full_suite_status = "NOT_RUN"
        self.ci_status = "NOT_RUN"

    def set_command(self, cmd: str) -> None:
        self.test_command = cmd

    def add_test(self, rec: TestResultRecord) -> None:
        if self.commit_sha and not rec.commit_sha:
            rec.commit_sha = self.commit_sha
        if self.branch and not rec.branch:
            rec.branch = self.branch
        self.tests.append(rec)
        self.summary["total"] += 1
        key = {"PASS": "passed", "FAIL": "failed", "ERROR": "errors", "SKIPPED": "skipped"}.get(rec.status)
        if key:
            self.summary[key] += 1

    def add_limitation(self, text: str) -> None:
        self.limitations.append(text)

    def add_not_proven(self, text: str) -> None:
        self.not_proven.append(text)

    def add_observation(self, obs: ObservationRecord) -> None:
        self.observations.append(obs)

    def observation_ids(self) -> set:
        return {o.observation_id for o in self.observations}

    def add_claim(self, claim: ClaimRecord) -> ClaimRecord:
        known = self.observation_ids()
        missing = [oid for oid in claim.supporting_observation_ids if oid not in known]
        if missing:
            claim.limitations = list(claim.limitations) + [
                f"missing_observations:{','.join(sorted(missing))}"
            ]
            if claim.verification_status == "VERIFIED":
                claim.verification_status = "REJECTED"
                claim.unproven = list(claim.unproven) + [
                    "cannot_verify_without_supporting_observations"
                ]
            elif claim.verification_status not in ("REJECTED",):
                claim.verification_status = "UNRESOLVED"
        if claim.verification_status == "VERIFIED" and not claim.supporting_observation_ids:
            claim.verification_status = "REJECTED"
            claim.unproven = list(claim.unproven) + ["verified_claim_requires_observations"]
        if claim.category in ("authority", "authorization", "production_authorization"):
            if claim.verification_status == "VERIFIED" and not claim.evidence_refs:
                claim.verification_status = "REJECTED"
                claim.unproven = list(claim.unproven) + [
                    "authority_claims_require_independent_evidence_refs"
                ]
            claim.limitations = list(claim.limitations) + [
                "OBSERVATION≠AUTHORITY; claim category cannot manufacture permit"
            ]
        self.claims.append(claim)
        return claim

    def promote_claim(
        self,
        claim_id: str,
        new_status: str,
        *,
        required_observation_ids: Optional[List[str]] = None,
    ) -> ClaimRecord:
        claim = next((c for c in self.claims if c.claim_id == claim_id), None)
        if claim is None:
            raise KeyError(f"unknown_claim:{claim_id}")
        if new_status == "VERIFIED":
            req = list(required_observation_ids or claim.supporting_observation_ids)
            known = self.observation_ids()
            if not req or any(oid not in known for oid in req):
                claim.verification_status = "REJECTED"
                claim.unproven = list(claim.unproven) + [
                    "promotion_requires_present_observations"
                ]
                return claim
            if claim.category in ("authority", "authorization", "production_authorization"):
                claim.verification_status = "REJECTED"
                claim.unproven = list(claim.unproven) + [
                    "cannot_promote_authority_claim_via_report_builder"
                ]
                return claim
            if claim.category == "universal_proof":
                claim.verification_status = "REJECTED"
                claim.unproven = list(claim.unproven) + [
                    "passing_test_is_not_universal_proof"
                ]
                return claim
        claim.verification_status = new_status
        return claim

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_type": self.report_type,
            "repository": self.repository,
            "commit_sha": self.commit_sha,
            "branch": self.branch,
            "test_command": self.test_command,
            "environment": {"python": platform.python_version(), "platform": platform.platform()},
            "generated_at": time.time(),
            "test_summary": dict(self.summary),
            "full_suite_status": self.full_suite_status,
            "ci_status": self.ci_status,
            "tests": [t.to_dict() for t in self.tests],
            "observations": [o.to_dict() for o in self.observations],
            "claims": [c.to_dict() for c in self.claims],
            "halt_results": self.halt_results,
            "execution_results": self.execution_results,
            "bypass_results": self.bypass_results,
            "limitations": self.limitations,
            "not_proven": self.not_proven,
            "governance": {
                "proven": "NO",
                "sealed": "NO",
                "authorized": "NO",
                "production_authorized": "NO",
            },
        }

    def content_for_hash(self) -> Dict[str, Any]:
        data = self.to_dict()
        data.pop("generated_at", None)
        for t in data.get("tests", []):
            if isinstance(t, dict):
                t.pop("timestamp", None)
                t.pop("evidence_hash", None)
        stable_halts = []
        for h in data.get("halt_results", []):
            if not isinstance(h, dict):
                continue
            stable_halts.append({
                k: h.get(k)
                for k in (
                    "module", "reason_code", "decision", "execution_allowed",
                    "execution_occurred", "workflow_id", "node_id", "route_id",
                )
                if k in h
            })
        data["halt_results"] = stable_halts
        return data

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.content_for_hash(), sort_keys=True, separators=(",", ":"), default=str
        ).encode("utf-8")

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


def write_reports(builder: TestReportBuilder, out_dir: Path) -> Dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    sha = builder.commit_sha or "unknown"
    data = builder.to_dict()
    report_hash = builder.sha256()
    data["report_hash"] = report_hash
    data["hash_note"] = (
        "SHA-256 of time-stable canonical JSON (excludes generated_at, test timestamps, "
        "volatile evidence_hash; excludes report_hash field itself). "
        "HASH != AUTHORITY != TRUTH"
    )
    json_path = out_dir / f"{sha}.json"
    latest_json = out_dir / "latest.json"
    md_path = out_dir / f"{sha}.md"
    latest_md = out_dir / "latest.md"
    hash_path = out_dir / f"{sha}.sha256"
    payload = json.dumps(data, indent=2, sort_keys=True, default=str).encode("utf-8")
    json_path.write_bytes(payload)
    latest_json.write_bytes(payload)
    hash_path.write_text(report_hash + "\n")
    lines = [
        "# SWI TEST REPORT",
        "",
        f"Commit: `{sha}`",
        f"Hash: `{report_hash}`",
        f"Passed: {builder.summary['passed']}/{builder.summary['total']}",
        "",
    ]
    for t in builder.tests:
        lines.append(
            f"- {t.test_name}: {t.status} decision={t.actual_decision} exec={t.actual_execution_occurred}"
        )
    lines.append("")
    lines.append("HASH != AUTHORITY != TRUTH")
    lines.append("OBSERVATION ≠ CLAIM ≠ PROOF ≠ AUTHORIZATION")
    lines.append("PRODUCTION_AUTHORIZED = NO")
    md = "\n".join(lines)
    md_path.write_text(md)
    latest_md.write_text(md)
    return {
        "json": json_path,
        "md": md_path,
        "sha256": hash_path,
        "latest_json": latest_json,
        "latest_md": latest_md,
    }
