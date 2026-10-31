"""Append-only serial ledger with hash chain. Historical duplicates preserved as marked."""
from __future__ import annotations
import hashlib, json, threading
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from .status_model import LedgerMark

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

@dataclass
class LedgerEntry:
    serial: str
    record_id: str
    record_hash: str
    previous_hash: Optional[str]
    mark: str
    run_id: str
    record_type: str
    standard_id: str = ""
    note: str = ""

class LedgerError(Exception):
    pass

class SerialLedger:
    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def read_entries(self) -> List[Dict[str, Any]]:
        text = self.path.read_text(encoding="utf-8").strip()
        if not text:
            return []
        return [json.loads(line) for line in text.splitlines() if line.strip()]

    def last_hash(self) -> Optional[str]:
        entries = self.read_entries()
        if not entries:
            return None
        return entries[-1].get("record_hash")

    def append(self, entry: LedgerEntry) -> None:
        with self._lock:
            entries = self.read_entries()
            active_serials = {
                e["serial"] for e in entries
                if e.get("mark") not in (
                    LedgerMark.HISTORICAL_DUPLICATE.value,
                    LedgerMark.NOT_VALID_FOR_NEW_ADMISSION.value,
                )
            }
            if entry.mark == LedgerMark.ACTIVE.value and entry.serial in active_serials:
                raise LedgerError(f"duplicate active serial: {entry.serial}")
            expected_prev = entries[-1]["record_hash"] if entries else None
            if entry.previous_hash != expected_prev:
                raise LedgerError(
                    f"broken hash link: expected previous_hash={expected_prev!r}, got {entry.previous_hash!r}"
                )
            line = json.dumps(asdict(entry), sort_keys=True, separators=(",", ":"))
            with self.path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")

    def verify_chain(self) -> Dict[str, Any]:
        entries = self.read_entries()
        errors: List[str] = []
        seen_active: set = set()
        prev = None
        for i, e in enumerate(entries):
            if e.get("previous_hash") != prev:
                errors.append(f"entry[{i}] broken previous_hash link")
            prev = e.get("record_hash")
            mark = e.get("mark", LedgerMark.ACTIVE.value)
            serial = e.get("serial")
            if mark == LedgerMark.ACTIVE.value:
                if serial in seen_active:
                    errors.append(f"entry[{i}] duplicate active serial {serial}")
                seen_active.add(serial)
        return {
            "ok": len(errors) == 0,
            "entries": len(entries),
            "errors": errors,
            "outcome": "PASS" if not errors else "FAIL",
        }
