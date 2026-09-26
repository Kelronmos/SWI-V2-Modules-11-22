# SWI Repair & Recovery Checklist

**STATUS:** DESIGN  
**NOT IMPLEMENTED**  
**NOT SEALED**  
**PRODUCTION:** BLOCKED  

**Core Rule:** «Tampered data does not repair itself back into trust.»

---

### 1. Pre-Repair Freeze
- [ ] Freeze affected path / objects
- [ ] Snapshot current state
- [ ] Identify all affected objects and dependency descendants
- [ ] Calculate current integrity hashes
- [ ] Confirm production remains BLOCKED

### 2. Integrity Assessment
- [ ] Run integrity check against trusted expected hashes
- [ ] Record: expected_hash, actual_hash, detected_at, detector, reason
- [ ] Classify result: INTACT or TAMPERED
- [ ] If TAMPERED → proceed to Quarantine (never skip)

### 3. Quarantine (Mandatory on Tamper)
- [ ] Move / copy object into quarantine
- [ ] Create quarantine record (quarantine_id, original_hash, reason, authority_required)
- [ ] Block all execution, authorization, promotion, and evidence use of the object
- [ ] Retain original integrity evidence for audit
- [ ] Confirm object cannot re-enter trusted workflow automatically

### 4. Authority & Escalation Gate
- [ ] Determine whether human authority is required
- [ ] Determine whether escalation is required
- [ ] Record authority requirements (subject, object, scope, issuer, expiration)
- [ ] If authority missing / expired / wrong-scope → BLOCK
- [ ] If escalation required → emit ESCALATION_REQUIRED

### 5. Privacy-Domain Check
- [ ] Identify affected privacy domains (IDENTITY / MEDICAL / EDUCATION / FAMILY / FINANCIAL / EMPLOYMENT / LEGAL / OTHER)
- [ ] Confirm no cross-domain access is inherited
- [ ] Require independent domain authority + purpose + scope for any domain crossing
- [ ] Block any attempt to use one domain’s permission for another

### 6. Repair Authorization
- [ ] Explicit human authority record present and valid
- [ ] Authority bound to the exact object and transition
- [ ] Authority not expired, not revoked, correct issuer and scope
- [ ] Technical signatures / certificates / HSM / TPM / CI green are **not** treated as human authority

### 7. Perform Repair (Only After Authorization)
- [ ] Repair only within authorized scope
- [ ] Recalculate hashes after repair
- [ ] Revalidate structure and dependencies
- [ ] Generate **new** evidence (never reuse old verification as current)
- [ ] Invalidate any previous verification that depended on the old hash / state

### 8. Post-Repair Verification Gates
- [ ] New validation completed
- [ ] New evidence package created
- [ ] New admission performed
- [ ] New verification performed
- [ ] Replay executed and compared
- [ ] Reproduction confirmed
- [ ] Dependency impact re-checked (primary failure + suppressed descendants retained)

### 9. State-Transition Compliance
- [ ] Only explicitly allowed transitions used
- [ ] Forbidden transitions rejected
- [ ] REJECT vs BLOCK vs QUARANTINE correctly distinguished
- [ ] No side-effect mutation on rejected transitions
- [ ] Full transition audit record written

### 10. Evidence & Report
- [ ] Repair report generated
- [ ] Report itself treated as evidence (not authorization)
- [ ] Production decision remains BLOCKED unless separately authorized

### 11. Final Acceptance Gate (Before Any Seal Review)
A repaired component is accepted **only** when all of the following are true:
- [ ] IMPLEMENTED
- [ ] TESTED
- [ ] DEPENDENCIES VERIFIED
- [ ] EVIDENCE VALID + PROVENANCE VALID
- [ ] REPLAYABLE + REPRODUCIBLE
- [ ] AUTHORITY SATISFIED
- [ ] SECURITY CHECK PASSED
- [ ] SAFETY CHECK PASSED
- [ ] DOCUMENTATION ALIGNED

→ Only then is **SEAL REVIEW** permitted (never automatic sealing).

### 12. Master Invariants (Must Never Be Violated)
- [ ] DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
- [ ] TESTED ≠ VERIFIED ≠ SEALED ≠ AUTHORIZED
- [ ] SIGNATURE / CERTIFICATE / CI_GREEN ≠ HUMAN AUTHORITY
- [ ] No silent trust restoration after integrity failure
- [ ] No cross-domain permission inheritance
- [ ] One missing mandatory condition is sufficient to BLOCK action
- [ ] TRUE ZERO → system stops

---

**Default Safe Mode:** Audit only. No automatic mutation.  
**Production Rule:** Remains BLOCKED until independent authorization is obtained.
