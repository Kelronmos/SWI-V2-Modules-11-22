"""Anti-stale evidence guard for the experimental law lane.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED

Fails if evidence/law/manifest.json is orphaned from HEAD, or if recorded
authority/registry blob SHAs disagree with the working tree.

source_tip may be an ancestor of HEAD when the only newer commits are
evidence-package updates (honest SWI evidence lag pattern).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "evidence" / "law" / "manifest.json"


def _git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _is_ancestor(anc: str, head: str) -> bool:
    r = subprocess.run(
        ["git", "merge-base", "--is-ancestor", anc, head],
        cwd=ROOT,
        capture_output=True,
    )
    return r.returncode == 0


def _blob_sha(rel: str) -> str:
    data = (ROOT / rel).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


@pytest.mark.skipif(not MANIFEST.is_file(), reason="no evidence manifest")
def test_evidence_source_tip_reachable_from_head():
    data = json.loads(MANIFEST.read_text())
    tip = data.get("source_tip") or data.get("tip")
    assert tip, "manifest missing source_tip"
    head = _git_head()
    assert tip == head or _is_ancestor(tip, head), (
        f"stale/orphaned evidence: source_tip {tip!r} is not HEAD {head!r} "
        f"and not an ancestor of HEAD"
    )


@pytest.mark.skipif(not MANIFEST.is_file(), reason="no evidence manifest")
def test_evidence_authority_registry_blobs_match_tree():
    data = json.loads(MANIFEST.read_text())
    auth = data.get("authority_py_blob_sha")
    reg = data.get("registry_py_blob_sha")
    if not auth or not reg:
        pytest.skip("manifest lacks blob fields (pre-formal evidence format)")
    assert auth == _blob_sha("experimental/law/authority.py")
    assert reg == _blob_sha("experimental/law/registry.py")
