# SAMH SWI — Student Monitor Architecture

**Status:** DESIGN / DRAFT  
**Seal:** NOT SEALED  
**Production:** BLOCKED  
**Date:** 26 September 2026

> Governed student-support and safeguarding information system.  
> **Not** an autonomous system that decides a child is “high risk” and acts on that decision.

**Hard invariant:**

```text
DATA → SIGNAL → EVIDENCE → INTERPRETATION → RECOMMENDATION
  → HUMAN REVIEW → AUTHORIZATION → ACTION

NEVER: DATA → AI → ACTION
AI_SIGNAL ≠ HUMAN_DECISION
```

Related: `docs/INSTITUTIONAL_GOVERNANCE_VISIBILITY.md` · `docs/PROGRAM_PROOF_BOUNDARY.md` · `docs/SWI_WEB_EXTEND_RULE.md`

---

## 1. Ten governed layers (conceptual)

| Layer | Role |
|-------|------|
| L10 | Human authority / safeguarding decision |
| L9 | Notification / intervention gate (human review) |
| L8 | SWI AI assistant (explain, summarize, recommend, educate) |
| L7 | Risk & signal analysis (engagement, attendance, wellbeing trends) |
| L6 | Dashboard / reporting (role-scoped) |
| L5 | Real-time data fabric (adapters) |
| L4 | Identity + RBAC + relationship authority |
| L3 | Privacy / security / audit |
| L2 | SWI control plane (gates, pause/wake, S-suite as defined) |
| L1 | Source data (attendance, engagement, check-ins, feedback) |

---

## 2. Prohibited outputs (especially minors)

```text
NO diagnosis
NO personality classification
NO mental-health diagnosis
NO disciplinary prediction
NO "problem child" label
NO permanent risk label
NO automated punishment
NO automated exclusion
NO automated parent notification solely because an AI score crossed a threshold
```

Prefer support language:

> Observed: attendance decreased X%. Engagement decreased Y%. Check-in changed.  
> Interpretation: multiple indicators changed vs baseline.  
> Suggested next step: teacher/counsellor review.  
> Student may add context or correct information.

**Not:** “Student is high risk.”

RandomForest (or similar) trained on tiny sample rows is **not** a legitimate production risk engine.

---

## 3. Signal index (not diagnostic risk score)

```text
Engagement · Attendance · Wellbeing · Change · Context signals
  → SIGNAL INDEX → Low / Review / Elevated
  → Explain contributing evidence
  → Human review where required
```

Identify a **support signal** without claiming psychological state.

---

## 4. Relationship-based authorization

Role alone is insufficient.

```text
Teacher → employed_by School → assigned_to Class → Student
Parent → verified_relationship → Child
District officer → authorized_scope → District → Schools
```

Valid account ≠ universal search key.

Domains (typical): Student (self) · Parent (linked) · Teacher (assigned) · School Admin · District (aggregate) · Ministry (aggregate/de-identified by default).

---

## 5. Data model separation

Separate tables/collections conceptually: identity · engagement · attendance · wellbeing check-in · access_event audit.  
Do not put everything in one giant student table.

Canonical events carry **provenance** (source, connector, received_at, source_version).

Adapters: Google Sheets / Firebase / SQL → canonical model → event fabric → dashboards / AI / audit.  
Sheets are not the authoritative high-scale operational store.

---

## 6. Control plane (CEK / LAP / etc.)

```text
REQUEST → CEK → (PASS → LAP → security → authority → human review → APPROVED/REJECTED)
                (FAIL → PAUSE)
```

```text
CEK ≠ AUTHORIZATION
LAP ≠ AUTHORIZATION
SIGNATURE ≠ AUTHORIZATION
```

They establish conditions and evidence for an authority decision.

---

## 7. Action tiers

| Tier | Meaning |
|------|---------|
| T0 | Informational — AI may respond |
| T1 | Personalized recommendation — user confirmation |
| T2 | Support workflow — authorized human review |
| T3 | Safeguarding escalation — designated authority |
| T4 | Exceptional institutional action — multi-person authorization |

Do not turn every interaction into a ceremony; do not skip human authority on T2+.

---

## 8. Core equation

```text
ACTION(student) ⇔
  VALID_DATA ∧ VALID_PROVENANCE ∧ AUTHORIZED_ACTOR ∧ VALID_POLICY
  ∧ CONTROL_GATES_PASS ∧ HUMAN_AUTHORITY ∧ AUDITABLE

NO_EVIDENCE → NO_PROMOTION
NO_AUTHORITY → NO_ACTION
NO_PROVENANCE → NO_TRUST
NO_AUDIT → NO_COMMIT
AI_SIGNAL ≠ HUMAN_DECISION
```

---

## 9. Legal / privacy posture (design intent)

Children’s data, profiling, automated decision-making, transparency, and human intervention require careful handling under applicable law (e.g. GDPR principles; POPIA restrictions on solely automated decisions with substantial effect).  
Large-scale monitoring implies privacy impact assessment as a **prerequisite**, not afterthought.  
This document does **not** constitute legal advice or compliance certification.

Educational / design work uses **synthetic** students only. Real student data disallowed until separately authorized.

---

## 10. Preserve existing SWI flow

Do not rewrite the core SWI path to “fit” SAMH. Add SAMH as a **governed string** of the web. See `docs/SWI_WEB_EXTEND_RULE.md`.

**Non-claims:** No implementation, seal, production deployment, or diagnosis capability asserted.
