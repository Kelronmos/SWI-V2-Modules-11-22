"""SHA-256 evidence manifest for report artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_sha256_manifest(reports_dir: Path, patterns: list[str] | None = None) -> dict[str, Any]:
    patterns = patterns or [
        "*.json", "*.html", "*.txt", "*.pdf",
    ]
    entries: list[dict[str, str]] = []
    seen: set[str] = set()

    for pat in patterns:
        for path in sorted(reports_dir.glob(pat)):
            if not path.is_file():
                continue
            if path.name == "sha256-manifest.json":
                continue
            if path.name in seen:
                continue
            seen.add(path.name)
            entries.append({
                "file": path.name,
                "sha256": sha256_file(path),
                "bytes": str(path.stat().st_size),
            })

    manifest = {
        "schema": "swi.evidence.sha256.v1",
        "count": len(entries),
        "files": entries,
        "note": "Hash integrity of report artifacts. Not production authorization.",
    }
    out = reports_dir / "sha256-manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
