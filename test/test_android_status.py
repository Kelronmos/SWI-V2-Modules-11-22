"""Unit tests for SWI Android local runtime status and recovery.

These tests verify prototype behaviour only.
They do not prove production readiness or seal any component.
"""
from __future__ import annotations

import time
from pathlib import Path

import pytest

from swi_v2.android.status import (
    ServiceState,
    StatusRecord,
    mark_stale_if_old,
    missing_evidence,
)
from swi_v2.android.recovery import ObjectIdentity, RecoverySuite
from swi_v2.android.runtime import RuntimeSupervisor, ServiceSpec


def test_missing_evidence_is_unknown_not_green():
    rec = missing_evidence("kernel")
    assert rec.state is ServiceState.UNKNOWN
    assert rec.evidence_present is False
    assert rec.is_ok() is False
    assert rec.proven is False
    assert rec.production_authorized is False


def test_running_without_evidence_is_not_ok():
    rec = StatusRecord(
        component="svc",
        state=ServiceState.RUNNING,
        observed_at=time.time(),
        evidence_present=False,
    )
    assert rec.is_ok() is False


def test_stale_conversion_only_for_running():
    old = StatusRecord(
        component="svc",
        state=ServiceState.RUNNING,
        observed_at=time.time() - 1000,
        evidence_present=True,
    )
    stale = mark_stale_if_old(old, max_age_seconds=300)
    assert stale.state is ServiceState.STALE

    failed = StatusRecord(
        component="svc",
        state=ServiceState.FAILED,
        observed_at=time.time() - 1000,
        evidence_present=True,
    )
    still_failed = mark_stale_if_old(failed, max_age_seconds=300)
    assert still_failed.state is ServiceState.FAILED


def test_recovery_retains_identity_on_missing(tmp_path: Path):
    suite = RecoverySuite(tmp_path)
    suite.register_identity(
        ObjectIdentity(swi_key="obj-1", expected_hash="abc", last_seen_path="/old")
    )
    rec = suite.report_missing("obj-1")
    assert rec.outcome == "MISSING"
    assert "obj-1" in suite.identities
    assert suite.identities["obj-1"].swi_key == "obj-1"


def test_recovery_detects_hash_mismatch(tmp_path: Path):
    suite = RecoverySuite(tmp_path)
    f = tmp_path / "payload.bin"
    f.write_bytes(b"hello")
    suite.register_identity(
        ObjectIdentity(swi_key="obj-2", expected_hash="deadbeef")
    )
    rec = suite.verify_path("obj-2", f)
    assert rec.outcome == "CORRUPT"


def test_supervisor_identity_and_checkpoint(tmp_path: Path):
    sup = RuntimeSupervisor(tmp_path)
    sup.register(ServiceSpec(name="diag"))
    path = sup.write_checkpoint("boot", {"note": "start"})
    assert path.exists()
    ident = sup.identity()
    assert ident["proven"] is False
    assert ident["production_authorized"] is False
    assert "diag" in ident["services"]
