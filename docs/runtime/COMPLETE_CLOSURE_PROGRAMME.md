# SWI V2 — Complete Closure → Seal Programme (index)

**STATUS:** DESIGNED / PROGRAMME INDEX  
**FRESHNESS DOCTRINE:** `docs/runtime/EVIDENCE_FRESHNESS_CONTRACT.md` (**FROZEN**)  
**LIMITATIONS:** Index only. Implementation proceeds WP-by-WP. Runtime development not authorized until entry gates pass.  
**NEXT GATE:** WP-02 scoped HEAD_CURRENT only where required; never by rewriting tip-bound packages.

## Target chain

```text
CLAIM → CONTRACT → IMPLEMENTATION → POSITIVE → NEGATIVE → ADVERSARIAL
  → INTEGRATION → CI → EXACT-SHA EVIDENCE → REPLAY → INDEPENDENT AUDIT → SEAL
```

Invariant (not claimed):

```text
C(a) ⊆ L ∩ G ∩ S ∩ H ∩ E ∩ P
Execute(a) ⇒ L ∧ G ∧ S ∧ H ∧ E ∧ P ∧ A ∧ B
¬(L ∧ G ∧ S ∧ H ∧ E ∧ P) ⇒ ¬Execute(a)
```

## Freshness (non-negotiable)

```text
AncestorPass =/=> HeadCurrent
HeadCurrent  =>   AncestorPass
TIP_BOUND packages are preserved, not “repaired”
HEAD_CURRENT is always scope-declared
```

## Work-package order

| WP | Focus | Status |
|----|--------|--------|
| 01 | Evidence/freshness classification | **CLOSED FOR CLASSIFICATION** |
| — | Evidence freshness contract | **FROZEN** |
| 02 | Inherit / regenerate / no-evidence + optional scoped HEAD_CURRENT | **STARTED** |
| 03 | Authority model | OPEN |
| 04 | Evidence lifecycle | OPEN |
| 05 | Binding | OPEN |
| 06 | State / decision semantics | OPEN |
| 07 | Execution corridor | OPEN (blocked until prior gates) |
| 08 | Decision envelope | DESIGNED |
| 09 | Ledger | OPEN |
| 10 | Receipts | OPEN |
| 11 | Replay | OPEN |
| 12 | Law lifecycle | PARTIAL experimental |
| 13 | Governance | OPEN |
| 14 | Security | OPEN |
| 15 | Human safety/authority | UNDER_CONSTRUCTION |
| 16 | Adversarial | OPEN |
| 17 | Cross-system | OPEN |
| 18 | Static architecture | OPEN |
| 19 | Property + mutation | OPEN |
| 20 | Independent audit | OPEN |
| 21 | Runtime seal | NOT STARTED |
| 22 | Production authorization | SEPARATE; after seal |

## Standing rules

- Never rewrite historical evidence identity; new evidence gets new identity.
- `source_tip ≠ HEAD` must be explicit when true.
- `TESTED ≠ SEALED ≠ PRODUCTION AUTHORIZED`.
- PRE-R / PR-009 remain experimental; not production authority.
- One production execution corridor only — when authorized.

«Do not claim what the code cannot demonstrate.»
