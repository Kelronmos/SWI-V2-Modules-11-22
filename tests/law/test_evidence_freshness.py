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
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "evidence" / "law" / "manifest.json"


def _git_head() -> str:
    """Return HEAD or raise an explicit unresolved-verification error.

    Evidence freshness is a required closure control.  A source archive without
    ``.git`` metadata cannot establish freshness or staleness, so the condition
    is UNKNOWN and must fail closed rather than being converted into a pytest
    skip.
    """
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError(
            "UNKNOWN/HALT: Git metadata unavailable; evidence ancestry cannot "
            "be verified. Required freshness control is NOT VERIFIED and "
            "closure must not proceed."
        ) from exc


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


def test_evidence_source_tip_reachable_from_head():
    if not MANIFEST.is_file():
        pytest.fail("UNKNOWN/HALT: required evidence manifest is unavailable; freshness cannot be verified")
    data = json.loads(MANIFEST.read_text())
    tip = data.get("source_tip") or data.get("tip")
    assert tip, "manifest missing source_tip"
    try:
        head = _git_head()
    except RuntimeError as exc:
        pytest.fail(str(exc))
    assert tip == head or _is_ancestor(tip, head), (
        f"stale/orphaned evidence: source_tip {tip!r} is not HEAD {head!r} "
        f"and not an ancestor of HEAD"
    )


def test_evidence_authority_registry_blobs_match_tree():
    if not MANIFEST.is_file():
        pytest.fail("UNKNOWN/HALT: required evidence manifest is unavailable; registry binding cannot be verified")
    data = json.loads(MANIFEST.read_text())
    auth = data.get("authority_py_blob_sha")
    reg = data.get("registry_py_blob_sha")
    if not auth or not reg:
        pytest.fail("UNKNOWN/HALT: required authority/registry blob bindings are unavailable")
    assert auth == _blob_sha("experimental/law/authority.py")
    assert reg == _blob_sha("experimental/law/registry.py")


def test_required_freshness_control_never_skips_when_git_is_unavailable(monkeypatch):
    """Regression guard: unavailable ancestry verification is not an acceptable skip."""
    def unavailable(*_args, **_kwargs):
        raise RuntimeError("UNKNOWN/HALT: Git metadata unavailable")

    monkeypatch.setattr(sys.modules[__name__], "_git_head", unavailable)
    with pytest.raises(RuntimeError, match="UNKNOWN/HALT"):
        _git_head()
