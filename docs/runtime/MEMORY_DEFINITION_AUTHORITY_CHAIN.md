# Memory → Definition → Authority Chain

**Status:** DESIGN / DOCTRINE  
**Date:** 2026-09-24  
**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Classification:** Documentation only — does **not** implement Firefly, does **not** open execution, does **not** claim S9 sealed.

---

## Governing principle

A fast system can turn an unproven memory or definition into an apparently authoritative fact, then use that fact to cross an accountability gate.

Memory and definitions must therefore be treated as **evidence-bearing objects**, not merely text.

---

## Required progression

```text
MEMORY
  → DEFINITION
  → PROVENANCE
  → VALIDATION
  → VERIFICATION
  → REPRODUCTION
  → AUTHORITY
  → ACTION
```

Each transition is a gate. A bridge between two gates must never become permission to skip the next gate.

---

## Layer questions

| Layer | Question that must be answered |
|---|---|
| **Memory** | Where did this information come from? |
| **Definition** | What exactly does the term mean in this workflow? |
| **Provenance** | Can we identify its origin and transformation history? |
| **Validation** | Does it satisfy the defined structural/technical requirements? |
| **Verification** | Can an independent process establish that it is what it claims to be? |
| **Reproduction** | Can another authorized process reproduce the result from the recorded inputs/rules? |
| **Authority** | Is this particular evidence authorized to cross this particular gate? |
| **Action** | What action, if any, is permitted after the gate? |

---

## Forbidden collapses

```text
MEMORY          ≠  TRUTH
DEFINITION      ≠  PROOF
VALIDATION      ≠  VERIFICATION
VERIFICATION    ≠  AUTHORIZATION
REPLAYABILITY   ≠  AUTHORITY
KNOWN           ≠  DEFINED
DEFINED         ≠  VALIDATED
VALIDATED       ≠  VERIFIED
VERIFIED        ≠  REPRODUCIBLE
REPRODUCIBLE    ≠  AUTHORIZED
AUTHORIZED      ≠  ACTIONABLE
```

These distinctions extend the existing SWI invariant:

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

---

## Memory object (conceptual)

A memory object that may participate in any consequential path should carry at least:

```text
content
source
created_at
definition_version
provenance
validation_status
verification_status
reproduction_status
authority_scope
expiry / freshness
superseded_by
replay_reference
```

The system must be able to distinguish the status of the memory itself, not merely the content string.

---

## Critical risk in high-speed paths

In a slow human process a participant may notice ambiguity.

In a high-speed agentic path the system may perform:

```text
retrieve → interpret → decide → execute
```

in milliseconds.

That makes **definitions themselves a security boundary**.

Unsafe pattern:

```text
AMBIGUOUS MEMORY
      ↓
ASSUMED DEFINITION
      ↓
AUTOMATIC INTERPRETATION
      ↓
GATE PASSED
      ↓
ACTION
```

Required pattern:

```text
MEMORY
  ↓
DEFINITION CHECK
  ↓
PROVENANCE CHECK
  ↓
VALIDATION
  ↓
INDEPENDENT VERIFICATION
  ↓
REPRODUCTION / REPLAY
  ↓
AUTHORITY CHECK
  ↓
ACTION SCOPE
  ↓
ACTION
```

Failure at one stage must not be silently converted into success at the next stage.

---

## Relation to existing contracts

- Extends `EVIDENCE_FRESHNESS_CONTRACT.md` (TIP-BOUND ≠ HEAD-CURRENT).
- Compatible with `HUMAN_AUTHORITY.md` (H remains UNDER_CONSTRUCTION).
- Compatible with claim ledger classifications (`INHERIT` | `REGENERATE` | `NO_EVIDENCE`).
- Does **not** authorize Firefly implementation.
- Does **not** change global status: Execution = BLOCKED · S9 = NOT_PROVEN · Production = NOT_AUTHORIZED.

---

## Non-claims

- This document is **doctrine only**.
- No runtime object is claimed to implement this chain.
- No Firefly adapter is claimed to exist.
- No seal, Foundation PASS, or production authorization is claimed.
