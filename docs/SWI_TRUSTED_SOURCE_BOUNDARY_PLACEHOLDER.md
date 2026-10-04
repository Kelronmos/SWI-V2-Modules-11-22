# SWI Trusted-Source Boundary — Placeholder

**Status:** PLACEHOLDER / STRUCTURAL ONLY  
**Date:** 2026-10-04  
**Does NOT claim:** law proven · policy authoritative · standard binding · production authorization

---

## Purpose

Before any law, policy, or standard reference can approach the SWI authorization spine, its **source → provenance → scope → boundary** must be explicit.

This document and the companion machine-readable record define a **structural placeholder** only.

```text
PLACEHOLDER PIPELINE GREEN ≠ TRUSTED SOURCE PROVEN
PLACEHOLDER PIPELINE GREEN ≠ AUTHORITY PROVEN
PLACEHOLDER PIPELINE GREEN ≠ SWI PRODUCTION AUTHORIZED
```

---

## Spine

```text
SWI HEADER
  → SOURCE
  → PROVENANCE
  → VERSION
  → STATUS
  → SCOPE
  → JURISDICTION
  → EVIDENCE
  → BOUNDARY
  → CLAIM
  → DECISION
```

If any mandatory spine element is missing, contradictory, or unverifiable:

```text
SPINE BREAK → HALT → NO GREEN → NO BINDING → NO AUTHORIZATION
```

---

## Hard separations

```text
STANDARD != LAW
LAW != POLICY
POLICY != HUMAN_AUTHORITY

SOURCE != AUTHORIZATION
OBSERVATION != AUTHORITY
SIGNATURE != AUTHORITY
API != AUTHORIZATION
VPN != AUTHORIZATION
CI_GREEN != PRODUCTION_AUTHORIZATION
```

A source may be trusted **for information** without being trusted **for authorization**.

```text
Trusted source → trusted for WHAT
              → under WHICH authority
              → within WHICH scope
              → at WHICH version/status
              → with WHICH provenance
              → subject to WHICH boundary
```

---

## Required header fields (machine-readable)

| Field | Meaning |
|-------|---------|
| `source_id` | Stable identifier of the source record |
| `source_type` | `standard` \| `law` \| `policy` \| `reference` \| … |
| `publisher` | Issuing body (descriptive, not authority proof) |
| `reference` | Citation / URL / catalogue id |
| `provenance` | Origin path / authentication trail (structural) |
| `trusted_for` | Purpose limit (e.g. information, mapping) — not authorization |
| `policy_version` | Exact version string |
| `policy_status` | draft \| active \| superseded \| withdrawn \| expired |
| `policy_scope` | Who/what/where/when governed (declared) |
| `jurisdiction` | Declared jurisdiction string (not inferred) |
| `evidence` | Evidence reference id/path |
| `boundary` | Where trust stops |
| `claim` | Explicit claim under inspection |

---

## Standards references (informative only)

| Reference | Role in this placeholder |
|-----------|--------------------------|
| ISO/IEC 27001:2022 | Informative anchor for ISMS *requirements language* — **not** SWI law |
| NIST CSF 2.0 / CSWP 29 | Informative mapping reference — **not** SWI authorization |

`STANDARD != LAW`. These references do not grant SWI production authority.

---

## Pipeline meaning

| Result | Means |
|--------|--------|
| Structural GREEN | Record satisfies implemented structural checks |
| HALT / SPINE BREAK | Missing, UNKNOWN, or CONFLICT on mandatory spine |
| AUTHORIZATION | **Always NO** from this layer alone |

No automatic green authority.

---

## Tools

| Tool | Role |
|------|------|
| `scripts/swi_trusted_source_spine_inspect.py` | Automated read-only inspector |
| `scripts/swi_trusted_source_spine_manual.sh` | Independent second-eye grep inspection |

If automated inspector says GREEN but manual inspection says HALT → treat as **CONFLICT** → halt.

---

## Related

- Machine record: `evidence/trusted_source_boundary_placeholder.json`
- Inspector: `swi_v2/trusted_source/spine_inspector.py`
