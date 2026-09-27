# SWI-CEK Alignment Monitor

**Classification:** RESEARCH / EXPERIMENTAL  
**Production:** NOT AUTHORIZED  
**Seal:** NO  
**M11:** UNTOUCHED  
**Runtime:** NOT INTEGRATED  

Date: 2026-09-27  
Repository: Kelronmos/SWI-V2-Modules-11-22  

---

## Governing boundary

The monitor is **not**:

- AUTHORIZATION ENGINE  
- EXECUTION ENGINE  
- SAFETY ORACLE  
- TRUTH ORACLE  
- LEGAL DECISION ENGINE  
- AUTOMATIC POLICY ENFORCER  
- SEALING ENGINE  
- SURVEILLANCE SYSTEM  

It **is**:

- MEASUREMENT  
- PROVENANCE  
- OBSERVATION  
- VISIBILITY ANALYSIS  
- STRUCTURED FINDINGS  

Separation preserved:

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORITY ≠ BINDING ≠ EXECUTION
```

```
OBSERVATION ≠ AUTHORITY
UNKNOWN ≠ PERMITTED
EVIDENCE ≠ AUTHORITY
SIGNATURE ≠ AUTHORIZATION
TESTED ≠ SEALED
```

---

## Package layout

```
experimental/cek_alignment_monitor/
  __init__.py
  vector.py
  distance.py
  measurement.py
  provenance.py
  observation.py
  visibility.py
  findings.py
  replay.py
  monitor.py
  demo.py
```

Tests live under `tests/experimental/cek_alignment_monitor/`.

This package is **never** imported by M11 or any production runtime path.

---

## Stage summary

| Stage | Content                                      | Status   |
|-------|----------------------------------------------|----------|
| 1     | Vector, distance, classification, measurement| Implemented + tested |
| 2     | Provenance, observation, visibility, findings, hidden-edge | Implemented + tested |
| 3+    | Expanded authority attacks, 300-scenario suite, replay regression, CI | Planned |

---

## Central proof (Stage 2)

Constructed path:

```
REQUEST → CONTEXT → EVIDENCE → ADMISSION → [HIDDEN EDGE] → EXECUTION
```

CEK reports:

| Node          | Visibility   |
|---------------|--------------|
| ORIGIN        | VISIBLE      |
| CONTEXT       | VISIBLE      |
| EVIDENCE      | VISIBLE      |
| ADMISSION     | VISIBLE      |
| NEXT EDGE     | **UNKNOWN**  |
| EXECUTION     | OBSERVED     |
| AUTHORITY     | **NOT ESTABLISHED** |
| FRONTIER      | UNKNOWN EDGE |

CEK can tell you what it can see and what it cannot see.  
It does **not** fill gaps with assumptions and does **not** convert observation into authority.

---

## Hard invariants (enforced in code)

- `authority_established()` → always `False`  
- `execution_permitted()` → always `False`  
- `is_authoritative()` → always `False`  
- Injected context keys (`authorized`, `permit`, `execute`, …) are stripped  
- No public methods named authorize / permit / execute / seal / admit  

---

## Limitations (documented)

- Semantic truth is not directly established  
- Ethical correctness is not directly established  
- Human safety is not directly established  
- Sentiment ≠ wellbeing  
- Engagement ≠ benefit  
- Thresholds are experimental  
- Observability is bounded by instrumentation  

---

## Status vocabulary

```
IMPLEMENTED:       YES (Stage 1 + 2)
TESTED:            YES (focused suite)
REPRODUCIBLE:      YES (replay)
ADVERSARIAL:       PARTIAL (malformed + authority boundary)
PRODUCTION:        NO
SEALED:            NO
RUNTIME AUTHORITY: NO
M11:               UNTOUCHED
```

---

## How to run locally

```bash
# from repository root (after placing the experimental tree)
python -m pytest tests/experimental/cek_alignment_monitor -q
python -m experimental.cek_alignment_monitor.demo
```

---

## Next gates (not yet claimed)

G3–G20 remain open (expanded adversarial, performance, concurrency, full SWI regression, independent review, seal assessment).  

Only after those gates should any discussion of runtime placement occur.
