"""Advisory invariant checks."""
from __future__ import annotations
from .urgency import Urgency, urgency_may_bypass_privacy, urgency_may_mint_authority
from .delivery import DeliveryRecord, DeliveryState, delivery_authorizes


def assert_advisory_invariants() -> None:
    for u in Urgency:
        assert urgency_may_bypass_privacy(u) is False
        assert urgency_may_mint_authority(u) is False
    rec = DeliveryRecord(
        notice_id="n1",
        recipient_role="TEACHER",
        state=DeliveryState.ACKNOWLEDGED,
        channel="email",
    )
    assert delivery_authorizes(rec) is False
    assert rec.authorized is False
