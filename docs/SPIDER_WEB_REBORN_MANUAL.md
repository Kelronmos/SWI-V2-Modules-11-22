# SWI Spider Web Reborn

**Full Implementation, Verification and Control Manual**

| Field | Value |
|-------|-------|
| **Document** | `docs/SPIDER_WEB_REBORN_MANUAL.md` |
| **System** | Structured Workflow Intelligence (SWI) V2 |
| **Status** | Specification / implementation guide |
| **Baseline** | `dbaee4fc7e7ecd0b369eb8036e5fd6f2564bbf50` |
| **Verification baseline** | SWI V2 Verification Run #186 — successful |

---

## 1. Purpose

Spider Web Reborn defines the controlled relationship between SWI components.

The objective is not merely to connect modules.

The objective is to make every important connection:

- typed;
- attributable;
- dependency-aware;
- evidence-aware;
- authority-aware;
- verifiable;
- reproducible;
- auditable;
- explicitly bounded.

The Spider Web is therefore a controlled graph of nodes and edges, not an unrestricted execution network.

Its governing principle is:

> Every connection must have a defined meaning, defined prerequisites, defined authority, defined failure behavior, and verifiable evidence.

The central workflow remains:

```text
DATA → EVIDENCE → ADMISSION → AUTHORIZATION → ACTION
```

The reverse direction is not assumed.

---

## 2. Non-Claims

This document is a **specification and implementation guide**.

By itself it does **not**:

- implement Spider Web Reborn;
- modify executable SWI behavior;
- seal any module;
- authorize execution;
- authorize production deployment;
- establish human authority;
- convert test success into authorization;
- convert signatures into authority;
- establish production safety;
- establish completion of any implementation requirement.

The existing green CI baseline remains evidence about the tests actually executed.
It is **not** evidence that Spider Web Reborn has been implemented.

Therefore:

```text
Specification  ≠  implementation
Implementation ≠  verification
Verification   ≠  authorization
Authorization  ≠  production execution
```

Additional mandatory distinctions:

```text
DOCUMENTED  ≠  IMPLEMENTED
IMPLEMENTED ≠  TESTED
TESTED      ≠  VERIFIED
VERIFIED    ≠  SEALED
SEALED      ≠  AUTHORIZED
AUTHORIZED  ≠  EXECUTED
```

---

## 3. Governing SWI Doctrine

The following distinctions must remain explicit throughout implementation.

```text
DATA
  ≠
EVIDENCE
  ≠
ADMISSION
  ≠
AUTHORIZATION
  ≠
ACTION
```

Additional controls:

```text
TESTED          ≠  SEALED
SIGNATURE       ≠  TRUTH
SIGNATURE       ≠  AUTHORITY
CERTIFICATE     ≠  HUMAN AUTHORIZATION
OBSERVATION     ≠  EXECUTION
SIMULATION      ≠  PRODUCTION PROOF
CI GREEN        ≠  PRODUCTION AUTHORIZATION
CA_GREEN        ≠  SWI_AUTHORIZED
```

No implementation may collapse these states.

A technical artifact **MUST NOT** silently acquire a stronger status.

---

## 4. Spider Web Model

The system is represented as a controlled graph:

```text
                 ┌───────────────┐
                 │     NODE      │
                 └───────┬───────┘
                         │
                       EDGE
                         │
                         ▼
                 ┌───────────────┐
                 │     NODE      │
                 └───────┬───────┘
                         │
                     EVIDENCE
                         │
                         ▼
                 ┌───────────────┐
                 │   VERIFIER    │
                 └───────┬───────┘
                         │
                    AUTHORITY
                         │
                         ▼
                 ┌───────────────┐
                 │   AUTH GATE   │
                 └───────┬───────┘
                         │
                         ▼
                      ACTION
```

Around the core sits the defensive web:

```text
┌──────── SECURITY ────────┐
│                          │
│  GOVERNANCE ─ SWI KERNEL ─ SAFETY
│                          │
└────── HUMAN CONTROL ─────┘
```

The graph must never imply that a path exists merely because two nodes can technically communicate.

A connection exists only when its edge contract permits it.

---

## 5. Node Definition

Every Spider Web node must have a machine-readable identity.

Minimum conceptual schema:

```yaml
node_id:
node_type:
version:
status:
owner:
inputs:
outputs:
dependencies:
authority_requirements:
verification_requirements:
provenance:
failure_policy:
```

### 5.1 node_id

Must uniquely identify the node.

Requirements:

- deterministic;
- stable;
- collision-resistant within the registry;
- never inferred from display names.

Example: `SWI.M11.MEMORY`

### 5.2 node_type

Node types must come from a controlled registry.

Example categories:

`TOKEN` · `IDENTIFIER` · `REGISTRY` · `VALIDATOR` · `EVIDENCE` · `ADMISSION` · `AUTHORIZATION` · `VERIFIER` · `OBSERVER` · `EXECUTOR` · `POLICY` · `LAW` · `GOVERNANCE` · `SAFETY`

Unknown node types must not silently default to a generic type.

### 5.3 Node Status

Status must be explicit. Recommended controlled values:

`DEFINED` · `IMPLEMENTED` · `TESTED` · `VERIFIED` · `SEALED` · `BLOCKED` · `REJECTED` · `DEPRECATED`

The implementation must not automatically promote:

```text
DEFINED → SEALED
TESTED  → AUTHORIZED
```

---

## 6. Edge Definition

An edge represents a permitted relationship between two nodes.

Minimum schema:

```yaml
edge_id:
source:
destination:
relationship_type:
preconditions:
required_evidence:
required_authority:
verification_state:
failure_behavior:
audit_record:
```

An edge is **not** equivalent to a function call.

An edge answers:

1. Who is connecting?
2. To whom?
3. Why?
4. Under what conditions?
5. With what evidence?
6. Under whose authority?
7. What verification is required?
8. What happens if the conditions fail?

An edge **MUST NOT** exist merely because two components can technically communicate.

---

## 7. Edge Types

Edge relationships must be typed.

Examples:

`DEPENDS_ON` · `PRODUCES` · `CONSUMES` · `VALIDATES` · `OBSERVES` · `PROVES` · `ADJUDICATES` · `ADMITS` · `AUTHORIZES` · `EXECUTES` · `REJECTS` · `BLOCKS` · `REPORTS` · `REPLAYS`

A node must not use an unrestricted generic relationship such as `CONNECTED_TO` when the actual relationship has a more precise semantic meaning.

---

## 8. Dependency Graph

Every node and edge must declare dependencies.

Example chain:

```text
TOKEN
  ↓
IDENTIFIER
  ↓
REGISTRY
  ↓
VALIDATION
  ↓
EVIDENCE
  ↓
ADMISSION
  ↓
AUTHORIZATION
  ↓
ACTION
```

Dependency resolution must be deterministic.

If dependency A requires B, then A cannot become operationally valid while B is unresolved.

Possible dependency results: `SATISFIED` · `MISSING` · `INVALID` · `BLOCKED`

A missing dependency must prevent dependent execution.

---

## 9. Typed Registry Architecture

Registries must be separate from the objects they index.

The registry provides controlled lookup.

Conceptually: `Registry[T]` where T is a defined registry member type.

Example registries:

- `IdentifierRegistry`
- `NodeRegistry`
- `EdgeRegistry`
- `ReservedWordRegistry`
- `ProtectedNameRegistry`
- `TokenCategoryRegistry`
- `OperatorRegistry`
- `LiteralRegistry`

---

## 10. Registry Membership

Registry membership must be typed.

An item belongs to a registry only when:

```text
item.type ∈ registry.accepted_types
```

Membership must **not** be inferred from:

- string similarity;
- naming convention alone;
- location in a folder;
- user intent;
- arbitrary metadata;
- successful parsing.

Duplicate node identifiers **MUST** be rejected.
Unknown node types **MUST** produce a registry error.

---

## 11. Lookup Semantics

Every lookup must distinguish:

| Result | Meaning |
|--------|---------|
| **SUCCESS / FOUND** | The requested item exists and satisfies registry constraints |
| **MISS** | The lookup operation executed correctly, but no matching item exists |
| **ERROR** | The lookup operation itself could not be correctly performed |

A miss is **not** an implementation failure.

Examples of ERROR:

- malformed query;
- invalid registry;
- corrupted registry;
- invalid type;
- unavailable registry;
- internal registry failure.

A miss must never be converted into an error merely because the caller expected the item to exist.

These **MUST NOT** collapse into the same diagnostic.

---

## 12. Reserved Words

Reserved words are language-level identifiers that cannot be used as ordinary user-defined identifiers.

The reserved-word registry must be machine-readable and define:

```yaml
word:
category:
language_version:
scope:
reason:
diagnostic_code:
```

Example:

```yaml
reserved_words:
  - if
  - else
  - while
  - return
  - import
  - class
```

---

## 13. Protected Names

Protected names are **distinct** from reserved words.

A protected name may be technically syntactically valid but unavailable for a particular implementation purpose.

Examples may include:

- internal namespace names
- system identifiers
- kernel identifiers
- security-critical names
- runtime-managed names

Therefore:

```text
RESERVED ≠ PROTECTED
```

The implementation **MUST** maintain separate registries.

The implementation **MUST NOT** treat these registries as interchangeable.

---

## 14. Operators, Literals and Token Categories

Operators and literals must not be incorrectly inserted into identifier registries.

Token categories must remain separate from registries.

Conceptual structure:

```text
TOKEN CATEGORY
     │
     ├── IDENTIFIER
     ├── OPERATOR
     ├── LITERAL
     ├── KEYWORD / RESERVED_WORD
     └── DELIMITER
```

Registries then manage the appropriate members.

A token category describes **what something is**.
A registry describes **which controlled members are recognized**.

```text
CATEGORY ≠ REGISTRY
```

---

## 15. Diagnostic Architecture

SWI must distinguish between:

**Implementation diagnostics** — designed for developers, maintainers, test systems, verification tooling, and CI. These may contain detailed internal information.

**Learner-facing diagnostics** — designed for students, users, educators, and non-technical operators. They must be understandable, deterministic, actionable, non-leaking, and appropriately scoped.

Internal implementation details must not automatically leak into learner-facing messages.

Every diagnostic requires:

```yaml
code:
class:
severity:
message:
source:
resolution:
```

---

## 16. Structured Failure Object

Failures must be machine-readable.

Conceptual schema:

```yaml
failure_id:
failure_class:
code:
severity:
source_node:
source_edge:
message:
  learner:
  implementation:
cause:
evidence:
dependency_state:
suppressed_descendants:
resolution:
```

A failure must identify the earliest meaningful cause rather than merely reporting downstream symptoms.

---

## 17. Deterministic Failure Selection

When multiple failures occur, SWI **MUST** select the primary failure deterministically.

Selection must **not** depend on:

- dictionary iteration order;
- thread timing;
- random ordering;
- filesystem ordering;
- nondeterministic traversal;
- message arrival order;
- message length.

Conceptual precedence model:

1. Invalid request / Structural failure
2. Dependency failure
3. Type/category failure
4. Registry failure
5. Validation failure
6. Evidence failure
7. Admission failure
8. Authorization failure
9. Execution failure
10. Descendant / suppressed failure

The exact precedence table **MUST** be version-controlled and maintained as a controlled specification.

---

## 18. Primary Failure Algorithm

Conceptual implementation:

```text
collect failures
    ↓
normalize failures
    ↓
remove duplicates
    ↓
classify failure classes
    ↓
resolve dependency ancestry
    ↓
identify root candidates
    ↓
apply deterministic precedence
    ↓
apply stable tie-breaker
    ↓
select primary failure
    ↓
mark descendants as suppressed where appropriate
    ↓
emit primary + suppressed failures
```

The algorithm must produce the same result for the same input state.

---

## 19. Suppressed-Descendant Detection

A descendant failure must not be presented as an independent root cause when its execution path was already invalidated by an upstream failure.

Example:

```text
A fails
 ↓
B cannot execute
 ↓
C cannot execute
```

Report:

```text
PRIMARY:   A
SUPPRESSED: B, C
```

rather than presenting B and C as independent failures without causal relationship.

Suppression does **not** mean deletion.

Suppressed failures must remain available for implementation diagnostics and audit where appropriate.

---

## 20. Evidence Model

Evidence must be explicit.

Minimum conceptual evidence record:

```yaml
evidence_id:
subject:
source:
content_hash:
created_at:
collector:
method:
provenance:
scope:
verification_state:
reproduction_reference:
```

Evidence must answer: *What exactly is being claimed, and what supports that claim?*

Evidence must be bound to its subject. Evidence from one subject cannot silently prove another.

Possible evidence states: `VALID` · `INVALID` · `INCOMPLETE` · `STALE` · `CONFLICTING` · `UNVERIFIED`

---

## 21. Evidence vs Admission

Evidence does **not** automatically admit an object into a workflow.

```text
EVIDENCE
    ↓
ADMISSION DECISION
```

Admission requires its own contract.

---

## 22. ReturnGate

ReturnGate controls ADMIT / REJECT boundaries.

```text
request
 ↓
evaluate
 ↓
ADMIT ─────────→ next permitted state
   │
REJECT
   ↓
STOP / HANDLER
```

A rejection **must not** be silently ignored.

The caller must either:

1. handle the rejection according to contract; or
2. remain blocked.

Caller-ignore-REJECT behavior **must** be explicitly tested as a security/control failure.

---

## 23. Authorization Boundary

Authorization must be separate from verification.

| Question | Domain |
|----------|--------|
| Has the required condition been demonstrated? | Verification |
| Has an authorized human or authority mechanism permitted the action? | Authorization |

```text
VERIFIED ≠ AUTHORIZED
```

An implementation must never infer authorization from:

- test success;
- cryptographic signature alone;
- CI success;
- certificate validity;
- model confidence;
- automated recommendation.

---

## 24. Human Authority

Where an action requires human authority, the authority record must identify:

```yaml
authority_id:
authority_type:
issuer:
subject:
scope:
decision:
timestamp:
expiration:
evidence_reference:
verification_reference:
```

The authority must be bound to the action or decision it actually authorizes.

A cryptographic signature may establish integrity or identity according to the applicable mechanism.
It does **not** automatically establish that the signer possessed authority for the action.

An unrelated valid signature must not be treated as authorization.

---

## 25. Observer Boundary

Observers may:

- inspect / measure / analyse / report / produce evidence.

Observers must **not** silently become executors.

```text
OBSERVE → ANALYSE → EVIDENCE
```

does **not** imply:

```text
OBSERVE → EXECUTE
```

The observer boundary must be adversarially tested.

---

## 26. Common Sense Boundary

The Common Sense layer may:

`MONITOR` · `ANALYSE` · `IDENTIFY` · `EXPLAIN` · `PRODUCE EVIDENCE`

It must **not** independently:

`EXECUTE` · `PROMOTE` · `SEAL` · `AUTHORIZE`

unless those capabilities have been explicitly and separately authorized by the system contract.

---

## 27. True Zero

True Zero is the safe baseline.

When required conditions are absent:

```text
NO EVIDENCE      →  NO ADMISSION
NO ADMISSION     →  NO AUTHORIZATION
NO AUTHORIZATION →  NO ACTION
```

The default must be non-execution.

True Zero must not be bypassed because:

- a prediction appears plausible;
- a test passes;
- a certificate exists;
- an automated system recommends execution;
- a previous action was authorized;
- an upstream node assumes permission.

Default state: **NO AUTHORITY → NO ACTION**

---

## 28. Execution Boundary

Action must be the final controlled transition.

```text
DATA
 ↓
VALIDATION
 ↓
EVIDENCE
 ↓
ADMISSION
 ↓
VERIFICATION
 ↓
AUTHORIZATION
 ↓
ACTION
```

Every transition must have a contract.

The executor must reject incomplete authorization state.

Required condition for `Permit(action)`:

- required conditions are satisfied **AND**
- evidence is sufficient **AND**
- admission is granted **AND**
- verification requirements are satisfied **AND**
- required authority exists **AND**
- security/safety requirements are satisfied

Otherwise: **BLOCK**

---

## 29. Security Web

Security-related controls must remain distinct from general workflow state.

Relevant boundaries include:

`LAW` · `GOVERNANCE` · `POLICY` · `SECURITY` · `HUMAN SAFETY`

A security mechanism may observe, validate, detect, block, report, or preserve evidence.

It must **not** silently convert observation into authorization.

```text
HSM / TPM / Secure Element / PKI / TLS / Certificate / Signature
        ≠
AUTHORIZATION
```

---

## 30. Provenance

Every important state transition must retain provenance.

At minimum:

`WHO` · `WHAT` · `WHEN` · `WHY` · `FROM WHERE` · `UNDER WHICH CONTRACT` · `WITH WHICH EVIDENCE` · `UNDER WHICH AUTHORITY`

Provenance must survive the transition sufficiently to support replay and audit.

---

## 31. Verification Ledger

Every implementation component must have a verification record.

Suggested fields:

```yaml
component:
requirement:
implementation_reference:
test_reference:
test_result:
evidence_reference:
replay_reference:
reproduction_status:
review_status:
seal_status:
authorization_status:
```

This ledger prevents “implemented” from being mistaken for “verified”.

No test should be considered complete merely because a test runner reports PASS.

---

## 32. Replay and Reproduction

### Replay

A verification result should be replayable where technically possible.

Replay must identify: input state, configuration, version, dependencies, test, expected result, actual result, evidence.

A simulation pass must **not** be represented as production execution.

### Reproduction

Reproduction means independently obtaining the same relevant result from the documented state.

Where reproduction fails, the ledger must record `REPRODUCTION_FAILED` rather than silently preserving `VERIFIED`.

---

## 33. Seal Model

A seal is a state transition, not a decorative label.

```text
DEFINED
   ↓
IMPLEMENTED
   ↓
TESTED
   ↓
VERIFIED
   ↓
SEAL REVIEW
   ↓
SEALED
```

Before sealing, dependencies, tests, verification, evidence, reproduction, authority review, and documentation alignment must be satisfied.

If a dependency remains unresolved: **NOT READY** must remain the state.

The system **MUST NOT** seal merely because the latest test suite is green.

A green CI run is one input to seal review, not the entire seal decision.

No implementation may skip the required states.

---

## 34. CI Integration and Interpretation

CI should verify at least:

- unit tests · integration tests · registry consistency · schema validation
- diagnostic determinism · dependency completeness · evidence references
- replay · security boundaries · documentation claims · seal conditions

**Mandatory rule:**

> CI GREEN verifies only the scope actually executed by CI.

Therefore CI GREEN may support `TESTED` or (where the verification contract permits) `VERIFIED`, but does **not** automatically establish `SEALED`, `AUTHORIZED`, or `PRODUCTION READY`.

---

## 35. Adversarial Testing

Spider Web Reborn should deliberately attack its own connections.

Minimum test categories:

| Category | Examples |
|----------|----------|
| Registry | unknown / duplicate node or edge; wrong registry; wrong token category |
| Token / Identifier | reserved-word collision; protected-name collision; category mismatch |
| Graph | invalid relationship; dependency bypass; cycle; orphan node |
| Diagnostic | multiple failures; failure-order manipulation; descendant masquerading as root; nondeterministic ordering |
| Evidence | missing / altered / stale / wrong subject / wrong provenance; replay mismatch |
| Admission | forced ADMIT; ignored REJECT; missing precondition |
| Authority | missing / expired / wrong scope / wrong subject; signature or certificate substitution |
| Execution | execute from VERIFIED or TESTED; execute without ADMISSION or AUTHORIZATION; execute after REJECT or authority expiry |
| Observer / Security | observer attempts execution; analysis attempts promotion; certificate attempts authorization |

Each test should produce a deterministic expected result.

---

## 36. Implementation Order

Implementation **must** proceed in dependency order.

```text
SPECIFICATION
    ↓
SCHEMA
    ↓
REGISTRIES
    ↓
GRAPH
    ↓
DIAGNOSTICS
    ↓
EVIDENCE
    ↓
ADMISSION
    ↓
VERIFICATION
    ↓
AUTHORITY
    ↓
SECURITY / SAFETY
    ↓
EXECUTION BOUNDARY
    ↓
INTEGRATION
    ↓
ADVERSARIAL VERIFICATION
    ↓
SEAL REVIEW
```

**Never** implement first and decide the contract afterward.

### Phase summary

| Phase | Focus |
|-------|-------|
| 1 — Foundations | Token model, identifier rules, reserved-word / protected-name registries, token-category model |
| 2 — Registries | Node registry, edge registry, typed lookup, lookup errors / misses |
| 3 — Diagnostics | Failure object, taxonomy, learner / implementation diagnostics, precedence, suppressed-descendant detection |
| 4 — Workflow controls | Validation, evidence, admission, ReturnGate, authorization, action boundary |
| 5 — Verification | Test ledger, replay, evidence binding, reproduction, seal criteria |
| 6 — Security | Observer boundary, Common Sense / SADU controls, security / authority boundary, adversarial tests |
| 7 — Integration | CI, full regression, cross-node verification, documentation verification, seal-readiness review |

---

## 37. Machine-Readable Status

Use explicit states. Do not overload one status to represent multiple meanings.

```text
DRAFT · IMPLEMENTING · TESTING · FAILED · VERIFIED · BLOCKED
AWAITING_EVIDENCE · AWAITING_CI · AWAITING_AUTHORITY
NOT_READY · SEALED
```

```text
VERIFIED  ≠  AUTHORIZED
AUTHORIZED ≠  EXECUTED
EXECUTED  ≠  SEALED
```

---

## 38. Definition of Done

A Spider Web component is implementation-complete only when:

- [ ] Defined
- [ ] Registered
- [ ] Typed
- [ ] Connected through explicit edges
- [ ] Dependencies identified
- [ ] Tests implemented
- [ ] Negative tests implemented
- [ ] Failure behavior defined
- [ ] Diagnostics verified
- [ ] Evidence recorded
- [ ] Replay possible
- [ ] Reproduction possible
- [ ] CI verified where applicable
- [ ] Authority boundary reviewed
- [ ] Seal impact determined

Completion of code alone is insufficient.

---

## 39. Current Baseline

At the time this document is introduced:

| Item | Value |
|------|-------|
| **HEAD** | `dbaee4fc7e7ecd0b369eb8036e5fd6f2564bbf50` |
| SWI V2 Verification | #186 = SUCCESS |
| Python 3.10 / 3.11 / 3.12 | SUCCESS |
| Full suite | PASS |
| verify.sh on 3.12 | PASS |
| pre-R boundary | #73 = SUCCESS |
| two-checkout-travel | #172 = SUCCESS |

This baseline must be treated as historical verification of the **existing** repository state.
It does **not** establish Spider Web implementation status.

---

## 40. Explicit Current State

Until implementation and verification occur:

| Item | State |
|------|-------|
| Spider Web specification | **DEFINED** (by this document) |
| Spider Web implementation | **NOT ESTABLISHED BY THIS DOCUMENT** |
| Spider Web verification | **NOT ESTABLISHED BY THIS DOCUMENT** |
| Spider Web seal | **NOT GRANTED** |
| Spider Web authorization | **NOT GRANTED** |
| Production execution | **NOT AUTHORIZED** |
| M11 seal status | Independently governed (unchanged by this document) |

---

## 41. Final Control Principle

The Spider Web Reborn is not intended to make SWI execute more freely.

It is intended to make unauthorized or unsupported transitions harder to hide.

The system should make it possible to answer:

- What happened?
- Why did it happen?
- Which node caused it?
- Which edge permitted it?
- What evidence supported it?
- What dependency was required?
- What authority permitted it?
- What verification established it?
- Can it be reproduced?
- Who authorized it?
- What happens when any requirement is missing?

The central principle is:

> No evidence → no promotion.  
> No verified path → no execution.  
> No authority → no authorization.  
> No authorization → no action.

And:

> A connected web is not enough.  
> Every connection must be accountable.
