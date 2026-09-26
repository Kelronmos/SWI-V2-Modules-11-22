# ATM Coverage Map — SWI-ATM-001 vs Current Codebase

**STATUS:** DESIGN  
**NOT IMPLEMENTED**  
**NOT SEALED**  
**PRODUCTION:** BLOCKED  

**Date:** 2026-09-26

---

## 1. Existing Coverage (Already Present)

| ATM Domain / Attack Class | Existing Tests | Location | Notes |
|---------------------------|----------------|----------|-------|
| Integrity / Tamper (content + metadata) | test_content_tampering_rejects, test_metadata_tampering_rejects, test_hash_substitution_rejects, field-by-field canonical tampering | V2 tests/law/test_integrity.py + test_adversarial_surface.py | Strong on hash mismatch & field mutation |
| Authority missing / wrong scope | test_missing_authorization_halts, test_wrong_scope_rejects, append_event authority matrix | V2 tests/law/test_authority.py | Composes with kernel require_authorization_for_action |
| Forged event / empty hash | Multiple forged-hash and empty-hash cases | V2 tests/law/test_adversarial_surface.py | Zero-write on failure |
| Replay | test_replay.py | V2 tests/law/ | Basic |
| Registry | test_registry.py | V2 tests/law/ | Present |
| Policy boundary | test_policy_boundary.py | V2 tests/law/ | Present |
| Schema / null / empty payload | test_null_module_id_rejected, test_empty_object_rejected | V1 tests/test_adversarial_contracts.py | Narrow, schema-level only |
| Authority containment (pre-R) | test_math_002_authority_containment.py | V2 tests/pre_r/ | Experimental |
| Response / enforcement boundary | test_response_boundary.py, test_pr009_enforcement.py | V2 tests/pre_r/ | Experimental |

**Strength:** Integrity, basic authority, and event-hash forgery are already under adversarial pressure in the experimental law lane.

---

## 2. Major Coverage Gaps (P0 Priority)

| ATM Section | Priority | Gap Description |
|-------------|----------|-----------------|
| Token adversarial (TKN-A01–A10) | High | No token-category / reserved-token tests |
| Identifier adversarial (ID-A01–A10) | High | No reserved/protected-name separation tests |
| Reserved vs Protected names | High | Architectural distinction not tested |
| Registry MISS vs ERROR | High | Critical invariant missing |
| Edge semantics | Critical | OBSERVES ≠ EXECUTES etc. not enforced |
| Dependency / Suppressed descendants | Critical | Causal failure propagation & suppression retention |
| Diagnostic determinism | High | Primary-failure selection stability |
| Evidence scope-binding | High | Evidence(A) ≠ Evidence(B) not tested |
| Admission / ReturnGate | Critical | REJECT propagation not fully proven |
| Verification promotion | Critical | TESTED→SEALED, CI_GREEN→AUTHORIZED etc. |
| Human Authority vs Crypto | Critical | Signature ≠ Human Authority not fully matrixed |
| True Zero | Critical | One missing condition → BLOCK |
| State-transition rejection (§31) | Critical | Closed transition table not implemented as tests |
| Privacy-domain isolation | Critical | Cross-domain access completely untested |
| Tamper quarantine re-entry | Critical | Quarantine re-entry path not tested |

---

## 3. Recommended Phased Approach

**Phase 1 – Foundation Repair Track (Immediate)**  
Map repair checklist items directly onto highest-risk ATM cases:

- Integrity → Quarantine → TAMPER-A01–A10
- No direct trust restoration → STATE-A07–A10 + TAMPER-A06
- Human authority required → STATE-A28–A30 + Authority matrix expansion
- Privacy-domain isolation → PRIV-A01–A08
- Closed state transitions → STATE-A01–A26
- REJECT propagation → Admission / ReturnGate cases
- Evidence invalidation after change → Evidence scope + hash-change cases

**Phase 2 – Kernel Surface**  
Once the closed `transition()` function exists, generate parametrized tests from the transition table itself.

**Phase 3 – Full 300-Scenario Corpus**  
Expand remaining domains after the repair gates are under test.

---

## 4. Next Artefact

Create machine-readable mapping entries under `docs/adversarial/` as individual scenario records move from DESIGN → IMPLEMENTED.
