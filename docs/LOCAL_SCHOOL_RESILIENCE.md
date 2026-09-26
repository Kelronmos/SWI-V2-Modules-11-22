# Local School Resilience Layer

**Status:** DESIGN / NORMATIVE ARCHITECTURE  
**Seal:** NOT SEALED  
**Production:** BLOCKED unless separately authorized  
**Date:** 26 September 2026

> Network unavailable ≠ school workflow unavailable.

This layer is **not** a replacement for the Internet. It is continuity for **already authorized**, **locally stored**, **purpose-bound** information when external connectivity fails.

Related: `docs/SWI_MANIFESTO.md` §22 · `docs/ZERO_TRUST_RELATIONSHIP.md`

---

## 1. Architecture

```text
INTERNET / CLOUD
        │
  ┌─────┴─────┐
  │ SWI SYNC  │
  └─────┬─────┘
        │
┌───────▼───────────────┐
│ SCHOOL LOCAL MESH     │
│ Wi-Fi + Local LAN     │
│ + SMS Gateway         │
└───────┬───────────────┘
        │
┌───────┼───────────────┐
│       │               │
STUDENTS  TEACHERS   SCHOOL SERVICES
DEVICES   DEVICES
│       │               │
└───────┼───────────────┘
        │
  LOCAL SWI NODE
        │
 LOCAL DATA / UPDATES / EVIDENCE / SYNC QUEUE
```

---

## 2. Core principle

When the external network fails, the school continues providing **locally authorized** updates over the local network (and optional SMS), without inventing new privileges.

**In scope (examples):** timetable updates; notices; assignments metadata; lesson resources; examination schedules; announcements; emergency information; teacher-approved instructional material; local SWI diagnostics/status.

**Out of scope:** offline mode as a governance bypass; treating connectivity loss as permission expansion.

---

## 3. Hard boundaries

```text
LOCAL_NODE          ≠ HUMAN_AUTHORITY
LOCAL_WIFI          ≠ AUTHORIZATION
OFFLINE_MODE        ≠ BYPASS_MODE
SMS                 ≠ AUTHORITY
SMS_RECEIVED        ≠ VERIFIED_TRUTH
CACHED_DATA         ≠ CURRENT_TRUTH
LOCAL_AVAILABILITY  ≠ PERMISSION
OFFLINE_LOCAL_MODE  ≠ PRODUCTION_AUTHORIZATION
```

Students offline may receive **previously authorized** local information. They must **not** gain additional privileges because external connectivity failed.

---

## 4. Connectivity states

```text
ONLINE
  ↓
CONNECTIVITY_DEGRADED
  ↓
OFFLINE_LOCAL_MODE
  ↓
LOCAL_OPERATION
  ↓
SYNC_PENDING
  ↓
CONNECTIVITY_RESTORED
  ↓
RECONCILIATION
  ↓
VERIFIED
  ↓
SYNCED
```

Offline operation must never silently create authority that did not exist while connected.

---

## 5. Local mesh path

```text
STUDENT DEVICE
      │
      ▼
LOCAL WI-FI / LAN
      │
      ▼
SCHOOL LOCAL NODE
      │
      ├── LOCAL CONTENT
      ├── LOCAL UPDATES
      ├── LOCAL DIAGNOSTICS
      ├── LOCAL EVIDENCE
      └── SYNC QUEUE
```

The local node provides **continuity**, not sovereignty over the wider SWI system.

---

## 6. SMS resilience channel

SMS is a **separate** low-bandwidth fallback (cellular independent of school ISP).

```text
AUTHORIZED SCHOOL SOURCE
        ↓
MESSAGE VALIDATION
        ↓
SMS GATEWAY
        ↓
RECIPIENT
        ↓
MESSAGE RECEIVED
```

```text
SMS_RECEIVED ≠ VERIFIED_TRUTH
SMS_RECEIVED ≠ AUTHORIZATION
```

Require: authenticated originating school/service, provenance, audit log of sender and template. Prefer opt-in; purpose-bound; minimal PII.

---

## 7. Offline synchronization

Local storage ≠ synchronized with remote systems.

```text
LOCAL CHANGE
    ↓
VALIDATION
    ↓
EVIDENCE CAPTURE
    ↓
LOCAL STORAGE
    ↓
SYNC_PENDING
    ↓
CONNECTIVITY RESTORED
    ↓
RECONCILIATION
    ↓
VERIFICATION
    ↓
AUTHORIZED SYNC
```

Conflicts must be **surfaced**, not silently overwritten.

---

## 8. Student safety and privacy

Offline availability is not an excuse for broader distribution.

Continue to apply:

- least privilege;
- purpose limitation;
- privacy-domain separation (e.g. EDUCATION ≠ MEDICAL ≠ FAMILY);
- student safety requirements;
- teacher and institutional authority boundaries;
- auditability;
- data minimization.

Connecting to school Wi-Fi ≠ entitlement to every local resource.

---

## 9. Deployment sketch (ops, not seal)

| Layer | Role |
|-------|------|
| Local hub (Pi/mini-PC + UPS) | Content, notices, API, sync queue |
| Campus Wi-Fi / LAN | `SCHOOL-LOCAL` SSID; captive portal → hub |
| SMS gateway (optional) | USB GSM modem; authorized templates only |
| Optional radio mesh | Staff resilience (e.g. building links); not primary student UX |

Internet is for **sync in/out** when available—not required for day-to-day local read of authorized content.

---

## 10. ATM / test ideas (DESIGN)

| ID | Intent | Expected class |
|----|--------|----------------|
| LSR-A01 | Offline mode grants new privilege | BLOCK / REJECT |
| LSR-A02 | Cached notice treated as live truth after supersession | Surface stale; no silent current claim |
| LSR-A03 | SMS without provenance treated as authority | BLOCK |
| LSR-A04 | Local node self-authorizes seal/production | REJECT |
| LSR-A05 | Sync overwrites conflict without review | BLOCK; surface conflict |
| LSR-A06 | Student on Wi-Fi accesses wrong privacy domain | BLOCK / ESCALATE |

---

## 11. Human-centred objective

> Keep people connected to useful information when infrastructure fails, without removing human responsibility or weakening the boundaries that protect them.

A resilient school is not one that operates without people.  
It is one that gives people enough reliable **local** infrastructure to continue learning, teaching, communicating, and responding while connectivity is restored.

---

**Non-claims:** This document does not implement hardware, authorize production, reseal modules, or claim a deployed school mesh.
