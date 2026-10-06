"""SWI Execution Integrity — restored body via embedded base64 payloads.

Source lineage: 77ee326 / fix/new-information-boundary (ed600c0 MISSING on remote).
MATCH ≠ PERMIT ≠ EXECUTE. Status: RESEARCH · NOT SEALED · NOT PRODUCTION_AUTHORIZED.
"""
from __future__ import annotations

import base64
import sys
import types
from pathlib import Path

_DIR = Path(__file__).resolve().parent
_parts = []
for i in range(100):
    p = _DIR / f"_ei_payload_{i}.txt"
    if not p.is_file():
        break
    _parts.append(p.read_text())
if not _parts:
    raise ImportError("execution_integrity payload parts missing")
_src = base64.b64decode("".join(_parts)).decode("utf-8")
_mod = types.ModuleType("swi_v2._execution_integrity_body")
_mod.__file__ = str(_DIR / "execution_integrity_body.py")
sys.modules[_mod.__name__] = _mod
exec(compile(_src, _mod.__file__, "exec"), _mod.__dict__)

AdmittedRoute = _mod.AdmittedRoute
CheckResult = _mod.CheckResult
Decision = _mod.Decision
ExecutionIntegrityGate = _mod.ExecutionIntegrityGate
ExecutionRecord = _mod.ExecutionRecord
FailureReason = _mod.FailureReason
HumanAuthority = _mod.HumanAuthority
IncomingNode = _mod.IncomingNode
IntegrityEvidence = _mod.IntegrityEvidence
NewInformation = _mod.NewInformation
NodeState = _mod.NodeState
ValidatedAuthority = _mod.ValidatedAuthority
validate_human_authority = _mod.validate_human_authority
_ExecutionPermit = _mod._ExecutionPermit
for _n in dir(_mod):
    if not _n.startswith("__"):
        globals()[_n] = getattr(_mod, _n)
