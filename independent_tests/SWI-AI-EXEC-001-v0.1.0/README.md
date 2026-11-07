# SWI-AI-EXEC-001 v0.1.0

Proposed controlled-workspace test harness. See `SPEC.md` for scope and limitations.

Run:

```bash
python -m pip install pytest
python -m pytest -q
```

This is a prototype, not a production monitor, security certification, or proof of arbitrary host-level file access. The observer only records operations routed through `EvidenceWorkspace`.
