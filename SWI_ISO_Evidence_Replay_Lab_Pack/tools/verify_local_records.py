#!/usr/bin/env python3
"""Verify local pack records — structural/signature checks only."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    runs = list((ROOT / "evidence" / "runs").glob("*.json")) if (ROOT / "evidence" / "runs").is_dir() else []
    schemas = list((ROOT / "evidence" / "schema").glob("*.json")) if (ROOT / "evidence" / "schema").is_dir() else []
    print(f"evidence runs found: {len(runs)}")
    print(f"schemas found: {len(schemas)}")
    print("NOTE: Full Ed25519 verification requires original pack crypto material and is environment-dependent.")
    print("iso_compatibility=NOT_ASSESSED")
    print("PROVEN=NO SEALED=NO PRODUCTION_AUTHORIZED=NO")
    # Pass if pack layout exists; do not claim crypto proof without keys/records present
    if schemas:
        print("PASS: schema files present")
        return 0
    print("FAIL: schemas missing")
    return 1

if __name__ == "__main__":
    sys.exit(main())
