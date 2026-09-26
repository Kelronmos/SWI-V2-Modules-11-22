# Comparative Test Framework — SWI and The Shift

**Status:** DESIGN / METHODOLOGY  
**Seal:** NOT SEALED  
**Production:** N/A (evaluation method, not a runtime module)  
**Date:** 26 September 2026

**Purpose:** Allow serious challenge of either system without forcing SWI onto The Shift’s floor, or The Shift onto SWI’s floor.

**Strongest outcome is not** proving that one floor wins.  
**Strongest outcome is** locating where floors, definitions, rules, implementation, or evidence differ.

See also: `docs/SWI_REBUILD_IMPLEMENTATION_GUIDE.md` (floor definition).

---

## Floor Distinction

SWI and The Shift are treated as **distinct systems** because they originate from **different floors**.

This is **not** merely a distinction between different assumptions, terminology, tests, or implementations.

### SWI

SWI is built on the **inherited computational floor**.

Its workflow-control architecture is:

```text
ADMISSION
    ↓
AUTHORITY
    ↓
ENFORCEMENT
    ↓
EXECUTION
```

(Full chain includes token → registry → validation → evidence → verification → human authority → security → safety → authorization → action.)

SWI may be **hardened** through stronger gates, authority checks, replay, bypass detection, stale-condition handling, evidence controls, verification, and enforcement.

Those improvements remain improvements to **SWI on the inherited computational floor**.

### The Shift

The Shift is described by its proponents as built from a **corrected floor**, including:

```text
CLASSICAL MATHEMATICS
        ↓
GENESIS 2.0ut
        ↓
RB1
        ↓
AHMR
        ↓
URK
        ↓
ELEMENTS BASIN
        ↓
LAWFUL CONTINUANCE
```

SWI records that description as belonging to **the other system**.  
SWI does **not** automatically validate or invalidate those foundational claims merely by mentioning them.

The Shift remains a **distinct system and category** from SWI.

### Non-Conflation Rule

```text
TESTING SWI                    ≠  TESTING THE SHIFT
USING THE SHIFT'S TESTS        ≠  MOVING SWI TO THE SHIFT FLOOR
USING THE SHIFT'S TERMINOLOGY  ≠  MOVING SWI TO THE SHIFT FLOOR
HARDENING SWI                  ≠  CHANGING SWI'S FLOOR
```

A test developed from The Shift may be applied to SWI as an **external challenge** if the test is explicitly defined and its applicability is stated.  
Use as a test does **not** transfer the originating system’s foundation to SWI.

Likewise, SWI’s tests do not establish or validate The Shift.

### System Boundary

The repository must **not** describe SWI improvements as movement from the inherited computational floor to a corrected floor.

SWI remains SWI unless its foundation itself is explicitly changed and that change is separately defined, implemented, tested, evidenced, reproduced, and verified.

> **«Different floor = different system.»**

This distinction must be preserved throughout SWI documentation, testing, terminology, evidence records, and architectural descriptions.

```text
IMPLEMENTATION CHANGE ≠ FLOOR CHANGE
TEST CHANGE           ≠ FLOOR CHANGE
TERMINOLOGY CHANGE    ≠ FLOOR CHANGE
HARDENING             ≠ FLOOR CHANGE
TEST TRANSFER         ≠ FLOOR TRANSFER
```

---

## Master rule (examination)

> Neither system is examined by secretly placing it on the other system’s floor.

| Forbidden | Required |
|-----------|----------|
| Judging The Shift only by SWI transition gates | Stating each system’s **floor** first |
| Judging SWI only by Shift geometry/order | Scoring each against **its own** stated rules |
| Treating hardening as floor migration | Recording floor as fixed unless explicitly changed |
| Declaring victory from category error | Mapping differences without forced equivalence |

---

## Parallel test areas

Fill both columns from **that system’s own statements**. Empty = not defined by that system.

| Test area | SWI (inherited computational floor) | The Shift (its stated corrected floor) |
|-----------|-------------------------------------|----------------------------------------|
| **Floor** | Inherited computational floor | Classical math → Genesis 2.0ut → RB1 → AHMR → URK → Elements Basin → lawful continuance *(as stated by Shift)* |
| **Core question** | What conditions permit a transition? | What constitutes correct standing / order? *(Shift-native)* |
| **Admission** | Explicit gate | Define from Shift principles |
| **Authority** | Explicit human authority boundary | Define corresponding Shift concept |
| **Enforcement** | Closed transitions; REJECT/BLOCK/QUARANTINE/ALLOW | Define corresponding mechanism |
| **Evidence** | Provenance, replay, reproduction, verification | Define what counts as evidence |
| **Failure** | Primary + suppressed descendants | Define failure/consequence handling |
| **Scope** | Explicit workflow; policy-bounded | Define from foundational rules |
| **Bypass** | Adversarial testing (ATM) | Bypass under its own rules |
| **Consequence** | Action only after required gates | Claimed lawful continuation |
| **Reproduction** | Same controlled input → same defined result | Equivalent reproduction if defined |
| **Floor stability** | Hardening stays on same floor | State whether claims change floor |

Do not rewrite Shift “standing/order” as “transition gate,” or SWI “gate” as “geometry,” unless a **joint mapping** is agreed *after* both floors are stated.

---

## Three levels of examination

```text
LEVEL 1 — FOUNDATIONAL CLAIMS (including floor)
        Is the floor and premises clearly defined?

LEVEL 2 — INTERNAL CONSISTENCY
        Do the rules follow from that floor and premises?

LEVEL 3 — IMPLEMENTATION / TEST
        Does behaviour match those stated rules?
```

Cross-system comparison only after each track has Level 1–3 material on **its own floor**.

---

## SWI evaluation path (own floor)

```text
CLAIM → DEFINITION → IMPLEMENTATION → TEST → RESULT
  → EVIDENCE → REPLAY → REPRODUCTION → VERIFICATION
```

Hardening and ATM results improve or falsify **SWI on the inherited computational floor**. They do not relocate SWI to The Shift’s floor.

---

## The Shift evaluation path (own floor)

Cite Shift-native definitions. Fill the Shift column without requiring SWI terms. Mark `NOT STATED` where missing. Do not force SWI analogues.

This framework does not author The Shift’s doctrine.

---

## Difference map (not a scoreboard)

| Dimension | SWI | Shift | Same? | Difference type |
|-----------|-----|-------|-------|-----------------|
| Floor | Inherited computational | Corrected (as stated) | No | **Floor / category** |
| … | … | … | … | definition / rule / implementation / evidence |

A **floor** difference is a category difference. It is not automatically a refutation of either system’s internal work.

---

## Challenge protocol

1. Name target system (SWI or The Shift).  
2. State the **floor** under examination.  
3. State level (1, 2, or 3).  
4. Use native vocabulary.  
5. Show mismatch (unclear floor/premise / inconsistent rule / behaviour ≠ claim).  
6. Do not smuggle the other floor’s pass criteria.

Optional: “Under SWI’s floor, X; under Shift’s floor, Y; difference type = floor | definition | …”

---

## External tests

```text
TEST TRANSFER ≠ FLOOR TRANSFER
```

Record: origin, author, version, definition, applicability, result, evidence.

---

## Working template

```text
examination_id:
target_system: SWI | THE_SHIFT
floor_under_test:
level: 1 | 2 | 3
premises_cited:
claim_under_test:
vocabulary: native | mapped (mapping_table_ref if mapped)
result: CLEAR | GAP | CONTRADICTION | CLAIM_NE_BEHAVIOUR | NOT_STATED | FLOOR_UNCHANGED
other_floor_criteria_used: none | list
```

---

**Non-claims:** Does not prove either floor, implement The Shift, reseal SWI, or authorize production.
