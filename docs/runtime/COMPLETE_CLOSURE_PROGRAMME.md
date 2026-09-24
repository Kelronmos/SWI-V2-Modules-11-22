# SWI V2 — Complete Closure → Seal Programme (index)

**STATUS:** DESIGNED / PROGRAMME INDEX  
**TIP AT DRAFT:** `8e369c6d5b22402dde20e6db0ea59d8fc8779e4a` (superseded as HEAD moves; re-bind in seal record)  
**LIMITATIONS:** Index only. Implementation proceeds WP-by-WP. Runtime development not authorized until entry gates pass.  
**NEXT GATE:** Finish WP-02 claim ledger; do not jump to execution corridor.

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

## Work-package order

| WP | Focus | Status |
|----|--------|--------|
| 01 | Evidence/freshness classification | **CLOSED FOR CLASSIFICATION** |
| 02 | Inherit / regenerate / no-evidence matrix + claim ledger | **STARTED** |
| 03 | Authority model | OPEN |
| 04 | Evidence lifecycle | OPEN |
| 05 | Binding | OPEN |
| 06 | State / decision semantics | OPEN |
| 07 | Execution corridor | OPEN (blocked until prior gates) |
| 08 | Decision semantics / envelope | DESIGNED |
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

Detail phases (geometry, contracts, envelope, human capability, adversarial A01–A30, seal criteria) live in design notes and prior manuals; this file is the **ordered gate index**, not the full specification dump.

«Do not claim what the code cannot demonstrate.»
