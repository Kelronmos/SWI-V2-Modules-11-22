# SWI V2 — Modules 11–22

```text
Serialized V1 evidence → M11 → AdmittedInput → post-admission seal → Kernel
```

**Licence:** [Apache License 2.0](LICENSE) · **Provenance:** [NOTICE](NOTICE) · [AUTHORS_AND_LEGACY.md](AUTHORS_AND_LEGACY.md)  
**Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md) · **Security:** [SECURITY.md](SECURITY.md)

**M11:** **SEALED** — record: [`docs/M11_SEAL_RECORD.md`](docs/M11_SEAL_RECORD.md)  
**Evidence tip:** V2 `1d6d7dc` · CI run [35253244912](https://github.com/Kelronmos/SWI-V2-Modules-11-22/actions/runs/35253244912)  
**M12–22:** **OPEN for controlled development** (claim → implement → test; not auto-complete)  
**CRTG / prod keys:** NOT IMPLEMENTED  

```bash
pip install -r requirements.txt && python -m pytest -q
```

Two-checkout: `.github/workflows/two_checkout_travel.yml`  
Status notes: [`docs/TWO_CHECKOUT_CI_STATUS.md`](docs/TWO_CHECKOUT_CI_STATUS.md)

## Governing formula (authorization spine)

```text
Permit(a) ⟺ ∀L,G,S,H: C(a) ⊆ L ∩ G ∩ S ∩ H  ∧  E(a) ≠ ∅
```

| Artifact | Path | Status |
|----------|------|--------|
| Predicate (pure evaluator) | [`swi_v2/kernel/governing_permit.py`](swi_v2/kernel/governing_permit.py) | **IMPLEMENTED / TESTED** |
| Executable tests | [`test/test_governing_formula.py`](test/test_governing_formula.py) | **TESTED** |
| Machine-readable test record | [`evidence/governing_formula_test_record.json`](evidence/governing_formula_test_record.json) | evidence only |
| Human-readable test record | [`docs/evidence/SWI_GOVERNING_FORMULA_TEST_RECORD.md`](docs/evidence/SWI_GOVERNING_FORMULA_TEST_RECORD.md) | evidence only |

**Hard non-claims (do not upgrade automatically):**

```text
TESTED ≠ PROVEN
PROVEN ≠ SEALED
SEALED ≠ PRODUCTION AUTHORIZED
production_authorized = false
```

## S9 / formal attack surface (not a proof)

S9 remains **NOT PROVEN**. The formal records document the equation under attack and counterexamples X1–X10:

| Record | Path |
|--------|------|
| S9 mathematical attack | [`docs/formal/S9_MATHEMATICAL_ATTACK_2026-09-24.md`](docs/formal/S9_MATHEMATICAL_ATTACK_2026-09-24.md) |
| S9 → 360 phase obligation binding | [`docs/formal/S9_360_PHASE_OBLIGATION_BINDING.md`](docs/formal/S9_360_PHASE_OBLIGATION_BINDING.md) |
| S9 ZIP / proof-package manual (branch) | `s9/zip-proof-package-harness` → [`docs/formal/S9_ZIP_PROOF_PACKAGE_MANUAL.md`](https://github.com/Kelronmos/SWI-V2-Modules-11-22/blob/s9/zip-proof-package-harness/docs/formal/S9_ZIP_PROOF_PACKAGE_MANUAL.md) |

```text
GENERATED ZIP ≠ EXECUTED PROOF
REPLAY RECORD ≠ DURABLE REPLAY
GREEN TEST ≠ S9 PROVEN
SIGNATURE ≠ AUTHORITY
```

Global: **S9 = NOT PROVEN** · **Execution corridor not production-authorized** · **Durable replay = NOT IMPLEMENTED** (see [`docs/MODULE_STATUS.md`](docs/MODULE_STATUS.md)).

## Collaboration

SWI is open to technical collaboration under Apache-2.0.

Developers, researchers, security reviewers, and independent implementers may inspect the repositories, reproduce tests, identify limitations, propose changes, and contribute improvements.

SWI follows an evidence-first model:

Claim → Implementation → Test → Result → Limitation → Next iteration.

Contributors must distinguish proposed, implemented, tested, CI-verified, audited, sealed, and independently verified behaviour.

Project provenance and contributor attribution are maintained separately from the technical evidence record.  
**Licence change does not alter the M11 seal or any historical technical evidence.**
