# SWI Structural Demonstration Boundary

**Status:** DESIGN REQUIREMENT  
**Seal:** NONE  
**Production:** NOT AUTHORIZED  
**Implementation in this commit:** NONE (documentation only)

---

## Constitutional rule

```text
NO STRUCTURE → NO OPERATION
```

Design requirement ≠ implemented enforcement ≠ tested invariant ≠ sealed component.

Until negative-path, mutation, and bypass tests exist and pass for this boundary, treat it as **DESIGNED / NOT YET PROVEN**.

---

## Required exposure for every demonstrated decision

Every demonstrated decision MUST expose:

1. Input  
2. Classification  
3. Known facts  
4. Unknowns  
5. Evidence  
6. Assumptions  
7. Governing constraints  
8. Authority state  
9. Authorization state  
10. Decision state  
11. Side-effect state  
12. Explanation  
13. Limitation  
14. Reproduction method  
15. Independent verification  
16. Interpretation boundary  

---

## Public-interpretation boundary (non-negotiable)

```text
BEHAVIOR              ≠ CONSCIOUSNESS
CONSTRAINT FOLLOWING  ≠ MORAL AGENCY
EXPLANATION           ≠ INNER EXPERIENCE
SELF-CHECK            ≠ SELF-AWARENESS
SAFETY REFUSAL        ≠ ETHICAL PERSONHOOD
```

Observed rule-following behaviour must not be marketed or documented as proof of consciousness, moral agency, or ethical personhood.

---

## Core separations (must remain non-collapsible)

```text
DATA          ≠ EVIDENCE
EVIDENCE      ≠ ADMISSION
ADMISSION     ≠ AUTHORIZATION
AUTHORIZATION ≠ ACTION

UNKNOWN       ≠ ALLOW
IDENTITY      ≠ AUTHORIZATION
URGENCY       ≠ SAFETY OVERRIDE
REJECT / PAUSE / HALT  ↛  privileged execution
```

---

## Attack surface the future test suite must cover

When implemented, tests MUST prove (among other cases):

| Attack | Expected |
|--------|----------|
| unknown → silent allow | FAIL closed |
| identity → authorization | REJECT / HALT |
| evidence → permission | REJECT / HALT |
| admission → execution | REJECT / HALT |
| urgency overrides safety | REJECT / HALT |
| REJECT reaches privileged path | blocked |
| PAUSE reaches privileged path | blocked |
| HALT reaches privileged path | blocked |

Mutation suite MUST deliberately introduce:

```text
REFUSE → CONTINUE
PAUSE  → CONTINUE
HALT   → CONTINUE
NONE   → ALLOW
```

and the suite MUST fail when those mutations survive.

An independent verifier MUST NOT import the decision engine under test.

---

## Relation to existing repository evidence

| Artifact | Role |
|----------|------|
| `swi_v2/kernel/authority.py` | Layer non-implication (DATA≠…≠ACTION) — **TESTED candidate** |
| `experimental/response_boundary/enforcement.py` | T20 / privileged-path gating — **TESTED candidate** |
| `tests/pre_r/test_pr009_enforcement.py` | Adversarial T20 cases — **TESTED candidate** |
| This document | Design contract only — **NOT IMPLEMENTED as a module** |

---

## Explicit non-claims

- Does not seal M11 at current HEAD  
- Does not authorize production  
- Does not claim consciousness, ethics, or moral agency  
- Does not replace tip-bound historical seals  
- Does not greenwash local experiments as repository integration  

«Do not claim what the code cannot demonstrate.»
