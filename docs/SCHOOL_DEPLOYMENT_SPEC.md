# School Deployment / Local Resilience — Use-Case Specification

**Status:** DESIGN / INTENDED USE  
**Classification:** Deployment / operational infrastructure — **not** a core SWI module  
**Seal:** NOT SEALED  
**Production:** BLOCKED unless separately authorized  
**Date:** 26 September 2026

> Network failure should not automatically become information failure.

**Boundary:** School infrastructure provides **resilience**. SWI governs **workflow integrity and evidence**. Humans govern **publication and consequential decisions**. Institutional **policy** defines the permitted world before SWI structures any workflow.

Related: `docs/SWI_MANIFESTO.md` §1A, §22, §23 · `docs/LOCAL_SCHOOL_RESILIENCE.md`

---

## 1. Placement

| Layer | Role |
|-------|------|
| **School policy** | Who may publish, what, to whom, which channels, retention, corrections |
| **Local hub / Wi-Fi / SMS** | Availability and delivery when Internet fails |
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

### Layer A — Local hub

Local source for authorized information without continuous Internet:

notices; timetable / room changes; assignment metadata; examination information; emergency information; learning resources; sync queues; local audit records.

```text
WAN UP   → AUTHORIZED SYNC → LOCAL HUB
WAN DOWN → LOCAL HUB → LOCAL DELIVERY CONTINUES
```

### Layer B — School local network

Example path:

```text
SCHOOL-LOCAL → LOCAL DHCP / NETWORK → school.local → LOCAL SCHOOL PORTAL
```

Basic authorized local notices should **not** require a cloud login. Multiple APs may share one hub as the common origin.

### Layer C — SMS resilience

Short, important messages when school Internet is down (cellular independent of ISP):

emergency; early closure; exam-room change; “check local portal.”

```text
HUMAN AUTHORIZED PUBLISHER → MESSAGE VALIDATION → SMS GATEWAY → RECIPIENT

SMS_RECEIVED ≠ VERIFIED_TRUTH
SMS_RECEIVED ≠ AUTHORIZATION
```

### Optional staff mesh

Wi-Fi mesh, store-and-forward, low-bandwidth or LoRa links for **staff / infrastructure** resilience. Student-facing path remains ordinary Wi-Fi + local web.

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

Publication restricted to explicitly defined school roles. Record at minimum:

```text
publisher_id · publisher_role · content_id · content_type
scope · purpose · created_at · published_at · expiry
evidence_reference · audit_reference
```

---

## 5. Policy-bounded workflow (school example)

```text
SCHOOL POLICY
     ↓
POLICY INTERPRETATION
     ↓
DEFINED WORKFLOW
     ↓
SWI STRUCTURES / VALIDATES / RECORDS
     ↓
HUMAN AUTHORITY
     ↓
AUTHORIZED OPERATION
```

**Not:**

```text
LOCAL WIFI → SWI → SWI DECIDES SCHOOL POLICY
```

School policy defines who may publish, what, receivers, channels, emergency rules, approval requirements, retention, and conflict handling. SWI structures that defined workflow only.

Example:

```text
SCHOOL POLICY
  "Authorized teacher may publish timetable change"
      ↓
SWI WORKFLOW
  IDENTIFY PUBLISHER → CHECK ROLE → CHECK SCOPE
  → CHECK CONTENT REQUIREMENTS → CHECK EVIDENCE
  → RECORD DECISION → HUMAN AUTHORITY (if required) → PUBLISH TO LOCAL HUB
```

If policy requires principal approval for emergency SMS, SWI must not drop that step because software can send SMS without it.

---

## 6. Offline does not change policy

```text
INTERNET AVAILABLE   → POLICY-DEFINED WORKFLOW → SWI STRUCTURE → LOCAL/REMOTE OP
INTERNET UNAVAILABLE → SAME POLICY → SAME AUTHORITY BOUNDARY → LOCAL WORKFLOW

OFFLINE ≠ POLICY BYPASS
OFFLINE ≠ NEW AUTHORITY
LOCAL NODE ≠ POLICY MAKER
LOCAL NETWORK ≠ AUTHORITY
```

---

## 7. Offline synchronization

```text
LOCAL CONTENT → VALIDATE → STORE → SERVE LOCALLY
        + INTERNET RETURNS +
SYNC QUEUE → RECONCILIATION → VERIFY → AUTHORIZED SYNC
```

Conflicts are surfaced, not silently overwritten.

---

## 8. Privacy defaults

Local notice systems should **not** become repositories for unnecessary medical, identity-document, financial, private family, sensitive disciplinary, or other protected personal data.

```text
LOCAL_ACCESS ≠ UNIVERSAL_ACCESS
```

---

## 9. SWI vs infrastructure boundary

| Provides | Owner |
|----------|--------|
| Availability, delivery, SMS transport | School local infrastructure |
| Evidence, provenance, validation, transitions, diagnostics, authorization **boundaries**, auditability | SWI (when deployed against defined workflow) |
| Publication and consequential decisions | Humans under school policy |

```text
NETWORK_UP ≠ AUTHORIZATION
NETWORK_DOWN ≠ BYPASS
CI_GREEN ≠ AUTHORIZATION
LOCAL_NODE ≠ AUTHORITY
CACHED_DATA ≠ CURRENT_TRUTH
AUTOMATION ≠ AUTONOMY
CAPABILITY ≠ POLICY
```

---

## 10. Success condition

A successful deployment should demonstrate that:

1. external Internet can be disconnected;
2. students can still access the local school portal;
3. previously authorized notices remain available;
4. authorized staff can publish appropriate local updates;
5. emergency SMS can operate independently where cellular service is available;
6. publication rights remain human-controlled;
7. local activity is auditable;
8. connectivity restoration does not silently overwrite conflicting information;
9. no offline mechanism creates unauthorized authority or access.

Objective: resilient local information supporting teaching, learning, communication, and safety — **not** a school that operates without people.

---

**Non-claims:** Does not implement hardware, authorize production, reseal modules, or assert a live school deployment.
