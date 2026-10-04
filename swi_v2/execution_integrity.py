"""
SWI Execution Integrity / Node Quarantine — bounded component.

Status: IMPLEMENTED + TESTED (bounded component + boundary hardening).
Does NOT modify M11, Security Maze, B1, or CRTG.
Does NOT claim production readiness, process-wide OS isolation, or universal safety.
Supported API: check()/execute(); direct _demo_action without permit is blocked.

Claim under test:
  An arriving node remains quarantined until SWI verifies that its
  execution request is still bound to the admitted workflow, approved
  node, expected route, relevant policy, and last verified execution.
  On mismatch: HALT → RECORD → REVALIDATE/RETRY → ESCALATE.
  Retry does not grant authority. Execution counter proves non-execution.
  New information that affects the evidence boundary INVALIDATES prior
  decisions; without bound authority the result is UNKNOWN (no execution).
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from swi_v2.kernel.halt import HaltRecord, HaltedWorkflow
