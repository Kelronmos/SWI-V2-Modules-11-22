# SWI V2 — Modules 11–22

```text
Serialized V1 evidence → M11 → AdmittedInput → post-admission seal → Kernel
```

**Licence:** [Apache License 2.0](LICENSE) · **Provenance:** [NOTICE](NOTICE) · [AUTHORS_AND_LEGACY.md](AUTHORS_AND_LEGACY.md)  
**Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md) · **Security:** [SECURITY.md](SECURITY.md)

**Control status (CURRENT):** see [`docs/CURRENT_POSITION.md`](docs/CURRENT_POSITION.md)

| Item | Control status |
|------|----------------|
| **M11** | Historical seal record at frozen tip `1d6d7dc` · CI [35253244912](https://github.com/Kelronmos/SWI-V2-Modules-11-22/actions/runs/35253244912) — **does not override CURRENT_POSITION** |
| M11 current control | Follow `docs/CURRENT_POSITION.md` / `docs/MODULE_STATUS.md` (historical SEALED ≠ production authorization) |
| Evidence freshness | Required control — fail-closed when Git history unavailable or tip unreachable |
| M12–22 | **OPEN / FROZEN / BLOCKED** per module status (claim → implement → test) |
| Execution | **BLOCKED** |
| Production | **NOT AUTHORIZED** |
| Foundation PASS | **NOT CLAIMED** |
| CRTG / prod keys | **NOT IMPLEMENTED** |

```bash
pip install -r requirements.txt && python -m pytest -q
```

Offline (when wheels vendored): `scripts/start_offline.sh` / `scripts/start_offline.bat`  
Two-checkout: `.github/workflows/two_checkout_travel.yml`  
Status notes: [`docs/TWO_CHECKOUT_CI_STATUS.md`](docs/TWO_CHECKOUT_CI_STATUS.md)

## Collaboration

SWI is open to technical collaboration under Apache-2.0.

Developers, researchers, security reviewers, and independent implementers may inspect the repositories, reproduce tests, identify limitations, propose changes, and contribute improvements.

SWI follows an evidence-first model:

Claim → Implementation → Test → Result → Limitation → Next iteration.

Contributors must distinguish proposed, implemented, tested, CI-verified, audited, sealed, and independently verified behaviour.

Project provenance and contributor attribution are maintained separately from the technical evidence record.

**Historical seal records do not equal current production authorization.**  
**Do not claim what the code cannot demonstrate.**
