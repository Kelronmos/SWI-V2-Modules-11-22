# SWI Module Completion Contract

**Status:** Common record template  
**Purpose:** Stop modules inventing private interpretations of authority.

## Required fields (every remaining module)

| Field | Content |
|-------|---------|
| Module | Identifier |
| Purpose | One-paragraph purpose |
| Inputs | Exact inputs |
| Outputs | Exact outputs |
| Authority | What authority it consumes / produces (if any) |
| Dependencies | Typed (see DEPENDENCY_GRAPH_MODEL) |
| Permitted transitions | Explicit list |
| Forbidden transitions | Explicit list |
| Evidence produced | What evidence objects, what they attest |
| Failure state | Behaviour on failure |
| HALT behaviour | How HALT is entered / remains |
| Runtime boundary | What is in / out of runtime scope |
| Tests | Unit, negative, adversarial, integration |
| Known limitations | Open list |
| Seal criteria | Module-specific; empty until defined |

## Completion sequence (per module)

```text
01 Contract
02 Threat model
03 Inputs
04 Outputs
05 Authority
06 Dependencies
07 Binding points
08 State transitions
09 Failure states
10 HALT behaviour
11 Evidence
12 Runtime interface
13 Unit tests
14 Negative tests
15 Adversarial tests
16 Integration tests
17 Replay
18 Regression
19 Documentation
20 Independent audit
21 Seal (own criteria only)
```

No module receives a weaker evidence standard because an earlier module passed.

## Explicit non-claims

- Completing this template does **not** seal the module.  
- Registry presence does **not** equal implementation.  
- PRE-CONSEQUENCES is not a module under this contract.
