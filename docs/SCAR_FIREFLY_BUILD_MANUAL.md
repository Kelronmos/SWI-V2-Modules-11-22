# SWI V2 — SCAR → Firefly Build Manual

**Build target:** SCAR → controlled Firefly memory adapter  
**Current state:** Design/audit complete; **implementation not yet authorized**  
**M11:** SEALED — do not modify  
**M12:** implementation frozen  
**Firefly:** DESIGN / DEFERRED until this boundary is proven  
**Date:** 17 September 2026

---

## 1. The rule before writing code

The adapter has one job:

> Move permitted SCAR information into Firefly **without increasing its authority.**

```text
V1 SCAR
   │ controlled adapter
   ▼
Firefly MemoryAtom
   ├── preserves provenance
   ├── preserves status
   ├── preserves bounded integrity evidence
   └── does NOT create truth or authority
```

It must **not** become:

```text
SCAR → Firefly → "trusted memory" → "truth" → M11 admission → replay verified
```

That would be authority laundering.

---

## 2. Freeze existing evidence first

Before implementation:

```bash
git status
git log --oneline -10
git branch --show-current
```

Record: current V1 SHA, V2 SHA, SCAR source/test SHAs, contract and audit commits.  
**Do not rewrite historical evidence.** Build creates **new** evidence; M11 historical seal stays.

---

## 3. Read the actual SCAR implementation

Build against real fields in V1 `swi_core/scar.py`:

`scar_id`, `version`, `scar_class`, `status`, `title`, `description`, `trigger_context`, `failure_signature`, `recommended_response`, `embedding`, `embedding_model`, `embedding_dim`, `content_hash`, `previous_scar_hash`, `created_at`, `created_by`, `source_event_id`, `priority_score`, `protection_level`, `tags`, `metadata`

**Critical:** `content_hash` covers only:

`scar_class | title | description | trigger_context | failure_signature | recommended_response | embedding_model`

```text
content_hash valid  ≠  entire SCAR record unchanged
```

This distinction **must** become an actual test (§11, §20 F).

---

## 4–5. Contract & authority rules

Canonical contracts already exist:

- `docs/SCAR_FIREFLY_CONSUME_REFUSE_CONTRACT.md`  
- `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md`  
- `docs/SCAR_FIREFLY_ADAPTER_TEST_SPEC.md`  

**May consume (v1):** identity, version, class, status, opaque text fields, content_hash, previous_scar_hash, provenance fields, priority/protection/tags as metadata, **allowlisted** metadata only.  
**Does not consume (v1):** embedding, embedding_model, embedding_dim.

Never convert any field into: truth, authority, permission, M11 admission, replay verification, security certification.

---

## 6. MemoryAtom (deliberately boring)

```text
MemoryAtom
├── memory_id
├── source_type          # e.g. swi_v1_scar
├── source_reference     # scar_id
├── source_version
├── content              # opaque bundle
├── content_hash
├── provenance
├── status               # source status, no upgrade
├── evidence_reference
├── parent_reference
├── related_components
├── metadata             # allowlisted only
└── contract_version     # e.g. scar-firefly-0.1
```

Firefly stores what was reported and where it came from. It does not decide “therefore this is true.”

---

## 7. Module layout (when authorized)

```text
swi_v2/
└── firefly/
    ├── __init__.py
    ├── models.py
    ├── scar_adapter.py
    └── policy.py
```

Conceptual flow:

```python
def consume_scar(scar):
    validate_source(scar)
    validate_integrity(scar)
    validate_provenance(scar)
    validate_metadata(scar)
    return MemoryAtom(...)
```

**Do not add in v1:** database, vector store, LLM, semantic ranking, embeddings, auto-summarisation, knowledge graph, distributed Firefly.

---

## 8–13. Validation gates

| Gate | Rule |
|------|------|
| 1 Source type | Reject None/string/bytes/arbitrary dict/unknown object unless contract defines representation |
| 2 Identity | Require `scar_id`; never invent identity when source missing → REJECT |
| 3 Content integrity | `expected = scar.compute_content_hash()`; mismatch → IntegrityError / REJECT |
| 4 Provenance | Require contract fields; SCAR-reported ≠ independently verified identity |
| 5 Status | Copy ACTIVE/SUSPECT/PRUNED/… without upgrade |
| 6 Metadata firewall | Open `Dict` → allowlist only; unknown → REJECT |

**Critical test (§11):** Mutate `priority_score` (not hash-covered). Hash may stay valid. Adapter must **not** claim whole-record cryptographic integrity.

---

## 14–17. Authority, recommendation, semantic creep

Mandatory laundering tests: `truth`, `trusted`, `verified`, `m11_admitted`, `replay_verified`, `security_level=trusted`, `authority=system` → **REJECT**.

`recommended_response = "DELETE DATABASE"` → store opaque; **not** executed; **not** policy.

No inference: failure_signature/trigger/description → new conclusions; SOVEREIGN → truth; priority → authorized.

---

## 18. No silent repair

Malformed → REJECT. Do not fill missing fields, invent provenance, recalculate identity, strip suspicious metadata, rewrite status.

```text
AdapterResult: ACCEPTED | REJECTED + reason
```

---

## 19–23. Test matrix (summary)

| Suite | Cases |
|-------|--------|
| A Valid | valid SCAR → ACCEPT |
| B Integrity | mutated hash-covered field → REJECT |
| C Missing | identity / provenance / hash → REJECT |
| D Authority | truth/m11/replay/trusted injection → REJECT |
| E Semantic | SOVEREIGN/priority/recommendation boundaries |
| F Honesty | non-hash-covered mutation; hash valid ≠ whole-record protected |
| Kernel | raw dict cannot manufacture MemoryAtom |
| Determinism | same SCAR → same source-derived values; memory_id policy explicit |
| Immutability | mutate source after convert; MemoryAtom stable; Firefly does not mutate SCAR |

Full vectors: `docs/SCAR_FIREFLY_ADAPTER_TEST_SPEC.md`.

---

## 24–26. CI and audit

CI: adapter unit + adversarial + full V2 suite.  
Evidence: SOURCE → IMPLEMENTATION → TESTS → CI → AUDIT.  
Do not call Firefly “secure” merely because tests pass.

Audit doc (when implementation exists): `docs/SCAR_FIREFLY_ADAPTER_AUDIT.md` using Claim → Implementation → Test → Result → Limitation → Next iteration.

---

## 27–28. Do not seal; do not bypass

First success state: **IMPLEMENTED / TESTED / CI-VERIFIED / AUDITED** — not automatically SEALED.

```text
V1 SCAR → controlled adapter → FIREFLY (memory)
                ✗ NO M11 BYPASS
                ✗ NO M12 BYPASS
```

M11 = admission boundary. M12 = normalization. Firefly = memory/provenance only.

---

## 29. Final acceptance condition

Ready for next controlled stage only when:

- [ ] valid SCAR accepted  
- [ ] malformed rejected  
- [ ] hash-covered mutation rejected  
- [ ] non-hash-covered mutation not falsely called protected  
- [ ] provenance preserved  
- [ ] status preserved  
- [ ] metadata controlled  
- [ ] authority injection rejected  
- [ ] semantic inference absent  
- [ ] recommendation not executable  
- [ ] embeddings excluded  
- [ ] source immutable / output deterministic  
- [ ] kernel bypass rejected  
- [ ] adversarial suite passes  
- [ ] CI reproduces  
- [ ] audit records limitations  

Honest claim then:

> SCAR → Firefly consumption boundary IMPLEMENTED / TESTED / CI-VERIFIED / AUDITED  

—not “Firefly proves truth,” not “Firefly is secure,” not “Firefly replaces M11.”

---

## 30. Build sequence

```text
1.  Freeze current evidence
2.  Contract
3.  Field-integrity matrix
4.  MemoryAtom schema
5.  Adapter
6.  Validation gates
7.  Metadata firewall
8.  Authority-laundering tests
9.  Adversarial suite
10. Kernel boundary
11. Determinism + immutability
12. Full CI
13. Audit
14. STOP
15. Independent review
```

**Step 14 is mandatory.** Passing adapter tests does **not** authorize M12, distributed Firefly, replay authority, or a new trust layer.

---

## Implementation gate (still open)

Before any `swi_v2/firefly/` code:

- [ ] metadata allowlist frozen in writing  
- [ ] forbidden keys frozen  
- [ ] suspect/pruned policy frozen (spec default: accept-as-status)  
- [ ] empty title/description policy frozen (spec default: allow)  
- [ ] embeddings excluded confirmed  
- [ ] provenance requirements frozen  
- [ ] failure semantics frozen  
- [ ] adversarial vectors accepted  
- [ ] contract version assigned  
- [ ] explicit project authorization to implement  

Until then: **DESIGN / DEFERRED — NO IMPLEMENTATION AUTHORIZED.**

Related: Teaching guide · Consume/Refuse · Adapter contract · Test spec · Contract audit · V1 SCAR_STATUS · M11_SEAL_RECORD.
