# Refusal-First Acceptance Standard (permanent)

**Applies to:** SWI V2 desktop app, browser dashboard, local runtime, public test environments.

**PROVEN:** NO · **SEALED:** NO · **PRODUCTION_AUTHORIZED:** NO  

## Principle

> A system is not governed because it knows when to proceed.  
> It is governed when it knows when it must not proceed, and cannot silently proceed anyway.

## Mandatory dual paths in every workflow demonstration

### PATH A — Permission

- Conditions satisfied  
- Evidence validated  
- Authority established  
- Governing constraints satisfied  
- Evaluator returns PERMITTED  
- Execution remains subject to the **separate** execution gate  

### PATH B — Refusal

- Evidence missing or invalid  
- Authority unknown or forged  
- Context or policy changed  
- Previous decision invalidated  
- Execution blocked  
- Refusal recorded  
- Resume requires fresh validation **and** legitimate authority  

## Dashboard visibility rule

Failures must be **as visible as** successes.

| Runtime outcome | Required display class |
|-----------------|------------------------|
| Valid evaluation | PERMITTED |
| Missing evidence | REFUSED |
| Unknown authority | UNKNOWN — REFUSED |
| Context mismatch | BLOCKED |
| New information (boundary) | PREVIOUS DECISION INVALIDATED |
| Pause active | EXECUTION BLOCKED |
| Unauthorized resume | RESUME REFUSED |
| Integrity failure | SYSTEM HALTED |

Labels are illustrative; the backend must report **actual** reason and state.

## Architectural rule

SWI must demonstrate not only how permission is established, but how **unauthorized consequences are prevented from forming**.

## Anti-patterns (reject)

- Green-only demo dashboards  
- Treating UNKNOWN as allow  
- Auto-resume after pause  
- Second authorization engine in the UI shell  
- Packaging placeholder modules as complete  
- Sacrificing refusal paths for CI green  

## Acceptance checklist (minimum)

- [ ] PATH A demonstrated with recorded evidence  
- [ ] PATH B demonstrated with recorded refusal reason  
- [ ] Resume without authority blocked  
- [ ] New information invalidates prior PASS on affected node  
- [ ] Dashboard shows refusal states without operator digging in logs  
- [ ] Desktop and browser use the same backend spine  
- [ ] Status ceiling not inflated by demo success  
