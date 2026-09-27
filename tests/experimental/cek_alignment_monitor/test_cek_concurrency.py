"""Concurrent measurements must not share mutable security state."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_parallel_measures_no_cross_contamination() -> None:
    mon = AlignmentMonitor()

    def work(i: int):
        m = mon.measure([0.5 + (i % 5) * 0.1] * 6, measurement_id=f"c-{i}")
        obs = mon.observe(
            [0.5 + (i % 5) * 0.1] * 6,
            context={"authorized": True, "idx": i},
        )
        assert m.is_authoritative() is False
        assert obs.authority_established() is False
        assert "authorized" not in obs.context
        return m.distance, obs.observation_id

    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(work, i) for i in range(32)]
        outs = [f.result() for f in as_completed(futs)]
    assert len(outs) == 32
    ids = [o[1] for o in outs]
    assert len(set(ids)) == 32
