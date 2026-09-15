# SWI V2 — Modules 11–22

**Volume 2** of Structured Workflow Intelligence.

| Volume | Repository | Scope |
|--------|------------|--------|
| 1 | [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10) | Foundation 00–10 |
| 2 | This repo | Continuation 11–22 |

## Principle

Volume 2 must **never** convert unverified data into verified data.  
Volume 2 must **never** claim Volume 1 verified something Volume 1 did not verify.

```text
RAW INPUT → HALT
V1 evidence envelope (PROPOSED) → M11 → AdmittedInput → Kernel → M12+
```

## Status

| Component | Status |
|-----------|--------|
| V2 Kernel | IMPLEMENTED / TESTED / **NOT SEALED** |
| M11 Foundation Admission | Fixture-tested against **PROPOSED** contract · **NOT SEALED** |
| CRTG (cross-repo trust) | **PROPOSED / DESIGN PENDING** |
| M12 | Type-gate only (rejects raw) · design pending |
| M13–22 | **DESIGN PENDING** |
| V1 foundation evidence **producer** | **NOT IMPLEMENTED** |

## Trust boundary (when built)

```text
Trusted CA → Repo certificate → Public key
Private key → Task signature → Envelope
  → CRTG → M11 → AdmittedInput → Kernel → M12+
```

Certificate validity ≠ evidence truth. Signature ≠ safe action.

## Verify

```bash
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

Passing tests ≠ universal AI safety or production certification.

## Roadmap

See `docs/ROADMAP.md`. **Do not implement M13–22** until M11 is sealed against **real** V1 evidence after Foundation Seal 5.
