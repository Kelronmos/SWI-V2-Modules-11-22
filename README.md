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

## Collaboration

SWI is open to technical collaboration under Apache-2.0.

Developers, researchers, security reviewers, and independent implementers may inspect the repositories, reproduce tests, identify limitations, propose changes, and contribute improvements.

SWI follows an evidence-first model:

Claim → Implementation → Test → Result → Limitation → Next iteration.

Contributors must distinguish proposed, implemented, tested, CI-verified, audited, sealed, and independently verified behaviour.

Project provenance and contributor attribution are maintained separately from the technical evidence record.  
**Licence change does not alter the M11 seal or any historical technical evidence.**
