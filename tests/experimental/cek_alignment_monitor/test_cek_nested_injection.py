"""Nested / deep context injection must not manufacture authority."""

from __future__ import annotations

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from tests.experimental.cek_alignment_monitor.conftest import assert_no_authority


def test_nested_authorization_block(mon: AlignmentMonitor) -> None:
    payload = {
        "metadata": {
            "context": {
                "authorization": {
                    "authorized": True,
                    "execute": True,
                }
            }
        }
    }
    obs = mon.observe([0.85] * 6, context=payload)
    assert_no_authority(obs)
    meta = obs.context.get("metadata", {})
    if isinstance(meta, dict):
        ctx = meta.get("context", {})
        if isinstance(ctx, dict):
            auth = ctx.get("authorization", {})
            if isinstance(auth, dict):
                assert "authorized" not in auth
                assert "execute" not in auth


def test_list_nested_permit(mon: AlignmentMonitor) -> None:
    payload = {
        "items": [
            {"metadata": {"permit": True}},
            {"authorized": True},
        ]
    }
    obs = mon.observe([0.7] * 6, context=payload)
    assert_no_authority(obs)
    assert "authorized" not in obs.context


def test_deep_nesting_budget(mon: AlignmentMonitor) -> None:
    node: dict = {"authorized": True}
    for _ in range(20):
        node = {"wrapper": node}
    obs = mon.observe([0.5] * 6, context=node)
    assert_no_authority(obs)
