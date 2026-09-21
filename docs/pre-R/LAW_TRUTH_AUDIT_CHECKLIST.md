# LAW-TRUTH Audit Checklist

Auditor must be able to answer from the recorded artifacts alone.

## Required package contents

- [ ] baseline SHA (`evidence/pre_r/baseline.sha`)
- [ ] diagnostic evidence record
- [ ] implementation files (core.py, enforcement.py, halt.py)
- [ ] full pre-R test suite + adversarial tests
- [ ] test-result artifacts
- [ ] artifact hashes (SHA-256)
- [ ] limitations register
- [ ] PRE-CONSEQUENCES separation document
- [ ] M11 seal criteria (separate; not satisfied by this phase)

## Questions the auditor must answer

1. What exact claim is being made?  
2. What code implements it?  
3. What tests exercise it?  
4. What is the scope of the tests?  
5. What remains unproven?  
6. Can the critical tests be replayed at the recorded SHA?  
7. Is PRE-CONSEQUENCES coupled to the runtime?  
8. Does any document claim an M11 seal from this evidence?

## Expected answers (as of this phase)

1. REJECT/HALT cannot reach privileged_action through the enforced API.  
2. experimental/response_boundary/{core,enforcement}.py + kernel/halt.py  
3. tests/pre_r/ (T20 + adversarial)  
4. Experimental API boundary only  
5. Level 4/5, process-wide, monkey-patch  
6. Yes (local run recorded)  
7. No  
8. No  
