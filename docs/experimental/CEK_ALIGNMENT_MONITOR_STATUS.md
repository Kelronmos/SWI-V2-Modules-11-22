# SWI-CEK Alignment Monitor — Experimental Status

Date: 2026-09-27

## Classification

RESEARCH / EXPERIMENTAL  
Production: **NOT AUTHORIZED**  
Seal: **NO**  
Runtime: **NOT INTEGRATED**  
M11: **UNTOUCHED**  
Architecture: **FROZEN** (failing tests fix experiment or evidence, not SWI design)

## Evidence chronology (do not overwrite)

| State | Result |
|-------|--------|
| LOCAL_SANDBOX_EXECUTION | up to 489 PASS |
| CLEAN_CLONE_REPRODUCTION (tip `ee2f87e` / suite land) | **451 PASS** — `pytest tests/cek_alignment_monitor -q`, no injection |
| FULL_SWI_REGRESSION (same clean clone) | **644 PASS, 1 FAIL** |
| Failure | `tests/law/test_evidence_freshness.py::test_evidence_source_tip_reachable_from_head` |
| Attribution | Evidence tip vs branch HEAD (pre-existing class of failure; not CEK package assertion) |
| STATIC_INSPECTION (cek package) | No `eval`/`exec`/`pickle`/`subprocess`/`os.system`/`shell=True` matches |
| HIDDEN_PATHS | None under experimental CEK or its tests |
| CI (PR #5) | **PENDING** (draft; workflow triggers on PR to main; status total_count 0) |
| INDEPENDENT REVIEW | **PENDING** |

## Scenario wording

The experimental suite contains **300 defined adversarial scenarios** within a **451-case** clean-clone verification suite (local host may show higher counts when extra modules are present).

Categories: 001–025 vector · 026–050 numeric · 051–075 weights · 076–100 measurement · 101–125 provenance · 126–150 visibility · 151–175 UNKNOWN · 176–200 evidence→authority · 201–225 signature · 226–250 HALT/REJECT · 251–275 replay · 276–300 observation→execution.

## Declared reproduce command

```bash
git clone -b experimental/cek-alignment-monitor https://github.com/Kelronmos/SWI-V2-Modules-11-22.git
cd SWI-V2-Modules-11-22
pip install -r requirements.txt   # pytest>=7, cryptography>=41
python -m pytest tests/cek_alignment_monitor -q
```

ZIP is transfer-only; repository is the source of truth.

## Non-claims

TESTED ≠ SEALED · CI PASS ≠ SEAL · EVIDENCE ≠ AUTHORITY · OBSERVATION ≠ AUTHORIZATION  
No claim of production security, universal safety, or runtime authorization.
