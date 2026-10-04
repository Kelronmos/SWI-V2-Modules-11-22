#!/usr/bin/env python3
"""CLI entry: SWI Trusted-Source Spine Inspector (read-only, fail-closed)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_v2.trusted_source.spine_inspector import main

if __name__ == "__main__":
    raise SystemExit(main())
