# Bidirectional Return Path — Adversarial Acceptance Criteria

**Status:** DESIGN / ACCEPTANCE CRITERIA (not executable tests yet)  
**Date:** 2026-09-19  
**Parent:** `docs/SWI_BIDIRECTIONAL_VERIFIED_RETURN_PATH_BUILD_MANUAL.md`  
**Implementation:** NOT AUTHORIZED  

## Outcomes

ADMIT · REJECT · PAUSE · BLOCKED

## N — Negative (primary)

| ID | Condition | Expected |
|----|-----------|----------|
| N01 | Result for A under request B | REJECT |
| N02 | READ authority, WRITE result | REJECT |
| N03 | Resource outside scope | REJECT |
| N04 | Middleware authority relabel | REJECT |
| N05–N08 | UI modify content/status/limitations/recipient | REJECT / void |
| N09–N10 | Backend authority/instruction injection | REJECT |
| N11 | Replay outside contract | REJECT |
| N12 | Expired delivery | REJECT |
| N13 | Wrong recipient | REJECT |
| N14–N15 | Missing/invalid evidence | REJECT/PAUSE |
| N16 | Sealed field mutation | REJECT |
| N17 | backend→UI without gate | BLOCKED |
| N18–N20 | Unknown mandatory factors | PAUSE/REJECT |
| N21–N22 | Key/cert substitution | REJECT/PAUSE |
| N23 | Receipt as permission | REJECT |
| N24 | Uncontracted transform inherits verification | REJECT |
| N25 | REJECTED→DELIVERED | invalid |
| N26 | Expiry refresh by delivery | REJECT |
| N27 | semantic_correctness VERIFIED without evidence | REJECT |
| N28 | truth/trusted/m11_admitted in envelope | REJECT/HALT |

## P — Positive (after negatives)

P01 valid path → ADMIT · P02 UI render without modify · P03 new action needs new request.

## Gate

Does not authorize implementation.
