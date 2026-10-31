"""Adapter that invokes existing SWI V2 kernel surfaces and records results.
Does NOT create a second authorization engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class KernelProbeResult:
    test_id: str
    outcome: str
    detail: str
    exception_type: Optional[str] = None

def probe_kernel() -> List[KernelProbeResult]:
    results: List[KernelProbeResult] = []
    try:
        from swi_v2.kernel import governing_permit, enforcement, replay_guard, canonical
    except Exception as e:
        return [KernelProbeResult("KERNEL_IMPORT", "FAIL", f"import failed: {e}", type(e).__name__)]

    try:
        ev = governing_permit.evaluate_governing_permit(conditions=[], evidence=None)
        decision = getattr(ev, "decision", None) or getattr(ev, "result", None) or str(ev)
        results.append(KernelProbeResult(
            "GOVERNING_PERMIT_EMPTY_CONDITIONS", "PASS",
            f"evaluate_governing_permit(conditions=[]) returned; decision={decision!r}",
        ))
    except Exception as e:
        results.append(KernelProbeResult(
            "GOVERNING_PERMIT_EMPTY_CONDITIONS", "FAIL", str(e), type(e).__name__
        ))

    try:
        try:
            enforcement.require_admitted({"not": "admitted"}, module="iso_lab")
            results.append(KernelProbeResult(
                "REQUIRE_ADMITTED_REJECTS_RAW", "FAIL",
                "require_admitted accepted raw dict — boundary regression",
            ))
        except Exception:
            results.append(KernelProbeResult(
                "REQUIRE_ADMITTED_REJECTS_RAW", "PASS",
                "require_admitted rejected non-AdmittedInput",
            ))
    except Exception as e:
        results.append(KernelProbeResult(
            "REQUIRE_ADMITTED_REJECTS_RAW", "FAIL", str(e), type(e).__name__
        ))

    try:
        replay_guard.ReplayGuard()
        results.append(KernelProbeResult(
            "REPLAY_GUARD_IN_PROCESS", "PASS",
            "ReplayGuard instantiated (in-memory scope; not distributed)",
        ))
    except Exception as e:
        results.append(KernelProbeResult(
            "REPLAY_GUARD_IN_PROCESS", "FAIL", str(e), type(e).__name__
        ))

    try:
        if hasattr(canonical, "canonical_hash"):
            h1 = canonical.canonical_hash({"a": 1, "b": 2})
            h2 = canonical.canonical_hash({"b": 2, "a": 1})
            ok = h1 == h2
            results.append(KernelProbeResult(
                "CANONICAL_HASH_DETERMINISM",
                "PASS" if ok else "FAIL", f"h1={h1} h2={h2}",
            ))
        else:
            results.append(KernelProbeResult(
                "CANONICAL_HASH_DETERMINISM", "NOT_RUN",
                "canonical.canonical_hash not found",
            ))
    except Exception as e:
        results.append(KernelProbeResult(
            "CANONICAL_HASH_DETERMINISM", "FAIL", str(e), type(e).__name__
        ))
    return results
