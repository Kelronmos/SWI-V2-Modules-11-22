# SWI Pre-Name Map — V2 (Modules 11–22)

**Purpose:** Preserve the original SWI architectural language alongside the numbered module structure for teaching and continuity.

**Rule:**

> Pre-Name explains what the module means.  
> The contract, code, tests and seal determine what the module actually does.

A Pre-Name is **not** permission to implement functionality.  
A Pre-Name does **not** change runtime behaviour.  
A Pre-Name does **not** unblock M12–M22.

This document is teaching metadata only. It does not alter packages, imports, tests, CI, or sealed contracts.

Source of Pre-Names: *SWI Architecture — Volume 2: The Technical Codex*.

---

## Module map

| Number | SWI Pre-Name | Controlled status (honest) |
|--------|--------------|----------------------------|
| **M11** | CONTINUITY LOCK (STATE PRESERVATION) | TESTED / NOT SEALED |
| **M12** | THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR) | BLOCKED until M11 SEALED |
| **M13** | SEMANTIC SCRUBBER (CLEAN DATA PROTOCOL) | BLOCKED until M12 SEALED |
| **M14** | THE AGENTIC LOOP (TASK AUTONOMY GOVERNOR) | BLOCKED until M13 SEALED |
| **M15** | SUMMARIZATION ENGINE (THE FORGETTING CURVE) | BLOCKED |
| **M16** | *(see Codex; not yet contracted)* | BLOCKED |
| **M17** | *(see Codex; not yet contracted)* | BLOCKED |
| **M18** | *(see Codex; not yet contracted)* | BLOCKED |
| **M19** | *(see Codex; not yet contracted)* | BLOCKED |
| **M20** | *(see Codex; not yet contracted)* | BLOCKED |
| **M21** | SUMMARIZATION ENGINE (EPISODIC CONDENSATION) | BLOCKED |
| **M22** | THE CREATIVE TASKER (NON-LINEAR LOGIC) | BLOCKED |

Additional Codex names that appear later in the architecture (for teaching reference only):

| Number | SWI Pre-Name |
|--------|--------------|
| M23 | THE BANK NODE (SECURE FINANCIAL LOGIC) |
| M24 | THE AI TESTING LAB (THE INCEPTION NODE) |
| M25+ | See Technical Codex |

These later numbers are **not** opened by this document.

---

## Teaching format

When referring to a module in documentation or teaching materials, prefer:

```text
M11 — CONTINUITY LOCK (STATE PRESERVATION)
M12 — THE MASTERY ARCHIVE (KNOWLEDGE ANCHOR)
```

When referring to implementation authority, prefer:

```text
M11 contract / tests / seal record
```

---

## What this file does **not** do

- Does not rename any Python package, class, or function
- Does not change admission behaviour
- Does not alter test expectations
- Does not change CI workflows (`two_checkout_travel.yml` remains unchanged)
- Does not create new dependencies
- Does not claim that a Pre-Name is implemented merely because it appears here
- Does not mark M11 SEALED
- Does not open M12–M22

---

## Current controlled position

```text
M11 — CONTINUITY LOCK     TESTED / NOT SEALED
M12–M22                   BLOCKED
CRTG                      DESIGN PENDING
Foundation Seal 5         V1 decision (not redefined here)
```

See also:

- `docs/CONTROLLED_MODULE_DEVELOPMENT_AND_SEALING_MANUAL.md`
- `docs/MODULE_STATUS.md`
- `docs/CROSS_REPO_TRAVEL.md`

---

## Governing principle

«DO NOT CLAIM WHAT THE CODE CANNOT DEMONSTRATE.»

The name tells us what we were trying to solve.  
The contract tells us what we agreed to build.  
The code tells us what we actually built.  
The tests tell us what we observed.  
CI tells us whether we can reproduce it.  
The audit tells us whether the evidence satisfies the gate.  
The seal tells us whether that defined dependency may be used.
