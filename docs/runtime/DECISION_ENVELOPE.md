# Decision Envelope Contract (design)

**STATUS:** DESIGNED  
**EVIDENCE:** None — no production runtime issues this envelope.  
**LIMITATIONS:** Specification only.  
**NEXT GATE:** Implement as a data contract with canonical serialization before any execution-capability work.

## Rule

No consequential result leaves SWI without governing context.

`PASS ≠ AUTHORIZED ≠ EXECUTED`  
`APPROVED ≠ EXECUTED`  
`ADMITTED ≠ AUTHORIZED`  
`LAW_RECEIVED ≠ LAW_ENFORCED`  
`signature valid ≠ claim true`

## Envelope (required fields when implemented)

- decision / disposition
- claim
- evidence
- law / policy / governance / ethics
- security / human_safety
- authority / binding
- provenance / limitations
- escalation / execution
- receipt

## Controlled dispositions

PASS, FAIL, BLOCKED, REFUSE, ESCALATE, HALT, APPROVED, AUTHORIZED, EXECUTED, NOT_EXECUTED, REQUIRES_HUMAN_REVIEW, UNKNOWN, CONFLICT, EXPIRED, REVOKED.

UNKNOWN must not become APPROVED.

## Human authorization (when required)

Human ID is bound to request + resource + action + evidence + law + policy.
A boolean `approved=true` is insufficient.
