SWI Distributed Node Isolation & Rebuild Manual

Project: Structured Workflow Intelligence (SWI)
Scope: SWI V1, SWI V2 and future module versions
Purpose: Rebuild, test and operate SWI modules across independent computers/nodes while preventing unauthorized module-to-node or module-to-resource access.

---

1. Core Principle

SWI modules may execute on separate computers at the same time.

However:

«A module must never be allowed to pull information from a node, resource, process, filesystem location, service or module that it has not been explicitly authorized to access.»

The existence of a network connection is not authorization.

The ability to discover a node is not authorization.

The possession of an identifier is not authorization.

The successful execution of another module is not authorization.

The system must therefore separate:

Discovery → Identity → Authorization → Access → Evidence

These are different operations and must not be silently combined.

---

2. Target Architecture

A distributed SWI deployment should conceptually look like this:

                    SWI WORKFLOW
                         |
          +--------------+--------------+
          |              |              |
        Module A       Module B       Module C
          |              |              |
        Node A         Node B         Node C
          |              |              |
     Local resources Local resources Local resources
          |              |              |
          +--------------+--------------+
                         |
                  Contract Boundary
                         |
                  Evidence Envelope
                         |
                  Continuity / M11

There should be no implicit mesh of unrestricted access:

M02 ---> Node B    DENY
M05 ---> Node C    DENY
M06 ---> Node A    DENY

unless the workflow contract explicitly authorizes that relationship.

---

3. Node Independence

Every node must be capable of rebuilding SWI locally.

A node should not depend on another node merely to:

- install dependencies;
- discover its hardware;
- establish its identity;
- execute its assigned module;
- generate local evidence;
- run local tests;
- verify its local integrity.

The initial rebuild should therefore be possible from a clean computer using the repository and documented instructions.

---

4. Hardware Grounding

SWI should distinguish between:

4.1 Hardware facts

Examples:

- operating-system family;
- operating-system version;
- CPU architecture;
- processor information;
- available memory;
- machine/runtime architecture;
- Python/runtime version;
- filesystem/runtime characteristics relevant to execution.

4.2 Application data

Examples:

- workflow inputs;
- user information;
- documents;
- credentials;
- module outputs;
- evidence payloads.

Hardware discovery must not automatically expose application data.

A module may know:

Node architecture = x86_64
OS = Linux
Runtime = Python 3.x

without being granted:

/home/user/private_document.pdf
database credentials
another module's state
another node's memory
another node's filesystem

---

5. Hardware Discovery Rule

Hardware/system discovery is for local execution grounding and diagnostics.

It is not an authorization mechanism.

Do not use:

"Node has CPU X, therefore M02 may access it."

Use:

Node identity
      +
Module identity
      +
Workflow identity
      +
Resource
      +
Operation
      +
Explicit authorization
      =
Access decision

---

6. Local Node Manifest

Each rebuilt node should generate a local manifest.

Example:

{
  "schema": "swi.node.manifest.v1",
  "node_id": "LOCAL-GENERATED-ID",
  "os_family": "linux",
  "architecture": "x86_64",
  "runtime": "python",
  "runtime_version": "3.x",
  "hardware": {
    "cpu": "local-inventory",
    "memory": "local-inventory"
  },
  "network_access": "not-authorized-by-discovery",
  "generated_at": "LOCAL-TIMESTAMP"
}

The exact fields should be deliberately minimized.

Do not place passwords, private keys, access tokens or unnecessary personal information in this manifest.

---

7. Node Identity

A node should have an explicit identifier.

The identifier is an identity reference, not an access credential.

For example:

NODE-A
NODE-B
NODE-C

or a generated UUID.

Do not make:

hostname == authorization

or:

IP address == authorization

A node can change its IP address.

A hostname can be spoofed or duplicated.

Authorization must therefore be independently verified.

---

8. Module Identity

Every SWI module participating in distributed execution should have an explicit module identity.

Example:

M02
M05
M06
M11

The access layer should be able to answer:

WHO is requesting?
WHAT resource is requested?
WHAT operation is requested?
WHY is it requested?
WHICH workflow does it belong to?
IS that relationship currently authorized?

---

9. Resource-Level Authorization

Authorization must be narrower than node-level authorization.

Bad:

M02 → Node B → EVERYTHING

Better:

M02 → Node B → Resource X → READ

Better still:

M02
 ↓
Workflow W123
 ↓
Resource X
 ↓
READ
 ↓
valid until condition/time

This prevents accidental privilege expansion.

---

10. Access Decision

Every cross-node request should produce one of:

ALLOW
DENY
HALT

Suggested semantics:

ALLOW

The request matches a valid authorization.

DENY

The request is outside the module's permitted boundary.

HALT

The system cannot safely determine whether access is permitted.

Examples:

- malformed authorization;
- invalid integrity;
- contradictory policy;
- missing required identity;
- corrupted evidence;
- ambiguous workflow state.

When authorization cannot be safely established:

«Do not guess. Halt.»

---

11. No Direct Node Pulling

A module must not be able to arbitrarily query another node.

Avoid designs such as:

requests.get("http://node-b/data")

simply because the address is reachable.

Instead:

Module
  ↓
Access Boundary
  ↓
Authorization Check
  ↓
Resource Contract
  ↓
Node
  ↓
Minimum permitted response

The boundary becomes the enforcement point.

---

12. Minimum-Data Response

Even an authorized request should receive only the information specified by its contract.

Example:

Requested:
M05 → Node B → PII evidence → READ

Permitted:
name_hash
classification
evidence_reference
integrity_reference

Not:

entire database
entire filesystem
all node state
all user records

This creates a second protection layer:

Authorization controls whether information can be accessed.

Data minimization controls how much information is returned.

---

13. V1 Requirement

For SWI V1, do not introduce hidden V2 dependencies.

V1 should continue to operate according to its existing boundaries.

The new node-isolation mechanism should be implemented as a clearly defined boundary around execution rather than silently importing V2 internals.

Conceptually:

V1 Module
   ↓
V1 contract
   ↓
Node Access Boundary
   ↓
Authorized local/remote resource

Do not turn this into:

V1 → V2 internal implementation

unless a future contract explicitly defines such a dependency.

---

14. V2 Requirement

V2 should inherit the same principle.

M11 is particularly relevant because distributed execution introduces continuity questions.

M11 should eventually be tested against:

Node A produces evidence
Node B produces evidence
Node C produces evidence
        ↓
Different completion times
        ↓
Continuity boundary
        ↓
Can the evidence be associated with the same valid workflow?

M11 must not assume that simultaneous execution means simultaneous state.

---

15. Concurrency Test

Create a test with:

M02 → Node A
M05 → Node B
M06 → Node C

Start all three independently.

Test:

M02 completes first
M06 completes second
M05 completes third

Then repeat:

M05 completes first
M02 completes second
M06 completes third

The result must not depend incorrectly on execution order.

---

16. Adversarial Node Tests

Every rebuilding environment should test:

Test A — Wrong node

M02 → Node B
Expected: DENY

Test B — Wrong resource

M02 → authorized Node A
      → unauthorized resource
Expected: DENY

Test C — Wrong operation

M02 → Resource X
      → WRITE
      → contract allows READ only
Expected: DENY

Test D — Expired authorization

valid authorization
      ↓
expires
      ↓
request
      ↓
DENY

Test E — Missing authorization

module identity = valid
node identity = valid
authorization = missing
      ↓
HALT or DENY according to contract

Test F — Tampered authorization

authorization altered
      ↓
integrity verification fails
      ↓
HALT

Test G — Node discovery without permission

M02 discovers Node B
      ↓
M02 attempts access
      ↓
DENY

This test is particularly important.

---

17. Hardware Grounding Scripts

Each platform should have a local script.

The scripts should collect only the minimum system information required for rebuild and testing.

They should not automatically transmit the results anywhere.

---

18. Windows CMD

Create:

tools\node_info.cmd

Example:

@echo off
setlocal

echo ==================================
echo SWI LOCAL NODE INFORMATION
echo ==================================

echo.
echo Computer:
hostname

echo.
echo OS:
ver

echo.
echo Architecture:
echo %PROCESSOR_ARCHITECTURE%

echo.
echo Processor:
echo %PROCESSOR_IDENTIFIER%

echo.
echo Python:
where python
python --version 2>nul

echo.
echo Git:
where git
git --version 2>nul

echo.
echo Timestamp:
echo %DATE% %TIME%

echo.
echo ==================================
echo LOCAL ONLY - NOT AN AUTHORIZATION
echo ==================================

endlocal

This is a diagnostic inventory only.

---

19. Windows BAT

Create:

tools\rebuild_swi.bat

Example:

@echo off
setlocal enabledelayedexpansion

echo ==================================
echo SWI LOCAL REBUILD
echo ==================================

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found.
    exit /b 1
)

where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git was not found.
    exit /b 1
)

echo Python:
python --version

echo Git:
git --version

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip

if exist requirements.txt (
    python -m pip install -r requirements.txt
)

echo.
echo Running tests...

python -m pytest

if errorlevel 1 (
    echo.
    echo SWI REBUILD/TEST FAILED
    exit /b 1
)

echo.
echo SWI REBUILD/TEST PASSED

endlocal

The repository should adapt the dependency and test commands to its actual implementation rather than assuming these commands are currently valid.

---

20. macOS

Create:

tools/node_info.sh

Example:

#!/usr/bin/env bash
set -euo pipefail

echo "=================================="
echo "SWI LOCAL NODE INFORMATION"
echo "=================================="

echo
echo "Computer:"
hostname

echo
echo "OS:"
sw_vers 2>/dev/null || uname -a

echo
echo "Architecture:"
uname -m

echo
echo "Processor:"
sysctl -n machdep.cpu.brand_string 2>/dev/null || true

echo
echo "Python:"
command -v python3 || true
python3 --version 2>/dev/null || true

echo
echo "Git:"
command -v git || true
git --version 2>/dev/null || true

echo
echo "Timestamp:"
date -Iseconds

echo
echo "=================================="
echo "LOCAL ONLY - NOT AN AUTHORIZATION"
echo "=================================="

Make executable:

chmod +x tools/node_info.sh

---

21. Linux

The same shell script can be used on most Linux systems:

./tools/node_info.sh

For additional local information:

uname -a
cat /etc/os-release
uname -m
python3 --version
git --version

Avoid making "/proc", "/sys", filesystem scans or hardware databases automatically available to SWI modules.

The operating system may expose information to the diagnostic script, but that does not mean every module should receive that information.

---

22. macOS/Linux Rebuild

Create:

tools/rebuild_swi.sh

Example:

#!/usr/bin/env bash
set -euo pipefail

echo "=================================="
echo "SWI LOCAL REBUILD"
echo "=================================="

command -v python3 >/dev/null 2>&1 || {
    echo "ERROR: Python 3 not found."
    exit 1
}

command -v git >/dev/null 2>&1 || {
    echo "ERROR: Git not found."
    exit 1
}

echo "Python:"
python3 --version

echo "Git:"
git --version

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

python -m pip install --upgrade pip

if [ -f requirements.txt ]; then
    python -m pip install -r requirements.txt
fi

echo
echo "Running tests..."

python -m pytest

echo
echo "SWI REBUILD/TEST PASSED"

Make executable:

chmod +x tools/rebuild_swi.sh

Run:

./tools/rebuild_swi.sh

---

23. Cross-Platform Entry Point

Where practical, expose a common conceptual interface:

Windows:
tools\rebuild_swi.bat

macOS:
./tools/rebuild_swi.sh

Linux:
./tools/rebuild_swi.sh

The commands may differ internally.

The expected result must not differ.

---

24. Rebuild Procedure

For every SWI repository:

Step 1 — Obtain repository

clone repository

Step 2 — Inspect repository

Confirm:

README
documentation
tests
requirements/dependencies
CI configuration
module boundaries

Step 3 — Identify local platform

Run:

node_info

Step 4 — Create isolated environment

Use:

.venv

or the repository's documented environment mechanism.

Step 5 — Install dependencies

Only documented dependencies should be installed.

Step 6 — Run baseline tests

Do not modify implementation before recording the baseline.

Record:

commit
platform
runtime
test count
failures

Step 7 — Run node-boundary tests

Test authorized and unauthorized requests.

Step 8 — Run concurrency tests

Execute independently assigned modules simultaneously.

Step 9 — Record evidence

Follow:

Claim
→ Implementation
→ Test
→ Result
→ Limitation
→ Next iteration

---

25. Evidence Record

A test result should identify at minimum:

repository
commit
module
node
test
runtime
platform
result
failure/reason
timestamp

Example:

Repository: SWI-V2-Modules-11-22
Module: M11
Node: NODE-B
Test: unauthorized_node_access
Result: DENIED
Runtime: Python 3.x
Platform: Linux x86_64

Do not call this proof of the entire distributed architecture.

It is proof of the specific tested behavior.

---

26. Security Boundary

The following distinction must remain explicit:

Hardware discovery
        ≠
Node identity
        ≠
Authorization
        ≠
Authentication
        ≠
Integrity
        ≠
Workflow continuity

A hardware fingerprint cannot replace authorization.

A hash cannot by itself prove that a module was authorized.

An authenticated node is not automatically authorized for every resource.

A valid evidence envelope does not automatically grant access to unrelated data.

---

27. Fail-Closed Rule

If the system cannot determine whether a request is authorized:

DO NOT:
guess
fallback to unrestricted access
ask the node for everything
use previous authorization indefinitely
silently continue

Instead:

HALT
 ↓
record reason
 ↓
preserve evidence
 ↓
require explicit resolution

---

28. Node Network Model

Future distributed deployments should prefer:

Module
  ↓
Policy / Access Boundary
  ↓
Authenticated Node
  ↓
Authorized Resource
  ↓
Minimum Response

rather than:

Module
  ↓
Network
  ↓
Search every reachable node
  ↓
Pull whatever exists

The latter creates unnecessary information exposure.

---

29. No Discovery-to-Access Escalation

A critical invariant should be added to the SWI test doctrine:

«Node discovery MUST NOT create access rights.»

Test:

discover Node B
      ↓
obtain Node B identifier
      ↓
request unauthorized resource
      ↓
DENY

This should become a regression test.

---

30. No Module-to-Module Implicit Trust

Likewise:

«Successful execution of one SWI module MUST NOT automatically authorize another module to access its state.»

Example:

M02 completed successfully
       ↓
M05 requests M02 private state
       ↓
No authorization
       ↓
DENY

If M05 requires information produced by M02, that information should cross a defined evidence/contract boundary.

---

31. Recommended Access Contract

A future common contract can contain:

{
  "request_id": "...",
  "workflow_id": "...",
  "module_id": "M05",
  "source_node": "NODE-B",
  "target_node": "NODE-A",
  "resource": "RESOURCE-X",
  "operation": "READ",
  "purpose": "DECLARED-WORKFLOW-STEP",
  "authorization": "...",
  "integrity": "...",
  "issued_at": "...",
  "expires_at": "..."
}

This is an architectural proposal.

It should not be represented as an already implemented SWI capability until code and tests establish it.

---

32. What Must Not Be Claimed

Until tested, do not claim:

"SWI is completely isolated."
"SWI prevents all unauthorized access."
"SWI provides complete node security."
"SWI is tamper-proof."
"SWI guarantees distributed security."

Instead state precisely:

"The tested boundary denies the tested unauthorized
module-to-node/resource requests under the documented conditions."

That keeps the implementation aligned with:

Claim → Implementation → Test → Result → Limitation → Next iteration.

---

33. Required Test Matrix

Each supported platform should eventually run:

Test| Windows| macOS| Linux
Local rebuild| ✓| ✓| ✓
Hardware discovery| ✓| ✓| ✓
Baseline module tests| ✓| ✓| ✓
Unauthorized node| ✓| ✓| ✓
Unauthorized resource| ✓| ✓| ✓
Wrong operation| ✓| ✓| ✓
Expired authorization| ✓| ✓| ✓
Tampered authorization| ✓| ✓| ✓
Concurrent execution| ✓| ✓| ✓
Node restart| ✓| ✓| ✓
Duplicate request| ✓| ✓| ✓
Replay attempt| ✓| ✓| ✓
Partial node failure| ✓| ✓| ✓

A checkmark means tested, not automatically passed.

---

34. First Implementation Stage

Do not immediately implement this across all modules.

Start with a small demonstrator:

M02 → Node A
M05 → Node B
M06 → Node C

Implement:

Node identity
Module identity
Resource identity
Access request
ALLOW/DENY
Evidence record

Then test unauthorized access.

Only after this boundary behaves correctly should it be generalized across additional modules.

---

35. Second Stage — Concurrency

Run:

M02 || M05 || M06

on separate nodes.

Introduce:

delay
duplicate
replay
failure
corruption
out-of-order completion

Verify that the access boundary remains enforced independently of execution timing.

---

36. Third Stage — M11

After the local access boundary is independently tested, evaluate its interaction with M11.

Questions:

Can M11 distinguish node identity?
Can M11 distinguish module identity?
Can M11 verify evidence belongs to the expected workflow?
Can a delayed result be rejected safely?
Can a replayed result be detected?
Can a missing authorization cause HALT?
Can a node restart without silently inheriting stale access?

These should become explicit M11 tests rather than assumptions.

---

37. Repository Layout

A possible future structure:

SWI-V1-Module-1-10/
│
├── modules/
├── tests/
├── docs/
├── tools/
│   ├── node_info.cmd
│   ├── rebuild_swi.bat
│   ├── node_info.sh
│   └── rebuild_swi.sh
│
├── contracts/
│   └── node_access/
│
└── .github/
    └── workflows/

V2 can use the same conceptual structure while maintaining its existing repository boundary.

---

38. CI vs Real Hardware

CI validates reproducible software behavior.

It does not automatically prove behavior on every physical machine.

Therefore distinguish:

CI evidence

from:

physical-node evidence

A successful GitHub Actions run should not be described as proof that every supported hardware environment behaves identically.

---

39. Local Hardware Evidence

A local rebuild can record:

platform
architecture
runtime
CPU information
memory information
repository commit
test result

But only record fields necessary for the purpose.

Avoid turning node manifests into unnecessary surveillance records.

The objective is:

«Ground execution in the environment without turning environment discovery into data collection.»

---

40. Final SWI Invariant

The proposed cross-version invariant is:

«Every SWI module operates within an explicit information boundary. A module may access only the resources authorized for its identity, workflow, operation and current state. Node discovery, network reachability, hardware identity, or successful execution of another module must never independently grant access. When authorization or continuity cannot be safely established, the system must deny or halt rather than infer permission.»

This should be treated as a proposed architectural invariant until implemented and tested.

---

41. Rebuild Philosophy

Every new computer should answer the same basic questions:

What am I running?
Which SWI commit am I running?
Which module am I running?
What node am I?
What resources can I access?
Why am I allowed to access them?
What evidence proves that access?
What happens when authorization is missing?
What happens when the node fails?
What happens when another module finishes first?

If the answer to an authorization question is uncertain:

HALT.

That is preferable to silently expanding the module's access boundary.

---

42. Completion Standard

This feature should not be considered complete because:

scripts exist

or:

modules run on multiple computers

Completion requires:

Implementation
+
cross-platform rebuild
+
authorization contract
+
positive access tests
+
negative access tests
+
concurrency tests
+
failure tests
+
evidence
+
documented limitations

Only then should the corresponding claim be elevated from design to tested behavior.
