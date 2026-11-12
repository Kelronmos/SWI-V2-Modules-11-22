"""Recovery suite helpers for SWI Android local prototype.

STATUS: PROTOTYPE
PROVEN = NO · SEALED = NO · PRODUCTION_AUTHORIZED = NO

Rules:
- A missing object that still has an SWI key retains identity and recovery record.
- Disappearance is never proof that the object never existed.
- Quarantine before destructive recovery actions.
- Report unrecoverable state honestly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import json
import time


@dataclass
class ObjectIdentity:
    swi_key: str
    expected_hash: Optional[str] = None
    last_seen_path: Optional[str] = None
    last_seen_at: Optional[float] = None
    notes: str = ""


@dataclass
class RecoveryRecord:
    swi_key: str
    action: str
    outcome: str  # FOUND | MISSING | CORRUPT | QUARANTINED | RESTORED | UNRECOVERABLE
    detail: str
    observed_at: float = field(default_factory=time.time)
    evidence_present: bool = True
    proven: bool = False
    sealed: bool = False
    production_authorized: bool = False


class RecoverySuite:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir = self.base_dir / "quarantine"
        self.quarantine_dir.mkdir(exist_ok=True)
        self.identities: Dict[str, ObjectIdentity] = {}
        self.records: List[RecoveryRecord] = []

    def register_identity(self, identity: ObjectIdentity) -> None:
        self.identities[identity.swi_key] = identity

    def _hash_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    def verify_path(self, swi_key: str, path: Path) -> RecoveryRecord:
        identity = self.identities.get(swi_key)
        if identity is None:
            rec = RecoveryRecord(
                swi_key=swi_key,
                action="verify",
                outcome="UNRECOVERABLE",
                detail="no identity registered for key",
                evidence_present=False,
            )
            self.records.append(rec)
            return rec

        if not path.exists():
            rec = RecoveryRecord(
                swi_key=swi_key,
                action="verify",
                outcome="MISSING",
                detail=f"path does not exist: {path}; identity retained",
            )
            self.records.append(rec)
            return rec

        actual = self._hash_file(path)
        if identity.expected_hash and actual != identity.expected_hash:
            # Quarantine the suspect file
            qpath = self.quarantine_dir / f"{swi_key}_{int(time.time())}"
            try:
                path.replace(qpath)
                detail = f"hash mismatch; quarantined to {qpath}"
            except OSError as exc:
                detail = f"hash mismatch; quarantine failed: {exc}"
            rec = RecoveryRecord(
                swi_key=swi_key,
                action="verify",
                outcome="CORRUPT",
                detail=detail,
            )
            self.records.append(rec)
            return rec

        # Update last-seen
        identity.last_seen_path = str(path)
        identity.last_seen_at = time.time()
        rec = RecoveryRecord(
            swi_key=swi_key,
            action="verify",
            outcome="FOUND",
            detail=f"hash ok: {actual[:16]}…",
        )
        self.records.append(rec)
        return rec

    def report_missing(self, swi_key: str) -> RecoveryRecord:
        """Record that an object is missing while preserving identity."""
        if swi_key not in self.identities:
            self.identities[swi_key] = ObjectIdentity(swi_key=swi_key, notes="registered on missing")
        rec = RecoveryRecord(
            swi_key=swi_key,
            action="report_missing",
            outcome="MISSING",
            detail="identity retained; disappearance is not proof of non-existence",
        )
        self.records.append(rec)
        return rec

    def write_log(self) -> Path:
        path = self.base_dir / f"recovery_log_{int(time.time())}.json"
        payload = {
            "identities": {
                k: {
                    "swi_key": v.swi_key,
                    "expected_hash": v.expected_hash,
                    "last_seen_path": v.last_seen_path,
                    "last_seen_at": v.last_seen_at,
                    "notes": v.notes,
                }
                for k, v in self.identities.items()
            },
            "records": [
                {
                    "swi_key": r.swi_key,
                    "action": r.action,
                    "outcome": r.outcome,
                    "detail": r.detail,
                    "observed_at": r.observed_at,
                    "evidence_present": r.evidence_present,
                    "proven": False,
                    "sealed": False,
                    "production_authorized": False,
                }
                for r in self.records
            ],
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return path
