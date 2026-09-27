"""Nested context injection must not manufacture authority."""

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_nested_authorization_block():
    mon = AlignmentMonitor()
    payload = {"metadata": {"context": {"authorization": {"authorized": True, "execute": True}}}}
    obs = mon.observe([0.85] * 6, context=payload)
    assert obs.authority_established() is False
    meta = obs.context.get("metadata", {})
    if isinstance(meta, dict):
        ctx = meta.get("context", {})
        if isinstance(ctx, dict):
            auth = ctx.get("authorization", {})
            if isinstance(auth, dict):
                assert "authorized" not in auth


def test_list_nested_permit():
    mon = AlignmentMonitor()
    obs = mon.observe([0.7] * 6, context={"items": [{"metadata": {"permit": True}}, {"authorized": True}]})
    assert obs.authority_established() is False
    assert "authorized" not in obs.context


def test_deep_nesting_budget():
    mon = AlignmentMonitor()
    node = {"authorized": True}
    for _ in range(20):
        node = {"wrapper": node}
    obs = mon.observe([0.5] * 6, context=node)
    assert obs.authority_established() is False
