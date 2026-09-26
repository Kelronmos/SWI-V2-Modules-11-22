# Local School Resilience Layer

**Status:** DESIGN / NORMATIVE ARCHITECTURE  
**Seal:** NOT SEALED  
**Production:** BLOCKED unless separately authorized  
**Date:** 26 September 2026

> Network unavailable ≠ school workflow unavailable.  
> Network failure should not automatically become information failure.

**Not** a replacement for the Internet. Continuity for **already authorized**, **policy-permitted**, **locally stored** information.

**Not** a core SWI module. **Intended use / deployment specification:** `docs/SCHOOL_DEPLOYMENT_SPEC.md`.  
**Manifesto:** §22 Local School Resilience · §23 Policy-Bounded Workflow.

---

## Boundary stack

```text
SCHOOL POLICY
     ↓
DEFINED WORKFLOW
     ↓
SWI STRUCTURES / VALIDATES / RECORDS
     ↓
HUMAN AUTHORITY
     ↓
AUTHORIZED OPERATION

INFRASTRUCTURE (hub / Wi-Fi / SMS) = means of delivery
SWI = workflow integrity within policy
HUMANS = publication and consequences
```

```text
CAPABILITY ≠ POLICY ≠ AUTHORITY ≠ AUTHORIZATION ≠ ACTION
LOCAL WIFI ↛ SWI DECIDES SCHOOL POLICY
OFFLINE ≠ POLICY BYPASS
LOCAL NODE ≠ POLICY MAKER
```

---

## Architecture (three layers)

```text
EXTERNAL INTERNET → OPTIONAL SYNC → LOCAL SCHOOL HUB
  (content, API, notices, sync queue, local audit)
         │              │
    Wi-Fi / LAN        SMS
         │              │
    SCHOOL Wi-Fi    CELLULAR GATEWAY
         │
  STUDENTS / STAFF
```

| Layer | Function |
|-------|----------|
| **A Hub** | Authorized local source without continuous Internet |
| **B School network** | `SCHOOL-LOCAL` → `school.local` portal; no cloud login required for basic notices |
| **C SMS** | Short fallback; independent of school ISP |
| Optional staff mesh | Building resilience; not primary student UX |

---

## Hard boundaries

```text
LOCAL_NODE ≠ HUMAN_AUTHORITY · LOCAL_WIFI ≠ AUTHORIZATION
OFFLINE_MODE ≠ BYPASS_MODE · SMS ≠ AUTHORITY
SMS_RECEIVED ≠ VERIFIED_TRUTH · CACHED_DATA ≠ CURRENT_TRUTH
LOCAL_AVAILABILITY ≠ PERMISSION · DEVICE_CONNECTED ≠ PUBLISH_AUTHORITY
OFFLINE_LOCAL_MODE ≠ PRODUCTION_AUTHORIZATION
```

---

## Connectivity states

```text
ONLINE → CONNECTIVITY_DEGRADED → OFFLINE_LOCAL_MODE → LOCAL_OPERATION
  → SYNC_PENDING → CONNECTIVITY_RESTORED → RECONCILIATION → VERIFIED → SYNCED
```

Same policy and authority boundary offline as online.

---

## Publication (human, role-bound)

Record: publisher_id, role, content_id, type, scope, purpose, timestamps, expiry, evidence_reference, audit_reference.

---

## Sync

```text
LOCAL CHANGE → VALIDATE → EVIDENCE → STORE → SYNC_PENDING
  → RESTORED → RECONCILE → VERIFY → AUTHORIZED SYNC
```

Conflicts surfaced, not silently overwritten.

---

## Privacy

Minimize student data on the local notice system. No default dumping of medical, identity documents, financial, private family, or sensitive disciplinary records.

`LOCAL_ACCESS ≠ UNIVERSAL_ACCESS`

---

## Success condition

Internet off → portal still serves authorized notices; staff publish under roles; SMS works on cellular if configured; rights stay human; audit exists; restore does not silent-overwrite; offline creates no new authority.

---

**Non-claims:** Design only; no hardware deployment or production authorization asserted.
