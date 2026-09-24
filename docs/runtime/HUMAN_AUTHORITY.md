# Human Authority (H) — Status

**STATUS:** UNDER_CONSTRUCTION / DESIGNED  
**EVIDENCE:** None — no runtime issues a bound human authorization capability.  
**LIMITATIONS:** Mentions of `human_approved` in authority field denylists and prose are *rejection signals*, not an implemented human-authority lane.  
**NEXT GATE:** Define `HumanAuthorization` / capability contract, level model, and binding to request+resource+action+evidence+law+policy; then tests that forbid boolean-only approval and AI-as-human.

This document does **not** authorize execution.  
This document does **not** claim `H` in `C(a) ⊆ L ∩ G ∩ S ∩ H ∩ E ∩ P` is closed.

---

## What exists today

| Item | Reality |
|------|--------|
| Field name `human_approved` in authority denylist / undeclared-authority checks | Treated as **forbidden undeclared authority**, not as a working human gate |
| Decision-envelope note | Design only: human ID must bind to exact action context |
| Escalation / REQUIRES_HUMAN_REVIEW disposition | Named in design vocabulary; not a first-class non-bypassable runtime state |
| WP-15 (human safety) in closure baseline | Ordered work package — **not started as implementation** |
| AI / system PASS | **Never** equals human authorization |

---

## Required separations (must hold when built)

```text
SYSTEM_RESULT ≠ HUMAN_AUTHORIZATION
APPROVED ≠ AUTHORIZED ≠ EXECUTED
signature valid ≠ human intent ≠ legal authority
human_id alone ≠ capability for this action
Level-N approval ≠ Level-(N+1) authority
```

When human review is required:

```text
HumanRequired(a) ⇒ Valid(HumanAuthorizationCapability)
```

and the capability must bind at least:

```text
human_id ∥ request ∥ resource ∥ action ∥ evidence ∥ law ∥ policy
```

Mutation of any bound component invalidates the capability.

---

## Explicit non-claims

- Human authority is **not** implemented.
- Human authority is **not** tested as a closed runtime gate.
- Human authority is **not** CI-verified, audited, or sealed.
- Presence of this file does **not** satisfy `H` in the six-way invariant.
- Escalation text in manuals is **not** proof of non-bypassable ESCALATE.

---

## Construction target (design sketch only)

1. `HumanAuthorization` record (identity, role, level, scope, reviewed digests, expiry).
2. `HumanAuthorizationCapability` issued only after review — not a boolean flag.
3. Level ladder (operator → reviewer → domain → institutional → statutory) enforced by policy/law, not by caller assertion.
4. ESCALATE / REQUIRES_HUMAN_REVIEW as terminal non-execute states until a valid capability is presented.
5. Adversarial tests: forge human_id, widen scope, reuse expired approval, substitute action after approval, treat model output as human.

Until those exist with evidence at an exact SHA:

```text
H = UNDER_CONSTRUCTION
```

«Do not claim what the code cannot demonstrate.»
