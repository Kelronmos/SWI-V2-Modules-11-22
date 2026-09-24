# Snyder Compatibility Matrix

**STATUS:** DESIGNED / OPEN  
**EVIDENCE:** None of the six requirements are independently demonstrated as a closed runtime at `f4755891238260ef28393d32c5affb25b4ea1105`.  
**LIMITATIONS:** Green module tests are not Snyder-runtime evidence.  
**NEXT GATE:** Implement one mandatory execution corridor + live authorization gate + ledger precondition, then re-score each row from tests + CI at an exact SHA.

Do not label the repository “Snyder compatible.”

| Requirement | Contract | Implementation | Test | Evidence | Status |
|-------------|----------|----------------|------|----------|--------|
| 1. Mandatory execution path | Mapped in architecture notes | Roadmap / fragments only | Module tests ≠ path-closure | Incomplete | OPEN |
| 2. Structured authority objects | MATH-002 local containment + authority docs | Partial scope/non-escalation | MATH-002 property cases | Local relation only | PARTIAL |
| 3. Live authorization gate | Experimental API path (`enforce` → require_executable) | Experimental | API-level | Does not prove every path | PARTIAL / EXPERIMENTAL |
| 4. Ledger as execution precondition | Integrity chains exist as concepts | Not closed as runtime precondition | Tamper tests ≠ ledger-gate | OPEN | OPEN |
| 5. First-class REFUSE / ESCALATE | REJECT/HALT/PAUSE exist | Not proven non-bypassable | Process-wide bypass unproven | OPEN | PARTIAL |
| 6. Deterministic receipts / replay | Receipt/digest concepts exist | Transition receipts not fully defined | Replay tests within stated limits | Incomplete | PARTIAL |

Anything not independently demonstrated remains **OPEN**.
