# Institutional UI Plates — UI-neutral specifications

**Status:** DESIGN / EXPERIMENTAL  
**Production:** NOT AUTHORIZED  
**S9:** NOT PROVEN  

The UI is a VIEW over the evidence/authority graph. The UI is NOT the authority.

## Shared case CASE-001

Same underlying case; different authorized projections.

### STUDENT plate
- VISIBLE: own case status, own requests
- HIDDEN: other students, aggregate ministry data
- REQUESTABLE: create own case, view own
- NOT ACTIONABLE: approve, seal, authorize others

### PARENT / GUARDIAN plate
- VISIBLE: subject-specific case status for linked subject only
- HIDDEN: unrelated students

### TEACHER plate
- VISIBLE: student_case_status within subject_scope
- HIDDEN: student_private_history by default (WITHHELD_PRIVACY)

### ADMIN plate
- human_authority_required may force AWAITING

### MINISTRY plate
- VISIBLE: aggregate_report only under sample config
- HIDDEN: individual student_case_status unless authority says otherwise

### REGION / COUNTRY / STATE plates
- Structure is configuration evidence, not hard-coded law

## Decision fields
decision · reason · receipt_id · authority_ref (or NO AUTHORITY) · evidence adequacy · S9 system_result if evaluated (never as proof)
