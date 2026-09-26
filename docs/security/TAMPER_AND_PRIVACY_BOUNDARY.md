# SWI Tamper & Sensitive-Information Boundary

**STATUS:** DESIGN  
**NOT IMPLEMENTED**  
**NOT SEALED**  
**PRODUCTION:** BLOCKED  

---

## Core Rules

> Any tampered, altered, corrupted, forged, or integrity-failed object is denied re-entry into the trusted workflow. Re-entry requires explicit human authority and, where applicable, escalation to the relevant authority.

> Private information must remain compartmentalized by identity and domain. Access to one domain must not imply access to another.

---

## Required Isolation Domains

```
IDENTITY
   │
   ├── MEDICAL
   ├── EDUCATION
   ├── FAMILY
   ├── FINANCIAL
   ├── EMPLOYMENT
   ├── LEGAL
   └── OTHER PRIVATE DATA
```

A valid identity reference does **not** grant access to every associated domain.

Examples:
- EDUCATION_ACCESS ≠ MEDICAL_ACCESS
- MEDICAL_ACCESS ≠ FAMILY_ACCESS
- FAMILY_ACCESS ≠ IDENTITY_ADMINISTRATION

---

## Tamper Path (Mandatory)

```
OBJECT
  ↓
INTEGRITY CHECK
  ↓
TAMPER DETECTED
  ↓
QUARANTINE
  ↓
NO RE-ENTRY
  ↓
HUMAN AUTHORITY REQUIRED
  ↓
RELEVANT ESCALATION
  ↓
NEW VALIDATION
  ↓
NEW EVIDENCE
  ↓
NEW ADMISSION
  ↓
NEW VERIFICATION
  ↓
AUTHORIZED ACTION
```

No shortcut from TAMPERED back to VALID.

A previous signature, certificate, successful test, cached admission, or historical authorization must **not** silently restore trust.

---

## Key Distinctions

| Concept | Meaning |
|---------|---------|
| IDENTITY | who/what the subject is |
| ACCESS | what the actor may access |
| AUTHORITY | who may authorize an action |
| DATA | information |
| EVIDENCE | validated information for a defined purpose |

These must never collapse into one permission.

---

## Privacy Rule

> Need-to-know, purpose-bound, least-privilege access. Crossing a protected information boundary requires its own authorization; it is never inherited merely because the same person, identity, account, node, or workflow is involved.

---

**Related:** See `docs/repair/SWI_REPAIR_CHECKLIST.md` and `docs/adversarial/SWI-ATM-001.md`.
