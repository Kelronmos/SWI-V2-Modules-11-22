# SWI Web Extend Rule

**Status:** DESIGN / NORMATIVE ADDITION RULE  
**Seal:** NOT SEALED  
**Date:** 26 September 2026

---

## Problem this corrects

When a new requirement appears (e.g. SAMH institutional graph, school resilience, educational frontier), the wrong move is to **rewrite** the existing SWI flow to absorb it.

The correct move is to **preserve** the existing flow and **add** a governed string/strand to the web.

---

## Rule

> When the existing SWI flow is valid, do not modify the flow to accommodate a new requirement. Add the requirement as another governed string of the web.

```text
EXISTING SWI FLOW
        │  unchanged
        ▼
   EXISTING WEB
        │
        ├── existing string
        ├── existing string
        └── NEW STRING → NEW NODES → NEW RELATIONS
```

```text
ADD ≠ ALTER
EXTEND ≠ REWRITE
OBSERVE ≠ AUTHORIZE
CONNECT ≠ PROMOTE
```

Do not unnecessarily alter: existing modules, transitions, gates, evidence paths, seals, or authority boundaries. Extend the web **around** them.

---

## New string lifecycle

```text
PRESERVE → EXTEND → TEST → VERIFY → ADMIT → AUTHORIZE → CONNECT
```

A new string must still pass existing SWI controls before it becomes part of the authoritative system.

```text
NEW STRING
   ↓ TEST → VERIFY → PROVENANCE → AUTHORITY
   ↓ [only then] permitted relationship to the existing web
```

---

## Terminology note

“String” and “web” here mean **governed path / composition of paths**, not programming strings or the World Wide Web unless a separate module defines those terms. Do not elevate informal metaphors to law without this definition.

---

## Floor

This rule operates on the **inherited computational floor**. Adding a string is not a floor change. See `docs/SWI_REBUILD_IMPLEMENTATION_GUIDE.md`.

**Non-claims:** Does not reseal modules or authorize production.
