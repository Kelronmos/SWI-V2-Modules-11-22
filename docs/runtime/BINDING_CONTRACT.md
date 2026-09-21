# Binding Contract

**Status:** Architectural specification — **NOT IMPLEMENTED**  
**Scope:** Future SWI binding surface  
**Does not grant:** execution, authority manufacture, or PRE-CONSEQUENCES semantics  

## Purpose

Binding answers:

> What is allowed to connect to what, under which contract, with which authority, and under which evidence condition?

Binding establishes a **permitted relationship**.  
**Execution is a later decision.**

## Conceptual shapes (not code)

```text
BindingRequest
    source
    destination
    interface
    authority
    evidence
    constraints
    lifetime

BindingDecision
    BIND | REJECT | HALT
```

`BIND` must never mean `EXECUTE`.

## Invariants (BIND-001 … BIND-010)

| ID | Invariant |
|----|-----------|
| BIND-001 | A module cannot bind to an undeclared interface. |
| BIND-002 | A binding cannot expand authority. |
| BIND-003 | A binding cannot manufacture authority. |
| BIND-004 | Evidence does not become authority merely because it accompanies a binding. |
| BIND-005 | A rejected binding cannot become executable through object conversion. |
| BIND-006 | A HALTED binding remains non-executable. |
| BIND-007 | Changing a material binding property invalidates the binding. |
| BIND-008 | A binding has an identifiable source and destination. |
| BIND-009 | Binding must respect module dependency direction. |
| BIND-010 | Runtime execution requires a valid binding. |

These become tests **before** runtime becomes large.

## Registry (descriptive / control state only)

A Binding Registry answers: what exists, what can connect, version, authority reference, evidence reference, state.

A registry entry saying `ALLOW` must **not** magically grant authority.

## Separation from existing experimental work

| Existing | Relation to Binding |
|----------|---------------------|
| ReturnGate | Admission only — not binding |
| PR-009 | Enforcement of rejection on privileged experimental path — not binding |
| PRE-CONSEQUENCES | Separate architecture — not binding |

## Non-claims

- No binding implementation in this commit  
- No claim that current PR-009 is the binding layer  
- No claim that BIND implies EXECUTE  
