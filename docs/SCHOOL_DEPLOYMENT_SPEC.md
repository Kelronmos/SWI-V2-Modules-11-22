# School Deployment / Local Resilience — Use-Case Specification

**Status:** DESIGN / INTENDED USE  
**Classification:** Deployment / operational infrastructure — **not** a core SWI module  
**Seal:** NOT SEALED  
**Production:** BLOCKED unless separately authorized  
**Date:** 26 September 2026

> Network failure should not automatically become information failure.

**Boundary:** School infrastructure provides **resilience**. SWI governs **workflow integrity and evidence**. Humans govern **publication and consequential decisions**. Institutional **policy** defines the **institutionally permitted workflow and its governance boundaries** before SWI structures any workflow.

> SWI structures a workflow defined by policy; it does not become the policy-maker.

Related: `docs/SWI_MANIFESTO.md` §1A, §22, §23 · `docs/LOCAL_SCHOOL_RESILIENCE.md`

---

## 1. Placement

| Layer | Role |
|-------|------|
| **School policy** | Who may publish, what, to whom, which channels, retention, corrections |
| **Local hub / Wi-Fi / SMS** | Means of delivery when Internet fails |
| **SWI** | Structure, validate, record evidence, enforce defined transitions |
| **Human authority** | Consequential approval and accountability |

This is **Intended Use → School Deployment / Local Resilience**, not a sealed SWI kernel module.

---

## 2. Three-layer model

```text
                 EXTERNAL INTERNET
                       │
                  OPTIONAL SYNC
                       │
             ┌─────────▼─────────┐
             │   LOCAL SCHOOL    │
             │       HUB         │
             │  Offline Content  │
             │  Local API        │
             │  Notice Service   │
             └───────┬─────┬─────┘
                     │     │
              Wi-Fi/LAN     SMS
                     │     │
              ┌──────▼─┐ ┌─▼────────┐
              │ SCHOOL │ │ CELLULAR │
              │  Wi-Fi │ │  GATEWAY │
              └───┬────┘ └──────────┘
                  │
           STUDENTS / STAFF
```

Local Wi-Fi, hub, SMS, or mesh are **means** of carrying out the policy-defined workflow — not independent authority layers.

### Layer A — Local hub

Local source for authorized information without continuous Internet: notices; timetable / room changes; assignment metadata; examination information; emergency information; learning resources; sync queues; local audit records.

```text
WAN UP   → AUTHORIZED SYNC → LOCAL HUB
WAN DOWN → LOCAL HUB → LOCAL DELIVERY CONTINUES
```

### Layer B — School local network

```text
SCHOOL-LOCAL → LOCAL DHCP / NETWORK → school.local → LOCAL SCHOOL PORTAL
```

Basic authorized local notices should **not** require a cloud login. Multiple APs may share one hub as the common origin.

### Layer C — SMS resilience

```text
HUMAN AUTHORIZED PUBLISHER → MESSAGE VALIDATION → SMS GATEWAY → RECIPIENT

SMS_RECEIVED ≠ VERIFIED_TRUTH
SMS_RECEIVED ≠ AUTHORIZATION
```

### Optional staff mesh

Staff / infrastructure resilience only. Student-facing path remains ordinary Wi-Fi + local web.

---

## 3. Content priority

| Priority | Content | Channel |
|----------|---------|---------|
| **P0** | Safety / emergency | SMS + local portal |
| **P1** | Timetable / room changes | Portal + optional SMS |
| **P2** | Notices / assignment metadata | Portal |
| **P3** | Offline learning resources | Portal / content store |

---

## 4. Human publication authority

```text
DEVICE_CONNECTED ≠ PUBLISH_AUTHORITY
WIFI_ACCESS      ≠ PUBLISH_AUTHORITY
LOCAL_NODE       ≠ HUMAN_AUTHORITY
SMS_ACCESS       ≠ HUMAN_AUTHORITY
```

Publication restricted to explicitly defined school roles. Record: publisher_id, role, content_id, type, scope, purpose, timestamps, expiry, evidence_reference, audit_reference.

---

## 5. Policy-bounded workflow (school example)

```text
POLICY → WHO MAY PUBLISH? → WHAT MAY BE PUBLISHED?
  → WHO MAY RECEIVE? → WHAT APPROVAL IS REQUIRED?
  → SWI STRUCTURES THAT WORKFLOW → LOCAL HUB / WIFI / SMS
```

**Not:** `LOCAL WIFI → SWI → SWI DECIDES SCHOOL POLICY`

If policy requires principal approval for emergency SMS, SWI must not drop that step because software can send without it.

---

## 6. Offline does not change policy

```text
INTERNET DOWN ≠ POLICY DOWN ≠ AUTHORITY DOWN ≠ GOVERNANCE BYPASS
OFFLINE ≠ POLICY BYPASS
LOCAL NODE ≠ POLICY MAKER
LOCAL NETWORK ≠ AUTHORITY
```

Same policy and authority boundary offline as online.

---

## 7–8. Sync and privacy

```text
LOCAL CONTENT → VALIDATE → STORE → SERVE LOCALLY
  + INTERNET RETURNS → SYNC QUEUE → RECONCILE → VERIFY → AUTHORIZED SYNC
```

Conflicts surfaced, not silently overwritten. Minimize protected personal data. `LOCAL_ACCESS ≠ UNIVERSAL_ACCESS`.

---

## 9. SWI vs infrastructure boundary

```text
CAPABILITY ≠ POLICY ≠ IMPLEMENTATION ≠ EVIDENCE ≠ AUTHORITY ≠ AUTHORIZATION ≠ ACTION
NETWORK_UP ≠ AUTHORIZATION · NETWORK_DOWN ≠ BYPASS
CI_GREEN ≠ AUTHORIZATION · LOCAL_NODE ≠ AUTHORITY
CACHED_DATA ≠ CURRENT_TRUTH · AUTOMATION ≠ AUTONOMY
```

---

## 10. Success condition

Internet off → portal serves authorized notices; staff publish under roles; SMS works on cellular if configured; rights stay human; audit exists; restore does not silent-overwrite; offline creates no new authority.

---

**Non-claims:** Design only; no hardware deployment or production authorization asserted.
