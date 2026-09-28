# SWI Multi-Level Institutional Demonstration

**Status:** EXPERIMENTAL / CONTROLLED DEVELOPMENT  
**S9:** NOT PROVEN (unchanged)  
**Production:** NOT AUTHORIZED  
**Main:** do not merge without review  

## Principle

Organizational levels (student → … → state) are **not** automatic authority levels.

One underlying model: CASE + EVIDENCE + AUTHORITY + PRIVACY + DEPENDENCY + RECEIPT + DECISION + ESCALATION + RECONCILIATION.

UI plates are views only.

## S9

Uses existing `swi_v2.s9.evaluator` when present to **tighten** decisions only.  
Does not set `s9_proven=true`. Does not alter S9 harness proof status.

## Run

```bash
python -m pytest -q tests/institutional/
python scripts/institutional_demo_run.py --commit <SOURCE_COMMIT>
```

## Claims forbidden

Do not claim legal compliance, privacy guarantee, S9 proof, production readiness, or that hierarchy replaces human authority.
