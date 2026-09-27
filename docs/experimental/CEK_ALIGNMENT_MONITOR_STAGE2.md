# CEK Alignment Monitor — Stage 2

**Classification:** RESEARCH / EXPERIMENTAL  
**Production:** NOT AUTHORIZED  
**Seal:** NO  
**M11:** UNTOUCHED  

---

## Additions

- `provenance.py` — origin / source / input-hash / output-hash / transformation  
- `observation.py` — CEK observation record; `authority_established() ≡ False`  
- `visibility.py` — visibility frontier (KNOWN … UNKNOWN); no interpolation across UNKNOWN  
- `findings.py` — VISIBLE / PARTIALLY_VISIBLE / UNKNOWN / UNTRACEABLE / INVALID / HALTED  
- `replay.py` — deterministic recompute + compare  
- `monitor.py` — facade + `hidden_edge_demo()` / `full_hidden_edge_observation()`  

---

## Hidden-edge demonstration (centrepiece)

```
REQUEST → CONTEXT → EVIDENCE → ADMISSION → [HIDDEN_EDGE] → EXECUTION
```

Result:

- Path visible up to ADMISSION  
- Next edge = UNKNOWN  
- Execution = OBSERVED  
- Authority = NOT ESTABLISHED  

---

## Authority-boundary attacks (must fail)

| Attack                        | Expected |
|-------------------------------|----------|
| UNKNOWN → PERMIT              | REJECTED |
| UNKNOWN → AUTHORITY           | REJECTED |
| UNKNOWN → EXECUTION           | REJECTED |
| EVIDENCE → AUTHORITY          | REJECTED |
| SIGNATURE → AUTHORITY         | REJECTED |
| OBSERVATION → AUTHORITY       | REJECTED |
| STABLE → AUTHORITY            | REJECTED |
| EXECUTION OBSERVED → NEW AUTH | REJECTED |

All enforced by hard-coded `False` returns and absence of execution methods.

---

## Non-claims preserved

No truth oracle, no safety oracle, no legal decision, no production authorization, no seal, no M11 modification.
