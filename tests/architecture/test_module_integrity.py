"""T01 — Repository / module integrity.

Tests what actually exists on the architecture branch.
Does not invent unimplemented business modules.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_t01_01_required_packages_exist():
    """Kernel and experimental packages that are known to exist must be present."""
    required = [
        REPO_ROOT / "swi_v2",
        REPO_ROOT / "swi_v2" / "kernel",
        REPO_ROOT / "experimental",
        REPO_ROOT / "experimental" / "common_sense",
        REPO_ROOT / "experimental" / "response_boundary",
        REPO_ROOT / "tests" / "pre_r",
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, f"Missing required paths: {missing}"


def test_t01_02_kernel_imports_resolve():
    """Core kernel modules must import without error."""
    modules = [
        "swi_v2",
        "swi_v2.kernel",
        "swi_v2.kernel.authority",
        "swi_v2.kernel.admission",
        "swi_v2.kernel.canonical",
        "swi_v2.kernel.enforcement",
        "swi_v2.kernel.halt",
        "swi_v2.kernel.replay_guard",
    ]
    for name in modules:
        mod = importlib.import_module(name)
        assert mod is not None


def test_t01_02_common_sense_imports_resolve():
    """Experimental Common Sense package must import."""
    from experimental.common_sense import (
        AuthorizationContext,
        CommonSenseDecision,
        CommonSenseMonitor,
        EvidenceRecord,
        HarmProfile,
        PatternObservation,
        Sensitivity,
        SimulationCase,
    )

    assert CommonSenseMonitor is not None
    assert CommonSenseDecision.HALT.value == "HALT"


def test_t01_03_common_sense_public_interface():
    """Expected public surface of Common Sense must be present."""
    from experimental.common_sense.monitor import CommonSenseMonitor

    monitor = CommonSenseMonitor()
    assert hasattr(monitor, "inspect")
    assert hasattr(monitor, "risk_score")
    assert hasattr(monitor, "may_cross_downstream_pipe")
    assert hasattr(monitor, "request_action")
    assert hasattr(monitor, "FORBIDDEN")


def test_t01_05_experimental_not_under_swi_v2_production_path():
    """Experimental packages must not live inside the production swi_v2 tree."""
    experimental = REPO_ROOT / "experimental"
    production = REPO_ROOT / "swi_v2"

    assert experimental.exists()
    assert production.exists()

    # Common Sense must remain under experimental/
    cs = experimental / "common_sense"
    assert cs.exists()
    assert not (production / "common_sense").exists()

    # response_boundary also experimental
    assert (experimental / "response_boundary").exists()
    assert not (production / "response_boundary").exists()


def test_t01_06_common_sense_deterministic_initialization():
    """Two monitors with default weights must produce identical risk for same case."""
    from datetime import datetime, timedelta, timezone

    from experimental.common_sense.monitor import (
        AuthorizationContext,
        CommonSenseMonitor,
        HarmProfile,
        PatternObservation,
        Sensitivity,
        SimulationCase,
    )

    now = datetime(2026, 9, 23, 22, 0, 0, tzinfo=timezone.utc)
    auth = AuthorizationContext(
        principal="research-human",
        scope=frozenset({"diagnostic"}),
        purpose="research",
        started_at=now - timedelta(minutes=5),
        expires_at=now + timedelta(minutes=5),
        conditions=frozenset({"human_review"}),
    )
    case = SimulationCase(
        case_id="DET-001",
        sensitivity=Sensitivity.PUBLIC,
        required_scope=frozenset({"diagnostic"}),
        required_conditions=frozenset({"human_review"}),
        now=now,
        authorization=auth,
        harm=HarmProfile(),
        pattern=PatternObservation(name="baseline"),
        equation_match=True,
        privacy_minimized=True,
        security_boundary_intact=True,
    )

    m1 = CommonSenseMonitor()
    m2 = CommonSenseMonitor()
    assert m1.risk_score(case) == m2.risk_score(case)
