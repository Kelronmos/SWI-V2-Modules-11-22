SWI V2 Continuation Manual

Distributed Node Authorization & Module Isolation

Repository: SWI-V2-Modules-11-22
Continuation point: M11 / Kernel — TESTED, NOT SEALED
Objective: Establish and test a strict boundary preventing an SWI module from retrieving resources from nodes or modules outside its explicit authorization.

---

1. Continuation Rule

Do not proceed directly to M12.

Before M11 is sealed, introduce a controlled distributed-node authorization experiment.

The objective is not to claim that SWI is universally secure.

The objective is narrower:

«Demonstrate whether an SWI module can be prevented from retrieving an unauthorized resource from another node, while authorized evidence can still cross the defined workflow boundary.»

This must be proven through implementation and tests.

---

2. Current Boundary

The existing V2 direction remains:

V1
 │
 │ Foundation Evidence
 ▼
V2
 │
 ▼
M11 / Kernel
 │
 ├── continuity
 ├── admission
 ├── integrity
 └── workflow state

The new boundary is:

M11 / Kernel
      │
      ▼
Node Access Boundary
      │
 ├────┴─────┐
 ▼          ▼
ALLOW      DENY/HALT

No M12–22 implementation should depend on this work until the contract is actually established.

---

3. New Invariant

Add this proposed invariant to the V2 architecture:

«Node reachability does not constitute authorization. A module may access only the explicitly authorized resource, operation, node and workflow context.»

The following are deliberately different:

DISCOVERED
AUTHENTICATED
AUTHORIZED
ACCESSIBLE
ADMITTED

One state must never silently imply another.

---

4. Threat Model

The first implementation should assume a module may attempt:

wrong node
wrong resource
wrong operation
wrong workflow
expired authorization
missing authorization
replayed authorization
tampered authorization

The system must not depend on the module voluntarily behaving correctly.

The boundary must enforce the restriction.

---

5. Three-Node Test Environment

Build the first test using three independently running nodes.

                 WORKFLOW
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       NODE-A    NODE-B    NODE-C
          │         │         │
         M02       M05       M06

Each node should have its own:

- repository checkout;
- runtime environment;
- process;
- node identity;
- local state;
- test output.

The initial implementation should avoid unnecessary shared filesystem state.

---

6. Hardware Grounding

Every node must be able to establish its local execution environment from the physical/virtual machine on which it runs.

Collect only necessary information such as:

OS
architecture
runtime
Python version
CPU information
memory information
repository commit

This information is for environment grounding and reproducibility.

It is not permission to access another node.

Therefore:

hardware identity ≠ authorization

---

7. Platform Rebuild Requirement

The repository should provide platform-specific entry points.

Recommended:

tools/
    node_info.cmd
    rebuild_swi.bat
    node_info.sh
    rebuild_swi.sh

Windows:

tools\rebuild_swi.bat

macOS/Linux:

./tools/rebuild_swi.sh

The scripts should:

1. verify runtime availability;
2. report the local environment;
3. create an isolated environment where required;
4. install documented dependencies;
5. run the repository tests;
6. return a non-zero failure status when tests fail.

The scripts must not silently download or expose unrelated node data.

(Note: these scripts were already added under tools/ in a prior commit.)

---

8. Node Manifest

Create a minimal local node description.

Conceptual structure:

{
  "schema": "swi.node.manifest.v1",
  "node_id": "NODE-A",
  "platform": "linux",
  "architecture": "x86_64",
  "runtime": "python",
  "runtime_version": "3.x",
  "repository_commit": "COMMIT"
}

The actual implementation should use the repository's established schema conventions.

Do not place credentials in the manifest.

---

9. Module Identity

Every access request must identify the requesting module.

Example:

module_id = M02

A module identity alone is insufficient.

The authorization decision must consider the complete request.

---

10. Resource Identity

Resources must be individually addressable.

Example:

NODE-A
 ├── RESOURCE-A1
 ├── RESOURCE-A2
 └── RESOURCE-A3

Avoid granting:

M02 → NODE-A → EVERYTHING

Prefer:

M02
 ↓
NODE-A
 ↓
RESOURCE-A1
 ↓
READ

---

11. Access Request

Introduce a conceptual access request:

request_id
workflow_id
module_id
source_node
target_node
resource_id
operation
authorization_reference

Example:

{
  "request_id": "REQ-001",
  "workflow_id": "WF-001",
  "module_id": "M02",
  "source_node": "NODE-B",
  "target_node": "NODE-A",
  "resource_id": "RESOURCE-A1",
  "operation": "READ"
}

This is a proposed contract.

Do not describe it as an existing V2 API until implemented.

---

12. Decision Engine

The access boundary produces:

ALLOW
DENY
HALT

ALLOW

All required authorization conditions are satisfied.

DENY

The request is clearly outside the permitted boundary.

HALT

The system cannot safely determine whether the request is valid.

Examples:

missing integrity
ambiguous authorization
corrupted authorization
contradictory workflow state
unknown module identity

The system must not interpret uncertainty as permission.

---

13. First Positive Test

Create an explicitly authorized relationship:

M05
 ↓
NODE-B
 ↓
RESOURCE-B1
 ↓
READ

Expected:

ALLOW

The returned data must be limited to the resource contract.

---

14. First Negative Test

Attempt:

M02
 ↓
NODE-B
 ↓
RESOURCE-B1
 ↓
READ

where M02 has no authorization.

Expected:

DENY

Critically:

Node B may be reachable.

That does not matter.

The request must still be rejected.

This proves the distinction:

network reachability ≠ authorization

---

15. Resource Boundary Test

Authorize:

M02 → NODE-A → RESOURCE-A1

Then request:

M02 → NODE-A → RESOURCE-A2

Expected:

DENY

This verifies that authorization is resource-specific rather than merely node-specific.

---

16. Operation Boundary Test

Authorize:

READ

Attempt:

WRITE

Expected:

DENY

This establishes:

resource authorization ≠ unlimited operation authorization

---

17. Workflow Boundary Test

Authorize M02 under:

WORKFLOW-001

Then replay the same authorization under:

WORKFLOW-002

Expected:

DENY

if workflow binding is part of the contract.

---

18. Expiration Test

Create authorization with a defined validity condition.

After expiration:

request
 ↓
authorization expired
 ↓
DENY

Do not silently reuse stale authorization.

---

19. Tamper Test

Modify the authorization after issuance.

Expected:

integrity verification
       ↓
FAIL
       ↓
HALT

Do not transform an integrity failure into a normal denial if the contract requires the event to be treated as a continuity/security fault.

The exact classification should be defined by implementation.

---

20. Discovery Test

Allow M02 to discover that NODE-B exists.

Then attempt access.

M02
 ↓
discovers NODE-B
 ↓
requests RESOURCE-B1
 ↓
no authorization
 ↓
DENY

This is one of the most important tests in the new work.

Expected invariant:

«Discovery must never escalate privileges.»

---

21. Concurrent Execution

Run:

NODE-A / M02
NODE-B / M05
NODE-C / M06

simultaneously.

Do not require synchronized completion.

Test:

M02 finishes first
M05 finishes first
M06 finishes first

Then test random delays.

The access boundary must remain independent of execution order.

---

22. Partial Failure

Terminate one node.

Example:

NODE-B
   ↓
OFFLINE

Then attempt a request.

The system must not:

fallback to unrestricted access

Instead it should produce the contractually defined:

DENY

or:

HALT

depending on whether the failure is an authorization failure or an unresolved continuity condition.

---

23. Replay Test

Capture a previously valid access request.

After its validity condition is no longer satisfied, replay it.

Expected:

REPLAY
 ↓
NOT ADMITTED

This should be tested independently from the existing M11 replay work.

The distinction is:

evidence replay

versus:

authorization/request replay

Both need explicit tests if both are within scope.

---

24. Duplicate Request

Send the same request twice.

Determine whether the contract requires:

ALLOW + idempotent result

or:

second request = DENY

Do not assume the answer.

Document the intended semantics first.

Then test them.

---

25. Out-of-Order Evidence

Run:

M02 → result A
M05 → result B
M06 → result C

with deliberately different completion times.

Then deliver:

C
A
B

instead of:

A
B
C

M11 should evaluate whether the evidence can still be associated with the correct workflow state.

If the relationship cannot be established safely:

HALT

---

26. Node Restart

Run:

NODE-A
 ↓
authorized workflow
 ↓
process terminates
 ↓
NODE-A restarts

Then test whether stale authorization survives.

The answer must be defined explicitly.

Do not let a restart accidentally produce:

old authorization = automatically trusted forever

---

27. Persistence Interaction

This test is particularly important following the V1 M07 finding.

If M11 or the access boundary persists state, test:

write
 ↓
restart
 ↓
load
 ↓
verify

Then corrupt the stored state:

stored state
 ↓
modify
 ↓
restart
 ↓
verification
 ↓
HALT

Do not assume disk persistence merely because a file exists.

Test the actual behavior.

---

28. Evidence

Every test should produce a precise record.

Minimum fields:

repository
commit
module
node
test
platform
runtime
request
authorization state
result
failure reason
timestamp

Example:

Test:
unauthorized_cross_node_resource

Requester:
M02 / NODE-C

Target:
NODE-A / RESOURCE-A1

Authorization:
NONE

Result:
DENY

---

29. Test Classification

Use:

DESIGNED
IMPLEMENTED
TESTED
PASSED
FAILED
BLOCKED
NOT TESTED

Do not use:

SECURE
FULLY SECURE
PROVEN SAFE

as substitutes for individual test results.

---

30. M11 Seal Gate

Before M11 is sealed, require evidence for:

[ ] local rebuild
[ ] node identity
[ ] module identity
[ ] resource identity
[ ] authorization contract
[ ] authorized access
[ ] unauthorized node access
[ ] unauthorized resource access
[ ] unauthorized operation
[ ] discovery ≠ authorization
[ ] authorization integrity
[ ] authorization expiration
[ ] concurrent nodes
[ ] node failure
[ ] restart
[ ] replay
[ ] duplicate request
[ ] out-of-order evidence

Any item not implemented should remain explicitly marked:

NOT IMPLEMENTED

or:

BLOCKED

---

31. V1/V2 Boundary

This work must not create an accidental dependency:

V2 → V1 internal modules

or:

V1 → V2 implementation

The cross-version relationship remains through the established evidence boundary.

The node authorization mechanism is an execution/access boundary, not a reason to collapse the repository architecture.

---

32. Future Module Expansion

Do not begin M12–M22 merely because the access boundary has been designed.

The sequence remains:

M11
 │
 ├── implement boundary
 ├── test boundary
 ├── adversarial testing
 ├── document limitations
 └── seal decision
          │
          ▼
         M12

M12 should consume an established contract rather than inherit an assumption.

---

33. Required Documentation Language

Until implementation is complete:

«SWI V2 is testing a distributed node-authorization boundary intended to prevent modules from retrieving resources outside their explicit authorization. This is an active engineering boundary and is not yet a claim of complete distributed-system security.»

After implementation, documentation should describe only the behaviors demonstrated by tests.

---

34. Engineering Doctrine

Continue using:

CLAIM
   ↓
IMPLEMENTATION
   ↓
TEST
   ↓
RESULT
   ↓
LIMITATION
   ↓
NEXT ITERATION

For this feature:

CLAIM:
M02 cannot access unauthorized Node-B resource.

IMPLEMENTATION:
Access boundary evaluates module/node/resource/operation authorization.

TEST:
M02 requests unauthorized Node-B resource.

RESULT:
DENY.

LIMITATION:
Only tested configurations/platforms are covered.

NEXT:
Expand node/concurrency/failure coverage.

---

35. First Deliverable

The first continuation PR should therefore be intentionally small.

Deliverable A

node information scripts

Deliverable B

cross-platform rebuild scripts

Deliverable C

node/module/resource identity model

Deliverable D

minimal access contract

Deliverable E

ALLOW / DENY / HALT boundary

Deliverable F

positive + negative tests

Deliverable G

evidence report

Do not implement all 47 modules or attempt a complete distributed architecture in this iteration.

---

36. First Proof Target

The first meaningful result should be extremely simple:

M02 @ NODE-A
        │
        │ requests
        ▼
RESOURCE @ NODE-B
        │
        │ unauthorized
        ▼
      DENY

Then:

M05 @ NODE-B
        │
        │ requests
        ▼
AUTHORIZED RESOURCE @ NODE-B
        │
        ▼
      ALLOW

Then deliberately make the environment hostile:

discover
delay
duplicate
replay
restart
corrupt
disconnect

and determine whether the same boundary still holds.

---

37. Definition of Success

Success is not:

«"SWI can run modules on three computers."»

Success is:

«The tested SWI boundary demonstrably restricts module access according to explicit authorization, remains enforced during concurrent execution and defined failure conditions, and produces evidence sufficient to reproduce exactly what was tested and what remains unproven.»

That is the appropriate continuation point before M11 sealing.
