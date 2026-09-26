# Comparative Test Framework — SWI and The Shift

**Status:** DESIGN / METHODOLOGY  
**Seal:** NOT SEALED  
**Production:** N/A (evaluation method, not a runtime module)  
**Date:** 26 September 2026

**Purpose:** Allow serious challenge of either system without forcing SWI to become The Shift, or The Shift to become SWI.

**Strongest outcome is not** proving that one “floor” wins.  
**Strongest outcome is** locating exactly where assumptions, definitions, rules, implementation, or evidence differ.

---

## 1. Master rule

> **Neither system gets tested by secretly imposing the other system’s assumptions on it.**

| Forbidden | Required |
|-----------|----------|
| Judging The Shift by SWI’s transition gates alone | Stating each system’s own premises first |
| Judging SWI by The Shift’s geometry/order alone | Scoring each against its own stated rules |
| Redefining one system’s terms mid-test | Recording assumptions explicitly before comparison |
| Declaring victory from category error | Mapping differences without forced equivalence |

Cross-system comparison is allowed **only after** each has been examined under Levels 1–3 on its own terms.

---

## 2. Parallel test areas

Fill **both** columns from **that system’s own statements**. Empty cells mean “not yet defined by that system” — not failure under the other system’s vocabulary.

| Test area | SWI (own premises) | The Shift (own premises) |
|-----------|--------------------|---------------------------|
| **Foundation** | Inherited computational workflow; evidence-first governance | Corrected geometry / natural-order premise *(define from Shift sources)* |
| **Core question** | What conditions permit a transition? | What constitutes correct standing / order? *(define)* |
| **Admission** | Explicit gate (ADMIT / REJECT / …) | Define admission (or equivalent) from its own principles |
| **Authority** | Explicit human authority boundary | Define corresponding authority concept |
| **Enforcement** | Closed transitions; REJECT / BLOCK / QUARANTINE / ALLOW | Define corresponding enforcement mechanism |
| **Evidence** | Provenance, replay, reproduction, verification | Define what counts as evidence |
| **Failure** | Primary failure + suppressed descendants; deterministic diagnostics | Define failure / consequence handling |
| **Scope** | Explicit workflow scope; policy-bounded | Define scope from foundational rules |
| **Bypass** | Adversarial testing (ATM) | Test whether bypass is possible under its own rules |
| **Consequence** | Action only after required gates | Test claimed lawful continuation / consequence |
| **Reproduction** | Same controlled input → same defined result | Determine whether equivalent reproduction exists |
| **Assumptions** | Explicitly recorded | Explicitly recorded |

**Instruction:** Do not rewrite The Shift’s “standing/order” as “transition gate,” or SWI’s “gate” as “geometry,” unless a **joint mapping table** is agreed *after* Level 1–2 for both.

---

## 3. Three levels of examination

```text
LEVEL 1 — FOUNDATIONAL CLAIMS
        Are the premises clearly defined?

LEVEL 2 — INTERNAL CONSISTENCY
        Do the rules follow from those premises?

LEVEL 3 — IMPLEMENTATION / TEST
        Does the implemented system behave according to those stated rules?
```

### Level 1 — Foundational claims

For **each** system, independently:

1. List atomic premises (no borrowed language from the other system unless cited as external).
2. State what is **in scope** and **out of scope**.
3. State what the system claims to decide vs what it claims **not** to decide.
4. Record open ambiguities as `UNDEFINED` — not as pass/fail against the other system.

**Pass criterion (Level 1):** A competent third party can restate the premises without inventing missing terms.

### Level 2 — Internal consistency

For **each** system, independently:

1. Derive claimed rules from Level 1 premises.
2. Check for contradictions, silent exceptions, and undefined transitions/operations.
3. Check whether authority, evidence, and consequence roles are distinct or conflated **inside that system**.
4. Note any place where implementation would require an assumption not stated in the premises.

**Pass criterion (Level 2):** Rules are coherent with stated premises; gaps are labeled, not papered over.

### Level 3 — Implementation / test

For **each** system that has an implementation or operational claim:

1. Map stated rules → observable behaviours or procedures.
2. Run tests **defined in that system’s vocabulary**.
3. Capture evidence the system itself treats as valid (for SWI: result, hash/provenance, replay, reproduction).
4. Report mismatch as `CLAIM ≠ BEHAVIOUR` under **its** rules — not as “fails the other floor.”

**Pass criterion (Level 3):** Behaviour matches stated rules under agreed tests; failures are diagnostic under that system.

---

## 4. SWI evaluation path (own track)

When examining **SWI only**:

```text
CLAIM
  ↓
DEFINITION
  ↓
IMPLEMENTATION
  ↓
TEST
  ↓
RESULT
  ↓
EVIDENCE
  ↓
REPLAY
  ↓
REPRODUCTION
  ↓
VERIFICATION
```

SWI-specific questions (not Shift questions):

- Are transition conditions explicit?
- Is human authority non-substitutable by technical signals?
- Do closed transitions reject undefined paths?
- Is primary failure deterministic under input permutation?
- Does offline/local resilience change connectivity without changing policy authority?
- Is the system policy-bounded (`CAPABILITY ≠ POLICY`)?

SWI references: manifesto, ATM-001, transition engine design, school deployment (policy-bounded), deterministic diagnostics doctrine.

---

## 5. The Shift evaluation path (own track)

When examining **The Shift only**:

1. Cite **Shift-native** definitions of geometry, natural order, standing, lawfulness, consequence.
2. Fill the right-hand column of §2 without requiring SWI terms.
3. Apply Levels 1–3 using **those** definitions.
4. If a concept has no Shift-native definition, mark `NOT STATED` and stop forcing a SWI analogue.

*(This framework does not author The Shift’s doctrine; it requires the challenger or Shift materials to supply Level 1 content.)*

---

## 6. After both tracks: difference map (not a scoreboard)

Only after Levels 1–3 for each (to the extent each has material):

| Dimension | SWI statement | Shift statement | Same? | Difference type |
|-----------|---------------|-----------------|-------|-----------------|
| What is being decided | … | … | Y/N/Partial | Category / definition / rule / test / evidence |
| Who/what holds authority | … | … | … | … |
| What blocks continuation | … | … | … | … |
| What counts as proof | … | … | … | … |
| What reproduction means | … | … | … | … |

**Difference types:**

- **Category** — systems answer different questions  
- **Definition** — same word, different meaning  
- **Rule** — same domain, different constraints  
- **Implementation** — same rule, different behaviour  
- **Evidence** — different standards of what settles a claim  

No automatic ranking. A category difference is not a refutation.

---

## 7. Challenge protocol

A serious challenge from either side should:

1. **Name the target system** (SWI or The Shift).
2. **State the level** (1, 2, or 3).
3. **Use that system’s vocabulary** for the claim under test.
4. **Show the mismatch** (premise unclear / rule inconsistent / behaviour ≠ claim).
5. **Not smuggle** the other system’s pass criteria as hidden premises.

Optional joint challenge: “Under SWI rules, X; under Shift rules, Y; the difference is type Z.”

---

## 8. What this framework refuses

- Declaring a universal “correct floor” without Level 1 clarity on both sides  
- Translating away disagreement by renaming terms  
- Treating missing Shift implementation as SWI’s win (or vice versa) without stating the claim level  
- Using school resilience, ZTA, or CI green as proof of metaphysical order (or the reverse)  

---

## 9. Relationship to SWI ATM

SWI-ATM-001 remains **SWI-internal** adversarial coverage (bypass, forgery, reordering, etc.).

This comparative framework is **cross-system methodology**. ATM results feed **SWI Level 3** only. They do not automatically falsify The Shift unless a joint mapping has been agreed.

---

## 10. Working template (copy per examination)

```text
examination_id:
target_system: SWI | THE_SHIFT
level: 1 | 2 | 3
premises_cited:
claim_under_test:
vocabulary: native | mapped (if mapped, mapping_table_ref:)
procedure:
result: CLEAR | GAP | CONTRADICTION | CLAIM_NE_BEHAVIOUR | NOT_STATED
evidence_refs:
other_system_assumptions_used: none | list (must be none for pure track)
difference_notes:
```

---

**Non-claims:** This document does not implement The Shift, adjudicate which foundation is true, reseal SWI, or authorize production. It defines how to test without category error.
