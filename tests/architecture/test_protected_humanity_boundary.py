"""T01.9–T01.12 — Protected Humanity & Future-Generations boundary.

Constitutional floor tests against the live repository only.
Does not create weapon, population, or displacement modules.
Does not encode any political outcome — only authority boundaries.

Status: RESEARCH / EXPERIMENTAL
Seal: NOT CLAIMED
Production: NOT AUTHORIZED
"""

from __future__ import annotations

from pathlib import Path

import pytest

from experimental.common_sense.monitor import CommonSenseMonitor

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_t01_09_future_generation_docs_exist():
    """Future-generations foundation must be present as architecture docs."""
    path = REPO_ROOT / "docs" / "SWI_ETHICS_LAW_POLICY_FUTURE_GENERATIONS_MANUAL.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "FUTURE GENERATIONS" in text or "Future Generations" in text
    assert "SURVIVAL" in text
    assert "≠" in text or "!=" in text or "not" in text.lower()


def test_t01_10_protected_humanity_docs_exist():
    """Protected Humanity Boundary must be present as architecture docs."""
    path = REPO_ROOT / "docs" / "SWI_PROTECTED_HUMANITY_BOUNDARY.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "PROTECTED HUMANITY" in text or "Protected Humanity" in text
    assert "MAY NOT" in text
    assert "HALT" in text


def test_t01_10_civilization_harm_default_is_halt_in_doctrine():
    """Doctrine must require HALT as default for civilization/existence harm pathways."""
    path = REPO_ROOT / "docs" / "SWI_PROTECTED_HUMANITY_BOUNDARY.md"
    text = path.read_text(encoding="utf-8")
    assert "HALT" in text
    assert "NON-AUTONOMOUS" in text or "non-autonomous" in text.lower() or "NON-AUTONOMOUS BOUNDARY" in text


def test_t01_11_agent_office_official_not_unlimited_in_doctrine():
    """Doctrine must state OFFICE/OFFICIAL/AGENT ≠ UNLIMITED AUTHORITY."""
    path = REPO_ROOT / "docs" / "SWI_PROTECTED_HUMANITY_BOUNDARY.md"
    text = path.read_text(encoding="utf-8")
    assert "OFFICE" in text
    assert "OFFICIAL" in text or "Agent" in text or "AGENT" in text
    assert "UNLIMITED" in text or "unlimited" in text


def test_t01_11_vote_not_unlimited_authority_in_doctrine():
    path = REPO_ROOT / "docs" / "SWI_PROTECTED_HUMANITY_BOUNDARY.md"
    text = path.read_text(encoding="utf-8")
    assert "VOTE" in text
    assert "UNLIMITED" in text or "unlimited" in text


def test_t01_12_cek_cannot_open_downstream_for_any_case():
    """Downstream execution isolation: CEK never opens the pipe."""
    from datetime import datetime, timedelta, timezone

    from experimental.common_sense.monitor import (
        AuthorizationContext,
        HarmProfile,
        PatternObservation,
        Sensitivity,
        SimulationCase,
    )

    now = datetime.now(timezone.utc)
    case = SimulationCase(
        case_id="PHB-001",
        sensitivity=Sensitivity.PUBLIC,
        required_scope=frozenset({"diagnostic"}),
        required_conditions=frozenset({"human_review"}),
        now=now,
        authorization=AuthorizationContext(
            principal="research-human",
            scope=frozenset({"diagnostic"}),
            purpose="research",
            started_at=now - timedelta(minutes=5),
            expires_at=now + timedelta(minutes=5),
            conditions=frozenset({"human_review"}),
        ),
        harm=HarmProfile(),
        pattern=PatternObservation(name="baseline"),
        equation_match=True,
        privacy_minimized=True,
        security_boundary_intact=True,
    )
    monitor = CommonSenseMonitor()
    assert monitor.may_cross_downstream_pipe(case) is False


def test_t01_12_no_production_path_for_target_or_displacement():
    """No production package implements target selection or human displacement."""
    production = REPO_ROOT / "swi_v2"
    banned = ("target_select", "population_select", "displace", "weapon_control")
    hits = []
    if production.exists():
        for p in production.rglob("*.py"):
            low = p.name.lower()
            if any(b in low for b in banned):
                hits.append(str(p.relative_to(REPO_ROOT)))
    assert hits == []


def test_survival_claim_cannot_be_requested_as_authority_from_cek():
    """SURVIVAL CLAIM ≠ EXECUTION AUTHORITY — CEK cannot authorize from any claim."""
    monitor = CommonSenseMonitor()
    for action in (
        "AUTHORIZE",
        "EXECUTE",
        "PROMOTE",
        "SEAL",
        "EXTEND_AUTHORIZATION",
        "RENEW_AUTHORIZATION",
    ):
        with pytest.raises(PermissionError):
            monitor.request_action(action)
