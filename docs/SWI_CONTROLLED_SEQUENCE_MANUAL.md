# SWI Controlled Sequence Manual

**Repository:** Kelronmos/SWI-V2-Modules-11-22  
**Date (UTC):** 2026-09-17  
**Rule:** Sign → verify independently → replay → distribute → standardize manuals → then build modules.

Do not build on an assumption that has not survived independent verification.

---

## 1. Governing law

Evidence before claim · boundary before expansion · contract before implementation · test for behaviour · CI for reproducibility · audit for confidence · seal for controlled dependency · independent verification for trust · replay for reconstruction · distribution for cross-node evidence · dependency before the next module · **never claim what the code cannot demonstrate**.

---

## 2. Critical distinctions (never collapse)

| This | Is not |
|------|--------|
| Signature | Replay proof |
| Hash validity | Factual truth |
| Seal validity | Implementation correctness |
| Implementation correctness | AI safety |
| Independent verification | Production certification |
| Distributed agreement | Truth |
| Successful test | Universal security |

---

## 3. Master gates (order is mandatory)

```text
GATE A  Independent verification (standalone verifier + live CI)
GATE B  Deterministic replay
GATE C  Distributed boundary evidence (NAB Stage 2)
GATE D  Controlled module manual schema
GATE E  M12 contract (draft may exist; freeze at implementation time)
GATE F  M12 implementation
GATE G  M12 tests + CI
GATE H  M12 audit
GATE I  M12 seal
GATE J  M13 dependency release
```

**One-line rule:** SIGN → VERIFY INDEPENDENTLY → REPLAY → DISTRIBUTE → STANDARDIZE EVIDENCE → BUILD NEXT MODULE.

---

## 4. Phase A — Prove the seal story

### A1 Independent verification

- Prefer a **standalone verifier repository** (own CI, tests, version) that does **not** `import` the sealer’s verification logic for the core check.
- Resolve live Actions: `run_id` → `head_sha` · `status` · `conclusion == success`.
- Separate `CI_SELF_ATTESTED` from `CI_INDEPENDENT`.
- Demo fixtures (`--demo-m11-regression`) = `mode: DEMO` · never `LIVE`.
- In-repo support: `scripts/v47_ci_resolver.py`, `scripts/historical_claim_verifier.py` (strict E4).

### A2 Deterministic replay

- Reconstruct commitments from admitted inputs + published rules; **do not** copy the expected commitment from the seal as the “reconstructed” value.
- Outcomes: `REPLAY_MATCH` | `REPLAY_MISMATCH` | `REPLAY_REJECTED` | `REPLAY_UNAVAILABLE` — never “truth confirmed.”
- Separate replay evidence record; do not rewrite the historical M11 seal.

### A3 Sparse Merkle

- Research branch only: `EXPERIMENTAL` · `NOT SEALED` · `NOT A DEPENDENCY`.

---

## 5. Phase B — Extend the boundary

Order: **replay protection → partial-node failure → cross-node M11 admission**.

- Policy explicit (ACCEPT / REJECT / REQUIRE NEW ADMISSION); crypto validity does not choose policy.
- Cross-node admission defines what the destination trusts, verifies, and **cannot infer**.
- **Firefly** deferred until replay exists; no privileged bypass of M11.
- **NAB Stage 2** after Foundation Seal 5 on V1.

---

## 6. Phase C — Module expansion

1. Controlled Module Manual Schema — `docs/CONTROLLED_MODULE_MANUAL_SCHEMA_v1.md`
2. M12 contract — `docs/M12_CONTRACT.md` (draft retained)
3. Implementation → tests → CI → audit → seal → dependency release

**M12 implementation is FROZEN until Gates A–D are met.**

Scaffold remains type boundary (`accepted_placeholder`).

---

## 7. Evidence levels

| Level | Meaning |
|-------|--------|
| E0 | Documented |
| E1 | Implementation surface |
| E2 | Tests exercise behaviour |
| E3 | Required CI independently established |
| E4 | Seal bound to audited commit + independent CI + non-stub surfaces |

E4 ≠ secure · safe · true · production-ready.

---

## 8. Status vocabulary (allowed)

`PROPOSED` · `DESIGN PENDING` · `SCAFFOLD` · `IMPLEMENTED` · `TESTED` · `CI VERIFIED` · `AUDITED` · `SEALED` · `EXPERIMENTAL` · `BLOCKED` · `DEFERRED` · `FROZEN`

Avoid as proven labels: secure · trusted · certified · production ready · safe — unless formally defined and evidenced.

---

## 9. Historical integrity

- **Do not rewrite** the M11 seal to fit a new verifier or roadmap.
- New properties → new evidence → new records.
- Prefer `ARCHIVED` over silent deletion of historical evidence.

---

## 10. Explicit exclusions (now)

- Substantive M12 normalization code
- M13–22 capability
- Distributed / multi-node Firefly
- Language ports (Rust/TS) as second source of truth
- Production HSM / full CRTG v1 custody
- Unsealed research as production dependency

---

## 11. Stop-the-line

Stop expansion when: claim exceeds evidence · contract ambiguous · test does not prove claim · CI unavailable · independent verification fails · replay nondeterministic · distributed state undefined · future functionality leaks backward.

Stopping is a control success.

---

## 12. Related documents

| Doc | Role |
|-----|------|
| `docs/SWI_TRUST_SEQUENCE.md` | Short priority ladder |
| `docs/CONTROLLED_MODULE_MANUAL_SCHEMA_v1.md` | 16-section module standard |
| `docs/M11_SEAL_RECORD.md` | Historical M11 seal |
| `docs/M12_CONTRACT.md` | M12 draft (not implementation auth) |
| `docs/GOVERNANCE_LOCK.md` | Current lock |
| `docs/V47_GATE_FREEZE.md` | Verifier / E4 freeze |

---

## 13. Final position

```text
SELF ASSERTION
      → REPLICATED VERIFICATION
      → RECONSTRUCTABLE EVIDENCE
      → DISTRIBUTED BOUNDARY
      → STANDARDIZED MODULE EVIDENCE
      → CONTROLLED MODULE EXPANSION
```

*3 years cannot be compressed into 3 months by claiming the missing evidence.*
