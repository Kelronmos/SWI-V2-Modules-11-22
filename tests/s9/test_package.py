"""S9 package builder — tip binding and refuse without commit."""
from __future__ import annotations

from pathlib import Path

import pytest

from swi_v2.s9.package import build_package, PackageRefused


def test_refuse_without_source_commit(tmp_path):
    with pytest.raises(PackageRefused):
        build_package(
            repo_root=Path("."),
            source_commit="",
            action={"action_id": "A", "constraints": [], "evidence": []},
            out_dir=tmp_path / "out",
        )


def test_package_builds_blocked_for_empty_action(tmp_path):
    root = Path(__file__).resolve().parents[2]
    out = build_package(
        repo_root=root,
        source_commit="aa62042888886f5252e2b80e7aec8dce49e4bab3",
        action={
            "action_id": "A-SYS",
            "constraints": ["c1"],
            "law": [],
            "governance": [],
            "security": [],
            "human": [],
            "evidence": [],
        },
        out_dir=tmp_path / "pkg",
    )
    assert out["s9_proven"] is False
    assert out["production_authorized"] is False
    assert out["system_result"] == "BLOCKED"
    assert Path(out["zip_path"]).exists()
