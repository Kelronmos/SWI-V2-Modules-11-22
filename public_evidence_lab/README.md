# SWI Public Evidence Lab (Prototype)

**Branch:** `prototype/public-evidence-lab-2026-11-03`  
**Status:** Prototype only — not production, not proven, not sealed.

## Purpose

Browser-local demonstration of:

- Place-hold interactions (in-memory only)
- Local runtime checks
- Evidence capture and multi-format export
- Explicit separation of presentation layer from trusted runner

## Truth boundaries (non-negotiable)

```
TESTED != PROVEN
PROVEN != SEALED
SEALED != PRODUCTION_AUTHORIZED
CI_GREEN != SWI_AUTHORIZED
INDEPENDENT_REVIEW_PENDING != INDEPENDENT_REVIEW_APPROVED
```

A green local check is **not** evidence of binding to the SWI authorization spine.

## How to use

### 1. Browser presentation layer

Open `public/index.html` in a modern browser.

- Place / release holds
- Click **Run prototype checks**
- Export JSON / TXT / CSV / HTML snapshot

All results are browser-local. A commit SHA typed into the form is **never** treated as verified.

### 2. Trusted local runner

```bash
cd public_evidence_lab
python3 runner/public_evidence_runner.py --startup-kind first-start --out-dir evidence/first-start
python3 runner/public_evidence_runner.py --startup-kind subsequent-start --out-dir evidence/subsequent-start
```

The runner:

- Derives commit / branch / dirty status only from local git metadata
- Captures process identity
- Forces `PROVEN=false`, `SEALED=false`, `PRODUCTION_AUTHORIZED=false`
- Emits a single canonical JSON record + TXT + CSV + SHA-256 manifest
- Marks PDF / XLSX / JPG as `NOT_GENERATED` when dependencies are absent

## What this does **not** do

- Does not connect to the SWI authorization spine
- Does not reboot the host or restart production services
- Does not grant production authorization
- Does not perform independent review
- Does not treat UI-entered values as trusted evidence

## Directory layout

```
public_evidence_lab/
├── public/
│   └── index.html          # Presentation layer only
├── runner/
│   └── public_evidence_runner.py
├── evidence/               # Generated at runtime (not committed)
└── README.md
```

## Acceptance notes

- All work remains on the isolated prototype branch.
- No merge to `main`.
- Independent review still required before any claim elevation.
