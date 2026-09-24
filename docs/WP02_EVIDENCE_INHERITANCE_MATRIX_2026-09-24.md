# WP-02 Evidence Inheritance Matrix — 24 September 2026

**STATUS:** STARTED / DESIGNED  
**EVIDENCE:** Git history `8245e3f..HEAD` path classification; WP-01 location report.  
**LIMITATIONS:** Not a full claim ledger yet. Not CI-VERIFIED inheritance. Not seal.  
**NEXT GATE:** Expand claim-by-claim ledger (`FOUNDATION-*`, `LAW-*`, …) with exact test paths; regenerate only where domain = REGENERATE.

Execution: **BLOCKED**. Do not open runtime corridor under WP-02.

---

## 1. Bounded evidence domain (law package)

```text
Evidence package (law)
  source_tip     = 8245e3f03d8673c966abf9c63be9d838073159b0
  ancestor_of    = current main HEAD (post PR #2)
  blobs_match    = true (authority.py, registry.py)
  freshness_tests = 2 passed (local)
        |
        v
   TIP-BOUND EVIDENCE
        |
        +-- supports claims about experimental/law at 8245e3f
        +-- does NOT automatically support later commits outside that domain
```

---

## 2. What changed after `8245e3f` (path view)

| Domain | Commits after tip (summary) | Inheritance |
|--------|----------------------------|-------------|
| `experimental/law` **code** (authority/registry) | No content drift; blobs still match | **INHERIT** formal + pytest-law claims for that surface |
| `tests/law` anti-stale guard | `1b1206b` added freshness tests | **INHERIT** tip results; guard is meta-evidence |
| `evidence/law` | Package itself written for tip | **INHERIT** as tip-bound record |
| `docs/*` (closure, H, WP-01, position) | Documentation only | **NO EVIDENCE NEEDED** for runtime claims; docs ≠ proof |
| `swi_v2/` production kernel path | No commits in `8245e3f..HEAD` for this slice | **NO EVIDENCE** from law package for runtime closure |
| Decision envelope / human capability | Design docs only | **NO EVIDENCE** (UNDER_CONSTRUCTION / DESIGNED) |
| Full V2 module suite at **current** HEAD | Prior CI at older tips (e.g. `f475589`) | **REGENERATE / RE-VERIFY** before claiming HEAD-CURRENT |
| Two-checkout travel | Historical PASS on older tip | **REGENERATE** for post-baseline HEAD if claimed CURRENT |
| PRE-R | Separate experimental surface | **BOUNDED** — do not inherit into production runtime |

---

## 3. Claim buckets for WP-02

### A — INHERIT (tip-bound, still valid for named tip)

- Z3 F-001…F-006 **model** results at `8245e3f` (formal PASS ≠ Python proof ≠ seal).
- Experimental law pytest count recorded in package (40 passed at generation).
- Authority/registry blob identity unchanged ⇒ containment **of those files** still tip-bound.

### B — REGENERATE before HEAD-CURRENT claim

- Any statement “current main HEAD is CI-green for full suite”.
- Two-checkout / cross-repo travel as **current**.
- Foundation non-execution PASS as **current**.
- Any expansion of law formal results to post-tip **code** changes (if/when authority/registry change).

### C — NO EVIDENCE yet

- Six-way `C(a) ⊆ L ∩ G ∩ S ∩ H ∩ E ∩ P`.
- Mandatory execution corridor / `ExecutionCapability`.
- HumanAuthorizationCapability (H).
- DecisionEnvelope as issued runtime object.
- Ledger-as-precondition.
- Process-wide REFUSE/ESCALATE non-bypass.
- Snyder six as closed runtime.
- Runtime seal / production authorization.

---

## 4. Ordered programme (do not skip gates)

```text
WP-01  CLOSED FOR CLASSIFICATION, OPEN FOR RE-PROOF WHERE REQUIRED
  ↓
WP-02  Evidence/foundation closure (this matrix → claim ledger)
  ↓
WP-03  Authority model (beyond local MATH-002)
  ↓
WP-04  Evidence lifecycle
  ↓
WP-05  Binding
  ↓
WP-06  State / decision semantics
  ↓
WP-07  Canonical execution corridor
  …
WP-15  Human safety/authority
  …
WP-21  RUNTIME SEAL
  ↓
WP-22  Production authorization (separate)
```

Each WP: small proof increment at exact SHA → claim/evidence/limitation update → tests → then unlock next. No giant single commit of the full programme.

---

## 5. Human authority reminder (not WP-02 deliverable)

`H` docs do **not** satisfy `H`.

```text
SYSTEM DECISION → REQUIRES HUMAN?
  NO  → continue only if law/policy permits
  YES → HUMAN REVIEW → verified human ID + authority/scope
      → reviewed claim/evidence/law/policy/ethics
      → HumanAuthorizationCapability → binding → execution gate
```

`human_id` alone must never become authority.

---

## 6. Non-claims

This matrix does **not**:

- claim Foundation PASS
- open execution
- reseal M11
- convert tip-bound law evidence into HEAD-wide proof
- implement DecisionEnvelope or HumanAuthorizationCapability

«Do not claim what the code cannot demonstrate.»
