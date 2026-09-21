# SWI — Remaining Path to Runtime

**Status:** Architectural programme — **NOT AUTHORIZED FOR RUNTIME IMPLEMENTATION** until Runtime Entry Gate passes.  
**Date:** 2026-09-21  
**Baseline reference:** LAW-TRUTH-BOUNDARY-01 + PR-009 Level-3 evidence  

## Path

```text
CURRENT TESTED MODULES
      ↓
CONTRACT FREEZE
      ↓
DEPENDENCY / AUTHORITY MAP
      ↓
BINDING MODEL
      ↓
BINDING IMPLEMENTATION
      ↓
EXECUTION KERNEL
      ↓
RUNTIME ORCHESTRATION
      ↓
EVIDENCE / CONTINUITY
      ↓
ADVERSARIAL RUNTIME TESTING
      ↓
INDEPENDENT AUDIT
      ↓
SWI RUNTIME SEAL
```

## Critical distinctions (non-negotiable)

| Concept | Meaning |
|---------|---------|
| **Binding** | What is *allowed to connect* to what, under which contract and authority |
| **Execution** | The actual performance of an operation |
| **Admission** | May this request enter the workflow? |
| **Authority** | What authority exists for this context? |
| **Evidence** | What actually happened (integrity / provenance) |
| **Continuity** | Can the workflow legitimately continue from this state? |

**Binding ≠ Execution.**  
**Evidence ≠ Authority.**  
**A successful earlier transition does not automatically authorize the next.**

## What this document does *not* authorize

- Runtime kernel implementation  
- PRE-CONSEQUENCES runtime  
- Automatic M11 or M12–M22 seals  
- Process-wide enforcement claims beyond current experimental Level-3 evidence  

See also:

- `RUNTIME_ENTRY_GATE.md`
- `BINDING_CONTRACT.md`
- `DEPENDENCY_GRAPH_MODEL.md`
- `MODULE_COMPLETION_CONTRACT.md`
