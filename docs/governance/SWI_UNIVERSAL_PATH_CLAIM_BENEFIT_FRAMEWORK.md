# SWI Universal Path, Claim, Evidence and Benefit Framework

**Status:** DESIGN / CONTROLLED DEVELOPMENT  
**Production:** NOT AUTHORIZED  
**Seal:** NOT REQUESTED  
**Tip binding:** `aa62042888886f5252e2b80e7aec8dce49e4bab3`  
**Branch intent:** `governance/universal-path-claim-benefit-framework`

This framework defines how new or edited SWI paths are classified, investigated, evidenced, reviewed, reproduced and closed.

It does **not** create authority merely by recording authority fields.  
It does **not** convert experimental evidence into proof.  
It does **not** create automatic ownership or royalty entitlement.  
It does **not** force adoption of any benefit-allocation term.

```text
REVIEW ≠ APPROVAL
EVIDENCE ≠ AUTHORITY
EXPERIMENT PASS ≠ PRODUCTION
TEST PASS ≠ CLOSED ≠ SEALED ≠ AUTHORIZED ≠ EXECUTED
PRODUCTION-READY ≠ FORCED BENEFIT TERM
```

---

## 0. Scope and non-claims

| May do | Must not do |
|--------|-------------|
| Record path identity, claims, evidence, consequences | Grant permission from a JSON field |
| Classify claim balance and risk/consequence class | Treat balance score as authority |
| Flag CLAIM_IMBALANCE, MISSING evidence, STALE | Auto-repair history or invent claims |
| Map affected parties / decisions / votes | Political persuasion or vote manipulation |
| Record required authority class | Manufacture human capability (H remains open) |
| Offer optional benefit-allocation term for voluntary adoption | Force 75% (or any %) on all projects |
| Record royalty/benefit *measurement* when a term is adopted | Automatic payment or contractual entitlement without legal instrument |

**M11:** untouched. Historical seal records are not rewritten by this framework.

---

## 1. Universal path

```text
NEW PATH
  ↓ IDENTITY → PURPOSE → SCOPE → STRUCTURE
  ↓ DEPENDENCIES → AVAILABLE EVIDENCE → PROVENANCE / FRESHNESS
  ↓ EXPERIMENT → TEST → REPLAY
  ↓ FORMAL CHECK / PROOF WHERE APPLICABLE
  ↓ ADVERSARIAL REVIEW → CONSEQUENCE REVIEW
  ↓ AFFECTED-PARTY REVIEW → DECISION / VOTE IMPACT REVIEW
  ↓ SECURITY → HUMAN SAFETY → AUTHORITY → BINDING
  ↓ EXECUTION CONDITIONS
  ↓ BEFORE / DURING / AFTER → RECONCILIATION
  ↓ INDEPENDENT REVIEW → CLOSURE
```

Every step produces records. No step alone creates execution authority.

---

## 2. Claim record

Schema: `docs/governance/claim_schema.json` (`swi.claim.v1`).

Controlled claim categories:

```text
STRUCTURE · IMPLEMENTATION · EVIDENCE · PROVENANCE · DEPENDENCY
TEST · EXPERIMENT · REPLAY · FORMAL · SECURITY
AUTHORITY · HUMAN_IMPACT · CONSEQUENCE · GOVERNANCE · REMEDY
```

**Claim balance** compares actual distribution against the required profile for the path’s risk/consequence class. Imbalance is flagged as `CLAIM_IMBALANCE`; the system does not invent claims to “balance” numbers.

Risk/consequence scaling determines *review depth*, not permission:

| Class | Review depth (indicative) |
|-------|---------------------------|
| S0/C0 | Minimal |
| S1/C1 | Evidence + test |
| S2/C2 | Dependency + verification |
| S3/C3 | Authority + consequence + replay |
| S4/C4 | Independent multidisciplinary review |
| S5/C5 | Maximum applicable controls |

---

## 3. Path record

Schema: `docs/governance/path_record.schema.json`.

Required conceptual fields: path_id, path_version, parent_path, source, purpose, scope, size_class, risk_class, consequence_class, dependencies, affected_parties, affected_decisions, affected_votes, evidence, experiments, tests, replay, formal_checks, security_review, authority_review, human_safety_review, status.

---

## 4. Consequence review

See `docs/governance/CONSEQUENCE_REVIEW.md`.

Questions (impact analysis, not persuasion):

- What does it change?
- Who / what systems / what decisions can be affected?
- Can it affect a vote, eligibility, counting, or information presented to decision-makers?
- Can it suppress, duplicate, or alter a recorded decision?
- Direct vs downstream consequence; reversibility; remedy.

---

## 5. Evidence inventory

Schema: `docs/governance/evidence_inventory.schema.json`.

Statuses: `VALID_CURRENT` · `VALID_HISTORICAL` · `EXPERIMENTAL` · `STALE` · `CONTRADICTORY` · `UNRESOLVED` · `UNTRUSTED` · `MISSING`.

**Experimental** is never promoted to production by this framework alone.

---

## 6. Replay and proof

Replay: original input → recorded → replay → compare → MATCH / MISMATCH / UNRESOLVED. Mismatch produces a diagnostic; it does not rewrite the original.

Proof registry categories (`docs/governance/proof_registry.json`):

```text
NONE · OBSERVED · TESTED · REPRODUCED · FORMALLY_CHECKED · INDEPENDENTLY_VERIFIED
```

Example mapping:

| Result | Classification |
|--------|----------------|
| pytest PASS | TESTED |
| Independent replay | REPRODUCED |
| Z3 property (where applicable) | FORMALLY_CHECKED |
| Independent model↔code correspondence | INDEPENDENTLY_VERIFIED |

Z3 or formal PASS is limited to the stated model and tip binding; it is not a claim about the entire SWI system.

---

## 7. Authority boundary

**Reuse existing SWI authority surfaces** (`swi_v2/kernel/authority.py`, halt, INV-08 / H).

This framework may *record*:

- required_authority  
- authority_reference  
- authority_scope  
- authority_status  

```text
recorded authority ≠ actual authority
```

Actual authority remains subject to the established multi-way condition with **H = UNDER_CONSTRUCTION** until INV-08 is closed by evidenced capability work.  
JSON fields such as `"authorized": true` remain data only and are not a permission mechanism.

---

## 8. Edited-path detection

```text
OLD PATH → DIFF → claims / evidence / dependencies affected
  → tests to re-run → replay required? → formal check required?
  → seal impact → REVALIDATION_REQUIRED
```

Material dependency change invalidates inherited verification. Do not inherit old verification blindly.

---

## 9. Future-generations benefit — optional term

See `docs/governance/FUTURE_GENERATIONS_BENEFIT_POLICY.md`.

**Adoption model: OPTIONAL.**

SWI offers a voluntary production-governance term for parties who want a transparent, auditable future-generations commitment. Reaching production readiness does **not** force adoption.

Where the term is **voluntarily adopted**, the agreed percentage, beneficiaries, qualifying uses, governance mechanism, and audit requirements must be explicitly recorded before production authorization. Reference allocation (when adopted): 75% of the *defined* benefit/royalty pool toward verified future-generations benefit, subject to the applicable agreement and legal review.

```text
DESIGN → EXPERIMENTAL → TESTED → VERIFIED → PRODUCTION-READY
  → OPTIONAL TERMS (if chosen) → AUTHORIZED PRODUCTION
```

```text
75% ALLOCATED ≠ 75% BENEFIT PROVEN
OPTIONAL TERM OFFERED ≠ TERM ADOPTED ≠ PAYMENT EXECUTED
```

**Status:** DESIGN · HUMAN / LEGAL REVIEW REQUIRED · **NOT AUTOMATICALLY CONTRACTUAL** · not an automatic payment mechanism · not forced on all projects.

---

## 10. Acceptance questions (per path)

A first implementation of this framework is successful only when SWI can answer, for a new or edited path:

1. What changed?  
2. What is claimed?  
3. What evidence exists?  
4. What is experimental?  
5. What can be replayed?  
6. What has actually been proven or formally checked?  
7. What depends on it?  
8. Who/what can be affected?  
9. Can decisions or votes be affected?  
10. What are the consequences?  
11. What authority is required?  
12. What remains unknown?  
13. What must be revalidated?  
14. Was any optional benefit term adopted? If so, under which instrument?  
15. What benefit/royalty event occurred (if any)?  
16. Where did any agreed future-generations allocation go?  
17. Can all of this be audited?

Only after those answers are structured and evidenced should the framework itself be reviewed for sealing.

**For this first implementation:** do not touch M11, do not activate production execution, and do not make any benefit allocation an automatic authority or payment mechanism.

---

## Related frozen gates

| Gate | Relationship |
|------|----------------|
| INV-05 | Baseline integrity remains prerequisite for trusting inventory used by paths |
| INV-08 / H | Human capability still UNDER_CONSTRUCTION; framework records required class only |
| System check | Protocol only; observation ≠ privilege |
| Production / seal | NOT AUTHORIZED / NOT REQUESTED by this document |

```text
«Do not claim what the code cannot demonstrate.»
```
