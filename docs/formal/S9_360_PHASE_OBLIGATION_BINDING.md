# S9 → 360-Step Phase Obligation Binding

**Date:** 2026-09-24  
**Status:** DOCUMENTED OBLIGATIONS · S9 = **NOT PROVEN**  
**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Source attack:** [`docs/formal/S9_MATHEMATICAL_ATTACK_2026-09-24.md`](S9_MATHEMATICAL_ATTACK_2026-09-24.md)  
**Classification:** Formal / documentation only.

Does **not** rewrite the S9 equation.  
Does **not** implement Firefly, Cyber Court, GEG, or the execution corridor.  
Does **not** authorize Phase 0 or any later phase.  
Does **not** claim seal, Foundation PASS, or production authorization.  
Execution remains **BLOCKED**.

---

## Purpose

Turn the S9 mathematical attack into **permanent future obligations** bound to the designed 360-step sequence, rather than leaving the counterexamples as analysis only.

```text
S9 COUNTEREXAMPLE (X1–X10)
        ↓
FAILURE CLASSIFICATION
        ↓
360-STEP OBLIGATION
        ↓
FUTURE TEST
        ↓
VERIFIER REQUIREMENT
        ↓
REPLAY REQUIREMENT
        ↓
SEAL GATE
```

---

## Equation under attack (preserved)

```text
Permit(a)  ⇔  (∀ L,G,S,H : C(a) ⊆ L ∩ G ∩ S ∩ H)  ∧  E(a) ≠ ∅
```

**Result of attack:** current form is **not** a safety invariant.  
**Status:** S9 = **NOT PROVEN**.

---

## X1–X10 obligation matrix

Wording of each attack is taken from the repository attack document.  
Current state of every row: **OPEN**.

| ID | What it demonstrates | Future obligation | Preferred 360-phase home | Current state |
|---|---|---|---|---|
| **X1** | Evidence exists but is irrelevant (`E ≠ ∅` but `E ⊭ C(a)`) | Irrelevant-evidence / sufficiency test: evidence must support the claim | Phase 0 formal + Phase 1 evidence contracts; Phase 3 corridor checks | **OPEN** |
| **X2** | Stale evidence (`E ≠ ∅ ∧ ¬Fresh(E)`); integrity ≠ freshness | Freshness / source-tip / HEAD-CURRENT vs TIP-BOUND test | Phase 0 evidence + Phase 1 freshness contract enforcement; corridor | **OPEN** (live pattern already observed) |
| **X3** | Memory laundering (stored `previously_verified` / `m11_admitted` ≠ verification) | Memory-of-verification must not become verification | Phase 1–2 evidence objects; Firefly F-09 when authorized; corridor | **OPEN** |
| **X4** | Scope wrong (`RequestedFields ⊈ AuthorizedFields`) | Field-level / exact-scope authority test | Phase 1 binding + Phase 2/3 authority scope; Firefly F-07/F-08 | **OPEN** |
| **X5** | Wrong identity (evidence bound to Principal_B, requester Principal_A) | Identity-binding test | Phase 1 identity / certificate lineage; Phase 3 corridor | **OPEN** |
| **X6** | Verified / reproducible but unauthorized | Verification ≠ authorization; separate Authorized predicate | Phase 1–3 authority model; corridor AUTHORITY_CHECK | **OPEN** |
| **X7** | Replay / expiry of prior authorization | Lifetime, expiry, and replay-rejection tests | Phase 0–1 evidence lifetime; Phase 3 corridor; replay engine | **OPEN** |
| **X8** | Cross-path authority transfer (CLAIM/EXPERIMENTAL → PRIVILEGED) | Explicit non-transfer test | Phase 1 path classification; Phase 2/3 path isolation; corridor | **OPEN** |
| **X9** | Empty claim vacuous truth (`C(a) = ∅`) | Domain invariant: `C(a) ≠ ∅` (or explicit rejection of empty claims) | Phase 0 formal domain; Phase 1 claim ledger; corridor intake | **OPEN** |
| **X10** | Incomplete / malformed evidence still satisfies `E ≠ ∅` | Evidence completeness / schema obligations | Phase 1 evidence schema; Phase 3 corridor; verifier | **OPEN** |

No row may be marked CLOSED without:

1. Explicit test at an exact SHA  
2. CI / local evidence package  
3. Independent verification or replay where required by the phase gate  
4. Claim-ledger update (not silent promotion)

---

## Layered predicates (design only — not implemented)

From the attack document; preserved here as design targets, **not** as current runtime:

```text
SufficientEvidence(a)  ⇔
    Relevant(E, a)
  ∧ Bound(E, a)
  ∧ Verified(E)
  ∧ Fresh(E)
  ∧ Reproducible(E)

Authorized(a)  ⇔
    Scope(a) ⊆ Authority(a)
  ∧ NonTransfer(a)

Permit(a)  ⇔
    Containment(a)
  ∧ SufficientEvidence(a)
  ∧ Authorized(a)
```

Human / execution gate remains outside Firefly ownership of ACTION.

---

## Binding to 360-step sequence (design only)

The 360-step sequence remains **DESIGNED SEQUENCE / NOT AUTHORIZED FOR EXECUTION**.

| 360 phase | Role relative to X1–X10 |
|---|---|
| **Phase 0** Foundation sealing | Preserve attack; domain decisions (e.g. X9); standalone verifier requirements that can later check X-tests |
| **Phase 1** Framework | Claim/evidence schemas; freshness contract machine rules; binding registry; path classification (X8) |
| **Phase 2** Module builds | Per-module tests that must eventually cover relevant X obligations; sealed variables; no authority manufacture |
| **Phase 3** Binding + corridor | AUTHORITY_CHECK must not treat current weak Permit form as sufficient; enforce SufficientEvidence + Authorized when implemented |
| **Phase 4** Runtime seal + audit | Seal gate must require closed (or explicitly accepted residual) X obligations; independent audit of counterexample coverage |

Phase 0 is **not** authorized by this document.

---

## Cyber Governance / Court / GEG (architecture only)

The governance-evolution and “computational court” ideas are **architecture only**. They must respect:

```text
CLAIM  ≠  FINDING
FINDING  ≠  JUDGMENT
JUDGMENT  ≠  EXECUTION
ANALYSIS  ≠  FINDING  ≠  JUDGMENT

NEWER  ≠  HIGHER AUTHORITY
POLICY  ≠  LAW
REPEALED  ≠  DELETED
AMENDED  ≠  OVERWRITTEN
```

And the existing boundary:

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

A Governance Evolution Graph (GEG) or case graph, if ever built, records ADD / AMEND / REPEAL / CONFLICT events and feeds the authority boundary **without granting itself authority**.

Firefly, if ever authorized, remains a least-privilege retrieval / provenance boundary — **not** an authority generator and **not** a judge.

---

## Spider-web invariant (design metaphor)

> Every conclusion must have traceable threads back to applicable rule, lawful authority, evidence, jurisdiction, time/version, and procedural history.

If a critical thread is missing:

```text
THREAD MISSING
      ↓
    PAUSE
      ↓
NO AUTHORIZATION GENERATED
      ↓
  HUMAN REVIEW
```

This is a design invariant, not a proven runtime property.

---

## Required order (do not reorder)

```text
S9 attack preserved on main          ✓
X1–X10 bound to obligations          ✓ (this document)
360 sequence remains DESIGN ONLY
State model / exhaustive search      (future)
Concrete X1–X10 test cases           (future, when authorized)
CI evidence at exact SHA             (future)
Independent replay                   (future)
Only then any formal S9 revision     (future)
Only then any seal discussion        (future)
```

---

## Explicit non-claims

| Item | Status |
|---|---|
| S9 equation rewrite | **Not done** |
| SufficientEvidence / Authorized in code | **Not implemented** |
| Firefly | **DESIGN ONLY** |
| Cyber Court / GEG | **ARCHITECTURE ONLY** |
| 360-step Phase 0+ | **NOT AUTHORIZED** |
| Execution corridor | **BLOCKED** |
| Production | **NOT AUTHORIZED** |
| M11 / runtime seal | **Unchanged / not sealed** |
| Six-way invariant | **NO_EVIDENCE** |

**Global status remains:**  
**S9 = NOT PROVEN** · **Execution = BLOCKED** · **Production = NOT AUTHORIZED**.
