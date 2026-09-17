# M11 Claim Ledger (property-level, Pass 1)

**Mode:** surface mapping · **Not** proof that pytest assertions were executed in this pass.
**Seal:** historical — do not rewrite (`docs/M11_SEAL_RECORD.md`).

| Claim ID | Claim | Implementation | Test surface | Assertion intent |
|----------|-------|----------------|--------------|------------------|
| M11-P001 | Tampered evidence rejected at admission | `swi_v2/kernel/admission.py` | `test/test_module11_admission.py`, `test/test_m11_post_admission_seal.py` | admission rejects tamper/integrity fail |
| M11-P002 | Raw input cannot enter seal boundary | `seal.py`, `admission.py` | `test/test_m11_seal_boundary_attacks.py` | create_seal rejects non-AdmittedInput |
| M11-P003 | Merkle proof substitution rejected | `seal.py`, `merkle.py` | boundary attacks | verify_seal false on foreign proof |
| M11-P004 | Domain substitution rejected | `seal.py` | boundary attacks | wrong domain fails |
| M11-P005 | Verification reconstructs seal material | `seal.py` | post-admission + end-to-end | reconstruct commitment/proof |
| M11-P006 | Factual truth of payload | — | — | **EXPLICIT NON-CLAIM** |

Machine-readable twin: `docs/V47_M11_PROPERTY_MAP.json`.
