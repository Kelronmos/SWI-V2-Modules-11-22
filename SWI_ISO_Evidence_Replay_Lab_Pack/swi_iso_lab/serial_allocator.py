"""Globally unique, monotonic serial allocation. Append-only. No reuse."""
from __future__ import annotations
import json, os, threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Set

class SerialError(Exception):
    pass

@dataclass
class AllocationResult:
    serial: str
    sequence: int
    standard_id: str
    utc_date: str

class SerialAllocator:
    """Central sequence allocator. Format: SWI-ISO-<STANDARD-ID>-<YYYYMMDD>-<SEQ6>"""
    def __init__(self, state_path: Path):
        self.state_path = state_path
        self._lock = threading.Lock()
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_path.exists():
            self._write({"next_sequence": 1, "allocated": [], "standard_last": {}})

    def _read(self) -> Dict[str, Any]:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def _write(self, data: Dict[str, Any]) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, self.state_path)

    def allocated_set(self) -> Set[str]:
        with self._lock:
            return set(self._read().get("allocated", []))

    def allocate(self, standard_id: str) -> AllocationResult:
        with self._lock:
            data = self._read()
            allocated = set(data.get("allocated", []))
            seq = int(data.get("next_sequence", 1))
            utc_date = datetime.now(timezone.utc).strftime("%Y%m%d")
            sid = standard_id.replace("/", "-").replace(" ", "")
            serial = f"SWI-ISO-{sid}-{utc_date}-{seq:06d}"
            if serial in allocated:
                raise SerialError(f"duplicate serial would be allocated: {serial}")
            allocated.add(serial)
            data["allocated"] = sorted(allocated)
            data["next_sequence"] = seq + 1
            data.setdefault("standard_last", {})[standard_id] = serial
            self._write(data)
            return AllocationResult(serial=serial, sequence=seq, standard_id=standard_id, utc_date=utc_date)
