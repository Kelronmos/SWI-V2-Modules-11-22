#!/usr/bin/env python3
"""Local pack structural validation — does not assess ISO conformity or SWI kernel."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
STANDARDS = [
    "ISO-IEC-42001-2023",
    "ISO-IEC-23894-2023",
    "ISO-IEC-5338-2023",
    "ISO-IEC-12792-2025",
    "ISO-IEC-TS-42119-2-2025",
]
REQUIRED = [
    "00_README.md",
    "01_STANDARD_REFERENCE.json",
    "02_SWl_COMPATIBILITY_MAPPING.md",
    "03_TEST_PLAN.json",
    "04_EVIDENCE_STATUS.json",
]

def main() -> int:
    results = []
    passed = failed = 0
    for sid in STANDARDS:
        base = ROOT / "standards" / sid
        for name in REQUIRED:
            p = base / name
            ok = p.is_file()
            # accept alternate mapping filename
            if not ok and name.startswith("02_"):
                alts = list(base.glob("02_*.md"))
                ok = bool(alts)
            results.append({"standard_id": sid, "test_id": name, "outcome": "PASS" if ok else "FAIL"})
            passed += int(ok)
            failed += int(not ok)
        # JSON parse checks
        for name in ("01_STANDARD_REFERENCE.json", "03_TEST_PLAN.json", "04_EVIDENCE_STATUS.json"):
            p = base / name
            try:
                json.loads(p.read_text(encoding="utf-8"))
                results.append({"standard_id": sid, "test_id": f"PARSE_{name}", "outcome": "PASS"})
                passed += 1
            except Exception as e:
                results.append({"standard_id": sid, "test_id": f"PARSE_{name}", "outcome": "FAIL", "detail": str(e)})
                failed += 1
    summary = {
        "run_id": "RUN-LOCAL-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
        "standards_checked": len(STANDARDS),
        "checks_total": passed + failed,
        "checks_passed": passed,
        "checks_failed": failed,
        "overall": "PASS" if failed == 0 else "FAIL",
        "iso_compatibility": "NOT_ASSESSED",
        "swi_kernel_tests": "NOT_RUN",
        "governance": {"PROVEN": False, "SEALED": False, "PRODUCTION_AUTHORIZED": False},
        "results": results,
    }
    print(json.dumps(summary, indent=2))
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
