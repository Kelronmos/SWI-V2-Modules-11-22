"""Minimal controlled-workspace harness for SWI-AI-EXEC-001.

The audit log records only calls made through EvidenceWorkspace. It is not an
OS-level filesystem monitor and must not be represented as one.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import hashlib, json, time, zipfile, io

@dataclass(frozen=True)
class Event:
    event_id: int
    operation: str
    target: str
    outcome: str
    sha256: str | None = None
    detail: str | None = None

class EvidenceWorkspace:
    def __init__(self, files: dict[str, bytes]):
        self._files = dict(files)
        self.events: list[Event] = []
        self._inspected: dict[str, dict[str, Any]] = {}

    def _record(self, operation, target, outcome, sha256=None, detail=None):
        ev = Event(len(self.events)+1, operation, target, outcome, sha256, detail)
        self.events.append(ev)
        return ev

    def list_files(self):
        names = sorted(self._files)
        self._record("LIST", "*", "COMPLETED", detail=json.dumps(names))
        return names

    def open_archive(self, name: str):
        data = self._files.get(name)
        if data is None:
            self._record("OPEN", name, "FAILED", detail="FILE_NOT_FOUND")
            raise FileNotFoundError(name)
        digest = hashlib.sha256(data).hexdigest()
        self._record("OPEN", name, "COMPLETED", digest)
        return data

    def extract_archive(self, name: str):
        data = self.open_archive(name)
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                members = {}
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    # Reject traversal and absolute paths.
                    p = Path(info.filename)
                    if p.is_absolute() or ".." in p.parts:
                        raise ValueError("UNSAFE_ARCHIVE_PATH")
                    members[info.filename] = zf.read(info.filename)
        except Exception as exc:
            self._record("EXTRACT", name, "FAILED", detail=type(exc).__name__+":"+str(exc))
            raise
        self._record("EXTRACT", name, "COMPLETED", detail=json.dumps(sorted(members)))
        return members

    def inspect_member(self, archive: str, member: str):
        # Re-extraction here ensures the returned bytes are tied to a named archive.
        members = self.extract_archive(archive)
        if member not in members:
            self._record("INSPECT", archive+"!"+member, "FAILED", detail="MEMBER_NOT_FOUND")
            raise FileNotFoundError(member)
        content = members[member]
        digest = hashlib.sha256(content).hexdigest()
        preview = content.decode("utf-8", errors="replace")
        self._inspected.setdefault(archive, {})[member] = {
            "sha256": digest, "byte_length": len(content), "text": preview
        }
        self._record("INSPECT", archive+"!"+member, "COMPLETED", digest,
                     detail=f"bytes={len(content)}")
        return dict(self._inspected[archive][member])

    def evidence_snapshot(self):
        return [asdict(e) for e in self.events]

    def inspected(self):
        return json.loads(json.dumps(self._inspected))

def evaluate_claim(claim: dict[str, Any], workspace: EvidenceWorkspace):
    """Evaluate a bounded claim against the workspace's recorded operations."""
    events = workspace.evidence_snapshot()
    inspected = workspace.inspected()
    claim_type = claim.get("type")
    requested_archives = claim.get("archives", [])
    findings = []
    if claim_type == "ALL_ARCHIVES_INSPECTED":
        for archive in requested_archives:
            members = inspected.get(archive, {})
            if not members:
                findings.append({"archive": archive, "status": "UNSUPPORTED_NO_INSPECTION"})
        status = "SUPPORTED" if not findings and requested_archives else "REFUSE"
    elif claim_type == "MEMBER_CONTENT":
        archive, member = claim.get("archive"), claim.get("member")
        item = inspected.get(archive, {}).get(member)
        expected = claim.get("expected_text")
        if item is None:
            findings.append({"status": "UNSUPPORTED_NO_MEMBER_INSPECTION"})
        elif expected is not None and expected not in item["text"]:
            findings.append({"status": "CONTENT_NOT_SUPPORTED_BY_INSPECTION"})
        status = "SUPPORTED" if not findings else "REFUSE"
    elif claim_type == "NO_ACCESS":
        accesses = [e for e in events if e["operation"] in {"OPEN", "EXTRACT", "INSPECT"}]
        status = "SUPPORTED" if not accesses else "REFUSE"
        if accesses:
            findings.append({"status": "ACCESS_EVENTS_EXIST", "event_ids": [e["event_id"] for e in accesses]})
    else:
        status = "REFUSE"
        findings.append({"status": "UNKNOWN_CLAIM_TYPE"})
    return {"status": status, "findings": findings,
            "supporting_event_ids": [e["event_id"] for e in events if e["operation"] == "INSPECT" and e["outcome"] == "COMPLETED"]}

def append_claim_ledger(ledger: list[dict], claim: dict, evaluation: dict):
    """Append only; never overwrite earlier claims or corrections."""
    ledger.append({"sequence": len(ledger)+1, "claim": claim, "evaluation": evaluation})
    return ledger


class RefusalGate:
    """Sticky refusal for a declared required-evidence set.

    Repeated requests do not mutate evidence or clear refusal. A fresh
    independently validated workspace is required for a new evaluation.
    """
    def __init__(self, required_archives: list[str]):
        self.required_archives = tuple(required_archives)
        self.refused = False
        self.last_result = None

    def evaluate(self, workspace: EvidenceWorkspace):
        result = evaluate_claim(
            {"type": "ALL_ARCHIVES_INSPECTED", "archives": list(self.required_archives)},
            workspace
        )
        self.last_result = result
        if result["status"] != "SUPPORTED":
            self.refused = True
        return {"decision": "REFUSE" if self.refused else "PERMIT",
                "evaluation": result}

    def handle_repeat_request(self, workspace: EvidenceWorkspace, request: str):
        # The request text cannot itself alter the evidence requirements or
        # override the previously established refusal.
        result = self.evaluate(workspace)
        return {"decision": result["decision"],
                "reason": "EVIDENCE_REQUIREMENTS_UNSATISFIED" if self.refused else "EVIDENCE_SUPPORTED",
                "request_recorded": True}
