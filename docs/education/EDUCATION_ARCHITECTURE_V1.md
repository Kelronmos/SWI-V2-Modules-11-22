# SWI Education Architecture V1

**Document:** `docs/education/EDUCATION_ARCHITECTURE_V1.md`  
**Status:** SPECIFICATION / PROPOSED  
**Date:** 2026-09-30  
**Scope:** Levels 1–6 education framework  
**Does not modify:** M11 sealed path, kernel, B1 batch contract

---

## 1. Core Purpose

Build an SWI Education Suite that teaches children and learners how to:

- observe
- ask questions
- understand
- practise
- make mistakes safely
- detect mistakes
- recover
- verify
- explain
- apply knowledge
- connect learning to real life
- develop discipline, curiosity, creativity and responsibility

SWI education must **not** replace established academic subjects.

- Mathematics remains mathematics.
- Science remains science.
- Languages remain languages.
- Agriculture remains agriculture.
- Finance remains finance.

SWI provides a common structured-learning method across them.

---

## 2. Education Principle — The Learning Cycle

Every lesson follows a common cycle:

```text
DISCOVER
   ↓
UNDERSTAND
   ↓
PRACTISE
   ↓
TEST
   ↓
MAKE / FIND ERROR
   ↓
RECOVERY REFLEX
   ↓
VERIFY
   ↓
EXPLAIN
   ↓
APPLY
   ↓
REFLECT
```

The learner is not judged only by the final answer.

The system should also teach:

- «How did you arrive there?»
- «What evidence supports your answer?»
- «What changed?»
- «What went wrong?»
- «Can you recover?»
- «Can you reproduce the result?»

---

## 3. Recovery Reflex

Recovery Reflex is a foundational educational principle.

A mistake does not automatically mean failure.

The learner is taught to:

```text
ERROR
 ↓
STOP
 ↓
IDENTIFY WHAT CHANGED
 ↓
RETURN TO LAST VERIFIED STATE
 ↓
CHECK EVIDENCE
 ↓
CORRECT
 ↓
RETEST
 ↓
CONTINUE
```

Never teach: ERROR → HIDE ERROR → CONTINUE  
Teach: ERROR → DETECT → UNDERSTAND → RECOVER → VERIFY

Recovery does not erase history.

«Recovery means restoring valid continuity, not pretending the mistake never happened.»

---

## 4. Setho and Botho

The education suite incorporates Setho and Botho as human-centred principles.

**Setho** — respect for knowledge, learning, discipline, responsibility, community, environment, work, truthfulness and cultural heritage.

**Botho** — knowledge and ability carry responsibility toward other people. Learning therefore develops respect, empathy, cooperation, dignity, responsibility, service, patience and accountability.

These principles must **not** replace evidence or academic standards.  
They provide the human context in which learning is applied.

---

## 5. Subject Suite Architecture

```text
SWI EDUCATION CORE
       │
       ├── Mathematics
       ├── Languages
       ├── Science
       ├── Finance
       ├── Agriculture
       ├── Culture
       ├── Medical / Health Education
       ├── Technology
       ├── Arts
       ├── Engineering
       └── Learner Passion / Career Exploration
```

Each subject contains Levels 1–6.

---

## 6. Passion Path

The learner is not forced into a single predefined identity.

The system records:

```text
INTEREST → EXPLORATION → PRACTICE → PROJECT → EVIDENCE → REFLECTION → NEXT POSSIBILITY
```

Early interest is never treated as a permanent career assignment.

---

## 7. Mathematics as Cross-Subject Language

Mathematics appears naturally across subjects (seed count → yield, income → balance, measurement → conclusion, etc.).  
The goal is not to force mathematics into every lesson, but to show that it can describe relationships in many real-world systems.

---

## 8. Universal Lesson Record (minimum fields)

```json
{
  "lesson_id": "",
  "subject": "",
  "level": "",
  "learning_objective": "",
  "prior_knowledge": [],
  "materials": [],
  "activity": "",
  "mathematics_connection": "",
  "language_connection": "",
  "culture_context": "",
  "setho_botho_context": "",
  "recovery_reflex": "",
  "assessment": "",
  "evidence": [],
  "learner_reflection": "",
  "limitations": [],
  "next_iteration": ""
}
```

---

## 9. Educational Evidence

Educational evidence records learning artefacts (exercise, explanation, project, correction, reflection, reproducible result).  
It must **not** be confused with proof of a person’s worth or intelligence.  
Do not infer more than the evidence supports.

---

## 10. Assessment Dimensions

Avoid reducing every assessment to RIGHT / WRONG.

Use multiple dimensions:

- UNDERSTANDING
- APPLICATION
- REASONING
- EVIDENCE
- COMMUNICATION
- RECOVERY
- CREATIVITY
- COLLABORATION
- REFLECTION

A learner who makes an error and successfully identifies and corrects it should have the opportunity to demonstrate that learning.

---

## 11. Status Model (evidence-driven)

```text
PROPOSED → DRAFTED → REVIEWED → PILOTED → TESTED → REVISED → REVIEWED AGAIN
```

Do **not** call material scientifically validated, medically validated, pedagogically proven, universally suitable, or safe for all learners unless appropriate evidence exists.

---

## 12. Safety Boundaries

Education involving medicine, finance, agriculture, laboratory science, machinery, chemicals or technology must contain age-appropriate safety boundaries.

```text
LEARN → SIMULATE → SUPERVISE → VERIFY → APPLY WHEN APPROPRIATE
```

Educational simulation must never silently become real-world authorization.

---

## 13. Engineering Boundary

The Education Suite must not create a competing governance architecture.

It reuses existing SWI principles (structured cycle, recovery, evidence discipline, non-overclaiming).

It does **not** modify:

- M11 sealed path
- M11 cryptographic contract
- existing Merkle implementation
- B1 batch contract

---

## 14. Implementation Method

```text
DISCOVER → CONTRACT → BUILD → TEST → REVIEW → RECOVER → REPLAY → DOCUMENT → FREEZE
```

For every educational feature:

Claim → Implementation → Test → Result → Limitation → Next iteration

---

## 15. First Implementation Phase (documentation first)

| Stage | Deliverable |
|-------|-------------|
| E0 | Education architecture (this document) |
| E1 | Levels 1–6 curriculum framework |
| E2 | Recovery Reflex educational framework |
| E3 | Setho/Botho framework |
| E4 | Subject-suite contracts |
| E5–E11 | Subject progressions and medical/health boundaries |
| E12 | Passion Path |
| E13–E14 | Lesson and assessment schemas |
| E15–E19 | Pilot lessons, testing, limitations, revision, freeze |

---

## 16. Final Educational Principle

The objective is not to create children who merely know answers.

The objective is to help learners become capable of asking:

- «What do I know?»
- «How do I know it?»
- «What don’t I know?»
- «What changed?»
- «What should I check?»
- «Can I recover?»
- «Can I explain my reasoning?»
- «How does what I know affect other people?»
- and eventually «What do I want to learn next?»

That is where Setho, Botho, mathematics, science, language, culture, practical knowledge and personal passion can coexist inside one structured learning architecture.

---

## 17. Status Summary

| Claim | Status |
|-------|--------|
| Initial education architecture | SPECIFIED |
| Educational validation | NOT CLAIMED |
| Medical validation | NOT CLAIMED |
| Pedagogical validation | NOT CLAIMED |
| Universal curriculum suitability | NOT CLAIMED |

SWI Education ≠ replacement for formal education.  
It is a proposed structured framework for organising learning, evidence, recovery, reflection and application.

---

**End of SWI Education Architecture V1**
