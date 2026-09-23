"""Workflow-state registry is closed vocabulary and machine-readable."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REG = REPO / "docs" / "workflow_state_registry.json"


def test_registry_exists_and_closed_labels():
    data = json.loads(REG.read_text(encoding="utf-8"))
    allowed = set(data["allowed_labels"])
    assert "PIPE_SEALED" in allowed
    assert "NOT_PROVEN" in allowed
    assert "NOT_AUTHORIZED" in allowed
    for item in data["items"]:
        assert item["label"] in allowed, item


def test_pipe_sealed_never_implies_production_in_registry_note():
    text = REG.read_text(encoding="utf-8")
    assert "PIPE_SEALED" in text
    assert "PRODUCTION" in text.upper() or "production" in text.lower()
    data = json.loads(text)
    prod = next(i for i in data["items"] if i["id"] == "Production")
    assert prod["label"] == "NOT_AUTHORIZED"
