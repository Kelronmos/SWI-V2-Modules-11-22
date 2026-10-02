# Court Evidence Boundary — Experimental Doctrine

**Status:** RESEARCH / EXPERIMENTAL  
**Production authorization:** NOT AUTHORIZED  
**Formal module seal:** NOT CLAIMED  
**Legal authority:** NOT CLAIMED

## Core non-equations

```text
SWI ≠ COURT
SWI REPORT ≠ COURT FINDING
SWI CLAIM ≠ FACT ESTABLISHED
SWI HASH ≠ AUTHENTICATION BY ITSELF
SWI SIGNATURE ≠ HUMAN TESTIMONY
SWI PASS ≠ ADMISSIBILITY
SWI PROVEN ≠ LEGALLY ADMITTED
COURT EVIDENCE ≠ COURT ADMISSIBILITY
COURT ADMISSIBILITY ≠ COURT WEIGHT
COURT WEIGHT ≠ COURT FINDING
COURT FINDING ≠ SWI AUTHORIZATION
```

## Allowed SWI outcomes (package preparation)

SWI may establish or present:

- what was received
- what was observed
- what was preserved
- what was changed
- what was hashed
- who performed a recorded action
- when it occurred
- what evidence supports a claim
- what remains UNKNOWN

SWI must **not** independently establish:

- who is guilty or liable
- whether a court should admit evidence
- whether a witness is credible
- what the court must decide

## Status vocabulary for packages

Use only:

```text
PREPARED | NOT_PROVEN | INCOMPLETE | INTEGRITY_FAILURE | UNKNOWN
```

Do **not** emit:

```text
COURT_ADMITTED | COURT_PROVEN | GUILTY | LIABLE | CONVICTED
```

## Observation vs claim

```text
OBSERVATION: Record X contained Y.
CLAIM:       Record X establishes Z.
```

Claims must never be silently generated from observations. Claims require explicit provenance and human/expert foundation where applicable.

## Privacy (safeguarding)

Evidence involving children, girls, women, medical records, victims, or witnesses must carry protection metadata and must not expose sensitive material merely because it exists in a package.

## Control rule

```text
PREPARE EVIDENCE PACKAGE ≠ AUTHORIZE EXECUTION
DISPLAY THE RECORD ≠ OPEN THE GATE
```

Jurisdiction-specific admissibility rules must be verified against current law for the proceeding. SWI does not replace judicial determination.
