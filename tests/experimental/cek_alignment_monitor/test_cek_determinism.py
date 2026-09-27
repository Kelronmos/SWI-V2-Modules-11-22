"""Same input → identical measurement results (100×)."""

from __future__ import annotations

from experimental.cek_alignment_monitor.monitor import AlignmentMonitor


def test_measure_100_identical(mon: AlignmentMonitor) -> None:
    v = [0.91, 0.83, 0.78, 0.88, 0.62, 0.74]
    results = [mon.measure(v, measurement_id=f"d-{i}") for i in range(100)]
    distances = [r.distance for r in results]
    classes = [r.classification.value for r in results]
    assert len(set(distances)) == 1
    assert len(set(classes)) == 1
    r = mon.replay(results[0])
    assert r.match is True
